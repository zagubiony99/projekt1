const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
const clamp = (v: number, a = 0, b = 1) => Math.min(b, Math.max(a, v));

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

/* ---------- Scroll-linked scenes (one rAF loop) ---------- */
const darks = [...document.querySelectorAll<HTMLElement>('[data-dark]')];
const hero = document.querySelector<HTMLElement>('[data-hero]');
const scrub = document.querySelector<HTMLElement>('[data-scrub]');
const pin = document.querySelector<HTMLElement>('[data-pin]');
const rows = pin ? [...pin.querySelectorAll<HTMLElement>('.row')] : [];
const sum = pin?.querySelector<HTMLElement>('[data-sum]');
const rail = document.querySelector<HTMLElement>('[data-rail]');
const jobs = rail ? [...rail.querySelectorAll<HTMLElement>('.job')] : [];

// progress of a tall pinned section: 0 when its top hits the viewport top, 1 when its bottom does
const pinProgress = (el: HTMLElement, vh: number) => {
  const r = el.getBoundingClientRect();
  return clamp(-r.top / Math.max(1, r.height - vh));
};

let ticking = false;
const onScroll = () => {
  ticking = false;
  const vh = window.innerHeight;
  nav?.classList.toggle('is-scrolled', window.scrollY > 8);
  const overDark = darks.some((el) => {
    const r = el.getBoundingClientRect();
    return r.top <= 26 && r.bottom >= 26;
  });
  nav?.classList.toggle('is-dark', overDark);

  if (reduce) return;
  if (hero) hero.style.setProperty('--h', clamp(window.scrollY / (vh * 0.8)).toFixed(4));
  if (scrub) scrub.style.setProperty('--p', (pinProgress(scrub, vh) * 1.3).toFixed(4));
  if (pin) {
    const p = pinProgress(pin, vh);
    pin.style.setProperty('--p', p.toFixed(4));
    // bots resolve one by one as the scene scrolls, then the verdict appears
    rows.forEach((row, i) => row.classList.toggle('is-done', p > 0.28 + i * 0.08));
    sum?.classList.toggle('is-done', p > 0.28 + rows.length * 0.08 + 0.04);
  }
  if (rail) {
    const r = rail.getBoundingClientRect();
    const fill = clamp((vh * 0.6 - r.top) / r.height);
    rail.style.setProperty('--r', fill.toFixed(4));
    jobs.forEach((j) => j.classList.toggle('is-lit', j.getBoundingClientRect().top + 40 < vh * 0.6));
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
  scrub?.style.setProperty('--p', '1.3');
  pin?.style.setProperty('--p', '1');
  rows.forEach((r) => r.classList.add('is-done'));
  sum?.classList.add('is-done');
  rail?.style.setProperty('--r', '1');
  jobs.forEach((j) => j.classList.add('is-lit'));
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
  { rootMargin: '0px 0px -10% 0px', threshold: 0.1 },
);
document.querySelectorAll('[data-reveal]').forEach((el) => io.observe(el));

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
  whenVisible(
    el,
    () => {
      const t0 = performance.now();
      const dur = 1600;
      const step = (now: number) => {
        const k = clamp((now - t0) / dur);
        el.textContent = fmt(target * (1 - Math.pow(1 - k, 4)));
        if (k < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    },
    0.6,
  );
});

/* ---------- Tiles: cursor spotlight + gentle 3D tilt ---------- */
if (finePointer && !reduce) {
  document.querySelectorAll<HTMLElement>('[data-tilt]').forEach((el) => {
    el.addEventListener('pointermove', (e) => {
      const r = el.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width;
      const y = (e.clientY - r.top) / r.height;
      el.style.setProperty('--mx', `${(x * 100).toFixed(1)}%`);
      el.style.setProperty('--my', `${(y * 100).toFixed(1)}%`);
      el.style.setProperty('--ry', `${((x - 0.5) * 6).toFixed(2)}deg`);
      el.style.setProperty('--rx', `${((0.5 - y) * 6).toFixed(2)}deg`);
    });
    el.addEventListener('pointerleave', () => {
      el.style.setProperty('--rx', '0deg');
      el.style.setProperty('--ry', '0deg');
    });
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
  const head = [topics && `${d.lTopics}: ${topics}`, url && `${d.lUrl}: ${url}`].filter(Boolean).join('\n');
  const body = head ? `${head}\n\n${msg}` : msg;
  window.location.href = `mailto:${d.email}?subject=${encodeURIComponent(d.subject ?? '')}&body=${encodeURIComponent(body)}`;
});
