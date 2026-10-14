import type { Dict } from './pl';

export const en: Dict = {
  lang: 'en',
  locale: 'en_US',
  path: '/en/',
  meta: {
    title: 'Maciej Zięciak — SEO Consultant | Audits, Strategy, AI Search Visibility',
    description:
      'Independent SEO consultant. Technical audits, content strategy, e-commerce SEO, site migrations and visibility in AI search. Organic traffic that turns into revenue.',
  },
  skip: 'Skip to content',
  nav: {
    services: 'Services',
    process: 'Process',
    about: 'About',
    faq: 'FAQ',
    contact: 'Contact',
    cta: 'Let’s talk',
    switchLabel: 'Wersja polska',
    menu: 'Menu',
    close: 'Close',
  },
  hero: {
    pill: 'SEO consultant · EN / PL',
    title: [{ t: 'Your business on ' }, { t: 'page one.', hl: true }, { t: ' And in the black.' }],
    sticker: ['SEO', '+ AI', 'search'],
    lead:
      'An SEO consultant who speaks human. Audits, content strategy and visibility in Google and ChatGPT — so your traffic ends in an inquiry, not just a pretty chart.',
    ctaPrimary: 'Book a free call',
    ctaSecondary: 'What do I do?',
  },
  serp: {
    pill: 'Simulation',
    title: 'From the back pages straight to the top.',
    text: 'This is the direction I work towards: your site where customers actually click. No honest consultant guarantees rankings — I guarantee the method and full transparency.',
    query: 'seo consultant',
    label: 'Search results — simulation',
    title2: 'Maciej Zięciak — SEO Consultant',
    snippet: 'Technical audits, content strategy and AI search visibility.',
    replay: 'Play again',
  },
  ticker: [
    'Technical SEO',
    'Core Web Vitals',
    'Content strategy',
    'AI Overviews & GEO',
    'E-commerce SEO',
    'Site migrations',
    'Structured data',
    'Link building',
    'Local SEO',
    'Analytics & GA4',
  ],
  services: {
    label: 'Services',
    title: 'How I can help',
    intro: 'Six areas where I make the biggest difference. Take one, or take them all.',
    deliverablesLabel: 'You get',
    timeLabel: 'Timeline',
    items: [
      {
        name: 'Technical audit',
        tag: 'Technical SEO',
        desc:
          'Crawling, indexation, JavaScript rendering, information architecture, Core Web Vitals. I look for everything that stops Google from understanding and rewarding your site.',
        deliverables: ['Issues ranked by traffic impact', 'Ready-to-ship developer tickets', 'Walkthrough call'],
        time: '2–3 weeks',
      },
      {
        name: 'Content strategy',
        tag: 'Content',
        desc:
          'Keyword research built on intent, not volume. Topic maps, competitive gaps and a publishing plan that makes business sense.',
        deliverables: ['Topic and cluster map', 'Writer briefs', 'Priorities ranked by revenue potential'],
        time: '3–4 weeks',
      },
      {
        name: 'AI search visibility',
        tag: 'GEO / AI Overviews',
        desc:
          'ChatGPT, Perplexity, Gemini, AI Overviews. Entities, structured data and content that models like to cite — so your brand is in the answer, not just below it.',
        deliverables: ['Audit of your brand in AI answers', 'Entity and citation plan', 'schema.org implementation'],
        time: '2–4 weeks',
      },
      {
        name: 'E-commerce SEO',
        tag: 'E-commerce',
        desc:
          'Categories, filters, faceted navigation, product pages, crawl budget. Stores play a different game — thousands of URLs and every mistake multiplied by scale.',
        deliverables: ['Category and filter architecture', 'Product content templates', 'Indexation control'],
        time: '3–6 weeks',
      },
      {
        name: 'Migrations & relaunches',
        tag: 'Migration',
        desc:
          'New CMS, new domain, new design. A migration is the easiest way to lose half your traffic in a week. I make sure that doesn’t happen.',
        deliverables: ['URL redirect map', 'Pre- and post-launch checklist', '8 weeks of post-launch monitoring'],
        time: 'Whole project',
      },
      {
        name: 'Ongoing partnership',
        tag: 'Retainer',
        desc:
          'Monthly support: I set priorities, back up your team, review changes and report in numbers the board cares about — leads, revenue, market share.',
        deliverables: ['Monthly plan and report', 'Pre-release change review', 'Direct line, no account managers'],
        time: '3 months +',
      },
    ],
  },
  manifesto: {
    label: 'Approach',
    parts: [
      { t: 'I don’t sell ' },
      { t: '80-page audits', strike: true },
      { t: ' that end up in a drawer. You get a list of what to do, ranked by ' },
      { t: 'how much money it will make', mark: true },
      { t: ' — and I make sure it gets done.' },
    ],
  },
  process: {
    label: 'Process',
    title: 'How I work',
    intro: 'No magic, no black boxes. At every stage you know what I’m doing, why, and what it leads to.',
    steps: [
      {
        name: 'Diagnosis',
        when: 'Week 1–2',
        desc: 'We talk business goals, I get access to your data, crawl the site and map the competition. I find out where you really stand.',
        out: 'A clear picture and a list of quick wins',
      },
      {
        name: 'Strategy',
        when: 'Week 2–4',
        desc: 'I prioritise by impact and cost of implementation. We agree on KPIs that can be tied to revenue.',
        out: 'A 3–6 month roadmap',
      },
      {
        name: 'Execution',
        when: 'From month 1',
        desc: 'I write developer tickets and content briefs and review the work. Or I ship it myself — whichever makes more sense.',
        out: 'Changes in production, not in a slide deck',
      },
      {
        name: 'Measurement',
        when: 'Monthly',
        desc: 'I check what worked, what didn’t and why, then move priorities to wherever the data shows the best return.',
        out: 'A report in business numbers',
      },
    ],
  },
  about: {
    label: 'About',
    title: 'One consultant. Zero middlemen.',
    paragraphs: [
      'I’m Maciej Zięciak and I do SEO. I work with companies for whom search traffic means real money — online stores, service businesses and SaaS products.',
      'At an agency, your project often goes to a junior once the contract is signed. With me, you talk to the person who actually runs the audit, writes the strategy and owns the result.',
    ],
    facts: [
      { k: 'Working with', v: 'Me, directly' },
      { k: 'Languages', v: 'English / Polish' },
      { k: 'Location', v: 'Remote, Poland & worldwide' },
      { k: 'Reporting', v: 'Leads and revenue, not just rankings' },
    ],
  },
  faq: {
    label: 'FAQ',
    title: 'Questions I hear most often',
    items: [
      {
        q: 'When will I see results?',
        a: 'Technical fixes can show impact within a few weeks. Sustained organic growth usually takes 3–6 months, depending on competition and the state of the site at the start.',
      },
      {
        q: 'How much does it cost?',
        a: 'Audits are a one-off fee, ongoing work is billed monthly. The price depends on the size of the site and the scope. After a short call you get a concrete quote — no “starting from” pricing.',
      },
      {
        q: 'Do you guarantee the #1 spot?',
        a: 'No. Anyone guaranteeing Google rankings is either stretching the truth or ranking you for phrases nobody searches. What I guarantee is transparency: you know what I do, why, and what it achieves.',
      },
      {
        q: 'Do you advise or also implement?',
        a: 'Both. I can work alongside your dev team — writing tickets and reviewing changes — or implement parts of it myself.',
      },
      {
        q: 'Do you work with companies outside Poland?',
        a: 'Yes. I run projects in English and Polish, including for companies entering new markets that need international SEO done right (hreflang, language versions, site structure).',
      },
    ],
  },
  contact: {
    label: 'Contact',
    title: 'Let’s talk.',
    lead: 'Write a few sentences about your company and what you want to achieve. The first call is free and comes with no strings attached.',
    topicsLabel: 'What do you need?',
    topics: ['Audit', 'Content strategy', 'AI search', 'E-commerce', 'Migration', 'Ongoing work'],
    urlLabel: 'Your website',
    urlPlaceholder: 'https://yourcompany.com',
    msgLabel: 'Message',
    msgPlaceholder: 'What do you do and what do you want to achieve?',
    submit: 'Send message',
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
