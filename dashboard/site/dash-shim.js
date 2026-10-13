// Stand-in for the Claude dashboard runtime, so dashboard/index.html runs as a
// plain web page on GitHub Pages. It implements only what that page uses:
// dash.calc, dash.data, dash.onData and dash.colors. Datasets are JSON files
// loaded with dash._load(id, url).
(function () {
  const results = {};
  const calcs = [];
  const listeners = [];
  const pending = { status: 'loading', data: [], columns: [], meta: [], refreshing: false };

  const run = (fn) => {
    try { fn(); } catch (err) { console.error(err); }
  };
  const notify = () => listeners.forEach(run);

  function compute() {
    calcs.forEach((c) => {
      const inputs = c.inputs.map((id) => results[id]);
      if (inputs.some((r) => !r || r.status === 'loading')) return;
      if (inputs.some((r) => r.status !== 'ok')) {
        results[c.id] = { ...pending, status: 'error' };
        return;
      }
      try {
        const data = c.fn(...inputs.map((r) => r.data));
        results[c.id] = { status: 'ok', data, columns: Array.isArray(data) && data[0] ? Object.keys(data[0]) : [], meta: [], refreshing: false };
      } catch (err) {
        console.error(`calc ${c.id} failed`, err);
        results[c.id] = { ...pending, status: 'error', message: String(err) };
      }
    });
  }

  window.dash = {
    colors: [1, 2, 3, 4, 5, 6, 7, 8].map((i) => `var(--series-${i})`),
    calc(id, spec) { calcs.push({ id, ...spec }); },
    data(id) { return results[id] || pending; },
    onData(fn) { listeners.push(fn); run(fn); },
    params() { return {}; },
    setParams() {},
    resetParams() {},
    setLink() {},
    refresh() {},
    async _load(id, url) {
      try {
        const res = await fetch(url, { cache: 'no-cache' });
        if (!res.ok) throw new Error(`${url}: HTTP ${res.status}`);
        const body = await res.json();
        const rows = Array.isArray(body) ? body : body.rows || body.data || body.results || [];
        results[id] = { status: 'ok', data: rows, columns: rows[0] ? Object.keys(rows[0]) : [], meta: [], refreshing: false, body };
      } catch (err) {
        console.error(err);
        results[id] = { ...pending, status: 'error', message: String(err) };
      }
      compute();
      notify();
      return results[id];
    },
  };

  let timer;
  let lastWidth = window.innerWidth;
  window.addEventListener('resize', () => {
    if (window.innerWidth === lastWidth) return;
    lastWidth = window.innerWidth;
    clearTimeout(timer);
    timer = setTimeout(notify, 150);
  });
})();
