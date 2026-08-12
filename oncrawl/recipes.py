"""Biblioteka gotowych recept SEO (ready-made queries).

Każda recepta to deklaratywny opis analizy: jakich pól wymaga, jakie OQL
buduje, jakie kolumny pokazać i jak posortować.

Zasada: NIC nie jest zgadywane. Recepta deklaruje `needs` — listę pól, bez
których nie ma sensu — i jest pokazywana tylko wtedy, gdy wszystkie te pola
istnieją w /fields danego projektu i data_type. Dzięki temu ta sama lista
działa na kontach o różnych planach i różnych segmentacjach.

Testy pilnują niezmiennika: każde pole użyte w OQL recepty musi być
zadeklarowane w `needs` (inaczej recepta mogłaby wygenerować zapytanie
o nieistniejące pole).
"""

from __future__ import annotations

from typing import Any, Iterable

from .capabilities import FieldSet

# Grupy — kolejność wyznacza kolejność w UI.
GROUPS = [
    "Money pages",
    "Status & redirects",
    "Indexability",
    "Sitemaps",
    "Content quality",
    "Internal linking",
    "Performance",
    "AI crawlers & answers",
    "Googlebot & crawl budget",
    "Logs",
]

# Rodziny botów AI obecne w polach crawla (logs_bot_hits_* / logs_bot_status_code_*).
# Każda rodzina daje własne recepty, więc brak jednej nie ukrywa pozostałych.
AI_BOT_FAMILIES = [
    ("openai_gpt_bot", "OpenAI GPTBot"),
    ("openai_search_bot", "OpenAI SearchBot"),
    ("openai_chat_gpt_user", "ChatGPT-User"),
    ("claude_bot", "ClaudeBot"),
    ("claude_search_bot", "Claude-SearchBot"),
    ("claude_user", "Claude-User"),
    ("perplexity_bot", "PerplexityBot"),
    ("perplexity_user", "Perplexity-User"),
    ("google_gemini_deep_research", "Gemini Deep Research"),
    ("mistral_user", "Mistral-User"),
]

# Źródła ruchu z asystentów AI (logs_seo_visits_*).
AI_ANSWER_SOURCES = [
    ("openai", "ChatGPT"),
    ("perplexity", "Perplexity"),
    ("gemini", "Gemini"),
    ("claude", "Claude"),
    ("mistral", "Mistral"),
]


def _r(**kw) -> dict:
    kw.setdefault("sort", None)
    kw.setdefault("data_type", "pages")
    return kw


