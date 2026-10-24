(function () {
  const picker = document.getElementById('picker');
  if (!picker) return;

  const input = document.getElementById('picker-input');
  const list = document.getElementById('picker-list');
  const places = JSON.parse(document.getElementById('locations-data').textContent);
  const currentId = picker.dataset.currentId;
  const currentName = input.value;

  const GROUPS = [
    ['state', 'States'],
    ['district', 'Districts'],
    ['town', 'Towns'],
    ['division', 'Divisions'],
    ['recreation', 'Recreation centres'],
    ['unknown', 'Other'],
  ];

  let visible = [];   // places currently listed, in order
  let items = [];     // their <li> elements
  let active = -1;    // highlighted index

  // Remember this choice for next time
  try { localStorage.setItem('weatherLocation', currentId); } catch (e) { }

  function render(query) {
    const q = query.trim().toLowerCase();
    visible = [];
    list.textContent = '';

    for (const [type, label] of GROUPS) {
      const matches = places.filter((p) =>
        p.type === type &&
        (q === '' || p.name.toLowerCase().includes(q) || p.location_id.toLowerCase().includes(q))
      );
      if (!matches.length) continue;

      const heading = document.createElement('li');
      heading.className = 'picker-group';
      heading.setAttribute('role', 'presentation');
      heading.textContent = `${label} (${matches.length})`;
      list.appendChild(heading);

      for (const p of matches) {
        const li = document.createElement('li');
        li.className = 'picker-item';
        li.setAttribute('role', 'option');
        li.dataset.index = visible.length;
        li.textContent = p.name;
        if (p.location_id === currentId) li.classList.add('current');
        visible.push(p);
        list.appendChild(li);
      }
    }

    if (!visible.length) {
      const empty = document.createElement('li');
      empty.className = 'picker-empty';
      empty.textContent = 'No matching places';
      list.appendChild(empty);
    }

    items = Array.from(list.querySelectorAll('.picker-item'));
    // Searching: highlight the first hit. Browsing: highlight the current place.
    const start = q ? 0 : visible.findIndex((p) => p.location_id === currentId);
    setActive(visible.length ? start : -1);
  }

  function setActive(i) {
    if (items[active]) items[active].classList.remove('active');
    active = i;
    if (items[active]) {
      items[active].classList.add('active');
      items[active].scrollIntoView({ block: 'nearest' });
    }
  }

    function open() {
    const wasOpen = list.classList.contains('open');
    list.classList.add('open');                       // show it first...
    render(input.value === currentName ? '' : input.value);   // ...then build and scroll
    input.setAttribute('aria-expanded', 'true');

    // Small slide-in, only when opening and only if animations are allowed
    if (!wasOpen && window.anime && document.documentElement.classList.contains('animate')) {
      anime.animate(list, { opacity: [0, 1], translateY: [-6, 0], duration: 180, ease: 'outQuad' });
    }
  }

  function close() {
    list.classList.remove('open');
    input.setAttribute('aria-expanded', 'false');
    input.value = currentName;
  }

  function choose(place) {
    if (!place) return;
    if (place.location_id === currentId) { close(); input.blur(); return; }
    window.location.href = '/?location=' + encodeURIComponent(place.location_id);
  }

  input.addEventListener('focus', () => { input.select(); open(); });
  input.addEventListener('blur', close);
  input.addEventListener('input', () => open());

  input.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (!list.classList.contains('open')) open();
      else setActive(Math.min(active + 1, items.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setActive(Math.max(active - 1, 0));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      choose(visible[active]);
    } else if (e.key === 'Escape') {
      input.blur();
    }
  });

  // mousedown (not click) so the input doesn't lose focus before we read the choice
  list.addEventListener('mousedown', (e) => {
    e.preventDefault();
    const li = e.target.closest('.picker-item');
    if (li) choose(visible[Number(li.dataset.index)]);
  });
})();