import type { Dict } from './pl';

export const en: Dict = {
  lang: 'en',
  locale: 'en_GB',
  path: '/en/',
  meta: {
    title: 'Technical SEO & AI Search Consultant | Maciej Zięciak, 9 years of experience',
    description:
      'Technical SEO and AI search visibility for large websites, e-commerce and enterprise. 9 years of experience: audits, rendering, indexation, migrations, hreflang and AI crawler access.',
  },
  ids: { services: 'services', experience: 'experience', process: 'process', faq: 'faq', contact: 'contact', gets: 'what-you-get' },
  skip: 'Skip to content',
  nav: {
    services: 'Services',
    experience: 'Experience',
    process: 'Process',
    faq: 'FAQ',
    contact: 'Contact',
    cta: 'Book a call',
    switchLabel: 'Wersja polska',
    menu: 'Menu',
    close: 'Close',
  },
  hero: {
    pill: 'Technical SEO & AI Search · 9 years of experience',
    titleA: 'Visible in Google.',
    titleB: 'Cited by AI.',
    lead:
      'Technical SEO and AI search for large websites, online stores and enterprise brands. I find and fix what blocks your traffic from Google and AI answers, with clear priorities and tickets your team can ship.',
    ctaPrimary: 'Book a free consultation',
    ctaSecondary: 'See my experience',
    ctaNote: '30 minutes · online · no strings attached',
    trustLabel: 'Experience includes',
    card: {
      title: 'Who can see your page?',
      url: 'example.com/category/product',
      note: 'Sample excerpt from an audit',
      summary: '3 of 6 bots have trouble accessing the content',
      rows: [
        { bot: 'Googlebot', s: 'ok', t: '200 · renders JS · indexable' },
        { bot: 'Bingbot', s: 'ok', t: '200 · indexable' },
        { bot: 'OAI-SearchBot', s: 'warn', t: 'Sees 38% of content without JS' },
        { bot: 'PerplexityBot', s: 'err', t: '403 · blocked by WAF' },
        { bot: 'ClaudeBot', s: 'err', t: 'Disallowed in robots.txt' },
        { bot: 'Google-Extended', s: 'ok', t: 'Allowed' },
      ],
    },
  },
  statement: {
    label: 'Why now',
    parts: [
      { t: 'Google is no longer the only place your customers search. They ask ChatGPT, Perplexity and AI Overviews. The question is: ' },
      { t: 'is your website in the answer?', mark: true },
    ],
  },
  stage: {
    eyebrow: 'Bot access audit',
    title: 'See your site through the eyes of bots.',
    text: 'Googlebot renders JavaScript. Most AI crawlers don’t. I check what each of them actually sees, and what your WAF, CDN or robots.txt blocks along the way.',
  },
  stats: {
    label: 'By the numbers',
    items: [
      { v: '9 years', k: 'in SEO: agency, own project, consulting, enterprise' },
      { v: '1.1M', k: 'pages on a website I grew from scratch' },
      { v: '670k', k: 'URLs indexed by Google at peak' },
      { v: '115k', k: 'monthly organic visits at peak' },
    ],
  },
  tools: {
    label: 'Tools I work with',
    items: ['Botify', 'Lumar', 'OnCrawl', 'Screaming Frog', 'GetBeast'],
  },
  bands: {
    afterServices: {
      title: 'Not sure where to start?',
      text: 'On a free consultation I’ll review your site and point out the 3 things worth fixing first.',
      btn: 'Book a free consultation',
    },
    afterProcess: {
      title: 'The first step takes 30 minutes.',
      text: 'A short call, concrete takeaways, no commitment.',
      btn: 'Pick a time for a call',
    },
  },
  compare: {
    label: 'Why a consultant, not an agency',
    title: 'A senior on your project. From day one.',
    me: 'With me',
    them: 'Typical agency',
    rows: [
      { k: 'Who does the work', me: 'Me, personally: from audit to release review', them: 'Often a junior; the senior shows up in meetings' },
      { k: 'Specialism', me: 'Technical SEO and AI search', them: 'A bit of everything: SEO, Ads, social' },
      { k: 'Experience', me: '9 years, incl. enterprise at PMI and Accenture Song', them: 'Depends on who gets assigned' },
      { k: 'What you get', me: 'Developer tickets ranked by impact', them: 'A PDF report and a rankings summary' },
      { k: 'Contact', me: 'Directly with me', them: 'Through an account manager' },
      { k: 'Engagement', me: 'One-off audit or ongoing support, your call', them: 'Often packages with minimum terms' },
    ],
  },
  sticky: { text: 'Free consultation · 30 min', btn: 'Book' },
  services: {
    label: 'Services',
    title: 'How I can help',
    intro:
      'Technical SEO is the foundation. If search engines and AI crawlers can’t fetch, render and understand a page, content and links won’t perform the way they should.',
    items: [
      {
        name: 'Technical SEO audit',
        desc: 'Crawling, JavaScript rendering, indexation, canonicals, redirects, Core Web Vitals and server logs. You get issues ranked by traffic impact, with ready-to-ship developer tickets.',
        tags: ['Crawl & rendering', 'Indexation', 'Server logs', 'Core Web Vitals'],
      },
      {
        name: 'AI search & LLM visibility',
        desc: 'I check whether AI crawlers can access your content and see it without JavaScript, fix structured data and entities, then measure how your brand shows up in ChatGPT, Perplexity and AI Overviews.',
        tags: ['AI crawler access', 'Schema.org', 'Entities', 'Citation tracking'],
      },
      {
        name: 'Large sites & programmatic SEO',
        desc: 'Hundreds of thousands of URLs, faceted navigation, crawl budget, page templates. I grew a website past one million pages myself, so I know where these projects break.',
        tags: ['Crawl budget', 'Faceted navigation', 'Templates', 'Scale'],
      },
      {
        name: 'Enterprise & international SEO',
        desc: 'Adobe Experience Manager, multiple markets and language versions, hreflang. Working with development teams and within corporate processes.',
        tags: ['AEM', 'Hreflang', 'Multi-market', 'Dev processes'],
      },
      {
        name: 'Migrations & relaunches',
        desc: 'Changing CMS, domain or URL structure without losing traffic: redirect mapping, pre-launch testing and post-launch monitoring.',
        tags: ['Redirect mapping', 'Pre-launch QA', 'Monitoring'],
      },
      {
        name: 'E-commerce SEO',
        desc: 'Categories, filters, product pages and indexation control. Hands-on with PrestaShop, Magento, WordPress, Shoper, RedCart and custom platforms.',
        tags: ['Categories & filters', 'Product pages', 'PL & CZ markets'],
      },
    ],
  },
  experience: {
    label: 'Experience',
    title: '9 years in SEO',
    intro:
      'From an agency and my own project, through consulting, to enterprise teams at Accenture Song and Philip Morris International.',
    items: [
      {
        when: '2026 — present',
        org: 'Philip Morris International',
        role: 'Manager SEO & AI Search Operations',
        desc: 'Previously Tech SEO Operations Senior Specialist.',
      },
      {
        when: '2021 — 2026',
        org: 'Accenture Song',
        role: 'Digital Marketing Senior Strategy Analyst (SEO)',
        desc: 'Previously Senior Technical SEO Expert. Technical SEO strategy for international audiences, Adobe Experience Manager websites.',
      },
      {
        when: '2020 — 2022',
        org: 'Self-employed',
        role: 'SEO Consultant',
        desc: 'Audits and consulting: technical SEO, on-page and off-page.',
      },
      {
        when: '2019 — 2021',
        org: 'IG',
        role: 'Technical SEO Specialist',
        desc: 'Optimising websites built on Adobe Experience Manager.',
      },
      {
        when: '2018 — 2019',
        org: 'SEO agency, Kraków',
        role: 'E-commerce SEO, PL & CZ markets',
        desc: 'Audits, strategy and implementation across many store platforms, client workshops, coordination within a 20-person team.',
      },
      {
        when: '2017 — 2023',
        org: 'Own project',
        role: 'Co-founder, SEO lead',
        desc: 'A Polish business directory where I was the only SEO: over 1.1M pages, 670k indexed URLs and 115k monthly organic visits at peak. Later consulted for the new owners.',
        highlight: true,
      },
    ],
  },
  process: {
    label: 'Process',
    title: 'How I work',
    steps: [
      { name: 'Diagnosis', desc: 'Data access, crawl, logs, rendering and bot-access analysis. I find out where the site is really losing.' },
      { name: 'Priorities', desc: 'Actions ranked by impact and cost of implementation, with KPIs tied to business goals.' },
      { name: 'Execution', desc: 'Developer tickets, pre-release review, team support, and hands-on implementation when needed.' },
      { name: 'Measurement', desc: 'Monitoring indexation, traffic and AI search presence. I move priorities to wherever the data shows the best return.' },
    ],
  },
  faq: {
    label: 'FAQ',
    title: 'Common questions',
    items: [
      {
        q: 'What happens on the free consultation?',
        a: '30 minutes online. You tell me about the site and your goals; I review it live and point out the 3 things worth fixing first. No commitment: after the call you decide whether we go further.',
      },
      {
        q: 'How is technical SEO different from “regular” SEO?',
        a: 'Technical SEO decides whether search engines and AI crawlers can find, fetch, render and understand your site. If something is broken here, content and links can’t perform fully, no matter how good they are.',
      },
      {
        q: 'Can you “rank” a website in ChatGPT?',
        a: 'There’s no single switch. What you can do is make sure AI crawlers can access your content, see it without JavaScript, understand what your brand is (entities, structured data), and that your brand appears in the sources models rely on. The results are measurable.',
      },
      {
        q: 'Do you work with large and enterprise websites?',
        a: 'Yes, that’s my specialty: sites with hundreds of thousands of URLs, platforms such as Adobe Experience Manager, multiple markets and languages, and working within development processes.',
      },
      {
        q: 'Do you advise or also implement?',
        a: 'Both. Most often I write developer tickets and review changes, but I can implement parts of the work myself.',
      },
      {
        q: 'Can you work with our agency or dev partner?',
        a: 'Yes. I usually work alongside the client’s dev teams and agencies: writing tickets, reviewing changes and answering technical questions.',
      },
      {
        q: 'Will you sign an NDA?',
        a: 'Yes. For projects that need access to data, logs and code, signing an NDA before we start is standard.',
      },
      {
        q: 'How much does it cost?',
        a: 'Audits are a one-off fee, ongoing work is billed monthly. The price depends on the size of the site and the scope. After a short call you get a concrete quote.',
      },
    ],
  },
  contact: {
    label: 'Contact',
    title: 'Let’s talk about your website.',
    lead: 'On a free 30-minute call I’ll review your site and point out the 3 things worth fixing first. No strings attached.',
    topicsLabel: 'What is it about?',
    topics: ['Technical audit', 'AI search', 'Large website', 'Enterprise / AEM', 'Migration', 'Ongoing work'],
    urlLabel: 'Website',
    urlPlaceholder: 'https://yourcompany.com',
    msgLabel: 'Message',
    msgPlaceholder: 'What do you do and what do you want to achieve?',
    submit: 'Book a free consultation',
    note: 'I reply personally. Your details are used only to answer your enquiry.',
    booking: 'Prefer to pick a time right away?',
    bookingBtn: 'Open calendar',
    sending: 'Sending…',
    success: 'Thanks! Your message is in. I’ll get back to you with a time for the call.',
    error: 'Something went wrong. Please email me directly at',
    subject: 'SEO inquiry — maciejzieciak.com',
    bodyTopics: 'Topic',
    bodyUrl: 'Website',
    orEmail: 'Or email me directly',
  },
  footer: {
    rights: 'All rights reserved.',
    top: 'Back to top',
    built: 'Static HTML, zero trackers, self-hosted fonts.',
  },
};
