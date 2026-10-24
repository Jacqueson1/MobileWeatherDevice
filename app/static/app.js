(function () {
  const root = document.documentElement;

  // Reduced motion: stay static. Library missing: show the page normally.
  if (!root.classList.contains('animate')) return;
  if (!window.anime) { root.classList.remove('animate'); return; }

  const { animate, stagger } = anime;

  function countUp(el, delay, duration) {
    const target = Number(el.dataset.value);
    if (!Number.isFinite(target)) return;
    const state = { v: 0 };
    el.textContent = '0';
    animate(state, {
      v: target,
      duration: duration,
      delay: delay,
      ease: 'outExpo',
      onUpdate: () => { el.textContent = Math.round(state.v); },
    });
  }

  try {
    // ---- Hero ----
    const hero = document.querySelector('.hero');
    if (hero) {
      animate(hero, { opacity: [0, 1], translateY: [20, 0], duration: 800, ease: 'outExpo' });

      hero.querySelectorAll('.count').forEach((el) => countUp(el, 250, 1800));

      animate('.hero .part', {
        opacity: [0, 1],
        translateY: [16, 0],
        duration: 700,
        ease: 'outExpo',
        delay: (el, i) => 400 + i * 110,
      });

      animate('.part-bar-fill', {
        scaleX: [0, 1],
        duration: 900,
        ease: 'outExpo',
        delay: (el, i) => 700 + i * 110,
      });

      // Slow floating glows behind the content
      animate('.glow-a', { translateX: [-30, 30], translateY: [-10, 20], duration: 9000, ease: 'inOutSine', alternate: true, loop: true });
      animate('.glow-b', { translateX: [25, -25], translateY: [10, -15], duration: 11000, ease: 'inOutSine', alternate: true, loop: true });
    }

    // ---- Day cards (start after the hero) ----
    const cards = document.querySelectorAll('.card');

    animate(cards, {
      opacity: [0, 1],
      translateY: [28, 0],
      scale: [0.96, 1],
      duration: 800,
      ease: 'outExpo',
      delay: (el, i) => 500 + i * 90,
    });

    cards.forEach((card, i) => {
      card.querySelectorAll('.count').forEach((el) => countUp(el, 750 + i * 90, 1400));
    });

    animate('.range-fill', {
      scaleX: [0, 1],
      duration: 900,
      ease: 'outExpo',
      delay: (el, i) => 950 + i * 90,
    });

    // ---- Weather icons (hero, parts and cards) ----
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
          duration: 1700 - level * 250,
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
          loopDelay: 2600 - level * 500,
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
  } catch (err) {
    console.error('Animation error:', err);
    root.classList.remove('animate');   // fall back to a normal, visible page
  }
})();