RECIPES: list[dict] = [
    # ------------------------------------------------------------------ #
    # Money pages — strony, które realnie zarabiają ruchem
    # ------------------------------------------------------------------ #
    _r(
        id="money_pages",
        label="Money pages (most SEO traffic)",
        group="Money pages",
        why="Pages with the most search traffic. Any issue here costs the most — check these first.",
        needs=["url", "seo_visits"],
        oql={"field": ["seo_visits", "gt", 0]},
        columns=["url", "seo_visits", "seo_visits_per_day", "status_code", "inrank", "depth", "word_count", "title"],
        sort="seo_visits:desc",
    ),
    _r(
        id="money_pages_at_risk",
        label="Money pages with errors",
        group="Money pages",
        why="Pages that earn traffic but return an error or redirect — direct revenue loss.",
        needs=["url", "seo_visits", "status_code"],
        oql={"and": [
            {"field": ["seo_visits", "gt", 0]},
            {"field": ["status_code", "gte", 300]},
        ]},
        columns=["url", "seo_visits", "status_code", "redirect_location", "depth"],
        sort="seo_visits:desc",
    ),
    _r(
        id="money_pages_not_indexable",
        label="Traffic pages that are non-indexable",
        group="Money pages",
        why="Pages with traffic that are blocked from indexing — a contradiction, usually a misconfiguration.",
        needs=["url", "seo_visits", "meta_robots_index"],
        oql={"and": [
            {"field": ["seo_visits", "gt", 0]},
            {"field": ["meta_robots_index", "equals", False]},
        ]},
        columns=["url", "seo_visits", "meta_robots", "meta_robots_index", "status_code"],
        sort="seo_visits:desc",
    ),
    _r(
        id="high_inrank_no_traffic",
        label="Strong internal linking but no traffic",
        group="Money pages",
        why="High InRank (lots of internal link equity) but zero traffic — untapped potential.",
        needs=["url", "inrank", "seo_visits"],
        oql={"and": [
            {"field": ["inrank", "gte", 5]},
            {"field": ["seo_visits", "equals", 0]},
        ]},
        columns=["url", "inrank", "seo_visits", "status_code", "word_count", "title"],
        sort="inrank:desc",
    ),

    # ------------------------------------------------------------------ #
    # Status & redirects
    # ------------------------------------------------------------------ #
    _r(
        id="errors_4xx_5xx",
        label="Errors 4xx / 5xx",
        group="Status & redirects",
        why="All pages returning a client or server error.",
        needs=["url", "status_code"],
        oql={"field": ["status_code", "gte", 400]},
        columns=["url", "status_code", "depth", "nb_inlinks", "seo_visits"],
        sort="nb_inlinks:desc",
    ),
    _r(
        id="errors_with_inlinks",
        label="404s that are linked internally",
        group="Status & redirects",
        why="Errors that your own pages link to — fix these first, they waste crawl budget and link equity.",
        needs=["url", "status_code", "nb_inlinks"],
        oql={"and": [
            {"field": ["status_code", "gte", 400]},
            {"field": ["nb_inlinks", "gt", 0]},
        ]},
        columns=["url", "status_code", "nb_inlinks", "follow_inlinks", "depth", "seo_visits"],
        sort="nb_inlinks:desc",
    ),
    _r(
        id="redirects_3xx",
        label="Redirects 3xx",
        group="Status & redirects",
        why="All redirects together with their destination.",
        needs=["url", "status_code"],
        oql={"and": [
            {"field": ["status_code", "gte", 300]},
            {"field": ["status_code", "lt", 400]},
        ]},
        columns=["url", "status_code", "redirect_location", "final_redirect_location", "depth", "nb_inlinks"],
        sort="nb_inlinks:desc",
    ),
    _r(
        id="redirect_chains",
        label="Redirect chains (2+ hops)",
        group="Status & redirects",
        why="Redirect chains waste crawl budget and leak link equity.",
        needs=["url", "redirect_count"],
        oql={"field": ["redirect_count", "gt", 1]},
        columns=["url", "redirect_count", "redirect_location", "final_redirect_location", "final_redirect_status"],
        sort="redirect_count:desc",
    ),
    _r(
        id="redirect_loops",
        label="Redirect loops",
        group="Status & redirects",
        why="Redirect loops — the page never resolves.",
        needs=["url", "is_redirect_loop"],
        oql={"field": ["is_redirect_loop", "equals", True]},
        columns=["url", "redirect_location", "redirect_count", "nb_inlinks"],
    ),

    # ------------------------------------------------------------------ #
    # Indexability
    # ------------------------------------------------------------------ #
    _r(
        id="noindex_pages",
        label="Noindex pages",
        group="Indexability",
        why="Pages excluded from the index via meta robots.",
        needs=["url", "meta_robots_index"],
        oql={"field": ["meta_robots_index", "equals", False]},
        columns=["url", "meta_robots", "status_code", "nb_inlinks", "seo_visits"],
        sort="nb_inlinks:desc",
    ),
    _r(
        id="robots_blocked",
        label="Blocked by robots.txt",
        group="Indexability",
        why="URLs blocked in robots.txt even though they are linked internally.",
        needs=["url", "robots_txt_denied"],
        oql={"field": ["robots_txt_denied", "equals", True]},
        columns=["url", "status_code", "nb_inlinks", "depth"],
        sort="nb_inlinks:desc",
    ),
    _r(
        id="canonicalized_away",
        label="Canonicalized to another URL",
        group="Indexability",
        why="Pages whose canonical points elsewhere — they will not be indexed on their own.",
        needs=["url", "is_canonical"],
        oql={"field": ["is_canonical", "equals", False]},
        columns=["url", "rel_canonical", "canonical_evaluation", "status_code", "seo_visits"],
        sort="seo_visits:desc",
    ),
    _r(
        id="canonical_issues",
        label="Canonical problems",
        group="Indexability",
        why="Conflicting or missing canonical declarations.",
        needs=["url", "canonical_evaluation"],
        oql={"field": ["canonical_evaluation", "not_equals", "matching"]},
        columns=["url", "canonical_evaluation", "canonical_declaration", "rel_canonical", "status_code"],
    ),
    _r(
        id="hreflang_errors",
        label="Hreflang errors",
        group="Indexability",
        why="Hreflang errors break language targeting across international markets.",
        needs=["url", "hreflang_errors"],
        oql={"field": ["hreflang_errors", "has_value"]},
        columns=["url", "hreflang_errors", "hreflang_langs", "language", "status_code"],
    ),

    # ------------------------------------------------------------------ #
    # Sitemaps
    # ------------------------------------------------------------------ #
    _r(
        id="sitemap_errors",
        label="Errors in sitemap",
        group="Sitemaps",
        why="URLs submitted in a sitemap that return an error — sitemaps should only contain 200s.",
        needs=["url", "sitemaps_file_origin", "status_code"],
        oql={"and": [
            {"field": ["sitemaps_file_origin", "has_value"]},
            {"field": ["status_code", "gte", 400]},
        ]},
        columns=["url", "status_code", "sitemaps_file_origin", "nb_inlinks", "seo_visits"],
        sort="status_code:desc",
    ),
    _r(
        id="sitemap_redirects",
        label="Redirects in sitemap",
        group="Sitemaps",
        why="A sitemap should point at final URLs, not redirects.",
        needs=["url", "sitemaps_file_origin", "status_code"],
        oql={"and": [
            {"field": ["sitemaps_file_origin", "has_value"]},
            {"field": ["status_code", "gte", 300]},
            {"field": ["status_code", "lt", 400]},
        ]},
        columns=["url", "status_code", "redirect_location", "sitemaps_file_origin"],
    ),
    _r(
        id="sitemap_noindex",
        label="Non-indexable pages in sitemap",
        group="Sitemaps",
        why="Conflicting signal: you submit the page for indexing while blocking it at the same time.",
        needs=["url", "sitemaps_file_origin", "meta_robots_index"],
        oql={"and": [
            {"field": ["sitemaps_file_origin", "has_value"]},
            {"field": ["meta_robots_index", "equals", False]},
        ]},
        columns=["url", "meta_robots", "sitemaps_file_origin", "status_code"],
    ),
    _r(
        id="sitemap_orphans",
        label="In sitemap but not linked (orphans)",
        group="Sitemaps",
        why="Pages in a sitemap with no internal links — hard to reach for both crawlers and users.",
        needs=["url", "sitemaps_file_origin", "nb_inlinks"],
        oql={"and": [
            {"field": ["sitemaps_file_origin", "has_value"]},
            {"field": ["nb_inlinks", "equals", 0]},
        ]},
        columns=["url", "nb_inlinks", "sitemaps_file_origin", "status_code", "seo_visits", "depth"],
    ),
    _r(
        id="missing_from_sitemap",
        label="Indexable pages missing from sitemap",
        group="Sitemaps",
        why="Good pages (200, indexable) that are missing from every sitemap.",
        needs=["url", "sitemaps_file_origin", "status_code", "meta_robots_index"],
        oql={"and": [
            {"field": ["sitemaps_file_origin", "has_no_value"]},
            {"field": ["status_code", "equals", 200]},
            {"field": ["meta_robots_index", "equals", True]},
        ]},
        columns=["url", "status_code", "seo_visits", "nb_inlinks", "depth", "word_count"],
        sort="seo_visits:desc",
    ),

    # ------------------------------------------------------------------ #
    # Content quality
    # ------------------------------------------------------------------ #
    _r(
        id="missing_title",
        label="Missing title",
        group="Content quality",
        why="A missing title is one of the most serious on-page gaps.",
        needs=["url", "title"],
        oql={"field": ["title", "has_no_value"]},
        columns=["url", "title", "status_code", "seo_visits", "nb_inlinks"],
        sort="seo_visits:desc",
    ),
    _r(
        id="duplicate_titles",
        label="Duplicate titles",
        group="Content quality",
        why="Duplicate titles make pages hard to tell apart in search results.",
        needs=["url", "has_duplicate_title_issue"],
        oql={"field": ["has_duplicate_title_issue", "equals", True]},
        columns=["url", "title", "duplicate_title_status", "seo_visits", "status_code"],
        sort="seo_visits:desc",
    ),
    _r(
        id="duplicate_descriptions",
        label="Duplicate meta descriptions",
        group="Content quality",
        why="Duplicate descriptions lower click-through rate in search results.",
        needs=["url", "has_duplicate_description_issue"],
        oql={"field": ["has_duplicate_description_issue", "equals", True]},
        columns=["url", "meta_description", "duplicate_description_status", "seo_visits"],
        sort="seo_visits:desc",
    ),
    _r(
        id="missing_description",
        label="Missing meta description",
        group="Content quality",
        why="No description — Google will generate its own, usually a worse one.",
        needs=["url", "meta_description"],
        oql={"field": ["meta_description", "has_no_value"]},
        columns=["url", "title", "meta_description", "seo_visits", "status_code"],
        sort="seo_visits:desc",
    ),
    _r(
        id="missing_h1",
        label="Missing H1",
        group="Content quality",
        why="Pages without an H1 heading.",
        needs=["url", "num_h1"],
        oql={"field": ["num_h1", "equals", 0]},
        columns=["url", "title", "num_h1", "word_count", "seo_visits"],
        sort="seo_visits:desc",
    ),
    _r(
        id="multiple_h1",
        label="Multiple H1 tags",
        group="Content quality",
        why="More than one H1 dilutes the page's main topic.",
        needs=["url", "num_h1"],
        oql={"field": ["num_h1", "gt", 1]},
        columns=["url", "num_h1", "h1", "title", "seo_visits"],
        sort="num_h1:desc",
    ),
    _r(
        id="thin_content",
        label="Thin content (<300 words)",
        group="Content quality",
        why="Little content means little chance of ranking for anything competitive.",
        needs=["url", "word_count", "status_code"],
        oql={"and": [
            {"field": ["word_count", "lt", 300]},
            {"field": ["status_code", "equals", 200]},
        ]},
        columns=["url", "word_count", "title", "status_code", "seo_visits", "depth"],
        sort="seo_visits:desc",
    ),
    _r(
        id="near_duplicates",
        label="Near-duplicate content",
        group="Content quality",
        why="Pages that are nearly identical — keyword cannibalisation and wasted crawl budget.",
        needs=["url", "has_nearduplicate_issue"],
        oql={"field": ["has_nearduplicate_issue", "equals", True]},
        columns=["url", "nearduplicate_content_similarity", "nearduplicate_status", "word_count", "seo_visits"],
        sort="nearduplicate_content_similarity:desc",
    ),
    _r(
        id="missing_alt",
        label="Images without alt text",
        group="Content quality",
        why="Missing alt attributes — hurts accessibility and image SEO.",
        needs=["url", "num_missing_alt"],
        oql={"field": ["num_missing_alt", "gt", 0]},
        columns=["url", "num_missing_alt", "num_img", "num_img_alt", "seo_visits"],
        sort="num_missing_alt:desc",
    ),

    # ------------------------------------------------------------------ #
    # Internal linking
    # ------------------------------------------------------------------ #
    _r(
        id="orphan_pages",
        label="Orphan pages (no inlinks)",
        group="Internal linking",
        why="Pages with no internal links — effectively invisible in the site structure.",
        needs=["url", "nb_inlinks", "status_code"],
        oql={"and": [
            {"field": ["nb_inlinks", "equals", 0]},
            {"field": ["status_code", "equals", 200]},
        ]},
        columns=["url", "nb_inlinks", "depth", "seo_visits", "word_count", "status_code"],
        sort="seo_visits:desc",
    ),
    _r(
        id="deep_pages",
        label="Deep pages (depth ≥ 5)",
        group="Internal linking",
        why="The deeper a page sits in the structure, the less often it gets crawled.",
        needs=["url", "depth"],
        oql={"field": ["depth", "gte", 5]},
        columns=["url", "depth", "nb_inlinks", "inrank", "seo_visits", "status_code"],
        sort="depth:desc",
    ),
    _r(
        id="nofollow_only",
        label="Pages with only nofollow inlinks",
        group="Internal linking",
        why="Pages reachable only through nofollow links — they receive no link equity.",
        needs=["url", "follow_inlinks", "nb_inlinks"],
        oql={"and": [
            {"field": ["follow_inlinks", "equals", 0]},
            {"field": ["nb_inlinks", "gt", 0]},
        ]},
        columns=["url", "nb_inlinks", "follow_inlinks", "nofollow_inlinks", "inrank", "seo_visits"],
        sort="nb_inlinks:desc",
    ),

    # ------------------------------------------------------------------ #
    # Performance / Core Web Vitals
    # ------------------------------------------------------------------ #
    _r(
        id="slow_pages",
        label="Slow pages (load > 1s)",
        group="Performance",
        why="Slow pages lose users and burn crawl budget.",
        needs=["url", "load_time"],
        oql={"field": ["load_time", "gte", 1000]},
        columns=["url", "load_time", "weight", "status_code", "seo_visits"],
        sort="load_time:desc",
    ),
    _r(
        id="poor_lcp",
        label="Poor LCP (> 2.5s)",
        group="Performance",
        why="Largest Contentful Paint above the Core Web Vitals 'good' threshold.",
        needs=["url", "cwv_lcp"],
        oql={"field": ["cwv_lcp", "gt", 2500]},
        columns=["url", "cwv_lcp", "cwv_cls", "cwv_tbt", "cwv_performance_score", "seo_visits"],
        sort="cwv_lcp:desc",
    ),
    _r(
        id="poor_cls",
        label="Poor CLS (> 0.1)",
        group="Performance",
        why="Cumulative Layout Shift above the 'good' threshold — content jumping around.",
        needs=["url", "cwv_cls"],
        oql={"field": ["cwv_cls", "gt", 0.1]},
        columns=["url", "cwv_cls", "cwv_lcp", "cwv_performance_score", "seo_visits"],
        sort="cwv_cls:desc",
    ),
    _r(
        id="low_perf_score",
        label="Low performance score (< 50)",
        group="Performance",
        why="The weakest pages by overall performance score.",
        needs=["url", "cwv_performance_score"],
        oql={"field": ["cwv_performance_score", "lt", 50]},
        columns=["url", "cwv_performance_score", "cwv_lcp", "cwv_tbt", "cwv_bytes_saving", "seo_visits"],
        sort="cwv_performance_score:asc",
    ),

    # ------------------------------------------------------------------ #
    # Googlebot & crawl budget
    # ------------------------------------------------------------------ #
    _r(
        id="not_crawled_by_google",
        label="Not crawled by Googlebot",
        group="Googlebot & crawl budget",
        why="Pages Googlebot did not visit during the analysed period.",
        needs=["url", "crawled_by_googlebot"],
        oql={"field": ["crawled_by_googlebot", "equals", False]},
        columns=["url", "crawled_by_googlebot", "googlebot_hits", "depth", "nb_inlinks", "seo_visits"],
        sort="nb_inlinks:desc",
    ),
    _r(
        id="googlebot_status_mismatch",
        label="Googlebot sees a different status",
        group="Googlebot & crawl budget",
        why="The status Googlebot sees differs from the crawl — possible cloaking or instability.",
        needs=["url", "googlebot_status_code_differ_from_oncrawl"],
        oql={"field": ["googlebot_status_code_differ_from_oncrawl", "equals", True]},
        columns=["url", "status_code", "googlebot_status_code", "googlebot_hits", "seo_visits"],
        sort="googlebot_hits:desc",
    ),
    _r(
        id="most_crawled",
        label="Most crawled by Googlebot",
        group="Googlebot & crawl budget",
        why="Where your crawl budget actually goes.",
        needs=["url", "googlebot_hits"],
        oql={"field": ["googlebot_hits", "gt", 0]},
        columns=["url", "googlebot_hits", "googlebot_hits_per_day", "seo_visits", "depth", "status_code"],
        sort="googlebot_hits:desc",
    ),
    # (recepty per bot AI dokładane niżej przez _ai_recipes())

    # ------------------------------------------------------------------ #
    # Logs (data_type = logs)
    # ------------------------------------------------------------------ #
    _r(
        id="log_bot_errors",
        label="Bots hitting errors",
        group="Logs",
        data_type="logs",
        why="Bots hitting errors — wasted crawl budget, straight from server logs.",
        needs=["event_url", "event_status_code", "event_is_bot_hit"],
        oql={"and": [
            {"field": ["event_is_bot_hit", "equals", True]},
            {"field": ["event_status_code", "gte", 400]},
        ]},
        columns=["event_url", "event_status_code", "event_bot_name", "event_bot_kind", "event_day"],
        sort="event_day:desc",
    ),
    _r(
        id="log_ai_bots",
        label="AI bot activity",
        group="Logs",
        data_type="logs",
        why="All AI bot visits (ai search / ai training / ai user) recorded in the logs.",
        needs=["event_url", "event_bot_kind"],
        oql={"or": [
            {"field": ["event_bot_kind", "equals", "ai search"]},
            {"field": ["event_bot_kind", "equals", "ai training"]},
            {"field": ["event_bot_kind", "equals", "ai user"]},
        ]},
        columns=["event_url", "event_bot_name", "event_bot_kind", "event_status_code", "event_day"],
        sort="event_day:desc",
    ),
    _r(
        id="log_seo_visits",
        label="SEO visits (from search)",
        group="Logs",
        data_type="logs",
        why="Actual search-engine entries recorded in the logs.",
        needs=["event_url", "event_is_seo_visit"],
        oql={"field": ["event_is_seo_visit", "equals", True]},
        columns=["event_url", "event_visit_source", "event_visit_device", "event_status_code", "event_day"],
        sort="event_day:desc",
    ),
    _r(
        id="log_slow_responses",
        label="Slow server responses (> 1s)",
        group="Logs",
        data_type="logs",
        why="URLs your server is slowest to return — real timings from logs, not a simulation.",
        needs=["event_url", "event_time_in_ms"],
        oql={"field": ["event_time_in_ms", "gt", 1000]},
        columns=["event_url", "event_time_in_ms", "event_status_code", "event_bot_name", "event_day"],
        sort="event_time_in_ms:desc",
    ),

    # ------------------------------------------------------------------ #
    # AI crawlers & answers — analizy z logów (data_type = logs)
    # ------------------------------------------------------------------ #
    _r(
        id="log_ai_bots_errors",
        label="AI bots hitting errors (4xx/5xx)",
        group="AI crawlers & answers",
        data_type="logs",
        why="AI crawlers receiving errors instead of content. Every such hit is a page that "
            "will not make it into AI answers — and it burns their crawl budget on your site.",
        needs=["event_url", "event_bot_kind", "event_status_code"],
        oql={"and": [
            {"or": [
                {"field": ["event_bot_kind", "equals", "ai search"]},
                {"field": ["event_bot_kind", "equals", "ai training"]},
                {"field": ["event_bot_kind", "equals", "ai user"]},
            ]},
            {"field": ["event_status_code", "gte", 400]},
        ]},
        columns=["event_url", "event_status_code", "event_bot_name", "event_bot_kind", "event_day"],
        sort="event_day:desc",
    ),
    _r(
        id="log_ai_bots_redirects",
        label="AI bots hitting redirects",
        group="AI crawlers & answers",
        data_type="logs",
        why="AI crawlers following redirects instead of getting content directly — "
            "some AI bots do not follow redirects at all, so the page may never be read.",
        needs=["event_url", "event_bot_kind", "event_status_code"],
        oql={"and": [
            {"or": [
                {"field": ["event_bot_kind", "equals", "ai search"]},
                {"field": ["event_bot_kind", "equals", "ai training"]},
                {"field": ["event_bot_kind", "equals", "ai user"]},
            ]},
            {"field": ["event_status_code", "gte", 300]},
            {"field": ["event_status_code", "lt", 400]},
        ]},
        columns=["event_url", "event_status_code", "event_bot_name", "event_bot_kind", "event_day"],
        sort="event_day:desc",
    ),
    _r(
        id="log_ai_search_vs_training",
        label="AI search bots only (answer engines)",
        group="AI crawlers & answers",
        data_type="logs",
        why="Bots that feed live answer engines ('ai search'), as opposed to training crawlers. "
            "These drive your visibility in AI answers right now.",
        needs=["event_url", "event_bot_kind"],
        oql={"field": ["event_bot_kind", "equals", "ai search"]},
        columns=["event_url", "event_bot_name", "event_status_code", "event_day", "event_urlpath"],
        sort="event_day:desc",
    ),
    _r(
        id="log_ai_training_bots",
        label="AI training crawlers only",
        group="AI crawlers & answers",
        data_type="logs",
        why="Crawlers collecting data for model training. Useful if you need to decide what to "
            "allow or block in robots.txt.",
        needs=["event_url", "event_bot_kind"],
        oql={"field": ["event_bot_kind", "equals", "ai training"]},
        columns=["event_url", "event_bot_name", "event_status_code", "event_day"],
        sort="event_day:desc",
    ),
    _r(
        id="log_ai_slow",
        label="Slow responses served to AI bots",
        group="AI crawlers & answers",
        data_type="logs",
        why="AI crawlers often use short timeouts. Slow responses mean the content may be "
            "skipped even though the URL returns 200.",
        needs=["event_url", "event_bot_kind", "event_time_in_ms"],
        oql={"and": [
            {"or": [
                {"field": ["event_bot_kind", "equals", "ai search"]},
                {"field": ["event_bot_kind", "equals", "ai training"]},
                {"field": ["event_bot_kind", "equals", "ai user"]},
            ]},
            {"field": ["event_time_in_ms", "gt", 1000]},
        ]},
        columns=["event_url", "event_time_in_ms", "event_bot_name", "event_status_code", "event_day"],
        sort="event_time_in_ms:desc",
    ),
    _r(
        id="log_ai_user_fetches",
        label="Live fetches triggered by AI users",
        group="AI crawlers & answers",
        data_type="logs",
        why="'ai user' hits happen when someone asks an assistant about a page and it fetches "
            "it live. Direct evidence that your content is being consulted in conversations.",
        needs=["event_url", "event_bot_kind"],
        oql={"field": ["event_bot_kind", "equals", "ai user"]},
        columns=["event_url", "event_bot_name", "event_status_code", "event_day", "event_referer"],
        sort="event_day:desc",
    ),
]


