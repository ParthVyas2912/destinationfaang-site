import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const source = await readFile(new URL("../worker/counter.js", import.meta.url), "utf8");
const { default: worker } = await import(
  `data:text/javascript;base64,${Buffer.from(source).toString("base64")}`
);

function storage(initial = "123") {
  let value = initial;
  const writes = [];
  return {
    writes,
    COUNTER: {
      async get(key) {
        assert.equal(key, "unique_visitors");
        return value;
      },
      async put(key, next) {
        assert.equal(key, "unique_visitors");
        value = next;
        writes.push(next);
      },
    },
  };
}

for (const origin of [
  "https://destinationengineer.com",
  "https://www.destinationengineer.com",
  "https://destinationfaang.com",
  "https://www.destinationfaang.com",
]) {
  test(`preserves credentials and existing visitor count for ${origin}`, async () => {
    const env = storage();
    const response = await worker.fetch(new Request("https://counter.example/", {
      headers: { Origin: origin, Cookie: "df_visitor=1" },
    }), env);
    assert.equal(response.headers.get("Access-Control-Allow-Origin"), origin);
    assert.equal(response.headers.get("Access-Control-Allow-Credentials"), "true");
    assert.equal(response.headers.get("Vary"), "Origin");
    assert.equal(response.headers.get("Set-Cookie"), null);
    assert.deepEqual(await response.json(), { count: 123 });
    assert.deepEqual(env.writes, []);
  });
}

test("new visitors use the same storage key and cookie name", async () => {
  const env = storage();
  const response = await worker.fetch(new Request("https://counter.example/", {
    headers: { Origin: "https://destinationengineer.com" },
  }), env);
  assert.deepEqual(await response.json(), { count: 124 });
  assert.deepEqual(env.writes, ["124"]);
  assert.match(response.headers.get("Set-Cookie"), /^df_visitor=1;/);
});

test("untrusted origins are not reflected, including lookalike domains", async () => {
  for (const origin of ["https://untrusted.example", "https://destinationengineer.com.evil.example", "null"]) {
    const response = await worker.fetch(new Request("https://counter.example/", {
      method: "OPTIONS",
      headers: { Origin: origin },
    }), storage());
    assert.equal(response.headers.get("Access-Control-Allow-Origin"), "https://destinationengineer.com");
  }
});

test("preflight and unsupported methods never update the count", async () => {
  const env = storage();
  const options = await worker.fetch(new Request("https://counter.example/", {
    method: "OPTIONS",
    headers: { Origin: "https://destinationengineer.com" },
  }), env);
  assert.equal(options.headers.get("Access-Control-Allow-Methods"), "GET, OPTIONS");
  const post = await worker.fetch(new Request("https://counter.example/", { method: "POST" }), env);
  assert.equal(post.status, 405);
  assert.deepEqual(env.writes, []);
});
