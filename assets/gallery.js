// ⌘K / Ctrl+K (or "/") jumps to the header search, as on the Mantine docs.
(function () {
  const isMac = 'mac' in document.documentElement.dataset;  // set in <head>

  document.addEventListener('keydown', (event) => {
    const search = document.getElementById('site-search');
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
})();
