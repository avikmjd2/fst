// ================================================================
//  Pullinguistics — Frontend Logic (Multi-Language)
//  Calls API at localhost:8000, renders results + state graph
// ================================================================

const API_BASE = "http://localhost:8000";

// ── DOM refs ─────────────────────────────────────────────────────
const wordInput      = document.getElementById("wordInput");
const analyzeBtn     = document.getElementById("analyzeBtn");
const langSelect     = document.getElementById("langSelect");
const statusText     = document.getElementById("statusText");
const badgeDot       = document.querySelector(".badge-dot");
const resultsSection = document.getElementById("resultsSection");
const sourceBadge    = document.getElementById("sourceBadge");
const wordEcho       = document.getElementById("wordEcho");
const analysisList   = document.getElementById("analysisList");
const analysisCount  = document.getElementById("analysisCount");
const graphCard      = document.getElementById("graphCard");
const graphStates    = document.getElementById("graphStates");
const graphArcs      = document.getElementById("graphArcs");
const fstSvg         = document.getElementById("fstSvg");
const traversalSec   = document.getElementById("traversalSection");
const traversalPath  = document.getElementById("traversalPath");
const quickChips     = document.getElementById("quickChips");

// ── Per-language config ──────────────────────────────────────────
const LANG_CONFIG = {
  eng: {
    placeholder: "Type a word…  e.g. walked, running, happiness",
    chips: ["walked", "running", "happiness", "flies", "unfair", "churches", "xylophone"],
    fontClass: "",
  },
  ben: {
    placeholder: "একটি শব্দ লিখুন…  যেমন: করি, বই, মেয়ে",
    chips: ["করি", "বই", "মেয়ে", "ছেলে", "দেখি", "ভালো", "মানুষ", "দেশের", "আমি"],
    fontClass: "font-bengali",
  },
  hin: {
    placeholder: "एक शब्द लिखें…  जैसे: लड़का, सुन्दर, पानी",
    chips: ["इसके", "स्थल", "हैं", "भीम", "गुफा", "दर्शनीय", "पताका"],
    fontClass: "font-hindi",
  },
};

// ── Language switch ──────────────────────────────────────────────
function updateLanguageUI() {
  const lang = langSelect.value;
  const cfg = LANG_CONFIG[lang];

  wordInput.placeholder = cfg.placeholder;
  wordInput.value = "";
  resultsSection.hidden = true;

  // Font class on input
  wordInput.className = cfg.fontClass;

  // Rebuild chips
  quickChips.innerHTML = "";
  cfg.chips.forEach(word => {
    const chip = document.createElement("span");
    chip.className = `chip ${cfg.fontClass}`;
    chip.dataset.word = word;
    chip.textContent = word;
    chip.addEventListener("click", () => {
      wordInput.value = word;
      analyzeWord(word);
    });
    quickChips.appendChild(chip);
  });
}

langSelect.addEventListener("change", updateLanguageUI);
updateLanguageUI(); // initial

// ── Health check ─────────────────────────────────────────────────
async function checkHealth() {
  try {
    const res = await fetch(`${API_BASE}/health`);
    const data = await res.json();
    if (data.status === "ok") {
      const langs = data.languages || {};
      const count = Object.values(langs).filter(Boolean).length;
      statusText.textContent = `API Online (${count} lang)`;
      badgeDot.classList.add("online");
      analyzeBtn.disabled = false;
      return true;
    }
  } catch (_) { /* fall through */ }
  statusText.textContent = "API Offline";
  badgeDot.classList.remove("online");
  analyzeBtn.disabled = true;
  return false;
}

checkHealth();
setInterval(checkHealth, 10000);

