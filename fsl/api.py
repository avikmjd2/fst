"""
api.py - Unified Multi-Language Morphological Analyzer API

Supports:
  - English (eng): FST + Neural fallback → analyses + state graph
  - Bengali (ben): Dictionary FST → analyses + state graph (no neural)
  - Hindi  (hin): Dictionary FST → analyses + state graph (no neural)

Run from fsl/ directory:
    uvicorn api:app --reload --port 8000
"""
import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import pynini

# ── Path setup ────────────────────────────────────────────────────
FSL_DIR = os.path.dirname(__file__)
BEN_DIR = os.path.abspath(os.path.join(FSL_DIR, "..", "bengali_fst"))
HIN_DIR = os.path.abspath(os.path.join(FSL_DIR, "..", "hindi_fst"))

sys.path.insert(0, FSL_DIR)


# ── Pydantic Models ──────────────────────────────────────────────

class AnalyzeRequest(BaseModel):
    word: str = Field(..., example="walked")
    language: str = Field("eng", example="eng")   # eng | ben | hin


class BatchAnalyzeRequest(BaseModel):
    words: list[str] = Field(..., example=["walked", "running"])
    language: str = Field("eng", example="eng")


class FSTArc(BaseModel):
    src: int
    dst: int
    input_label: str
    output_label: str


class FSTState(BaseModel):
    id: int
    is_start: bool = False
    is_final: bool = False
    arcs: list[FSTArc] = []


class TraversalStep(BaseModel):
    state: int
    input_char: str
    output_char: str
    next_state: int


class FSTGraph(BaseModel):
    states: list[FSTState]
    num_states: int
    num_arcs: int
    start_state: int
    traversal: list[TraversalStep] = []


class Analysis(BaseModel):
    raw: str
    lemma: str
    features: str


class AnalyzeResponse(BaseModel):
    word: str
    language: str
    source: str                        # "FST", "Neural", or "Dictionary"
    analyses: list[Analysis]
    fst_graph_raw: FSTGraph | None = None
    fst_graph_textbook: FSTGraph | None = None


# ── FST graph helpers ─────────────────────────────────────────────

def _label_str(label: int, symtab) -> str:
    if label == 0:
        return "ε"
    if symtab:
        s = symtab.find(label)
        if s != "":
            return s
    # For Unicode characters (Bengali/Hindi), use chr() for valid codepoints
    try:
        return chr(label)
    except (ValueError, OverflowError):
        return f"<{label}>"


def _extract_graph(lattice: pynini.Fst) -> FSTGraph:
    """Pull every state and arc out of a composed lattice."""
    isym = lattice.input_symbols()
    osym = lattice.output_symbols()
    start = lattice.start()
    states, total_arcs = [], 0

    for sid in lattice.states():
        arcs = []
        for a in lattice.arcs(sid):
            arcs.append(FSTArc(
                src=sid, dst=a.nextstate,
                input_label=_label_str(a.ilabel, isym),
                output_label=_label_str(a.olabel, osym),
            ))
        total_arcs += len(arcs)
        fw = float(lattice.final(sid))
        states.append(FSTState(
            id=sid, is_start=(sid == start),
            is_final=(fw != float("inf")), arcs=arcs,
        ))

    # Shortest-path traversal
    traversal = []
    try:
        sp = pynini.shortestpath(lattice)
        sp.rmepsilon()
        cur = sp.start()
        sp_isym, sp_osym = sp.input_symbols(), sp.output_symbols()
        while cur != pynini.NO_STATE_ID:
            found = False
            for a in sp.arcs(cur):
                traversal.append(TraversalStep(
                    state=cur,
                    input_char=_label_str(a.ilabel, sp_isym),
                    output_char=_label_str(a.olabel, sp_osym),
                    next_state=a.nextstate,
                ))
                cur = a.nextstate
                found = True
                break
            if not found:
                break
    except Exception:
        pass

    return FSTGraph(
        states=states, num_states=len(states),
        num_arcs=total_arcs, start_state=start,
        traversal=traversal,
    )

