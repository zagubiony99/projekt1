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
// the hero's scroll value is set only on the parts that use it (--h is non-inherited)
const heroParts = hero ? [...hero.querySelectorAll<HTMLElement>('.glow, [data-hero-inner], [data-demo]')] : [];
const scrub = document.querySelector<HTMLElement>('[data-scrub]');
const pin = document.querySelector<HTMLElement>('[data-pin]');
const rows = pin ? [...pin.querySelectorAll<HTMLElement>('.row')] : [];
const sum = pin?.querySelector<HTMLElement>('[data-sum]');
const pinParts = pin ? [...pin.querySelectorAll<HTMLElement>('.head, [data-stage]')] : [];
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

// progress of a tall pinned section from a rect read earlier in the frame:
// 0 when its top hits the viewport top, 1 when its bottom does
const progress = (r: DOMRect | undefined, vh: number) => (r ? clamp(-r.top / Math.max(1, r.height - vh)) : 0);

// Write a CSS variable only when its value changes: unchanged writes still invalidate styles
const vars = new WeakMap<HTMLElement, Record<string, string>>();
const setVar = (el: HTMLElement | null | undefined, name: string, value: string) => {
  if (!el) return;
  const cur = vars.get(el) ?? {};
  if (cur[name] === value) return;
  cur[name] = value;
  vars.set(el, cur);
  el.style.setProperty(name, value);
};

let ticking = false;
const onScroll = () => {
  ticking = false;
  // 1) read: every layout query happens before any write, so the frame lays out once
  const vh = window.innerHeight;
  const y = window.scrollY;
  const overDark = darks.some((el) => {
    const r = el.getBoundingClientRect();
    return r.top <= 26 && r.bottom >= 26;
  });
  const motion = !reduce;
  const scrubR = motion ? scrub?.getBoundingClientRect() : undefined;
  const pinR = motion ? pin?.getBoundingClientRect() : undefined;
  const hsR = motion && hsTravel > 0 ? hs?.getBoundingClientRect() : undefined;
  const jobTops = motion ? jobs.map((j) => j.getBoundingClientRect().top) : [];
  const stepsR = motion ? steps?.getBoundingClientRect() : undefined;

  // 2) write
  nav?.classList.toggle('is-scrolled', y > 8);
  nav?.classList.toggle('is-dark', overDark);
  if (!motion) return;
  const hv = clamp(y / (vh * 0.8)).toFixed(3);
  heroParts.forEach((el) => setVar(el, '--h', hv));
  if (scrub) setVar(scrub, '--p', (progress(scrubR, vh) * 1.3).toFixed(3));
  if (pin) {
    const p = progress(pinR, vh);
    pinParts.forEach((el) => setVar(el, '--q', p.toFixed(3)));
    // bots resolve one by one as the scene scrolls, then the verdict appears
    rows.forEach((row, i) => row.classList.toggle('is-done', p > 0.28 + i * 0.08));
    sum?.classList.toggle('is-done', p > 0.28 + rows.length * 0.08 + 0.04);
  }
  if (hsR && track) {
    const p = progress(hsR, vh);
    setVar(track, '--x', `${(-p * hsTravel).toFixed(1)}px`);
    setVar(hbar, '--hp', (0.15 + p * 0.85).toFixed(3));
  }
  if (jobTops.length) {
    // the job crossing the middle of the screen drives the big sticky years
    let idx = 0;
    jobTops.forEach((top, i) => { if (top < vh * 0.5) idx = i; });
    jobs.forEach((j, i) => j.classList.toggle('is-active', i === idx));
    setActive(slides, idx);
    dots.forEach((d, i) => d.classList.toggle('on', i === idx));
  }
  if (stepsR && stepPanels.length) {
    const p = progress(stepsR, vh);
    const idx = Math.min(stepPanels.length - 1, Math.floor(p * stepPanels.length * 0.999));
    setActive(stepPanels, idx);
    setActive(stepNums, idx);
    setVar(sbar, '--sp', (0.08 + p * 0.92).toFixed(3));
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
  pinParts.forEach((el) => el.style.setProperty('--q', '1'));
  rows.forEach((r) => r.classList.add('is-done'));
  sum?.classList.add('is-done');
}
onScroll();

/* ---------- Hero AI-answer demo: plays once when the window is well in view ---------- */
const demo = document.querySelector<HTMLElement>('[data-demo]');
if (demo && !reduce) {
  const dio = new IntersectionObserver(([e]) => {
    if (e.isIntersecting) { demo.classList.add('play'); dio.disconnect(); }
  }, { threshold: 0.45 });
  dio.observe(demo);
}

/* ---------- Compare: each row resolves (me lights up, agency is struck) as it passes 60% of the screen ---------- */
const vsRows = document.querySelectorAll<HTMLElement>('[data-vs]');
if (vsRows.length && !reduce) {
  const vio = new IntersectionObserver((entries) => entries.forEach((e) => {
    if (e.isIntersecting) { e.target.classList.add('hit'); vio.unobserve(e.target); }
  }), { rootMargin: '0px 0px -40% 0px', threshold: 0 });
  vsRows.forEach((r) => vio.observe(r));
}

/* ---------- Reveal on scroll ---------- */
const io = new IntersectionObserver(
  (entries) =>
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add('is-in');
        io.unobserve(e.target);
      }
    }),
  { rootMargin: '0px 0px -6% 0px', threshold: 0 },
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

