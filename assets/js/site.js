/* Nur für die Navigation. Alle Inhalte bleiben auch ohne JavaScript sichtbar. */
const header = document.querySelector('.site-header');
const toggle = document.querySelector('.menu-toggle');
const menu = document.querySelector('#hauptmenue');

if (header && toggle && menu) {
  header.classList.add('js-menu');
  toggle.hidden = false;

  function closeMenu() {
    header.classList.remove('menu-open');
    toggle.setAttribute('aria-expanded', 'false');
  }

  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    header.classList.toggle('menu-open', open);
    toggle.setAttribute('aria-expanded', String(open));
  });

  menu.addEventListener('click', (event) => {
    if (event.target.closest('a')) closeMenu();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
      closeMenu();
      toggle.focus();
    }
  });

}
