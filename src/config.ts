// Single source of truth for personal/contact data — edit here, it propagates everywhere.
export const site = {
  name: 'Maciej Zięciak',
  domain: 'maciejzieciak.com',
  url: 'https://maciejzieciak.com',
  email: 'kontakt@maciejzieciak.com',
  // Leave empty to hide. Used in footer + JSON-LD sameAs.
  linkedin: '',
  // Path in /public, e.g. '/maciej.jpg'. Empty = typographic placeholder.
  photo: '',
  city: 'Polska',
  // Form backend (recommended): e.g. Formspree 'https://formspree.io/f/xxxx' or Web3Forms
  // 'https://api.web3forms.com/submit' (+ formAccessKey). Empty = fallback to opening the mail app.
  formEndpoint: '',
  formAccessKey: '',
  // Booking calendar (Cal.com / Calendly). When set, a "pick a time" link appears next to the form.
  bookingUrl: '',
};
