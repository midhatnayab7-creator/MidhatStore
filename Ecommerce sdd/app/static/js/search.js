/**
 * search.js — Optional debounced live search enhancement
 *
 * Submits the search form automatically after the user stops typing for 400ms.
 * Falls back gracefully if the element is not found (e.g., error pages).
 */
(function () {
  "use strict";

  const input = document.getElementById("search-input");
  if (!input) return;

  let debounceTimer;

  input.addEventListener("input", function () {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(function () {
      // Only auto-submit if the user has typed something or cleared the box
      input.closest("form").submit();
    }, 400);
  });
})();
