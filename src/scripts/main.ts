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
const hs = document.querySelector<HTMLElement>('[data-hscroll]');
const track = hs?.querySelector<HTMLElement>('[data-track]');
const hbar = hs?.querySelector<HTMLElement>('[data-hbar]');
const exp = document.querySelector<HTMLElement>('[data-exp]');
const jobs = exp ? [...exp.querySelectorAll<HTMLElement>('[data-job]')] : [];
const slides = exp ? [...exp.querySelectorAll<HTMLElement>('[data-slide]')] : [];
const dots = exp ? [...exp.querySelectorAll<HTMLElement>('[data-dot]')] : [];
const steps = document.querySelector<HTMLElement>('[data-steps]');
const stepPanels = steps ? [...steps.querySelectorAll<HTMLElement>('[data-step]')] : [];
const stepNums = steps ? [...steps.querySelectorAll<HTMLElement>('[data-snum]')] : [];
const sbar = steps?.querySelector<HTMLElement>('[data-sbar]');
const wide = window.matchMedia('(min-width: 900px)');

// Horizontal gallery: the section is as tall as the sideways distance the track must travel
let hsTravel = 0;
const sizeGallery = () => {
  if (!hs || !track) return;
  if (!wide.matches || reduce) {
    hs.style.height = '';
    track.style.removeProperty('--x');
    hsTravel = 0;
    return;
  }
  hsTravel = Math.max(0, track.scrollWidth - window.innerWidth);
  hs.style.height = `${window.innerHeight + hsTravel}px`;
};
sizeGallery();

// Switch the active item in a "one at a time" scene
const setActive = (items: HTMLElement[], idx: number) =>
  items.forEach((el, i) => {
    el.classList.toggle('on', i === idx);
    el.classList.toggle('out', i < idx);
  });

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
  if (hs && track && hsTravel > 0) {
    const p = pinProgress(hs, vh);
    track.style.setProperty('--x', `${(-p * hsTravel).toFixed(1)}px`);
    hbar?.style.setProperty('--hp', (0.15 + p * 0.85).toFixed(4));
  }
  if (exp && jobs.length) {
    // the job crossing the middle of the screen drives the big sticky years
    let idx = 0;
    jobs.forEach((j, i) => { if (j.getBoundingClientRect().top < vh * 0.5) idx = i; });
    jobs.forEach((j, i) => j.classList.toggle('is-active', i === idx));
    setActive(slides, idx);
    dots.forEach((d, i) => d.classList.toggle('on', i === idx));
  }
  if (steps && stepPanels.length) {
    const p = pinProgress(steps, vh);
    const idx = Math.min(stepPanels.length - 1, Math.floor(p * stepPanels.length * 0.999));
    setActive(stepPanels, idx);
    setActive(stepNums, idx);
    sbar?.style.setProperty('--sp', (0.08 + p * 0.92).toFixed(4));
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
  sizeGallery();
  requestTick();
});
if (reduce) {
  scrub?.style.setProperty('--p', '1.3');
  pin?.style.setProperty('--p', '1');
  rows.forEach((r) => r.classList.add('is-done'));
  sum?.classList.add('is-done');
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

/* ---------- Service cards: play their illustration once visible ---------- */
const cardIO = new IntersectionObserver(
  (entries) =>
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add('is-on');
        cardIO.unobserve(e.target);
      }
    }),
  { threshold: 0.55 },
);
document.querySelectorAll('[data-card]').forEach((el) => (reduce ? el.classList.add('is-on') : cardIO.observe(el)));

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

/* ---------- FAQ: smooth open/close (one open at a time) ---------- */
const accs = [...document.querySelectorAll<HTMLDetailsElement>('[data-acc]')];
const animateAcc = (d: HTMLDetailsElement, open: boolean) => {
  const summary = d.querySelector('summary')!;
  const from = d.offsetHeight;
  if (open) d.open = true;
  const to = open ? d.scrollHeight : summary.offsetHeight;
  if (!open) d.classList.add('is-closing');
  const anim = d.animate({ height: [`${from}px`, `${to}px`] }, { duration: reduce ? 0 : 420, easing: 'cubic-bezier(0.16, 1, 0.3, 1)' });
  d.style.overflow = 'hidden';
  anim.onfinish = () => {
    if (!open) d.open = false;
    d.classList.remove('is-closing');
    d.style.overflow = '';
  };
};
accs.forEach((d) => {
  d.removeAttribute('name'); // we handle exclusivity ourselves, with animation
  d.querySelector('summary')?.addEventListener('click', (e) => {
    e.preventDefault();
    const opening = !d.open;
    if (opening) accs.filter((o) => o !== d && o.open).forEach((o) => animateAcc(o, false));
    animateAcc(d, opening);
  });
});

/* ---------- Magnetic primary buttons ---------- */
if (finePointer && !reduce) {
  document.querySelectorAll<HTMLElement>('[data-magnet]').forEach((el) => {
    el.style.transition = 'transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), background-color 0.2s';
    el.addEventListener('pointermove', (e) => {
      const r = el.getBoundingClientRect();
      const x = (e.clientX - (r.left + r.width / 2)) * 0.25;
      const y = (e.clientY - (r.top + r.height / 2)) * 0.35;
      el.style.transform = `translate(${x.toFixed(1)}px, ${y.toFixed(1)}px)`;
    });
    el.addEventListener('pointerleave', () => (el.style.transform = ''));
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