def _build_textbook_graph(word: str, raw_analysis: str) -> FSTGraph:
    """
    Synthetically builds a perfectly aligned FST diagram.
    Matches input characters to lemma characters 1-to-1,
    and then adds a single transition for all morphological tags.
    """
    parts = raw_analysis.split("+", 1)
    if len(parts) == 1:
        parts = raw_analysis.split("|", 1)
        delimiter = "|" if len(parts) > 1 else ""
    else:
        delimiter = "+"
        
    lemma = parts[0]
    tags = delimiter + parts[1] if len(parts) > 1 else ""
    
    states = []
    traversal = []
    
    # 1-to-1 character mapping
    for i, char in enumerate(word):
        out_char = lemma[i] if i < len(lemma) else "ε"
        arcs = [FSTArc(src=i, dst=i+1, input_label=char, output_label=out_char)]
        states.append(FSTState(id=i, is_start=(i==0), is_final=False, arcs=arcs))
        traversal.append(TraversalStep(state=i, input_char=char, output_char=out_char, next_state=i+1))
        
    curr_node = len(word)
    
    # If lemma is longer than input word, output remaining characters
    if len(lemma) > len(word):
        rem_lemma = lemma[len(word):]
        arcs = [FSTArc(src=curr_node, dst=curr_node+1, input_label="ε", output_label=rem_lemma)]
        states.append(FSTState(id=curr_node, is_start=False, is_final=False, arcs=arcs))
        traversal.append(TraversalStep(state=curr_node, input_char="ε", output_char=rem_lemma, next_state=curr_node+1))
        curr_node += 1
        
    # Add tags
    if tags:
        arcs = [FSTArc(src=curr_node, dst=curr_node+1, input_label="ε", output_label=tags)]
        states.append(FSTState(id=curr_node, is_start=False, is_final=False, arcs=arcs))
        traversal.append(TraversalStep(state=curr_node, input_char="ε", output_char=tags, next_state=curr_node+1))
        curr_node += 1
        
    states.append(FSTState(id=curr_node, is_start=(curr_node==0), is_final=True, arcs=[]))
    
    return FSTGraph(
        states=states,
        num_states=len(states),
        num_arcs=len(traversal),
        start_state=0,
        traversal=traversal,
    )

def _parse(raw: str) -> Analysis:
    """Split 'walk+V;PST' into lemma and features."""
    parts = raw.split("+", 1)
    return Analysis(raw=raw, lemma=parts[0], features=parts[1] if len(parts) > 1 else "")


# ══════════════════════════════════════════════════════════════════
# Language-specific analyzers
# ══════════════════════════════════════════════════════════════════

# ── English ───────────────────────────────────────────────────────

def _analyze_english(word: str) -> AnalyzeResponse:
    """English: FST first, neural fallback."""
    word = word.strip().lower()
    analyzer_fst = _state["eng_fst"]
    neural = _state["eng_neural"]

    try:
        lattice = pynini.compose(
            pynini.accep(word, token_type="utf8"),
            analyzer_fst,
        )
        if lattice.start() != pynini.NO_STATE_ID:
            analyses = sorted(set(lattice.paths(output_token_type="utf8").ostrings()))
            graph_raw = _extract_graph(lattice)
            graph_textbook = _build_textbook_graph(word, analyses[0]) if analyses else None
            return AnalyzeResponse(
                word=word, language="eng", source="FST",
                analyses=[_parse(a) for a in analyses],
                fst_graph_raw=graph_raw,
                fst_graph_textbook=graph_textbook,
            )
    except Exception:
        pass

    neural_results = neural.analyze(word)
    return AnalyzeResponse(
        word=word, language="eng", source="Neural",
        analyses=[_parse(a) for a in neural_results],
        fst_graph_raw=None,
        fst_graph_textbook=None,
    )


# ── Bengali / Hindi ──────────────────────────────────────────────

def _analyze_dict_fst(word: str, lang: str) -> AnalyzeResponse:
    """
    Bengali / Hindi: compose word with the REAL FST from their
    fst_builder.py. Graph is extracted directly from the Pynini
    lattice — no extra logic.
    Analysis tags come from the VOCABULARY dict.
    """
    word = word.strip()
    fst = _state[f"{lang}_fst"]
    vocab = _state[f"{lang}_vocab"]
    fallback_fn = _state[f"{lang}_fallback"]

    # ── Compose with the REAL FST (from fst_builder.py) ──
    graph = None
    in_fst = False
    try:
        # Use utf8 tokens — matching how fst_builder.py builds it
        lattice = pynini.compose(pynini.accep(word, token_type="utf8"), fst)
        if lattice.start() != pynini.NO_STATE_ID:
            graph_raw = _extract_graph(lattice)
            in_fst = True
    except Exception:
        pass

    # ── Get analysis from VOCABULARY dict ──
    if word in vocab:
        lex = vocab[word]
        lemma = lex["lemma"]
        upos = lex["upos"]
        feats = lex.get("feats", "_")
        raw = f"{lemma}+{upos};{feats}" if feats != "_" else f"{lemma}+{upos}"
        analyses = [_parse(raw)]
        source = "FST" if in_fst else "Dictionary"
        graph_textbook = _build_textbook_graph(word, raw)
    else:
        # Heuristic fallback for OOV
        conllu_line = fallback_fn(1, word)
        parts = conllu_line.split("\t")
        lemma = parts[2] if len(parts) > 2 else word
        upos = parts[3] if len(parts) > 3 else "X"
        feats = parts[5] if len(parts) > 5 else "_"
        raw = f"{lemma}+{upos};{feats}" if feats != "_" else f"{lemma}+{upos}"
        analyses = [_parse(raw)]
        source = "Heuristic"
        graph_textbook = None

    return AnalyzeResponse(
        word=word, language=lang, source=source,
        analyses=analyses,
        fst_graph_raw=graph_raw,
        fst_graph_textbook=graph_textbook,
    )


