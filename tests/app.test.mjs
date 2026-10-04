import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import { createContext, runInContext } from "node:vm";

const source = await readFile(new URL("../assets/app.js", import.meta.url), "utf8");
const videos = [
  {
    id: "update", title: "Destination Engineer Channel Update",
    category: "misc", companies: ["Google"], difficulty: "Easy",
  },
  {
    id: "hashing", title: "Consistent Hashing",
    description: "A Destination Engineer lesson.", category: "system-design",
    companies: ["Microsoft"], difficulty: "Medium",
  },
  { id: "interviews", title: "FAANG Interview Guide", category: "behavioral" },
];

async function app(search = "") {
  const elements = new Map();
  const context = createContext({
    document: {
      getElementById(id) {
        if (!elements.has(id)) elements.set(id, { addEventListener() {} });
        return elements.get(id);
      },
      querySelectorAll() { return []; },
    },
    window: { location: { search, pathname: "/" } },
    history: { replaceState() {} },
    fetch: async () => ({ ok: true, json: async () => ({ videos }) }),
    URLSearchParams, console, setTimeout, clearTimeout,
  });
  await runInContext(source, context);
  assert.equal(elements.get("total").textContent, videos.length);
  return { context, elements };
}

function searchResults(context, query) {
  context.testQuery = query;
  return Array.from(runInContext("state.query = testQuery; filtered().map(v => v.id)", context));
}

test("legacy name searches find the rebranded catalog", async () => {
  const { context } = await app();
  const expected = ["update", "hashing"];
  for (const query of ["Destination Engineer", "Destination FAANG", "DESTINATION FAANG",
    "DestinationFAANG", "  destination   faang  "]) {
    assert.deepEqual(searchResults(context, query), expected, query);
  }
  assert.deepEqual(searchResults(context, "Destination FAANG Channel"), ["update"]);
});

test("old search links retain category filters", async () => {
  const { context, elements } = await app("?q=Destination+FAANG&cat=system-design");
  assert.deepEqual(Array.from(runInContext("filtered().map(v => v.id)", context)), ["hashing"]);
  assert.equal(elements.get("search").value, "Destination FAANG");
  assert.match(elements.get("grid").innerHTML, /Consistent Hashing/);
  assert.doesNotMatch(elements.get("grid").innerHTML, /Channel Update/);
});

test("brand aliases preserve company, difficulty, and generic topic searches", async () => {
  const { context } = await app();
  assert.deepEqual(searchResults(context, "FAANG"), ["interviews"]);
  runInContext('state.company = "Google"; state.difficulty = "Easy"', context);
  assert.deepEqual(searchResults(context, "Destination FAANG"), ["update"]);
  runInContext('state.difficulty = "Hard"', context);
  assert.deepEqual(searchResults(context, "Destination Engineer"), []);
});
