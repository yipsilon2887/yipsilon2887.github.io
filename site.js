(() => {
  let pages = {};
  try { pages = JSON.parse(document.getElementById('language-pages')?.textContent || '{}'); } catch { /* Native links remain available. */ }
  const root = new URL('./', document.querySelector('script[src$="site.js"]').src);
  document.querySelectorAll('head [href]').forEach(link => { link.href = new URL(link.getAttribute('href'), location.href).href; });
  const keyFor = url => url.origin === root.origin && url.pathname.startsWith(root.pathname)
    ? url.pathname.slice(root.pathname.length) : '';
  let current = keyFor(new URL(location.href));
  let homeHash = location.hash;
  let portrait = document.querySelector('.profile-photo');
  const parsed = new Map();

  function activateFromHash() {
    const panels = [...document.querySelectorAll('[role="tabpanel"]')];
    if (!panels.length) return;
    const panel = document.getElementById(location.hash.slice(1))?.closest('[role="tabpanel"]') || panels[0];
    panels.forEach(item => { item.hidden = item !== panel; });
    document.querySelectorAll('[role="tab"]').forEach(tab => {
      const active = tab.getAttribute('aria-controls') === panel.id;
      tab.setAttribute('aria-selected', String(active));
      tab.tabIndex = active ? 0 : -1;
    });
  }

  function render(key) {
    if (key === current) { activateFromHash(); return true; }
    if (!pages[key]) return false;
    if (!parsed.has(key)) {
      const page = new DOMParser().parseFromString(pages[key], 'text/html');
      const base = new URL(key, root);
      page.querySelectorAll('[href], [src]').forEach(element => {
        for (const attr of ['href', 'src']) {
          if (element.hasAttribute(attr)) element.setAttribute(attr, new URL(element.getAttribute(attr), base).href);
        }
      });
      parsed.set(key, page);
    }
    const next = parsed.get(key);
    const main = next.querySelector('main').cloneNode(true);
    const nextPhoto = main.querySelector('.profile-photo');
    if (portrait && nextPhoto) {
      portrait.querySelector('img').alt = nextPhoto.querySelector('img').alt;
      portrait.querySelector('img').src = nextPhoto.querySelector('img').src;
      portrait.querySelector('a').href = nextPhoto.querySelector('a').href;
      nextPhoto.replaceWith(portrait);
    } else if (nextPhoto) portrait = nextPhoto;
    const back = main.querySelector('.cv-actions a');
    if (back) back.href = new URL(key.split('/')[0] + '/' + homeHash, root).href;
    document.querySelector('main').replaceWith(main);
    for (const tag of ['header', 'footer']) document.querySelector(tag).replaceWith(next.querySelector(tag).cloneNode(true));
    document.querySelector('.skip').textContent = next.querySelector('.skip').textContent;
    document.documentElement.lang = next.documentElement.lang;
    document.title = next.title;
    for (const selector of ['meta[name="description"]', 'meta[property="og:title"]', 'meta[property="og:description"]']) {
      document.querySelector(selector)?.setAttribute('content', next.querySelector(selector).content);
    }
    current = key;
    activateFromHash();
    return true;
  }

  function showPhoto(link) {
    const dialog = document.createElement('dialog');
    dialog.className = 'photo-dialog';
    const close = document.createElement('button');
    close.className = 'photo-close';
    close.textContent = '\u00d7';
    close.setAttribute('aria-label', {ja: '\u9589\u3058\u308b', 'zh-CN': '\u5173\u95ed', en: 'Close'}[document.documentElement.lang] || 'Close');
    const image = document.createElement('img');
    image.src = link.href;
    image.alt = link.querySelector('img').alt;
    dialog.setAttribute('aria-label', image.alt);
    dialog.append(close, image);
    document.body.append(dialog);
    close.addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
    dialog.addEventListener('close', () => {
      document.documentElement.classList.remove('photo-open');
      dialog.remove();
      link.focus({preventScroll: true});
    }, {once: true});
    document.documentElement.classList.add('photo-open');
    dialog.showModal();
  }

  document.addEventListener('click', event => {
    if (!(event.target instanceof Element) || event.defaultPrevented || event.button !== 0 ||
        event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const photoLink = event.target.closest('.profile-photo a');
    if (photoLink && typeof HTMLDialogElement !== 'undefined') {
      event.preventDefault(); showPhoto(photoLink); return;
    }
    if (event.target.closest('#print')) { event.preventDefault(); window.print(); return; }
    const link = event.target.closest('a');
    if (!link || link.target || link.hasAttribute('download')) return;
    const url = new URL(link.href);
    const key = keyFor(url);
    if (!pages[key]) return;
    event.preventDefault();
    const languageSwitch = link.matches('.langs a');
    if (!current.includes('/cv/')) homeHash = location.hash;
    if (languageSwitch && !key.includes('/cv/')) url.hash = location.hash;
    const differentPage = key !== current;
    if (url.href !== location.href) {
      if (link.matches('[role="tab"]')) history.replaceState(null, '', url.href);
      else history.pushState(null, '', url.href);
    }
    if (!render(key)) { location.assign(url.href); return; }
    if (differentPage && !languageSwitch) {
      window.scrollTo(0, 0);
      const heading = document.querySelector('main h1');
      heading.tabIndex = -1;
      heading.focus({preventScroll: true});
    } else if (languageSwitch) document.querySelector('.langs [aria-current="page"]')?.focus({preventScroll: true});
  });

  document.addEventListener('keydown', event => {
    if (!(event.target instanceof Element)) return;
    const tab = event.target.closest('[role="tab"]');
    if (!tab) return;
    const tabs = [...document.querySelectorAll('[role="tab"]')];
    const index = tabs.indexOf(tab);
    let next;
    if (['ArrowDown', 'ArrowRight'].includes(event.key)) next = (index + 1) % tabs.length;
    if (['ArrowUp', 'ArrowLeft'].includes(event.key)) next = (index + tabs.length - 1) % tabs.length;
    if (event.key === 'Home') next = 0;
    if (event.key === 'End') next = tabs.length - 1;
    if (next !== undefined) { event.preventDefault(); tabs[next].focus(); tabs[next].click(); }
  });
  window.addEventListener('popstate', () => { render(keyFor(new URL(location.href))); });
  window.addEventListener('hashchange', activateFromHash);
  activateFromHash();
})();
