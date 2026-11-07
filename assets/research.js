(() => {
  const tools = document.querySelector('[data-research-tools]');
  if (!tools) return;
  const search = tools.querySelector('input[type="search"]');
  const buttons = [...tools.querySelectorAll('[data-topic]')];
  const entries = [...document.querySelectorAll('[data-research-entry]')];
  const groups = [...document.querySelectorAll('[data-research-group]')];
  const count = tools.querySelector('[data-results-count]');
  const empty = document.querySelector('[data-empty-state]');
  let topic = 'all';
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  function update() {
    const query = normalize(search.value.trim());
    let visible = 0;
    for (const entry of entries) {
      const matchesTopic = topic === 'all' || entry.dataset.topic === topic;
      const matchesQuery = normalize(entry.textContent).includes(query);
      entry.hidden = !(matchesTopic && matchesQuery);
      if (!entry.hidden) visible++;
    }
    for (const group of groups) {
      const groupCount = [...group.querySelectorAll('[data-research-entry]')].filter(entry => !entry.hidden).length;
      group.hidden = groupCount === 0;
      const badge = group.querySelector('h2 .count');
      if (badge) badge.textContent = String(groupCount).padStart(2, '0');
      const jumpLink = document.querySelector(`.page-aside a[href="#${group.id}"]`);
      if (jumpLink) {
        jumpLink.hidden = group.hidden;
        const jumpCount = jumpLink.querySelector('span');
        if (jumpCount) jumpCount.textContent = String(groupCount).padStart(2, '0');
      }
    }
    count.textContent = `Showing ${visible} of ${entries.length} research items.`;
    empty.hidden = visible !== 0;
    for (const button of buttons) button.setAttribute('aria-pressed', String(button.dataset.topic === topic));
  }
  for (const button of buttons) button.addEventListener('click', () => { topic = button.dataset.topic; update(); });
  search.addEventListener('input', update);
  tools.hidden = false;
  update();
})();
