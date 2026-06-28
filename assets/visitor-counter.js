"use strict";

/**
 * Destination FAANG — visitor counter (frontend).
 *
 * Fetches the running unique-visitor total from the Cloudflare Worker and
 * displays it in the footer. The counter element stays hidden until a real
 * number arrives, so the site never shows a broken/zero state if the Worker
 * is unreachable or not yet deployed.
 *
 * SETUP: set COUNTER_ENDPOINT to your deployed Worker URL (see worker/README.md).
 */
(function () {
  // TODO: replace with your deployed Worker URL, e.g.
  //   "https://df-visitor-counter.<your-subdomain>.workers.dev"
  // or, if mapped to a custom subdomain, "https://counter.destinationfaang.com".
  var COUNTER_ENDPOINT = "https://counter.destinationfaang.com";

  if (/REPLACE_WITH/.test(COUNTER_ENDPOINT)) return;

  var wrap = document.getElementById("visitor-counter");
  var valueEl = document.getElementById("visitor-count");
  if (!wrap || !valueEl) return;

  fetch(COUNTER_ENDPOINT, { credentials: "include" })
    .then(function (res) {
      if (!res.ok) throw new Error("bad status " + res.status);
      return res.json();
    })
    .then(function (data) {
      if (data && typeof data.count === "number") {
        valueEl.textContent = data.count.toLocaleString();
        wrap.hidden = false;
      }
    })
    .catch(function () {
      /* Worker unreachable — leave the counter hidden. */
    });
})();
