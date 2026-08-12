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
    "Bots & AI crawlers",
    "Logs",
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
        why="Strony z największym ruchem z wyszukiwarek. Tu każdy błąd kosztuje najwięcej — sprawdzaj je najpierw.",
        needs=["url", "seo_visits"],
        oql={"field": ["seo_visits", "gt", 0]},
        columns=["url", "seo_visits", "seo_visits_per_day", "status_code", "inrank", "depth", "word_count", "title"],
        sort="seo_visits:desc",
    ),
    _r(
        id="money_pages_at_risk",
        label="Money pages with errors",
        group="Money pages",
        why="Strony z ruchem, które zwracają błąd lub przekierowanie — bezpośrednia utrata pieniędzy.",
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
        why="Strony mające ruch, ale zablokowane dla indeksowania — sprzeczność, która zwykle oznacza błąd konfiguracji.",
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
        why="Wysoki InRank (dużo mocy z linkowania wewnętrznego), a zero ruchu — potencjał do odzyskania.",
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
        why="Wszystkie strony zwracające błąd klienta lub serwera.",
        needs=["url", "status_code"],
        oql={"field": ["status_code", "gte", 400]},
        columns=["url", "status_code", "depth", "nb_inlinks", "seo_visits"],
        sort="nb_inlinks:desc",
    ),
    _r(
        id="errors_with_inlinks",
        label="404s that are linked internally",
        group="Status & redirects",
        why="Błędy, do których prowadzą linki z Twojej strony — to te warto naprawić w pierwszej kolejności.",
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
        why="Wszystkie przekierowania wraz z celem.",
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
        why="Łańcuchy przekierowań marnują budżet crawlowania i tracą moc linków.",
        needs=["url", "redirect_count"],
        oql={"field": ["redirect_count", "gt", 1]},
        columns=["url", "redirect_count", "redirect_location", "final_redirect_location", "final_redirect_status"],
        sort="redirect_count:desc",
    ),
    _r(
        id="redirect_loops",
        label="Redirect loops",
        group="Status & redirects",
        why="Pętle przekierowań — strona nigdy się nie otworzy.",
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
        why="Strony wykluczone z indeksu przez meta robots.",
        needs=["url", "meta_robots_index"],
        oql={"field": ["meta_robots_index", "equals", False]},
        columns=["url", "meta_robots", "status_code", "nb_inlinks", "seo_visits"],
        sort="nb_inlinks:desc",
    ),
    _r(
        id="robots_blocked",
        label="Blocked by robots.txt",
        group="Indexability",
        why="Adresy zablokowane w robots.txt, mimo że są linkowane.",
        needs=["url", "robots_txt_denied"],
        oql={"field": ["robots_txt_denied", "equals", True]},
        columns=["url", "status_code", "nb_inlinks", "depth"],
        sort="nb_inlinks:desc",
    ),
    _r(
        id="canonicalized_away",
        label="Canonicalized to another URL",
        group="Indexability",
        why="Strony wskazujące canonical na inny adres — nie będą indeksowane samodzielnie.",
        needs=["url", "is_canonical"],
        oql={"field": ["is_canonical", "equals", False]},
        columns=["url", "rel_canonical", "canonical_evaluation", "status_code", "seo_visits"],
        sort="seo_visits:desc",
    ),
    _r(
        id="canonical_issues",
        label="Canonical problems",
        group="Indexability",
        why="Konflikty i braki w deklaracjach canonical.",
        needs=["url", "canonical_evaluation"],
        oql={"field": ["canonical_evaluation", "not_equals", "matching"]},
        columns=["url", "canonical_evaluation", "canonical_declaration", "rel_canonical", "status_code"],
    ),
    _r(
        id="hreflang_errors",
        label="Hreflang errors",
        group="Indexability",
        why="Błędy hreflang psują targetowanie językowe na rynkach międzynarodowych.",
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
        why="Adresy zgłoszone w sitemapie, które zwracają błąd — sitemapa powinna zawierać tylko strony 200.",
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
        why="Sitemapa powinna wskazywać docelowe adresy, nie przekierowania.",
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
        why="Sprzeczny sygnał: zgłaszasz stronę do indeksu, a jednocześnie ją blokujesz.",
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
        why="Strony w sitemapie bez żadnego linku wewnętrznego — trudne do znalezienia dla robotów i użytkowników.",
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
        why="Dobre strony (200, indeksowalne), których nie ma w żadnej sitemapie.",
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
        why="Brak tytułu to jeden z najpoważniejszych braków on-page.",
        needs=["url", "title"],
        oql={"field": ["title", "has_no_value"]},
        columns=["url", "title", "status_code", "seo_visits", "nb_inlinks"],
        sort="seo_visits:desc",
    ),
    _r(
        id="duplicate_titles",
        label="Duplicate titles",
        group="Content quality",
        why="Powielone tytuły utrudniają rozróżnienie stron w wynikach wyszukiwania.",
        needs=["url", "has_duplicate_title_issue"],
        oql={"field": ["has_duplicate_title_issue", "equals", True]},
        columns=["url", "title", "duplicate_title_status", "seo_visits", "status_code"],
        sort="seo_visits:desc",
    ),
    _r(
        id="duplicate_descriptions",
        label="Duplicate meta descriptions",
        group="Content quality",
        why="Powielone opisy obniżają CTR w wynikach.",
        needs=["url", "has_duplicate_description_issue"],
        oql={"field": ["has_duplicate_description_issue", "equals", True]},
        columns=["url", "meta_description", "duplicate_description_status", "seo_visits"],
        sort="seo_visits:desc",
    ),
    _r(
        id="missing_description",
        label="Missing meta description",
        group="Content quality",
        why="Brak opisu — Google wygeneruje własny, zwykle gorszy.",
        needs=["url", "meta_description"],
        oql={"field": ["meta_description", "has_no_value"]},
        columns=["url", "title", "meta_description", "seo_visits", "status_code"],
        sort="seo_visits:desc",
    ),
    _r(
        id="missing_h1",
        label="Missing H1",
        group="Content quality",
        why="Strony bez nagłówka H1.",
        needs=["url", "num_h1"],
        oql={"field": ["num_h1", "equals", 0]},
        columns=["url", "title", "num_h1", "word_count", "seo_visits"],
        sort="seo_visits:desc",
    ),
    _r(
        id="multiple_h1",
        label="Multiple H1 tags",
        group="Content quality",
        why="Więcej niż jeden H1 rozmywa główny temat strony.",
        needs=["url", "num_h1"],
        oql={"field": ["num_h1", "gt", 1]},
        columns=["url", "num_h1", "h1", "title", "seo_visits"],
        sort="num_h1:desc",
    ),
    _r(
        id="thin_content",
        label="Thin content (<300 words)",
        group="Content quality",
        why="Mało treści = mała szansa na ranking na cokolwiek konkurencyjnego.",
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
        why="Strony niemal identyczne treściowo — kanibalizacja i marnowanie budżetu crawlowania.",
        needs=["url", "has_nearduplicate_issue"],
        oql={"field": ["has_nearduplicate_issue", "equals", True]},
        columns=["url", "nearduplicate_content_similarity", "nearduplicate_status", "word_count", "seo_visits"],
        sort="nearduplicate_content_similarity:desc",
    ),
    _r(
        id="missing_alt",
        label="Images without alt text",
        group="Content quality",
        why="Brakujące atrybuty alt — dostępność i SEO obrazków.",
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
        why="Strony bez linków wewnętrznych — praktycznie niewidoczne w strukturze serwisu.",
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
        why="Im głębiej strona siedzi w strukturze, tym rzadziej jest crawlowana.",
        needs=["url", "depth"],
        oql={"field": ["depth", "gte", 5]},
        columns=["url", "depth", "nb_inlinks", "inrank", "seo_visits", "status_code"],
        sort="depth:desc",
    ),
    _r(
        id="nofollow_only",
        label="Pages with only nofollow inlinks",
        group="Internal linking",
        why="Strony, do których prowadzą wyłącznie linki nofollow — nie dostają mocy.",
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
        why="Wolne strony tracą użytkowników i budżet crawlowania.",
        needs=["url", "load_time"],
        oql={"field": ["load_time", "gte", 1000]},
        columns=["url", "load_time", "weight", "status_code", "seo_visits"],
        sort="load_time:desc",
    ),
    _r(
        id="poor_lcp",
        label="Poor LCP (> 2.5s)",
        group="Performance",
        why="Largest Contentful Paint powyżej progu 'good' wg Core Web Vitals.",
        needs=["url", "cwv_lcp"],
        oql={"field": ["cwv_lcp", "gt", 2500]},
        columns=["url", "cwv_lcp", "cwv_cls", "cwv_tbt", "cwv_performance_score", "seo_visits"],
        sort="cwv_lcp:desc",
    ),
    _r(
        id="poor_cls",
        label="Poor CLS (> 0.1)",
        group="Performance",
        why="Cumulative Layout Shift powyżej progu 'good' — skacząca zawartość.",
        needs=["url", "cwv_cls"],
        oql={"field": ["cwv_cls", "gt", 0.1]},
        columns=["url", "cwv_cls", "cwv_lcp", "cwv_performance_score", "seo_visits"],
        sort="cwv_cls:desc",
    ),
    _r(
        id="low_perf_score",
        label="Low performance score (< 50)",
        group="Performance",
        why="Najsłabsze strony wg łącznego wyniku wydajności.",
        needs=["url", "cwv_performance_score"],
        oql={"field": ["cwv_performance_score", "lt", 50]},
        columns=["url", "cwv_performance_score", "cwv_lcp", "cwv_tbt", "cwv_bytes_saving", "seo_visits"],
        sort="cwv_performance_score:asc",
    ),

    # ------------------------------------------------------------------ #
    # Bots & AI crawlers (dane z crawla wzbogacone logami)
    # ------------------------------------------------------------------ #
    _r(
        id="not_crawled_by_google",
        label="Not crawled by Googlebot",
        group="Bots & AI crawlers",
        why="Strony, których Googlebot nie odwiedził w analizowanym okresie.",
        needs=["url", "crawled_by_googlebot"],
        oql={"field": ["crawled_by_googlebot", "equals", False]},
        columns=["url", "crawled_by_googlebot", "googlebot_hits", "depth", "nb_inlinks", "seo_visits"],
        sort="nb_inlinks:desc",
    ),
    _r(
        id="googlebot_status_mismatch",
        label="Googlebot sees a different status",
        group="Bots & AI crawlers",
        why="Status widziany przez Googlebota różni się od tego z crawla — możliwe cloaking lub niestabilność.",
        needs=["url", "googlebot_status_code_differ_from_oncrawl"],
        oql={"field": ["googlebot_status_code_differ_from_oncrawl", "equals", True]},
        columns=["url", "status_code", "googlebot_status_code", "googlebot_hits", "seo_visits"],
        sort="googlebot_hits:desc",
    ),
    _r(
        id="most_crawled",
        label="Most crawled by Googlebot",
        group="Bots & AI crawlers",
        why="Gdzie realnie idzie budżet crawlowania.",
        needs=["url", "googlebot_hits"],
        oql={"field": ["googlebot_hits", "gt", 0]},
        columns=["url", "googlebot_hits", "googlebot_hits_per_day", "seo_visits", "depth", "status_code"],
        sort="googlebot_hits:desc",
    ),
    _r(
        id="ai_crawlers_openai",
        label="Pages crawled by OpenAI bots",
        group="Bots & AI crawlers",
        why="Które strony zbiera OpenAI (GPTBot / SearchBot / ChatGPT-User) — widoczność w odpowiedziach AI.",
        needs=["url", "logs_bot_hits_openai_gpt_bot"],
        oql={"field": ["logs_bot_hits_openai_gpt_bot", "gt", 0]},
        columns=["url", "logs_bot_hits_openai_gpt_bot", "logs_bot_hits_openai_search_bot",
                 "logs_bot_hits_openai_chat_gpt_user", "seo_visits", "status_code"],
        sort="logs_bot_hits_openai_gpt_bot:desc",
    ),
    _r(
        id="ai_crawlers_anthropic",
        label="Pages crawled by Claude bots",
        group="Bots & AI crawlers",
        why="Aktywność botów Anthropic (ClaudeBot / Claude-SearchBot / Claude-User).",
        needs=["url", "logs_bot_hits_claude_bot"],
        oql={"field": ["logs_bot_hits_claude_bot", "gt", 0]},
        columns=["url", "logs_bot_hits_claude_bot", "logs_bot_hits_claude_search_bot",
                 "logs_bot_hits_claude_user", "seo_visits", "status_code"],
        sort="logs_bot_hits_claude_bot:desc",
    ),
    _r(
        id="ai_visits",
        label="Traffic coming from AI assistants",
        group="Bots & AI crawlers",
        why="Wizyty przychodzące z ChatGPT / Perplexity / Gemini — nowy kanał ruchu.",
        needs=["url", "logs_seo_visits_openai"],
        oql={"field": ["logs_seo_visits_openai", "gt", 0]},
        columns=["url", "logs_seo_visits_openai", "logs_seo_visits_perplexity", "logs_seo_visits_gemini",
                 "logs_seo_visits_claude", "seo_visits"],
        sort="logs_seo_visits_openai:desc",
    ),

    # ------------------------------------------------------------------ #
    # Logs (data_type = logs)
    # ------------------------------------------------------------------ #
    _r(
        id="log_bot_errors",
        label="Bots hitting errors",
        group="Logs",
        data_type="logs",
        why="Boty trafiające na błędy — marnowany budżet crawlowania, widoczne w logach serwera.",
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
        why="Wszystkie odwiedziny botów AI (ai search / ai training / ai user) w logach.",
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
        why="Realne wejścia z wyszukiwarek zarejestrowane w logach.",
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
        why="Adresy, które serwer oddaje najwolniej — realne czasy z logów, nie symulacja.",
        needs=["event_url", "event_time_in_ms"],
        oql={"field": ["event_time_in_ms", "gt", 1000]},
        columns=["event_url", "event_time_in_ms", "event_status_code", "event_bot_name", "event_day"],
        sort="event_time_in_ms:desc",
    ),
]


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
