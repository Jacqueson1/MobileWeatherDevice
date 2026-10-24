(function () {
  const root = document.documentElement;

  // Reduced motion: stay static. Library missing: show the page normally.
  if (!root.classList.contains('animate')) return;
  if (!window.anime) { root.classList.remove('animate'); return; }

  const { animate, stagger } = anime;
  const cards = document.querySelectorAll('.card');

  // 1) Cards slide in one after another
  animate(cards, {
    opacity: [0, 1],
    translateY: [28, 0],
    scale: [0.96, 1],
    delay: stagger(90),
    duration: 800,
    ease: 'outExpo',
  });

  // 3a) Temperatures count up from 0
  cards.forEach((card, i) => {
    card.querySelectorAll('.count').forEach((el) => {
      const target = Number(el.dataset.value);
      if (!Number.isFinite(target)) return;
      const state = { v: 0 };
      el.textContent = '0';
      animate(state, {
        v: target,
        duration: 1400,
        delay: 250 + i * 90,
        ease: 'outExpo',
        onUpdate: () => { el.textContent = Math.round(state.v); },
      });
    });
  });

  // 3b) Range bars grow from the left
  animate('.range-fill', {
    scaleX: [0, 1],
    duration: 900,
    ease: 'outExpo',
    delay: (el, i) => 450 + i * 90,
  });

  // 2) Weather icons: each kind gets its own loop
  document.querySelectorAll('.icon').forEach((icon) => {
    const kind = icon.dataset.kind;
    const level = Number(icon.dataset.level) || 0;
    const find = (sel) => icon.querySelectorAll(sel);

    if (kind === 'none') {
      animate(find('.rays'), { rotate: 360, duration: 14000, ease: 'linear', loop: true });
    }
    if (kind === 'rain' || kind === 'thunderstorm') {
      animate(find('.drop'), {
        translateY: [0, 9],
        opacity: [1, 0],
        duration: 1700 - level * 250,      // heavier rain falls faster
        ease: 'inQuad',
        loop: true,
        delay: stagger(140),
      });
    }
    if (kind === 'thunderstorm') {
      animate(find('.bolt'), {
        opacity: [1, 0.1, 1, 0.25, 1],
        duration: 900,
        loop: true,
        loopDelay: 2600 - level * 500,      // stronger storms flash more often
      });
    }
    if (kind === 'haze') {
      animate(find('.haze-line'), {
        translateX: [-5, 5],
        duration: 2600,
        ease: 'inOutSine',
        alternate: true,
        loop: true,
        delay: stagger(350),
      });
    }
    if (find('.cloud').length) {
      animate(find('.cloud'), {
        translateX: [-2, 2],
        duration: 3500,
        ease: 'inOutSine',
        alternate: true,
        loop: true,
      });
    }
  });
})();