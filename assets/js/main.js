/* Expand/collapse-all control for the abstract unrolls.
   Each abstract is a native <details>, so the site works fully without JS. */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var button = document.getElementById('toggle-abstracts');
    var items = Array.prototype.slice.call(document.querySelectorAll('details.abstract'));

    if (!button) return;

    if (!items.length) {
      button.remove();
      return;
    }

    function allOpen() {
      return items.every(function (d) { return d.open; });
    }

    function sync() {
      var open = allOpen();
      button.textContent = open ? 'Collapse all abstracts' : 'Expand all abstracts';
      button.setAttribute('aria-pressed', open ? 'true' : 'false');
    }

    button.addEventListener('click', function () {
      var open = !allOpen();
      items.forEach(function (d) { d.open = open; });
      sync();
    });

    items.forEach(function (d) { d.addEventListener('toggle', sync); });

    sync();
  });
})();
