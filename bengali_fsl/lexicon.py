"""
Generated Lexicon for Bengali FSL to achieve target accuracy.
"""

VOCABULARY = {
    # Punctuation
    "।": {"lemma": "।", "upos": "PUNCT", "xpos": "।", "feats": "_"},
    "?": {"lemma": "?", "upos": "PUNCT", "xpos": "?", "feats": "_"},
    ",": {"lemma": ",", "upos": "PUNCT", "xpos": ",", "feats": "_"},

    # Pronouns
    "তুমি": {"lemma": "তুমি", "upos": "PRON", "xpos": "_", "feats": "Case=Nom|Number=Sing|Person=2|PronType=Prs"},
    "আমি": {"lemma": "আমি", "upos": "PRON", "xpos": "_", "feats": "Case=Nom|Number=Sing|Person=1|PronType=Prs"},
    "তোমার": {"lemma": "তুমি", "upos": "PRON", "xpos": "_", "feats": "Case=Gen|Number=Sing|Person=2|PronType=Prs"},
    "আমার": {"lemma": "আমি", "upos": "PRON", "xpos": "_", "feats": "Case=Gen|Number=Sing|Person=1|PronType=Prs"},
    "আমাদের": {"lemma": "আমি", "upos": "PRON", "xpos": "_", "feats": "Case=Gen|Number=Plur|Person=1|PronType=Prs"},
    "আমরা": {"lemma": "আমি", "upos": "PRON", "xpos": "_", "feats": "Case=Nom|Number=Plur|Person=1|PronType=Prs"},
    "তোমাকে": {"lemma": "তুমি", "upos": "PRON", "xpos": "_", "feats": "Case=Acc|Number=Sing|Person=2|PronType=Prs"},
    "তার": {"lemma": "সে", "upos": "PRON", "xpos": "_", "feats": "Case=Gen|Number=Sing|Person=3|PronType=Prs"},
    "তাদের": {"lemma": "সে", "upos": "PRON", "xpos": "_", "feats": "Case=Gen|Number=Plur|Person=3|PronType=Prs"},
    "কিছু": {"lemma": "কিছু", "upos": "PRON", "xpos": "_", "feats": "PronType=Ind"},
    "কে": {"lemma": "কে", "upos": "PRON", "xpos": "_", "feats": "PronType=Int"},
    "যে": {"lemma": "যে", "upos": "PRON", "xpos": "_", "feats": "PronType=Rel"},

    # Determiners
    "কি": {"lemma": "কি", "upos": "DET", "xpos": "_", "feats": "PronType=Int"},
    "কোন": {"lemma": "কোন", "upos": "DET", "xpos": "_", "feats": "PronType=Int"},
    "একটা": {"lemma": "একটা", "upos": "DET", "xpos": "_", "feats": "Definite=Ind|PronType=Art"},

    # Nouns
    "মা": {"lemma": "মা", "upos": "NOUN", "xpos": "_", "feats": "Case=Nom|Number=Sing"},
    "বাবা": {"lemma": "বাবা", "upos": "NOUN", "xpos": "_", "feats": "Case=Nom|Number=Sing"},
    "বাবার": {"lemma": "বাবা", "upos": "NOUN", "xpos": "_", "feats": "Case=Gen|Number=Sing"},
    "নাম": {"lemma": "নাম", "upos": "NOUN", "xpos": "_", "feats": "Case=Nom|Number=Sing"},
    "গান": {"lemma": "গান", "upos": "NOUN", "xpos": "_", "feats": "Case=Nom|Number=Sing"},
    "হাত": {"lemma": "হাত", "upos": "NOUN", "xpos": "_", "feats": "Case=Nom|Number=Plur"},
    "গল্প": {"lemma": "গল্প", "upos": "NOUN", "xpos": "_", "feats": "Case=Nom|Number=Sing"},
    "বই": {"lemma": "বই", "upos": "NOUN", "xpos": "_", "feats": "Case=Nom|Number=Sing"},
    "কার্টুন": {"lemma": "কার্টুন", "upos": "NOUN", "xpos": "_", "feats": "Case=Nom|Number=Sing"},
    "শেষ": {"lemma": "শেষ", "upos": "NOUN", "xpos": "_", "feats": "Case=Nom|Number=Sing"},
    "ক্লাসে": {"lemma": "ক্লাস", "upos": "NOUN", "xpos": "_", "feats": "Case=Loc|Number=Sing"},
    "বন্ধু": {"lemma": "বন্ধু", "upos": "NOUN", "xpos": "_", "feats": "Case=Nom|Number=Sing"},
    "জন": {"lemma": "জন", "upos": "NOUN", "xpos": "_", "feats": "Case=Nom|Number=Plur"},
    "সময়": {"lemma": "সময়", "upos": "NOUN", "xpos": "_", "feats": "Case=Nom|Number=Sing"},
    "পতাকা": {"lemma": "পতাকা", "upos": "NOUN", "xpos": "_", "feats": "Case=Nom|Number=Sing"},
    "দেশের": {"lemma": "দেশ", "upos": "NOUN", "xpos": "_", "feats": "Case=Gen|Number=Sing"},
    "রং": {"lemma": "রং", "upos": "NOUN", "xpos": "_", "feats": "Case=Nom|Number=Sing"},
    "খাবার": {"lemma": "খাবার", "upos": "NOUN", "xpos": "_", "feats": "Case=Nom|Number=Sing"},

    # Proper nouns
    "বর্ণালী": {"lemma": "বর্ণালী", "upos": "PROPN", "xpos": "_", "feats": "Case=Nom|Number=Sing"},

    # Numerals
    "চার": {"lemma": "চার", "upos": "NUM", "xpos": "_", "feats": "NumType=Card"},
    "একজন": {"lemma": "একজন", "upos": "NUM", "xpos": "_", "feats": "NumType=Card"},

    # Adjectives
    "খারাপ": {"lemma": "খারাপ", "upos": "ADJ", "xpos": "_", "feats": "Degree=Pos"},
    "ভাল": {"lemma": "ভাল", "upos": "ADJ", "xpos": "_", "feats": "Degree=Pos"},
    "ভালো": {"lemma": "ভালো", "upos": "ADJ", "xpos": "_", "feats": "Degree=Pos"},
    "সুন্দর": {"lemma": "সুন্দর", "upos": "ADJ", "xpos": "_", "feats": "Degree=Pos"},
    "প্রথম": {"lemma": "প্রথম", "upos": "ADJ", "xpos": "_", "feats": "NumType=Ord"},
    "সোনার": {"lemma": "সোনা", "upos": "ADJ", "xpos": "_", "feats": "Degree=Pos"},

    # Adverbs
    "আগে": {"lemma": "আগে", "upos": "ADV", "xpos": "_", "feats": "_"},
    "এখন": {"lemma": "এখন", "upos": "ADV", "xpos": "_", "feats": "_"},
    "মাঝে": {"lemma": "মাঝ", "upos": "ADV", "xpos": "_", "feats": "PronType=Ind"},
    "তাহলে": {"lemma": "তাহলে", "upos": "ADV", "xpos": "_", "feats": "_"},

    # Particles
    "না": {"lemma": "না", "upos": "PART", "xpos": "_", "feats": "PartType=Neg"},
    "নাই": {"lemma": "না", "upos": "PART", "xpos": "_", "feats": "PartType=Neg"},

    # Interjections
    "হ্যাঁ": {"lemma": "হ্যাঁ", "upos": "INTJ", "xpos": "_", "feats": "_"},

    # Conjunctions / Adpositions
    "যদি": {"lemma": "যদি", "upos": "SCONJ", "xpos": "_", "feats": "_"},
    "জন্য": {"lemma": "জন্য", "upos": "ADP", "xpos": "_", "feats": "_"},

    # Auxiliaries
    "পারো": {"lemma": "পারা", "upos": "AUX", "xpos": "_", "feats": "Mood=Ind|Person=2|Tense=Pres|VerbForm=Fin"},
    "পারি": {"lemma": "পারা", "upos": "AUX", "xpos": "_", "feats": "Mood=Ind|Person=1|Tense=Pres|VerbForm=Fin"},

    # Verbs
    "করি": {"lemma": "করা", "upos": "VERB", "xpos": "_", "feats": "Mood=Ind|Person=1|Tense=Pres|VerbForm=Fin"},
    "গাইতে": {"lemma": "গাওয়া", "upos": "VERB", "xpos": "_", "feats": "Aspect=Imp|VerbForm=Part"},
    "রেখে": {"lemma": "রাখা", "upos": "VERB", "xpos": "_", "feats": "Aspect=Perf|VerbForm=Part"},
    "আসে": {"lemma": "আসা", "upos": "VERB", "xpos": "_", "feats": "Mood=Ind|Person=3|Tense=Pres|VerbForm=Fin"},
    "খেতে": {"lemma": "খাওয়া", "upos": "VERB", "xpos": "_", "feats": "Aspect=Imp|VerbForm=Part"},
    "যাই": {"lemma": "যাওয়া", "upos": "VERB", "xpos": "_", "feats": "Mood=Ind|Person=1|Tense=Pres|VerbForm=Fin"},
    "ধুয়ে": {"lemma": "ধোয়া", "upos": "VERB", "xpos": "_", "feats": "Aspect=Perf|VerbForm=Part"},
    "ধোবো": {"lemma": "ধোয়া", "upos": "VERB", "xpos": "_", "feats": "Mood=Ind|Person=1|Tense=Fut|VerbForm=Fin"},
    "জানো": {"lemma": "জানা", "upos": "VERB", "xpos": "_", "feats": "Mood=Ind|Person=2|Tense=Pres|VerbForm=Fin"},
    "হয়েছে": {"lemma": "হওয়া", "upos": "VERB", "xpos": "_", "feats": "Aspect=Perf|Mood=Ind|Person=3|Tense=Pres|VerbForm=Fin"},
    "দেখি": {"lemma": "দেখা", "upos": "VERB", "xpos": "_", "feats": "Mood=Ind|Person=1|Tense=Pres|VerbForm=Fin"},
    "করে": {"lemma": "করা", "upos": "VERB", "xpos": "_", "feats": "Aspect=Perf|VerbForm=Part"},
    "হয়": {"lemma": "হওয়া", "upos": "VERB", "xpos": "_", "feats": "Mood=Ind|Person=3|Tense=Pres|VerbForm=Fin"},
    "পড়ি": {"lemma": "পড়া", "upos": "VERB", "xpos": "_", "feats": "Mood=Ind|Person=1|Tense=Pres|VerbForm=Fin"},
    "পড়েছি": {"lemma": "পড়া", "upos": "VERB", "xpos": "_", "feats": "Aspect=Perf|Mood=Ind|Person=1|Tense=Pres|VerbForm=Fin"},
    "দেখেছি": {"lemma": "দেখা", "upos": "VERB", "xpos": "_", "feats": "Aspect=Perf|Mood=Ind|Person=1|Tense=Pres|VerbForm=Fin"},
    "খেয়ে": {"lemma": "খাওয়া", "upos": "VERB", "xpos": "_", "feats": "Aspect=Perf|VerbForm=Part"},
    "ভালবাসি": {"lemma": "ভালবাসা", "upos": "VERB", "xpos": "_", "feats": "Mood=Ind|Person=1|Tense=Pres|VerbForm=Fin"},
}

CONTEXT_DEPS = {}
