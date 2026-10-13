(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  const onView = (els, cb, opts = { threshold: 0.25 }) => {
    const io = new IntersectionObserver(entries => entries.forEach(e => {
      if (e.isIntersecting) { cb(e.target); io.unobserve(e.target); }
    }), opts);
    els.forEach(el => io.observe(el));
  };

  const tween = (from, to, ms, step, done) => {
    if (reduce) { step(to); done?.(); return; }
    const t0 = performance.now();
    const tick = now => {
      const p = Math.min(1, (now - t0) / ms), e = 1 - Math.pow(1 - p, 3);
      step(from + (to - from) * e);
      if (p < 1) requestAnimationFrame(tick); else done?.();
    };
    requestAnimationFrame(tick);
  };

  const fmtTime = m => {
    m = ((Math.round(m) % 1440) + 1440) % 1440;
    return String(Math.floor(m / 60)).padStart(2, '0') + ':' + String(m % 60).padStart(2, '0');
  };

  /* nav */
  const nav = $('#nav');
  const lightSections = $$('.s-light, .s-morning');
  const updateNav = () => {
    nav.classList.toggle('scrolled', scrollY > 20);
    nav.classList.toggle('on-light', lightSections.some(s => {
      const r = s.getBoundingClientRect();
      return r.top <= 40 && r.bottom >= 40;
    }));
  };
  addEventListener('scroll', updateNav, { passive: true });
  updateNav();

  /* reveal */
  onView($$('.reveal'), el => el.classList.add('in'), { threshold: 0.15 });

  /* hero gauges */
  const setGauge = (g, val) => {
    const { pmin, pmax, suffix } = g.dataset;
    const p = Math.max(0, Math.min(1, (val - pmin) / (pmax - pmin)));
    $('.g-fg', g).style.strokeDashoffset = 314 * (1 - p * 0.85);
    $('b', g).textContent = Math.round(val) + suffix;
  };
  onView([$('.hero-panel')], panel => $$('.gauge', panel).forEach(g => {
    const to = +g.dataset.val, from = g.classList.contains('g-luz') ? 6500 : to * 0.6;
    tween(from, to, 1600, v => setGauge(g, v));
  }), { threshold: 0.1 });

  /* live metrics */
  const liveT = $('[data-live="temp"]'), liveH = $('[data-live="hum"]');
  let lt = 24.4, lh = 58;
  setInterval(() => {
    lt = Math.max(23.6, Math.min(25.2, lt + (Math.random() - .5) * .3));
    lh = Math.max(55, Math.min(61, lh + Math.round((Math.random() - .5) * 2)));
    liveT.textContent = lt.toFixed(1).replace('.', ',') + '°';
    liveH.textContent = lh + '%';
  }, 2500);

  /* app: lista de recursos + celular */
  const screen = $('.screen');
  const go = name => {
    screen.dataset.screen = name;
    $$('.tabbar button').forEach(b => b.classList.toggle('on', b.dataset.go === name));
    $$('.feat').forEach(b => {
      const on = b.dataset.go === name;
      b.classList.toggle('on', on);
      b.setAttribute('aria-selected', on);
    });
    if (name === 'hum') runHumidifier();
  };
  $$('[data-go]').forEach(b => b.addEventListener('click', () => go(b.dataset.go)));
  // no celular o aparelho fica abaixo da lista: leva até ele para ver a mudança
  $$('.feat').forEach(b => b.addEventListener('click', () => {
    if (innerWidth <= 980) $('#phone').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
  }));

  let ac = 23;
  const acRing = $('#acRing');
  const renderAC = () => {
    $('#acVal').textContent = ac + '°';
    if (acRing) acRing.style.strokeDashoffset = 327 * (1 - (ac - 16) / (30 - 16) * 0.9);
  };
  $$('[data-ac]').forEach(b => b.addEventListener('click', () => {
    ac = Math.max(16, Math.min(30, ac + +b.dataset.ac)); renderAC();
  }));
  renderAC();

  let hum = 41, humOn = true, humTimer;
  const humRing = $('#humRing');
  const renderHum = () => {
    $('#humVal').textContent = Math.round(hum) + '%';
    if (humRing) humRing.style.strokeDashoffset = 327 * (1 - hum / 100);
  };
  function runHumidifier() {
    clearInterval(humTimer);
    humTimer = setInterval(() => {
      const target = humOn ? 55 : 40;
      if (Math.abs(hum - target) < .5) return clearInterval(humTimer);
      hum += Math.sign(target - hum) * .5;
      renderHum();
    }, 120);
  }
  const rule = $('#humRule');
  rule.addEventListener('click', () => {
    humOn = !humOn;
    rule.classList.toggle('on', humOn);
    rule.setAttribute('aria-checked', humOn);
    $('.scr-hum .state').textContent = humOn ? 'Ligado' : 'Desligado';
    runHumidifier();
  });
  renderHum();


  /* cartões: do valor ruim ao ideal, com o aparelho reagindo */
  const hex = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
  const mix = (a, b, t) => 'rgb(' + hex(a).map((v, i) => Math.round(v + (hex(b)[i] - v) * t)).join(',') + ')';
  const CORES = { temp: ['#ef5b5b', '#5b6cf0'], hum: ['#e0a03c', '#4c8dff'], luz: ['#9fb8ff', '#ffb648'] };
  const fmt = (kind, v) => kind === 'luz' ? Math.round(v / 100) * 100 : Math.round(v);
  const playCard = card => {
    const m = $('.meter', card);
    if (!m || m._running) return;
    m._running = true;
    const { kind, unit } = m.dataset, from = +m.dataset.from, to = +m.dataset.to;
    const [c0, c1] = CORES[kind];
    const val = $('.m-val', m), label = $('.m-label', m), fill = $('.m-fill', m), dot = $('.m-dot', m);
    const ac = $('.ac-display', card), water = $('.h-water', card), bulb = $('.bulb', card);
    const step = t => {
      const v = from + (to - from) * t, cor = mix(c0, c1, t);
      val.textContent = fmt(kind, v).toLocaleString('pt-BR').replace('.', '') + unit;
      val.style.color = cor;
      fill.style.width = (t * 100) + '%';
      fill.style.background = 'linear-gradient(90deg,' + c0 + ',' + cor + ')';
      dot.style.left = (t * 100) + '%';
      dot.style.borderColor = cor;
      if (ac) ac.textContent = fmt(kind, v) + '°';
      if (water) water.style.height = v + '%';
      if (bulb) {
        const c = mix('#eef3ff', '#ffc56a', t);
        bulb.style.background = 'radial-gradient(circle at 40% 35%,#ffffff,' + c + ')';
        bulb.style.boxShadow = '0 0 40px ' + mix('#bcd0ff', '#ffb648', t) + ',0 0 90px ' + mix('#cfdcff', '#ffcf85', t);
      }
      const chegou = t >= 0.92;
      label.textContent = chegou ? label.dataset.good : label.dataset.bad;
      m.classList.toggle('done', chegou);
    };
    step(0);
    setTimeout(() => tween(0, 1, 2600, step, () => (m._running = false)), reduce ? 0 : 500);
  };
  const cardIO = new IntersectionObserver(entries => entries.forEach(e => {
    if (e.isIntersecting) playCard(e.target);
  }), { threshold: 0.55 });
  $$('#recursos .dev').forEach(c => cardIO.observe(c));

  /* uma noite: linha do tempo */
  const timeline = $('#timeline');
  const items = $$('li', timeline);
  const clock = $('#nightClock');
  const START = 22 * 60 + 30;
  const marks = items.map(li => {
    const [h, m] = li.dataset.t.split(':').map(Number);
    let t = h * 60 + m;
    if (t < START) t += 1440;
    return t - START;
  });
  const END = marks[marks.length - 1];
  const renderNight = t => {
    clock.textContent = fmtTime(START + t);
    let i = 0;
    while (i < marks.length - 2 && t >= marks[i + 1]) i++;
    const frac = Math.max(0, Math.min(1, (t - marks[i]) / (marks[i + 1] - marks[i])));
    timeline.style.setProperty('--p', ((i + frac) / (marks.length - 1)).toFixed(4));
    items.forEach((li, k) => li.classList.toggle('on', t >= marks[k]));
  };
  let running = false;
  const runNight = () => {
    if (running) return;
    running = true;
    renderNight(0);
    tween(0, END, 7000, renderNight, () => (running = false));
  };
  renderNight(-1);
  $('#bedtimeBtn').addEventListener('click', runNight);
  onView([timeline], runNight, { threshold: 0.4 });

  /* aprende: feedback + semana */
  const chips = $('#chips');
  chips.addEventListener('click', e => {
    if (e.target.tagName === 'BUTTON') e.target.classList.toggle('on');
  });
  const week = $('#week');
  const days = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Hoje'];
  const scores = [.38, .45, .44, .55, .6, .72, null];
  week.innerHTML = days.map((d, i) => `<div class="bar${i === 6 ? ' today' : ''}"><span></span><small>${d}</small></div>`).join('') +
    '<svg preserveAspectRatio="none"><path/><g></g></svg>';
  const bars = $$('.bar span', week);
  const svg = $('svg', week);
  const drawWeek = () => {
    const H = week.clientHeight, wr = week.getBoundingClientRect();
    svg.setAttribute('viewBox', `0 0 ${week.clientWidth} ${H - 24}`);
    const pts = [];
    scores.forEach((s, i) => {
      if (s == null) return;
      const r = bars[i].getBoundingClientRect();
      pts.push([r.left - wr.left + r.width / 2, H * (1 - s) + 6]);
    });
    $('path', svg).setAttribute('d', 'M' + pts.map(p => p.join(' ')).join(' L'));
    $('g', svg).innerHTML = pts.map(([x, y]) => `<circle cx="${x}" cy="${y}" r="5"/>`).join('');
  };
  const growBars = () => scores.forEach((s, i) => {
    if (s != null) bars[i].style.height = `calc(${s * 100}% - 24px)`;
  });
  onView([week], () => {
    growBars();
    setTimeout(drawWeek, reduce ? 0 : 1000);
  });
  addEventListener('resize', drawWeek);

  const send = $('#fbSend');
  send.addEventListener('click', () => {
    const picked = $$('.on', chips).map(b => b.textContent);
    const good = picked.includes('Dormi bem');
    const bad = picked.filter(t => t !== 'Dormi bem').length;
    scores[6] = Math.max(.3, Math.min(.9, (good ? .86 : .7) - bad * .08));
    growBars();
    setTimeout(drawWeek, reduce ? 0 : 1000);
    $('#fbDone').classList.add('show');
    send.disabled = true;
  });

  /* footer / CTA */
  $('#yr').textContent = new Date().getFullYear();
  $('#ctaMain').addEventListener('click', e => {
    e.preventDefault();
    // TODO: trocar pelo link real (WhatsApp, loja de apps ou formulário)
    location.href = 'mailto:contato@sonoperfeito.app?subject=Quero%20o%20Sono%20Perfeito';
  });
})();
