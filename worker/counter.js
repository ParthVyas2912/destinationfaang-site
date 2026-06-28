/**
 * Destination FAANG — unique visitor counter (Cloudflare Worker + KV).
 *
 * Counts UNIQUE visitors: a visitor is only counted once because we set a
 * long-lived `df_visitor` cookie. Repeat visits / refreshes send the cookie
 * back and are NOT counted again.
 *
 * Storage: a single KV key `unique_visitors` holding the running total.
 * Response: JSON `{ "count": <number> }` with CORS so the static site
 * (https://destinationfaang.com) can read it via fetch(..., {credentials:'include'}).
 *
 * Deploy: see worker/README.md. Bind a KV namespace as COUNTER (see wrangler.toml).
 */

const ALLOWED_ORIGIN = "https://destinationfaang.com";
const KV_KEY = "unique_visitors";
const COOKIE_NAME = "df_visitor";
const COOKIE_MAX_AGE = 60 * 60 * 24 * 365; // 1 year

function corsHeaders(origin) {
  // Echo the site origin (and its www variant) so credentialed requests work;
  // fall back to the canonical origin otherwise.
  const allowed =
    origin === ALLOWED_ORIGIN || origin === "https://www.destinationfaang.com"
      ? origin
      : ALLOWED_ORIGIN;
  return {
    "Access-Control-Allow-Origin": allowed,
    "Access-Control-Allow-Credentials": "true",
    "Vary": "Origin",
    "Cache-Control": "no-store",
    "Content-Type": "application/json; charset=utf-8",
  };
}

function hasVisitorCookie(request) {
  const cookie = request.headers.get("Cookie") || "";
  return new RegExp("(?:^|;\\s*)" + COOKIE_NAME + "=1(?:;|$)").test(cookie);
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const headers = corsHeaders(origin);

    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: { ...headers, "Access-Control-Allow-Methods": "GET, OPTIONS" },
      });
    }
    if (request.method !== "GET") {
      return new Response(JSON.stringify({ error: "method_not_allowed" }), {
        status: 405,
        headers,
      });
    }

    let count = parseInt((await env.COUNTER.get(KV_KEY)) || "0", 10);
    if (!Number.isFinite(count) || count < 0) count = 0;

    if (!hasVisitorCookie(request)) {
      count += 1;
      await env.COUNTER.put(KV_KEY, String(count));
      // Cross-subdomain, secure cookie. SameSite=None requires Secure.
      headers["Set-Cookie"] =
        COOKIE_NAME +
        "=1; Max-Age=" +
        COOKIE_MAX_AGE +
        "; Path=/; Secure; HttpOnly; SameSite=None";
    }

    return new Response(JSON.stringify({ count }), { headers });
  },
};
