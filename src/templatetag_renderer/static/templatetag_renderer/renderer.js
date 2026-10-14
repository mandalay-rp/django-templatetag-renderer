/**
 * renderer.js — ленивая подгрузка templatetags в HTML-слоты.
 * Находит [data-tag-url], фетчит HTML и вставляет его внутрь.
 */
(function () {
  "use strict";

  const ATTR = "data-tag-url";
  const LOADED = "data-tag-loaded";
  const ERROR_CLASS = "renderer-slot--error";
  const LOADING_CLASS = "renderer-slot--loading";

  const defaults = {
    fetcher: (url, init) => fetch(url, init),
    onRender: null,
    onError: null,
  };

  let options = { ...defaults };

  function setOptions(next) {
    options = { ...options, ...next };
  }

  async function loadSlot(el) {
    const url = el.getAttribute(ATTR);
    if (!url) return;
    if (el.hasAttribute(LOADED)) return;
    el.setAttribute(LOADED, "pending");
    el.classList.add(LOADING_CLASS);

    try {
      const res = await options.fetcher(url, {
        method: "GET",
        credentials: "same-origin",
        headers: { "X-Requested-With": "XMLHttpRequest" },
      });
      if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText}`);

      const html = await res.text();
      el.innerHTML = html;
      el.classList.remove(LOADING_CLASS);
      el.setAttribute(LOADED, "ok");

      if (typeof options.onRender === "function") options.onRender(el, html);
    } catch (err) {
      el.classList.remove(LOADING_CLASS);
      el.classList.add(ERROR_CLASS);
      el.setAttribute(LOADED, "error");
      el.innerHTML = '<span class="renderer-slot__error">Ошибка загрузки</span>';
      if (typeof options.onError === "function") options.onError(el, err);
      else console.error("[renderer] failed:", url, err);
    }
  }

  function renderSlots(root = document) {
    const nodes = root.querySelectorAll(`[${ATTR}]:not([${LOADED}])`);
    return Promise.all(Array.from(nodes, loadSlot));
  }

  function observe(root = document.body) {
    if (!root) return null;
    const mo = new MutationObserver((mutations) => {
      for (const m of mutations) {
        for (const node of m.addedNodes) {
          if (!(node instanceof Element)) continue;
          if (node.matches?.(`[${ATTR}]`)) loadSlot(node);
          node.querySelectorAll?.(`[${ATTR}]:not([${LOADED}])`)?.forEach(loadSlot);
        }
      }
    });
    mo.observe(root, { childList: true, subtree: true });
    return mo;
  }

  function init(opts = {}) {
    setOptions(opts);
    const boot = () => {
      renderSlots();
      observe();
    };
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", boot);
    } else {
      boot();
    }
  }

  window.TemplatetagRenderer = { init, renderSlots, setOptions };
  init();
})();
