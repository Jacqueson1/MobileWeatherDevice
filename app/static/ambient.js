(function () {
  const root = document.documentElement;

  // Same guards as app.js: reduced motion, or library missing -> do nothing
  if (!root.classList.contains('animate')) return;
  if (!window.anime) return;

  const { animate } = anime;
  const kind = document.body.dataset.weather;
  const level = Number(document.body.dataset.level) || 0;

  const rainy = (kind === 'rain' || kind === 'thunderstorm') && level > 0;
  if (!rainy) return;

  try {
    startRain(level);
    if (kind === 'thunderstorm') startLightning(level);
  } catch (err) {
    console.error('Ambient effect error:', err);
  }

  function startRain(level) {
    const count = [0, 14, 26, 42, 64][level] || 0;   // heavier rain = more drops

    const layer = document.createElement('div');
    layer.className = 'rain-layer';

    for (let i = 0; i < count; i++) {
      const drop = document.createElement('div');
      drop.className = 'raindrop';
      drop.style.left = Math.random() * 100 + '%';
      drop.style.height = 28 + Math.random() * 40 + 'px';
      drop.style.opacity = (0.25 + Math.random() * 0.5).toFixed(2);
      layer.appendChild(drop);
    }
    document.body.prepend(layer);

    const travel = layer.clientHeight;   // measured after it's in the page
    animate(layer.querySelectorAll('.raindrop'), {
      translateY: [-100, travel + 100],
      duration: () => 1100 - level * 130 + Math.random() * 500,   // heavier = faster
      delay: () => Math.random() * 2000,
      ease: 'linear',
      loop: true,
    });
  }

  function startLightning(level) {
    const hero = document.querySelector('.hero');
    if (!hero) return;

    const flash = document.createElement('div');
    flash.className = 'flash';
    hero.appendChild(flash);

    function strike() {
      // one quick, soft pulse, then a slow fade (never rapid flicker)
      animate(flash, {
        opacity: [0, 0.22],
        duration: 90,
        ease: 'outQuad',
        onComplete: () => animate(flash, { opacity: [0.22, 0], duration: 900, ease: 'outQuad' }),
      });
      // next strike in 5s to ~13s; stronger storms strike sooner
      setTimeout(strike, 5000 + Math.random() * (9000 - level * 1200));
    }
    setTimeout(strike, 2500);
  }
})();