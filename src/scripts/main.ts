const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const clamp = (v: number, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

/* ---------- Nav: scrolled state, progress, mobile sheet ---------- */
const nav = document.querySelector<HTMLElement>('[data-nav]');
const progress = document.querySelector<HTMLElement>('[data-progress]');
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

/* ---------- Scroll-linked effects (single rAF loop) ---------- */
const scrub = document.querySelector<HTMLElement>('[data-scrub]');
const word = document.querySelector<HTMLElement>('[data-word]');

// Fit the footer wordmark to the container width.
const wordSpan = word?.querySelector('span');
const fitWord = () => {
  if (!word || !wordSpan) return;
  word.style.fontSize = '';
  const size = parseFloat(getComputedStyle(word).fontSize);
  const w = wordSpan.getBoundingClientRect().width;
  if (w > 0) word.style.fontSize = `${(size * word.clientWidth) / w}px`;
};
fitWord();
document.fonts?.ready.then(fitWord);

let ticking = false;
const onScroll = () => {
  ticking = false;
  const vh = window.innerHeight;
  const y = window.scrollY;
  const max = document.documentElement.scrollHeight - vh;

  nav?.classList.toggle('is-scrolled', y > 24);
  progress?.style.setProperty('--p', String(max > 0 ? y / max : 0));

  if (reduce) return;
  if (scrub) {
    const r = scrub.getBoundingClientRect();
    scrub.style.setProperty('--p', (clamp((vh * 0.85 - r.top) / (r.height * 0.85)) * 1.08).toFixed(4));
  }
};
const requestTick = () => {
  if (!ticking) {
    ticking = true;
    requestAnimationFrame(onScroll);
  }
};
window.addEventListener('scroll', requestTick, { passive: true });
window.addEventListener('resize', () => {
  fitWord();
  requestTick();
});
onScroll();

/* ---------- SERP simulation: type the query, then climb to #1 ---------- */
const serp = document.querySelector<HTMLElement>('[data-serp]');
if (serp) {
  const list = serp.querySelector<HTMLElement>('[data-list]')!;
  const me = serp.querySelector<HTMLElement>('[data-me]')!;
  const badge = serp.querySelector<HTMLElement>('[data-badge]')!;
  const q = serp.querySelector<HTMLElement>('[data-q]')!;
  const text = q.dataset.text ?? '';
  const n = list.children.length;
  const ease = 'cubic-bezier(0.2, 0.7, 0.1, 1)';
  let run = 0;

  const flipUp = () => {
    const prev = me.previousElementSibling as HTMLElement | null;
    if (!prev) return;
    const a = me.getBoundingClientRect().top;
    const b = prev.getBoundingClientRect().top;
    list.insertBefore(me, prev);
    const dy = me.getBoundingClientRect().top - a;
    const dp = prev.getBoundingClientRect().top - b;
    me.animate([{ transform: `translateY(${-dy}px)` }, { transform: 'none' }], { duration: 560, easing: ease });
    prev.animate([{ transform: `translateY(${-dp}px)` }, { transform: 'none' }], { duration: 560, easing: ease });
  };

  const play = async () => {
    const id = ++run;
    list.appendChild(me);
    me.classList.remove('is-top');
    badge.textContent = `#${n}`;
    q.textContent = '';
    await sleep(450);
    for (let i = 1; i <= text.length; i++) {
      if (id !== run) return;
      q.textContent = text.slice(0, i);
      await sleep(45 + Math.random() * 70);
    }
    await sleep(700);
    for (let pos = n; pos > 1; pos--) {
      if (id !== run) return;
      flipUp();
      badge.textContent = `#${pos - 1}`;
      await sleep(pos > 3 ? 420 : 680);
    }
    if (id !== run) return;
    me.classList.add('is-top');
    badge.textContent = `#1 ↑${n - 1}`;
  };

  if (!reduce) {
    const seen = new IntersectionObserver(
      (entries) => {
        if (entries.some((e) => e.isIntersecting)) {
          seen.disconnect();
          play();
        }
      },
      { threshold: 0.4 },
    );
    seen.observe(serp);
  }
  serp.querySelector('[data-replay]')?.addEventListener('click', () => {
    if (!reduce) play();
  });
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
  const body = [topics && `${d.lTopics}: ${topics}`, url && `${d.lUrl}: ${url}`, '', msg]
    .filter((l, i) => l !== '' || i === 2)
    .join('\n')
    .trim();
  window.location.href = `mailto:${d.email}?subject=${encodeURIComponent(d.subject ?? '')}&body=${encodeURIComponent(body)}`;
});
