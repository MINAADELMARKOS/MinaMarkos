/* Measurement hooks only. No collector, storage, identifiers, or network requests.
 * An approved analytics integration may listen for portfolio:engagement after consent.
 */
(() => {
  'use strict';
  const emit = (name, detail = {}) => {
    if (window.PORTFOLIO_MEASUREMENT_CONSENT !== true) return;
    document.dispatchEvent(new CustomEvent('portfolio:engagement', {
      detail: { event: name, page_path: location.pathname, ...detail }
    }));
  };
  emit('page_view');
  document.addEventListener('click', event => {
    const link = event.target.closest('a');
    if (!link) return;
    let type = link.dataset.engagement;
    if (!type && link.closest('.portfolio_box')) type = 'project';
    if (!type && link.closest('.article-card')) type = 'article';
    if (!type && link.href.startsWith('https://github.com/') && location.pathname.includes('/insights/')) type = 'code';
    if (!type && link.getAttribute('href')?.startsWith('mailto:')) type = 'contact';
    if (type) emit('professional_interaction', { interaction_type: type });
  });
  const reached = new Set();
  let scheduled = false;
  const progress = () => {
    scheduled = false;
    if (!location.pathname.includes('/insights/') || window.PORTFOLIO_MEASUREMENT_CONSENT !== true) return;
    const article = document.querySelector('main article');
    if (!article) return;
    const bounds = article.getBoundingClientRect();
    const ratio = (innerHeight - bounds.top) / bounds.height;
    [50, 90].forEach(threshold => {
      if (ratio >= threshold / 100 && !reached.has(threshold)) {
        reached.add(threshold);
        emit('article_scroll', { percent: threshold });
      }
    });
  };
  addEventListener('scroll', () => {
    if (!scheduled) { scheduled = true; requestAnimationFrame(progress); }
  }, { passive: true });
})();
