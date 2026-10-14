const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const clamp = (v: number, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

/* ---------- Nav: mobile sheet ---------- */
const nav = document.querySelector<HTMLElement>('[data-nav]');
const burger = document.querySelector<HTMLButtonElement>('[data-burger]');
const sheet = document.querySelector<HTMLElement>('[data-sheet]');
const burgerLabel = document.querySelector<HTMLElement>('[data-burger-label]');

const setSheet = (open: boolean) => {
  if (!burger || !sheet) return;
  burger.setAttribute('aria-expanded', String(open));
  sheet.hidden = !open;
  document.body.style.overflow = open ? 'hidden' : '';
  if (burgerLabel) burgerLabel.textContent = (open ? burgerLabel.dataset.close : burgerLabel.dataset.open) ?? '';
};
burger?.addEventListener('click', () => setSheet(burger.getAttribute('aria-expanded') !== 'true'));
sheet?.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => setSheet(false)));
document.addEventListener('keydown', (e) => e.key === 'Escape' && setSheet(false));

/* ---------- Scroll-linked effects (one rAF loop) ---------- */
const darks = [...document.querySelectorAll<HTMLElement>('[data-dark]')];
const scrub = document.querySelector<HTMLElement>('[data-scrub]');
const stage = document.querySelector<HTMLElement>('[data-stage]');

let ticking = false;
const onScroll = () => {
  ticking = false;
  const vh = window.innerHeight;
  nav?.classList.toggle('is-scrolled', window.scrollY > 8);
  // Nav turns dark while it sits over a black section.
  const overDark = darks.some((el) => {
    const r = el.getBoundingClientRect();
    return r.top <= 26 && r.bottom >= 26;
  });
  nav?.classList.toggle('is-dark', overDark);

  if (reduce) return;
  if (scrub) {
    const r = scrub.getBoundingClientRect();
    const p = clamp(-r.top / (r.height - vh));
    scrub.style.setProperty('--p', (p * 1.3).toFixed(4));
  }
  if (stage) {
    const r = stage.getBoundingClientRect();
    stage.style.setProperty('--k', clamp((vh - r.top) / (vh * 0.75)).toFixed(3));
  }
};
const requestTick = () => {
  if (!ticking) {
    ticking = true;
    requestAnimationFrame(onScroll);
  }
};
window.addEventListener('scroll', requestTick, { passive: true });
window.addEventListener('resize', requestTick);
if (reduce) {
  scrub?.style.setProperty('--p', '1.2');
  stage?.style.setProperty('--k', '1');
}
onScroll();

/* ---------- Reveal on scroll ---------- */
const io = new IntersectionObserver(
  (entries) =>
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add('is-in');
        io.unobserve(e.target);
      }
    }),
  { rootMargin: '0px 0px -8% 0px', threshold: 0.08 },
);
document.querySelectorAll('[data-reveal]').forEach((el) => io.observe(el));

/* ---------- Once-when-visible helper ---------- */
const whenVisible = (el: Element, fn: () => void, threshold = 0.35) => {
  const o = new IntersectionObserver(
    (entries) => {
      if (entries.some((e) => e.isIntersecting)) {
        o.disconnect();
        fn();
      }
    },
    { threshold },
  );
  o.observe(el);
};

/* ---------- Bot access card: rows resolve one by one ---------- */
const card = document.querySelector<HTMLElement>('[data-bots]');
if (card) {
  const rows = [...card.querySelectorAll<HTMLElement>('.row')];
  const sum = card.querySelector<HTMLElement>('[data-sum]');
  const finish = () => {
    rows.forEach((r) => r.classList.add('is-done'));
    sum?.classList.add('is-done');
  };
  if (reduce) finish();
  else
    whenVisible(card, async () => {
      await sleep(300);
      for (const r of rows) {
        r.classList.add('is-done');
        await sleep(r.dataset.s === 'ok' ? 300 : 500);
      }
      await sleep(200);
      sum?.classList.add('is-done');
    });
}

/* ---------- Count-up numbers ("1,1 mln", "670 tys.", "9 years") ---------- */
document.querySelectorAll<HTMLElement>('[data-count]').forEach((el) => {
  const m = (el.textContent ?? '').match(/^([\d.,]+)(.*)$/s);
  if (!m || reduce) return;
  const raw = m[1];
  const sep = raw.includes(',') ? ',' : '.';
  const target = parseFloat(raw.replace(',', '.'));
  const decimals = (raw.split(/[.,]/)[1] ?? '').length;
  const suffix = m[2];
  const fmt = (v: number) => v.toFixed(decimals).replace('.', sep) + suffix;
  el.textContent = fmt(0);
  whenVisible(el, () => {
    const t0 = performance.now();
    const dur = 1400;
    const step = (now: number) => {
      const k = clamp((now - t0) / dur);
      el.textContent = fmt(target * (1 - Math.pow(1 - k, 3)));
      if (k < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }, 0.6);
});

/* ---------- Contact form → prefilled email ---------- */
const form = document.querySelector<HTMLFormElement>('[data-form]');
form?.addEventListener('submit', (e) => {
  e.preventDefault();
  const fd = new FormData(form);
  const d = form.dataset;
  const topics = fd.getAll('topic').join(', ');
  const url = String(fd.get('url') ?? '').trim();
  const msg = String(fd.get('body') ?? '').trim();
  const head = [topics && `${d.lTopics}: ${topics}`, url && `${d.lUrl}: ${url}`].filter(Boolean).join('\n');
  const body = head ? `${head}\n\n${msg}` : msg;
  window.location.href = `mailto:${d.email}?subject=${encodeURIComponent(d.subject ?? '')}&body=${encodeURIComponent(body)}`;
});
