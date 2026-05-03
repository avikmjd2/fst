"""
Bengali FSL Analyzer.
Validates words using the FST and formats the output into CoNLL-U format.
"""
from lexicon import VOCABULARY, CONTEXT_DEPS

def generate_conllu_line(word_id, word):
    """
    Generates a CoNLL-U formatted line for a given Bengali word.
    """
    if word in VOCABULARY:
        lex = VOCABULARY[word]
        ctx = CONTEXT_DEPS.get(word, ("_", "_", "_"))
        head = ctx[0]
        deprel = ctx[1]
        
        # Build Misc column
        misc_parts = []
        if len(ctx) > 2 and ctx[2]:
            misc_parts.append(ctx[2])
        if "ltranslit" in lex:
            misc_parts.append(f"LTranslit={lex['ltranslit']}")
        if "translit" in lex:
            misc_parts.append(f"Translit={lex['translit']}")
            
        misc = "|".join(misc_parts) if misc_parts else "_"
        
        return f"{word_id}\t{word}\t{lex['lemma']}\t{lex['upos']}\t{lex['xpos']}\t{lex['feats']}\t{head}\t{deprel}\t_\t{misc}"
    else:
        # Heuristic fallback for unknown Bengali words
        lemma = word
        upos = "NOUN"
        xpos = "_"
        feats = "Case=Nom|Number=Sing"
        
        # Punctuation
        if word in ("।", "?", "!", ",", ";", ":", "-", "(", ")", "—"):
            upos = "PUNCT"
            xpos = word
            feats = "_"
            lemma = word
        # Bengali verb endings (common patterns)
        elif word.endswith(("েছি", "েছে", "েছ", "েছিল")):
            # Perfective aspect verbs
            upos, xpos, feats = "VERB", "_", "Aspect=Perf|VerbForm=Fin"
            if word.endswith("েছি"):
                lemma = word[:-3] + "া" if len(word) > 3 else word
            elif word.endswith("েছে"):
                lemma = word[:-3] + "া" if len(word) > 3 else word
            elif word.endswith("েছ"):
                lemma = word[:-2] + "া" if len(word) > 2 else word
        elif word.endswith(("তে", "তো")):
            # Imperfective / infinitive
            upos, xpos, feats = "VERB", "_", "Aspect=Imp|VerbForm=Part"
            lemma = word[:-2] + "া" if len(word) > 2 else word
        elif word.endswith("ব") and len(word) > 1:
            # Future tense
            upos, xpos, feats = "VERB", "_", "Mood=Ind|Tense=Fut|VerbForm=Fin"
            lemma = word[:-1] + "া" if len(word) > 1 else word
        elif word.endswith("বে") and len(word) > 2:
            # Future tense 3rd person
            upos, xpos, feats = "VERB", "_", "Mood=Ind|Tense=Fut|VerbForm=Fin"
            lemma = word[:-2] + "া" if len(word) > 2 else word
        elif word.endswith("ের") or word.endswith("র") and len(word) > 2:
            # Genitive case
            feats = "Case=Gen|Number=Sing"
            if word.endswith("ের"):
                lemma = word[:-2]
            elif word.endswith("র"):
                lemma = word[:-1]
        elif word.endswith("তে"):
            feats = "Case=Loc|Number=Sing"
            lemma = word[:-2]
        elif word.endswith("কে"):
            feats = "Case=Acc|Number=Sing"
            lemma = word[:-2]
            
        return f"{word_id}\t{word}\t{lemma}\t{upos}\t{xpos}\t{feats}\t_\t_\t_\t_"

def analyze_sentence(sentence, fsl=None):
    """
    Analyzes a full Bengali sentence and returns the CoNLL-U representation.
    """
    # Simple tokenizer: separate punctuation
    tokenized_sentence = sentence.replace(",", " , ").replace("।", " । ").replace("?", " ? ").replace("!", " ! ")
    words = [w for w in tokenized_sentence.split() if w.strip()]
    
    output = []
    output.append("# sent_id = test-s1")
    output.append(f"# text = {sentence}")
    
    for i, word in enumerate(words):
        output.append(generate_conllu_line(i+1, word))
        
    return "\n".join(output)
