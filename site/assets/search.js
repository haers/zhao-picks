/* 仅搜索已公开的站内文章，不上传查询，不接入第三方服务。 */
(() => {
  document.getElementById('menu-button')?.setAttribute('aria-label', '展开或收起导航');
  for (const table of document.querySelectorAll('main table')) {
    const headers = [...table.querySelectorAll('thead th')].map(header => header.textContent.trim());
    if (headers.length !== 4 || !['项目', '专题'].includes(headers[0])) continue;
    table.classList.add('picks-directory');
    table.parentElement.classList.add('picks-directory-wrap');
    for (const row of table.querySelectorAll('tbody tr')) [...row.children].forEach((cell, index) => { cell.dataset.label = headers[index]; });
  }
  const container = document.querySelector('.picks-search');
  const input = document.getElementById('picks-search-input');
  const results = document.getElementById('picks-search-results');
  if (!container || !input || !results) return;
  let index;
  let request = 0;
  const close = () => { results.hidden = true; input.setAttribute('aria-expanded', 'false'); };
  const message = text => {
    const paragraph = document.createElement('p');
    paragraph.setAttribute('role', 'status');
    paragraph.textContent = text;
    results.replaceChildren(paragraph);
  };
  const search = async () => {
    const sequence = ++request;
    const query = input.value.trim().toLocaleLowerCase();
    if (!query) { close(); return; }
    results.hidden = false;
    input.setAttribute('aria-expanded', 'true');
    message('正在搜索…');
    try {
      index ??= fetch(container.dataset.index, { signal: AbortSignal.timeout(5000) }).then(response => {
        if (!response.ok) throw new Error('search unavailable');
        return response.json();
      }).then(data => {
        if (!Array.isArray(data) || data.some(item => !['title', 'url', 'text'].every(key => typeof item[key] === 'string') || !item.url.startsWith(new URL(container.dataset.index, location.href).pathname.replace(/search\.json$/, 'reviews/')))) throw new Error('invalid search index');
        return data;
      });
      const entries = await index;
      if (sequence !== request) return;
      const terms = query.split(/\s+/);
      const hits = entries.filter(item => terms.every(term => `${item.title} ${item.text}`.toLocaleLowerCase().includes(term))).sort((a, b) => Number(b.title.toLocaleLowerCase().includes(query)) - Number(a.title.toLocaleLowerCase().includes(query))).slice(0, 12);
      if (!hits.length) { message('没有找到相关项目，可以换个关键词或浏览项目目录。'); return; }
      const list = document.createElement('ul');
      for (const item of hits) {
        const row = document.createElement('li');
        const link = document.createElement('a');
        link.href = item.url;
        link.textContent = item.title;
        const preview = document.createElement('span');
        const position = Math.max(0, item.text.toLocaleLowerCase().indexOf(terms[0]) - 25);
        preview.textContent = item.text.slice(position, position + 100);
        link.appendChild(preview);
        row.appendChild(link);
        list.appendChild(row);
      }
      results.replaceChildren(list);
    } catch {
      if (sequence === request) message('搜索暂时不可用，请通过侧栏浏览项目目录。');
      index = undefined;
    }
  };
  input.addEventListener('input', search);
  input.addEventListener('search', search);
  input.addEventListener('keydown', event => { if (event.key === 'Escape') { request++; close(); } });
  document.addEventListener('click', event => { if (!container.contains(event.target)) { request++; close(); } });
})();
