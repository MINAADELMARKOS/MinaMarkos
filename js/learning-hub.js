/* Progressive enhancement: articles, categories, TOC, and code work without JS. */
(() => {
  'use strict';
  const controls = document.querySelector('.library-controls');
  if (controls) {
    const search = document.querySelector('#article-search');
    const category = document.querySelector('#category-filter');
    const cards = [...document.querySelectorAll('.article-card')];
    const count = document.querySelector('#result-count');
    const empty = document.querySelector('#no-results');
    const params = new URLSearchParams(location.search);
    const requestedCategory = params.get('category') || '';
    if ([...category.options].some(o => o.value === requestedCategory)) category.value = requestedCategory;
    search.value = params.get('q') || '';
    function filter(updateUrl = true) {
      const query = search.value.trim().toLocaleLowerCase();
      let visible = 0;
      cards.forEach(card => {
        const match = (!category.value || card.dataset.categories.split(' | ').includes(category.value)) &&
          (!query || card.dataset.search.toLocaleLowerCase().includes(query));
        card.hidden = !match;
        visible += Number(match);
      });
      count.textContent = `${visible} ${visible === 1 ? 'article' : 'articles'}`;
      empty.hidden = visible !== 0;
      if (updateUrl) {
        const url = new URL(location.href);
        query ? url.searchParams.set('q', search.value.trim()) : url.searchParams.delete('q');
        category.value ? url.searchParams.set('category', category.value) : url.searchParams.delete('category');
        history.replaceState(null, '', url);
      }
    }
    controls.hidden = false;
    controls.addEventListener('submit', event => event.preventDefault());
    search.addEventListener('input', () => filter());
    category.addEventListener('change', () => filter());
    controls.addEventListener('reset', () => setTimeout(() => { search.value = ''; category.value = ''; filter(); }, 0));
    filter(false);
  }
  document.querySelectorAll('.copy-code').forEach(button => {
    button.hidden = false;
    button.addEventListener('click', async () => {
      const sample = button.closest('.code-sample');
      const pre = sample.querySelector('pre');
      const status = sample.querySelector('.copy-status');
      try {
        if (!navigator.clipboard || !window.isSecureContext) throw new Error('Select manually');
        await navigator.clipboard.writeText(pre.querySelector('code').textContent);
        button.textContent = 'Copied';
        if (status) status.textContent = 'Code copied to clipboard.';
      } catch {
        const selection = window.getSelection();
        const range = document.createRange();
        range.selectNodeContents(pre);
        selection.removeAllRanges();
        selection.addRange(range);
        pre.focus();
        button.textContent = 'Selected — use Ctrl/Cmd+C';
        if (status) status.textContent = 'Code selected. Press Control C or Command C to copy.';
      }
      setTimeout(() => { button.textContent = 'Copy code'; }, 2500);
    });
  });
})();
