const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

/* ---------- Nav: scrolled state + mobile sheet ---------- */
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

const onScroll = () => nav?.classList.toggle('is-scrolled', window.scrollY > 16);
window.addEventListener('scroll', onScroll, { passive: true });
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
    (async () => {
      await sleep(900);
      for (const r of rows) {
        r.classList.add('is-done');
        await sleep(r.dataset.s === 'ok' ? 320 : 520);
      }
      await sleep(200);
      sum?.classList.add('is-done');
    })();
}

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