/* ---------- Sticky mobile CTA: visible after the hero, hidden over the contact form ---------- */
const sticky = document.querySelector<HTMLElement>('[data-sticky]');
if (sticky) {
  const contactEl = document.querySelector('.contact');
  let pastHero = false;
  let atContact = false;
  const sync = () => sticky.classList.toggle('on', pastHero && !atContact);
  const heroEl = document.querySelector('[data-hero], .sv-hero');
  if (heroEl) new IntersectionObserver(([e]) => { pastHero = !e.isIntersecting; sync(); }).observe(heroEl);
  if (contactEl) new IntersectionObserver(([e]) => { atContact = e.isIntersecting; sync(); }, { threshold: 0.05 }).observe(contactEl);
}

/* ---------- Measurement: first-touch campaign source + click events for GTM ---------- */
const dl = (o: Record<string, unknown>) => ((window as any).dataLayer ??= []).push(o);
const SRC = 'mz-source';
try {
  const q = new URLSearchParams(location.search);
  const keys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'gclid', 'li_fat_id'];
  const hit = keys.filter((k) => q.get(k)).map((k) => `${k}=${q.get(k)}`);
  if (hit.length && !sessionStorage.getItem(SRC)) sessionStorage.setItem(SRC, [...hit, `landing=${location.pathname}`].join('; '));
} catch {}
const source = () => { try { return sessionStorage.getItem(SRC) ?? ''; } catch { return ''; } };
document.addEventListener('click', (e) => {
  const a = (e.target as Element).closest?.('a');
  if (!a) return;
  if (a.dataset.event) dl({ event: a.dataset.event, page_path: location.pathname });
  else if (a.href.startsWith('mailto:')) dl({ event: 'email_click', page_path: location.pathname });
});

/* ---------- Page transitions: the clicked service title flies into the next page's eyebrow ---------- */
// The name is given at click time to that one title only (names must be unique on the page),
// and taken off the current eyebrow so it does not compete with the clicked title.
document.addEventListener('click', (e) => {
  const a = (e.target as Element).closest?.('a[href^="/"]');
  const title = a?.closest('li')?.querySelector<HTMLElement>('[data-vt-title]');
  if (!title) return;
  document.querySelectorAll<HTMLElement>('[data-vt-title], [data-vt-target]').forEach((el) => (el.style.viewTransitionName = 'none'));
  title.style.viewTransitionName = 'svc-title';
});
// Coming back from the back/forward cache: clear names left over from the last click
window.addEventListener('pageshow', (e) => {
  if (e.persisted) document.querySelectorAll<HTMLElement>('[data-vt-title], [data-vt-target]').forEach((el) => (el.style.viewTransitionName = ''));
});

/* ---------- Contact form: POST to a form backend if configured, else open the mail app ---------- */
const form = document.querySelector<HTMLFormElement>('[data-form]');
form?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const fd = new FormData(form);
  const d = form.dataset;
  if (fd.get('botcheck')) return; // honeypot
  const topics = fd.getAll('topic').join(', ');
  const url = String(fd.get('url') ?? '').trim();
  const msg = String(fd.get('body') ?? '').trim();
  const head = [topics && `${d.lTopics}: ${topics}`, url && `${d.lUrl}: ${url}`].filter(Boolean).join('\n');
  const body = head ? `${head}\n\n${msg}` : msg;

  if (!d.endpoint) {
    dl({ event: 'email_click', form: 'contact', page_path: location.pathname });
    window.location.href = `mailto:${d.email}?subject=${encodeURIComponent(d.subject ?? '')}&body=${encodeURIComponent(body)}`;
    return;
  }
  const btn = form.querySelector<HTMLButtonElement>('button[type="submit"]');
  const ok = form.querySelector<HTMLElement>('[data-ok]');
  const err = form.querySelector<HTMLElement>('[data-err]');
  const label = btn?.textContent ?? '';
  if (btn) { btn.disabled = true; btn.textContent = d.sending ?? '…'; }
  ok && (ok.hidden = true); err && (err.hidden = true);
  try {
    const payload = new FormData();
    fd.forEach((v, k) => k !== 'botcheck' && payload.append(k, v));
    payload.set('topic', topics);
    payload.set('message', body);
    if (source()) payload.set('source', source());
    const res = await fetch(d.endpoint, { method: 'POST', body: payload, headers: { Accept: 'application/json' } });
    if (!res.ok) throw new Error(String(res.status));
    form.reset();
    ok && (ok.hidden = false);
    dl({ event: 'generate_lead', form: 'contact', lead_topic: topics || '(none)', language: document.documentElement.lang, page_path: location.pathname });
  } catch {
    err && (err.hidden = false);
  } finally {
    if (btn) { btn.disabled = false; btn.textContent = label; }
  }
});