// ── Analyze word ─────────────────────────────────────────────────
async function analyzeWord(word) {
  if (!word.trim()) return;

  const btnText   = analyzeBtn.querySelector(".btn-text");
  const btnLoader = analyzeBtn.querySelector(".btn-loader");
  btnText.hidden = true;
  btnLoader.hidden = false;
  analyzeBtn.disabled = true;

  try {
    const res = await fetch(`${API_BASE}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ word: word.trim(), language: langSelect.value }),
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    renderResults(data);
  } catch (err) {
    console.error("Analyze error:", err);
    alert("Failed to reach the API. Make sure it's running on port 8000.");
  } finally {
    btnText.hidden = false;
    btnLoader.hidden = true;
    analyzeBtn.disabled = false;
  }
}

// ── Render results ───────────────────────────────────────────────
function renderResults(data) {
  resultsSection.hidden = false;
  const lang = data.language || "eng";
  const cfg = LANG_CONFIG[lang] || LANG_CONFIG.eng;

  // Source badge
  const srcLower = data.source.toLowerCase();
  sourceBadge.textContent = data.source;
  sourceBadge.className = `source-badge ${srcLower}`;

  // Echo the word
  wordEcho.textContent = data.word;
  wordEcho.className = `word-echo ${cfg.fontClass}`;

  // Analyses list
  analysisCount.textContent = `${data.analyses.length} result${data.analyses.length !== 1 ? "s" : ""}`;
  analysisList.innerHTML = "";

  data.analyses.forEach(a => {
    const item = document.createElement("div");
    item.className = "analysis-item";

    const featureTags = a.features
      ? a.features.split(";").map(f => `<span class="tag">${escHtml(f)}</span>`).join("")
      : "";

    // For Bengali/Hindi, also split on | (CoNLL-U feature separator)
    let extraTags = "";
    if (a.features && a.features.includes("|")) {
      extraTags = a.features.split("|").map(f => `<span class="tag">${escHtml(f)}</span>`).join("");
      // Clear the ; tags if we used | instead
      if (!a.features.includes(";")) {
        item.innerHTML = `
          <span class="analysis-raw ${cfg.fontClass}">${escHtml(a.raw)}</span>
          <div class="analysis-detail">
            <span class="tag lemma">lemma: ${escHtml(a.lemma)}</span>
            ${extraTags}
          </div>
        `;
        analysisList.appendChild(item);
        return;
      }
    }

    item.innerHTML = `
      <span class="analysis-raw ${cfg.fontClass}">${escHtml(a.raw)}</span>
      <div class="analysis-detail">
        <span class="tag lemma">lemma: ${escHtml(a.lemma)}</span>
        ${featureTags}
      </div>
    `;
    analysisList.appendChild(item);
  });

  // FST Graph
  if (data.fst_graph) {
    graphCard.hidden = false;
    graphStates.textContent = `${data.fst_graph.num_states} states`;
    graphArcs.textContent = `${data.fst_graph.num_arcs} arcs`;
    drawFSTGraph(data.fst_graph);
    renderTraversal(data.fst_graph.traversal);
  } else {
    graphCard.hidden = true;
  }

  resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

// ── Draw FST graph as SVG ────────────────────────────────────────
function drawFSTGraph(graph) {
  const { states, traversal } = graph;
  if (!states.length) return;

  const travStates = new Set();
  const travArcs = new Set();
  (traversal || []).forEach(t => {
    travStates.add(t.state);
    travStates.add(t.next_state);
    travArcs.add(`${t.state}->${t.next_state}`);
  });

  const R = 22;
  const PAD = 60;

  // Dynamically compute spacing based on longest arc label
  let maxLabelLen = 6;
  states.forEach(s => {
    (s.arcs || []).forEach(arc => {
      const lbl = arc.input_label === arc.output_label
        ? arc.input_label
        : `${arc.input_label}:${arc.output_label}`;
      maxLabelLen = Math.max(maxLabelLen, lbl.length);
    });
  });
  const SPACING_X = Math.max(120, Math.min(300, maxLabelLen * 12 + 60));
  const SPACING_Y = 90;

  const ordered = bfsOrder(states, graph.start_state);
  const statePos = {};
  
  // Lay nodes out linearly in a single row to prevent ugly overlapping backward arcs
  ordered.forEach((sid, i) => {
    statePos[sid] = {
      x: PAD + i * SPACING_X,
      y: PAD + 20, // slightly lower to make room for tall arcs
    };
  });

  const width  = PAD * 2 + Math.max(0, ordered.length - 1) * SPACING_X;
  const height = PAD * 2 + R * 2 + 40;

  fstSvg.innerHTML = "";
  fstSvg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  fstSvg.setAttribute("width", width);
  fstSvg.setAttribute("height", height);

  const defs = svgEl("defs");
  defs.innerHTML = `
    <marker id="arrowhead" markerWidth="8" markerHeight="6"
            refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L8,3 L0,6" fill="rgba(255,255,255,0.3)" />
    </marker>
    <marker id="arrowhead-active" markerWidth="8" markerHeight="6"
            refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L8,3 L0,6" fill="#8b5cf6" />
    </marker>
  `;
  fstSvg.appendChild(defs);

  states.forEach(s => {
    (s.arcs || []).forEach(arc => {
      if (!(arc.src in statePos) || !(arc.dst in statePos)) return;
      const from = statePos[arc.src];
      const to   = statePos[arc.dst];
      const isTrav = travArcs.has(`${arc.src}->${arc.dst}`);
      if (arc.src === arc.dst) {
        drawSelfLoop(fstSvg, from, R, arc, isTrav);
      } else {
        drawArc(fstSvg, from, to, R, arc, isTrav);
      }
    });
  });

  states.forEach(s => {
    if (!(s.id in statePos)) return;
    const pos = statePos[s.id];
    const isTrav = travStates.has(s.id);

    if (s.is_final) {
      const outer = svgEl("circle");
      outer.setAttribute("cx", pos.x);
      outer.setAttribute("cy", pos.y);
      outer.setAttribute("r", R + 4);
      outer.setAttribute("class", "final-ring");
      fstSvg.appendChild(outer);
    }

    const c = svgEl("circle");
    c.setAttribute("cx", pos.x);
    c.setAttribute("cy", pos.y);
    c.setAttribute("r", R);
    let cls = "state-circle";
    if (s.is_start) cls += " start";
    if (s.is_final) cls += " final";
    if (isTrav) cls += " traversed";
    c.setAttribute("class", cls);
    fstSvg.appendChild(c);

    const label = svgEl("text");
    label.setAttribute("x", pos.x);
    label.setAttribute("y", pos.y);
    label.setAttribute("class", "state-label");
    label.textContent = `q${s.id}`;
    fstSvg.appendChild(label);

    if (s.is_start) {
      const arrow = svgEl("line");
      arrow.setAttribute("x1", pos.x - R - 22);
      arrow.setAttribute("y1", pos.y);
      arrow.setAttribute("x2", pos.x - R - 2);
      arrow.setAttribute("y2", pos.y);
      arrow.setAttribute("class", "arc-line");
      arrow.style.markerEnd = "url(#arrowhead)";
      fstSvg.appendChild(arrow);
    }
  });
}

function drawArc(svg, from, to, R, arc, isTrav) {
  const dx = to.x - from.x;
  const dy = to.y - from.y;
  const dist = Math.sqrt(dx * dx + dy * dy);
  const nx = dx / dist, ny = dy / dist;
  const x1 = from.x + nx * R;
  const y1 = from.y + ny * R;
  const x2 = to.x - nx * (R + 6);
  const y2 = to.y - ny * (R + 6);
  const mx = (x1 + x2) / 2 - ny * 14;
  const my = (y1 + y2) / 2 + nx * 14;

  const path = svgEl("path");
  path.setAttribute("d", `M${x1},${y1} Q${mx},${my} ${x2},${y2}`);
  let cls = "arc-line";
  if (isTrav) cls += " traversed";
  path.setAttribute("class", cls);
  path.style.markerEnd = isTrav ? "url(#arrowhead-active)" : "url(#arrowhead)";
  svg.appendChild(path);

  const lx = mx, ly = my - 6;
  // Always show input:output format (textbook FST notation)
  const label = svgEl("text");
  label.setAttribute("x", lx);
  label.setAttribute("y", ly);
  label.setAttribute("class", isTrav ? "arc-label traversed" : "arc-label");

  const tIn = svgEl("tspan");
  tIn.setAttribute("class", "in-label");
  tIn.textContent = arc.input_label;

  const tSep = svgEl("tspan");
  tSep.setAttribute("class", "sep-label");
  tSep.textContent = ":";

  const tOut = svgEl("tspan");
  tOut.setAttribute("class", "out-label");
  tOut.textContent = arc.output_label;

  label.appendChild(tIn);
  label.appendChild(tSep);
  label.appendChild(tOut);
  svg.appendChild(label);
}

function drawSelfLoop(svg, pos, R, arc, isTrav) {
  const cx = pos.x, cy = pos.y - R - 16;
  const path = svgEl("path");
  path.setAttribute("d",
    `M${pos.x - 8},${pos.y - R} C${cx - 20},${cy - 14} ${cx + 20},${cy - 14} ${pos.x + 8},${pos.y - R}`
  );
  let cls = "arc-line";
  if (isTrav) cls += " traversed";
  path.setAttribute("class", cls);
  path.style.markerEnd = isTrav ? "url(#arrowhead-active)" : "url(#arrowhead)";
  svg.appendChild(path);

  const label = svgEl("text");
  label.setAttribute("x", cx);
  label.setAttribute("y", cy - 18);
  label.setAttribute("class", isTrav ? "arc-label traversed" : "arc-label");

  if (arc.input_label === arc.output_label) {
    const tIn = svgEl("tspan");
    tIn.setAttribute("class", "in-label");
    tIn.textContent = arc.input_label;
    label.appendChild(tIn);
  } else {
    const tIn = svgEl("tspan");
    tIn.setAttribute("class", "in-label");
    tIn.textContent = arc.input_label;

    const tSep = svgEl("tspan");
    tSep.setAttribute("class", "sep-label");
    tSep.textContent = ":";

    const tOut = svgEl("tspan");
    tOut.setAttribute("class", "out-label");
    tOut.textContent = arc.output_label;

    label.appendChild(tIn);
    label.appendChild(tSep);
    label.appendChild(tOut);
  }
  svg.appendChild(label);
}

function bfsOrder(states, startId) {
  const adj = {};
  states.forEach(s => {
    adj[s.id] = [];
    (s.arcs || []).forEach(a => {
      if (a.dst !== s.id) adj[s.id].push(a.dst);
    });
  });
  const visited = new Set();
  const order = [];
  const queue = [startId];
  visited.add(startId);
  while (queue.length) {
    const cur = queue.shift();
    order.push(cur);
    (adj[cur] || []).forEach(n => {
      if (!visited.has(n)) { visited.add(n); queue.push(n); }
    });
  }
  states.forEach(s => { if (!visited.has(s.id)) order.push(s.id); });
  return order;
}

// ── Render traversal path ────────────────────────────────────────
function renderTraversal(traversal) {
  if (!traversal || !traversal.length) { traversalSec.hidden = true; return; }
  traversalSec.hidden = false;
  traversalPath.innerHTML = "";
  addTravState(traversal[0].state);
  traversal.forEach(step => {
    const arrow = document.createElement("span");
    arrow.className = "trav-arrow"; arrow.textContent = "→";
    traversalPath.appendChild(arrow);

    const lbl = document.createElement("span");
    lbl.className = "trav-label";
    lbl.textContent = `${step.input_char}:${step.output_char}`;
    traversalPath.appendChild(lbl);

    const arrow2 = document.createElement("span");
    arrow2.className = "trav-arrow"; arrow2.textContent = "→";
    traversalPath.appendChild(arrow2);
    addTravState(step.next_state);
  });
}

function addTravState(sid) {
  const el = document.createElement("span");
  el.className = "trav-state"; el.textContent = `q${sid}`;
  traversalPath.appendChild(el);
}

// ── Helpers ──────────────────────────────────────────────────────
function svgEl(tag) {
  return document.createElementNS("http://www.w3.org/2000/svg", tag);
}
function escHtml(s) {
  const d = document.createElement("div");
  d.textContent = s;
  return d.innerHTML;
}

// ── Event listeners ──────────────────────────────────────────────
analyzeBtn.addEventListener("click", () => analyzeWord(wordInput.value));
wordInput.addEventListener("keydown", e => {
  if (e.key === "Enter") analyzeWord(wordInput.value);
});