# ══════════════════════════════════════════════════════════════════
# App lifecycle — load all models at startup
# ══════════════════════════════════════════════════════════════════

_state = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("=" * 60)
    print("LOADING ALL LANGUAGE MODELS...")
    print("=" * 60)

    # ── English ──
    print("\n[1/3] English FST + Neural...")
    from fst_builder import build_fst
    from neural.predict import NeuralAnalyzer

    gen, ana = build_fst()
    _state["eng_fst"] = ana
    _state["eng_neural"] = NeuralAnalyzer(
        os.path.join(FSL_DIR, "neural", "checkpoints")
    )

    # ── Bengali ──
    print("\n[2/3] Bengali FST...")
    ben_fst, ben_vocab, ben_fallback = _load_lang(BEN_DIR)
    _state["ben_fst"] = ben_fst
    _state["ben_vocab"] = ben_vocab
    _state["ben_fallback"] = ben_fallback
    print(f"  Bengali FST loaded ({len(ben_vocab)} words).")

    # ── Hindi ──
    print("\n[3/3] Hindi FST...")
    hin_fst, hin_vocab, hin_fallback = _load_lang(HIN_DIR)
    _state["hin_fst"] = hin_fst
    _state["hin_vocab"] = hin_vocab
    _state["hin_fallback"] = hin_fallback
    print(f"  Hindi FST loaded ({len(hin_vocab)} words).")

    print("\n" + "=" * 60)
    print("ALL MODELS READY — eng / ben / hin")
    print("=" * 60 + "\n")

    yield
    _state.clear()


def _load_lang(directory):
    """
    Load the REAL FST, VOCABULARY, and fallback from a language directory.
    Uses exact file paths to avoid picking up the wrong module.
    """
    import importlib.util

    conflicts = ["lexicon", "analyzer", "fst_builder"]

    # Save and remove any cached versions of these module names
    saved = {}
    for name in conflicts:
        if name in sys.modules:
            saved[name] = sys.modules.pop(name)

    def _load(name):
        """Load a module by exact file path and register it in sys.modules."""
        filepath = os.path.abspath(os.path.join(directory, f"{name}.py"))
        spec = importlib.util.spec_from_file_location(name, filepath)
        mod = importlib.util.module_from_spec(spec)
        # Register BEFORE exec so internal `from X import Y` resolves correctly
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
        return mod

    try:
        lex_mod = _load("lexicon")
        ana_mod = _load("analyzer")
        fst_mod = _load("fst_builder")

        vocab = lex_mod.VOCABULARY
        fallback = ana_mod.generate_conllu_line

        # Call the REAL build function (build_bengali_fsl or build_hindi_fsl)
        build_fn = None
        for attr in dir(fst_mod):
            if attr.startswith("build_") and callable(getattr(fst_mod, attr)):
                build_fn = getattr(fst_mod, attr)
                break
        if build_fn is None:
            raise RuntimeError(f"No build_* function in {directory}/fst_builder.py")

        fst = build_fn()
    finally:
        # Clean up — remove the modules we injected
        for name in conflicts:
            sys.modules.pop(name, None)
        # Restore the originals (English modules)
        for name, mod in saved.items():
            sys.modules[name] = mod

    return fst, vocab, fallback


# ══════════════════════════════════════════════════════════════════
# FastAPI app
# ══════════════════════════════════════════════════════════════════

app = FastAPI(
    title="Pullinguistics — Multi-Language Morphological Analyzer",
    version="2.0.0",
    lifespan=lifespan,
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "languages": {
            "eng": "eng_fst" in _state,
            "ben": "ben_fst" in _state,
            "hin": "hin_fst" in _state,
        },
    }


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest):
    lang = req.language.strip().lower()
    if lang == "eng":
        return _analyze_english(req.word)
    elif lang in ("ben", "hin"):
        return _analyze_dict_fst(req.word, lang)
    else:
        return AnalyzeResponse(
            word=req.word, language=lang, source="Unknown",
            analyses=[], fst_graph=None,
        )


@app.post("/analyze/batch", response_model=list[AnalyzeResponse])
async def analyze_batch(req: BatchAnalyzeRequest):
    lang = req.language.strip().lower()
    results = []
    for w in req.words:
        if lang == "eng":
            results.append(_analyze_english(w))
        elif lang in ("ben", "hin"):
            results.append(_analyze_dict_fst(w, lang))
    return results