# --------------------------------------------------------------------------- #
# Recepty generowane per bot AI — dzięki temu brak jednej rodziny botów
# nie ukrywa pozostałych (pola różnią się między kontami i okresami).
# --------------------------------------------------------------------------- #
def _ai_recipes() -> list[dict]:
    out: list[dict] = []

    for key, name in AI_BOT_FAMILIES:
        hits = f"logs_bot_hits_{key}"
        status = f"logs_bot_status_code_{key}"

        out.append(_r(
            id=f"ai_crawled_{key}",
            label=f"Pages crawled by {name}",
            group="AI crawlers & answers",
            why=f"Which of your pages {name} actually fetched — the raw material for AI answers.",
            needs=["url", hits],
            oql={"field": [hits, "gt", 0]},
            columns=["url", hits, f"logs_bot_hits_per_day_{key}", status,
                     "status_code", "word_count", "seo_visits"],
            sort=f"{hits}:desc",
        ))

        # Kluczowa analiza: bot AI dostał błąd zamiast treści.
        out.append(_r(
            id=f"ai_errors_{key}",
            label=f"{name} received an error",
            group="AI crawlers & answers",
            why=f"Pages where {name} got a 4xx/5xx instead of content — these can never appear "
                f"in AI answers, and the bot wastes its budget on them.",
            needs=["url", status],
            oql={"field": [status, "gte", 400]},
            columns=["url", status, f"logs_bot_hits_{key}", "status_code",
                     "nb_inlinks", "seo_visits"],
            sort=f"logs_bot_hits_{key}:desc",
        ))

        # Rozbieżność: bot AI widzi co innego niż crawler.
        out.append(_r(
            id=f"ai_status_mismatch_{key}",
            label=f"{name} sees a different status than the crawl",
            group="AI crawlers & answers",
            why=f"The status {name} received differs from what the crawl saw — often rate "
                f"limiting, bot protection or geo/UA-based blocking aimed at AI crawlers.",
            needs=["url", status, "status_code"],
            oql={"and": [
                {"field": [status, "has_value"]},
                {"field": ["status_code", "equals", 200]},
                {"field": [status, "gte", 400]},
            ]},
            columns=["url", "status_code", status, f"logs_bot_hits_{key}", "seo_visits"],
            sort=f"logs_bot_hits_{key}:desc",
        ))

    # Ruch przychodzący z asystentów AI (odpowiedniki wizyt SEO).
    for key, name in AI_ANSWER_SOURCES:
        visits = f"logs_seo_visits_{key}"
        vstatus = f"logs_seo_visits_status_code_{key}"

        out.append(_r(
            id=f"ai_visits_{key}",
            label=f"Traffic arriving from {name}",
            group="AI crawlers & answers",
            why=f"Real visits that came to your site from {name} — proof your content is being "
                f"cited in its answers.",
            needs=["url", visits],
            oql={"field": [visits, "gt", 0]},
            columns=["url", visits, vstatus, "seo_visits", "status_code", "title"],
            sort=f"{visits}:desc",
        ))

        out.append(_r(
            id=f"ai_visits_broken_{key}",
            label=f"{name} sends users to a broken page",
            group="AI crawlers & answers",
            why=f"{name} cites a URL that returns an error — the worst case: the assistant "
                f"recommends you and the user lands on a broken page.",
            needs=["url", visits, "status_code"],
            oql={"and": [
                {"field": [visits, "gt", 0]},
                {"field": ["status_code", "gte", 400]},
            ]},
            columns=["url", visits, "status_code", "redirect_location", "seo_visits"],
            sort=f"{visits}:desc",
        ))

    # Analizy przekrojowe — wymagają GPTBota jako reprezentanta rodziny AI,
    # bo pole per-bot musi istnieć, by dało się zbudować filtr.
    out.append(_r(
        id="ai_crawled_not_google",
        label="Crawled by AI bots but not by Googlebot",
        group="AI crawlers & answers",
        why="Pages that AI crawlers found but Googlebot did not — content already feeding AI "
            "answers while remaining weak in classic search.",
        needs=["url", "logs_bot_hits_openai_gpt_bot", "crawled_by_googlebot"],
        oql={"and": [
            {"field": ["logs_bot_hits_openai_gpt_bot", "gt", 0]},
            {"field": ["crawled_by_googlebot", "equals", False]},
        ]},
        columns=["url", "logs_bot_hits_openai_gpt_bot", "crawled_by_googlebot",
                 "googlebot_hits", "depth", "word_count"],
        sort="logs_bot_hits_openai_gpt_bot:desc",
    ))
    out.append(_r(
        id="ai_ignoring_good_pages",
        label="Googlebot crawls them, AI bots ignore them",
        group="AI crawlers & answers",
        why="Pages Google fetches often but AI crawlers never touched — candidates for improving "
            "AI visibility (structure, clarity, robots.txt rules for AI agents).",
        needs=["url", "googlebot_hits", "logs_bot_hits_openai_gpt_bot"],
        oql={"and": [
            {"field": ["googlebot_hits", "gt", 0]},
            {"field": ["logs_bot_hits_openai_gpt_bot", "equals", 0]},
        ]},
        columns=["url", "googlebot_hits", "logs_bot_hits_openai_gpt_bot",
                 "word_count", "seo_visits", "status_code"],
        sort="googlebot_hits:desc",
    ))
    out.append(_r(
        id="ai_crawling_thin_content",
        label="AI bots crawling thin content",
        group="AI crawlers & answers",
        why="AI crawlers spending their budget on pages with almost no content — you are "
            "teaching assistants your weakest material.",
        needs=["url", "logs_bot_hits_openai_gpt_bot", "word_count"],
        oql={"and": [
            {"field": ["logs_bot_hits_openai_gpt_bot", "gt", 0]},
            {"field": ["word_count", "lt", 300]},
        ]},
        columns=["url", "logs_bot_hits_openai_gpt_bot", "word_count", "status_code", "title"],
        sort="logs_bot_hits_openai_gpt_bot:desc",
    ))
    out.append(_r(
        id="ai_crawling_noindex",
        label="AI bots crawling noindex pages",
        group="AI crawlers & answers",
        why="Pages you exclude from search but AI crawlers still read — noindex does not stop "
            "AI agents; that needs robots.txt rules for their user agents.",
        needs=["url", "logs_bot_hits_openai_gpt_bot", "meta_robots_index"],
        oql={"and": [
            {"field": ["logs_bot_hits_openai_gpt_bot", "gt", 0]},
            {"field": ["meta_robots_index", "equals", False]},
        ]},
        columns=["url", "logs_bot_hits_openai_gpt_bot", "meta_robots", "status_code", "word_count"],
        sort="logs_bot_hits_openai_gpt_bot:desc",
    ))

    return out


