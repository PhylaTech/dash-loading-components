// Header search: ⌘K / Ctrl+K (or "/") focuses it; typing filters the index
// the page embeds; arrows move, Enter opens, Escape closes. Results are
// plain anchors, navigated through history so Dash re-renders without a
// reload.
(function () {
  const isMac = 'mac' in document.documentElement.dataset;  // set in <head>
  let entries = [];
  let active = -1;

  const results = () => document.getElementById('site-search-results');
  const input = () => document.getElementById('site-search');

  const go = (href) => {
    close();
    // The box is a React-controlled input: set it the way a keystroke would.
    Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set.call(input(), '');
    input().dispatchEvent(new Event('input', {bubbles: true}));
    input().blur();
    history.pushState({}, '', href);
    window.dispatchEvent(new PopStateEvent('popstate'));
  };

  const close = () => {
    const list = results();
    if (!list) return;
    list.hidden = true;
    list.replaceChildren();
    input().setAttribute('aria-expanded', 'false');
    active = -1;
  };

  const render = (query) => {
    const list = results();
    if (!list) return;
    const q = query.trim().toLowerCase();
    if (!q) return close();
    const hits = entries.filter((e) => (e.title + ' ' + e.group).toLowerCase().includes(q)).slice(0, 40);
    list.replaceChildren(...hits.map((e, i) => {
      const a = document.createElement('a');
      a.href = e.href;
      a.className = 'dlc-search-option';
      a.setAttribute('role', 'option');
      a.dataset.index = i;
      a.innerHTML = `<span class="dlc-search-title"></span><span class="dlc-search-group"></span>`;
      a.firstChild.textContent = e.title;
      a.lastChild.textContent = e.group;
      a.addEventListener('mousedown', (ev) => { ev.preventDefault(); go(e.href); });
      return a;
    }));
    if (!hits.length) {
      const empty = document.createElement('div');
      empty.className = 'dlc-search-empty';
      empty.textContent = 'No components match';
      list.append(empty);
    }
    list.hidden = false;
    input().setAttribute('aria-expanded', 'true');
    highlight(hits.length ? 0 : -1);
  };

  const highlight = (i) => {
    const options = results().querySelectorAll('.dlc-search-option');
    active = options.length ? (i + options.length) % options.length : -1;
    options.forEach((o, k) => o.toggleAttribute('data-active', k === active));
    if (active >= 0) options[active].scrollIntoView({block: 'nearest'});
  };

  document.addEventListener('input', (event) => {
    if (event.target.id !== 'site-search') return;
    if (!entries.length) {
      const index = document.getElementById('site-search-index');
      entries = index ? JSON.parse(index.dataset.index) : [];
    }
    render(event.target.value);
  });
  // dcc.Input takes no ARIA props, so the combobox role is added here.
  new MutationObserver((_records, observer) => {
    const search = input();
    if (!search) return;
    search.setAttribute('role', 'combobox');
    search.setAttribute('aria-label', 'Search components');
    search.setAttribute('aria-expanded', 'false');
    search.setAttribute('aria-controls', 'site-search-results');
    search.setAttribute('aria-autocomplete', 'list');
    observer.disconnect();
  }).observe(document.documentElement, {childList: true, subtree: true});
  document.addEventListener('focusout', (event) => {
    if (event.target.id === 'site-search') setTimeout(close, 0);
  });
  document.addEventListener('keydown', (event) => {
    if (event.target.id !== 'site-search') return;
    const options = results().querySelectorAll('.dlc-search-option');
    if (event.key === 'ArrowDown' && options.length) { event.preventDefault(); highlight(active + 1); }
    if (event.key === 'ArrowUp' && options.length) { event.preventDefault(); highlight(active - 1); }
    if (event.key === 'Enter' && active >= 0) { event.preventDefault(); go(options[active].getAttribute('href')); }
    if (event.key === 'Escape') { close(); event.target.blur(); }
  });

  document.addEventListener('keydown', (event) => {
    const search = input();
    if (!search) return;
    const typing = /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)
      || document.activeElement.isContentEditable;
    const chord = event.key.toLowerCase() === 'k' && (isMac ? event.metaKey : event.ctrlKey);
    if (chord || (event.key === '/' && !typing)) {
      event.preventDefault();
      search.focus();
      search.select();
    }
  });

  // Dash renders the page after the browser has already tried to jump to the
  // URL's #fragment, so /#family-premium (the breadcrumbs) landed at the top.
  // Jump once the target exists, once per URL.
  let lastHashUrl = null;
  new MutationObserver(() => {
    if (!location.hash || location.href === lastHashUrl) return;
    const target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (!target) return;
    lastHashUrl = location.href;
    target.scrollIntoView({block: 'start'});
  }).observe(document.documentElement, {childList: true, subtree: true});

  // Keep the current component's nav link in view. Arriving on /c/epic/...
  // from a search or a shared link otherwise leaves it 100 rows below the fold.
  let lastPath = null;
  new MutationObserver(() => {
    if (location.pathname === lastPath) return;
    const active = document.querySelector('#dlc-navbar a[data-active]');
    if (!active || !active.getAttribute('href').endsWith(location.pathname)) return;
    lastPath = location.pathname;
    active.scrollIntoView({block: 'nearest'});
  }).observe(document.documentElement, {subtree: true, attributes: true, attributeFilter: ['data-active']});

  // Color control: text field, native picker and swatch stay in step.
  window.dash_clientside = Object.assign({}, window.dash_clientside, {
    dlc: {
      syncColor(picked, typed) {
        const noUpdate = window.dash_clientside.no_update;
        const trigger = window.dash_clientside.callback_context.triggered[0] || {};
        const fromPicker = trigger.prop_id.includes('color-swatch');
        const value = fromPicker ? picked : (typed || '').trim();
        const hex = /^#[0-9a-fA-F]{6}$/.test(value) ? value : noUpdate;
        return [fromPicker ? picked : noUpdate, hex, {'--chip': value || 'transparent'}];
      },
    },
  });

  // Brand mark: a random loader every few seconds, sliding in from below.
  // Hero carousel: featured loaders in order, auto-advancing, paused while
  // hovered. Both work on stacked elements already in the page.
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const swap = (items, from, to, axis) => {
    if (from === to) return;
    const leaving = items[from], entering = items[to];
    entering.hidden = false;
    if (!reduced && leaving) {
      leaving.classList.add('is-leaving');
      entering.classList.add('is-entering');
      setTimeout(() => {
        leaving.hidden = true;
        leaving.classList.remove('is-leaving');
        entering.classList.remove('is-entering');
      }, 440);
    } else if (leaving) {
      leaving.hidden = true;
    }
  };

  const cycleMark = () => {
    const marks = document.querySelectorAll('.dlc-brand-mark .dlc-mark');
    if (!marks.length) return;
    let current = [...marks].findIndex((m) => !m.hidden);
    if (current < 0) { current = Math.floor(Math.random() * marks.length); marks[current].hidden = false; }
    setInterval(() => {
      let next = Math.floor(Math.random() * (marks.length - 1));
      if (next >= current) next += 1;
      swap(marks, current, next);
      current = next;
    }, 4000);
  };

  const carousel = () => {
    const root = document.querySelector('.dlc-hero-carousel');
    if (!root || root.dataset.ready) return;
    root.dataset.ready = '1';
    const slides = root.querySelectorAll('.dlc-slide');
    const dots = root.querySelector('.dlc-carousel-dots');
    dots.replaceChildren(...[...slides].map(() => document.createElement('i')));
    let current = 0, timer;
    const show = (i) => {
      const next = (i + slides.length) % slides.length;
      swap(slides, current, next);
      current = next;
      dots.querySelectorAll('i').forEach((d, k) => d.classList.toggle('is-active', k === current));
    };
    // Under reduced motion the arrows still work; the page just stops moving on its own.
    const start = () => { clearInterval(timer); if (!reduced) timer = setInterval(() => show(current + 1), 5000); };
    slides[0].hidden = false;
    show(0);
    start();
    root.querySelectorAll('.dlc-carousel-btn').forEach((b) => b.addEventListener('click', () => { show(current + +b.dataset.step); start(); }));
    root.addEventListener('mouseenter', () => clearInterval(timer));
    root.addEventListener('mouseleave', start);
  };

  let markStarted = false;
  new MutationObserver(() => {
    if (!markStarted && document.querySelector('.dlc-brand-mark .dlc-mark')) { markStarted = true; cycleMark(); }
    carousel();
  }).observe(document.documentElement, {childList: true, subtree: true});
})();
