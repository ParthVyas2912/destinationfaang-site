"use strict";

const CATEGORY_LABELS = {
  "dsa": "DSA",
  "system-design": "System Design",
  "behavioral": "Behavioral",
  "misc": "Miscellaneous",
};

const state = {
  videos: [],
  category: "all",
  company: "all",
  difficulty: "all",
  query: "",
};

const els = {
  grid: document.getElementById("grid"),
  status: document.getElementById("status"),
  empty: document.getElementById("empty"),
  search: document.getElementById("search"),
  tabs: document.getElementById("tabs"),
  companyFilter: document.getElementById("company-filter"),
  difficultyFilter: document.getElementById("difficulty-filter"),
  total: document.getElementById("total"),
};

async function load() {
  try {
    const res = await fetch("videos.json", { cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    state.videos = (data.videos || []).slice();
    state.videos.sort((a, b) => (b.publishedAt || "").localeCompare(a.publishedAt || ""));
    els.total.textContent = state.videos.length;
    updateCounts();
    render();
  } catch (err) {
    els.status.textContent =
      "Could not load videos.json. Serve this folder over http:// (e.g. `python -m http.server`) — opening index.html directly via file:// is blocked by the browser.";
    console.error(err);
  }
}

function updateCounts() {
  const counts = { all: state.videos.length, dsa: 0, "system-design": 0, behavioral: 0, misc: 0 };
  for (const v of state.videos) counts[v.category] = (counts[v.category] || 0) + 1;
  document.querySelectorAll(".count").forEach((el) => {
    const key = el.getAttribute("data-count");
    el.textContent = counts[key] ?? 0;
  });
}

function filtered() {
  const q = state.query.trim().toLowerCase();
  return state.videos.filter((v) => {
    if (state.category !== "all" && v.category !== state.category) return false;
    if (state.company !== "all" && !(v.companies || []).includes(state.company)) return false;
    if (state.difficulty !== "all" && v.difficulty !== state.difficulty) return false;
    if (!q) return true;
    return (
      (v.title || "").toLowerCase().includes(q) ||
      (v.description || "").toLowerCase().includes(q) ||
      (v.topics || []).some((t) => t.toLowerCase().includes(q))
    );
  });
}

function formatDate(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  if (isNaN(d)) return "";
  return d.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
}

function escapeHtml(s) {
  return (s || "").replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])
  );
}

function cardHtml(v) {
  const label = CATEGORY_LABELS[v.category] || "Misc";
  const thumb = v.thumbnail
    ? `<img loading="lazy" src="${escapeHtml(v.thumbnail)}" alt="" onerror="this.style.display='none'"/>`
    : "";
  const diff = v.difficulty
    ? `<span class="pill diff-${v.difficulty.toLowerCase()}">${v.difficulty}</span>`
    : "";
  const companies = (v.companies || [])
    .map((c) => `<span class="pill company">${escapeHtml(c)}</span>`)
    .join("");
  const topics = (v.topics || [])
    .slice(0, 3)
    .map((t) => `<span class="pill topic">${escapeHtml(t)}</span>`)
    .join("");
  return `
    <a class="card" href="${escapeHtml(v.url)}" target="_blank" rel="noopener">
      <div class="thumb">${thumb}<span class="play">▶</span>${diff}</div>
      <div class="card-body">
        <h3 class="card-title">${escapeHtml(v.title)}</h3>
        <div class="pills">${companies}${topics}</div>
        <div class="card-meta">
          <span class="badge ${v.category}">${label}</span>
          <span class="date">${formatDate(v.publishedAt)}</span>
        </div>
      </div>
    </a>`;
}

function render() {
  const list = filtered();
  const bits = [];
  if (state.category !== "all") bits.push(CATEGORY_LABELS[state.category]);
  if (state.company !== "all") bits.push(state.company);
  if (state.difficulty !== "all") bits.push(state.difficulty);
  if (state.query) bits.push(`\u201c${state.query}\u201d`);
  els.status.textContent =
    `Showing ${list.length} ${list.length === 1 ? "video" : "videos"}` +
    (bits.length ? ` \u00b7 ${bits.join(" \u00b7 ")}` : "");
  els.empty.hidden = list.length !== 0;
  els.grid.innerHTML = list.map(cardHtml).join("");
}

function wireChips(container, key) {
  container.addEventListener("click", (e) => {
    const chip = e.target.closest("[data-" + key + "]");
    if (!chip) return;
    state[key] = chip.getAttribute("data-" + key);
    container.querySelectorAll("[data-" + key + "]").forEach((c) =>
      c.classList.toggle("is-active", c === chip)
    );
    render();
  });
}

els.tabs.addEventListener("click", (e) => {
  const btn = e.target.closest(".tab");
  if (!btn) return;
  state.category = btn.getAttribute("data-cat");
  document.querySelectorAll(".tab").forEach((t) => t.classList.toggle("is-active", t === btn));
  render();
});

wireChips(els.companyFilter, "company");
wireChips(els.difficultyFilter, "difficulty");

let t;
els.search.addEventListener("input", (e) => {
  clearTimeout(t);
  t = setTimeout(() => {
    state.query = e.target.value;
    render();
  }, 120);
});

load();