RECIPES.extend(_ai_recipes())


def _fields_in_oql(node: Any) -> Iterable[str]:
    """Wyciąga nazwy pól użyte w drzewie OQL (do walidacji recept)."""
    if not isinstance(node, dict):
        return
    for op in ("and", "or"):
        if op in node:
            for child in node[op]:
                yield from _fields_in_oql(child)
            return
    leaf = node.get("field")
    if isinstance(leaf, list) and leaf:
        yield leaf[0]


def applicable_recipes(fieldset: FieldSet, data_type: str) -> list[dict]:
    """Recepty wykonalne dla danego data_type i zestawu pól.

    Recepta przechodzi, gdy wszystkie pola z `needs` istnieją, a pola użyte
    w OQL są filtrowalne. Kolumny są przycinane do tych, które faktycznie
    istnieją i da się wyświetlić; sort odpada, jeśli pole nie jest sortowalne.
    """
    out: list[dict] = []
    for rec in RECIPES:
        if rec["data_type"] != data_type:
            continue
        if not all(fieldset.exists(n) for n in rec["needs"]):
            continue
        if not all(fieldset.can_filter(f) for f in _fields_in_oql(rec["oql"])):
            continue

        columns = [c for c in rec["columns"] if fieldset.exists(c) and fieldset.can_display(c)]
        if not columns:
            continue

        sort = rec.get("sort")
        if sort:
            sort_field = sort.split(":")[0]
            if not fieldset.can_sort(sort_field):
                sort = None

        out.append(
            {
                "id": rec["id"],
                "label": rec["label"],
                "group": rec["group"],
                "why": rec["why"],
                "data_type": rec["data_type"],
                "oql": rec["oql"],
                "columns": columns,
                "sort": sort,
            }
        )
    # Kolejność grup jak w GROUPS, w grupie — kolejność definicji.
    out.sort(key=lambda r: GROUPS.index(r["group"]) if r["group"] in GROUPS else len(GROUPS))
    return out
