"""
Irregular forms: direct mappings for words that don't follow regular rules.
Format: (analysis_string, surface_form)

Analysis format follows UniMorph conventions:
  lemma+POS;FEATURE;FEATURE
"""

# =============================================================================
# IRREGULAR VERBS (top 60+ most common)
# =============================================================================
# Format: ("lemma+V;FEATURES", "surface_form")
IRREGULAR_VERBS = [
    # --- be ---
    ("be+V;NFIN", "be"),
    ("be+V;PRS;1;SG", "am"),
    ("be+V;PRS;3;SG", "is"),
    ("be+V;PRS;2", "are"),
    ("be+V;PRS;1;PL", "are"),
    ("be+V;PRS;3;PL", "are"),
    ("be+V;PST;1;SG", "was"),
    ("be+V;PST;3;SG", "was"),
    ("be+V;PST;2", "were"),
    ("be+V;PST;1;PL", "were"),
    ("be+V;PST;3;PL", "were"),
    ("be+V;V.PTCP;PRS", "being"),
    ("be+V;V.PTCP;PST", "been"),
    # --- have ---
    ("have+V;NFIN", "have"),
    ("have+V;PRS;3;SG", "has"),
    ("have+V;PST", "had"),
    ("have+V;V.PTCP;PRS", "having"),
    ("have+V;V.PTCP;PST", "had"),
    # --- do ---
    ("do+V;NFIN", "do"),
    ("do+V;PRS;3;SG", "does"),
    ("do+V;PST", "did"),
    ("do+V;V.PTCP;PRS", "doing"),
    ("do+V;V.PTCP;PST", "done"),
    # --- say ---
    ("say+V;NFIN", "say"),
    ("say+V;PRS;3;SG", "says"),
    ("say+V;PST", "said"),
    ("say+V;V.PTCP;PRS", "saying"),
    ("say+V;V.PTCP;PST", "said"),
    # --- go ---
    ("go+V;NFIN", "go"),
    ("go+V;PRS;3;SG", "goes"),
    ("go+V;PST", "went"),
    ("go+V;V.PTCP;PRS", "going"),
    ("go+V;V.PTCP;PST", "gone"),
    # --- get ---
    ("get+V;NFIN", "get"),
    ("get+V;PRS;3;SG", "gets"),
    ("get+V;PST", "got"),
    ("get+V;V.PTCP;PRS", "getting"),
    ("get+V;V.PTCP;PST", "gotten"),
    # --- make ---
    ("make+V;NFIN", "make"),
    ("make+V;PRS;3;SG", "makes"),
    ("make+V;PST", "made"),
    ("make+V;V.PTCP;PRS", "making"),
    ("make+V;V.PTCP;PST", "made"),
    # --- know ---
    ("know+V;NFIN", "know"),
    ("know+V;PRS;3;SG", "knows"),
    ("know+V;PST", "knew"),
    ("know+V;V.PTCP;PRS", "knowing"),
    ("know+V;V.PTCP;PST", "known"),
    # --- think ---
    ("think+V;NFIN", "think"),
    ("think+V;PRS;3;SG", "thinks"),
    ("think+V;PST", "thought"),
    ("think+V;V.PTCP;PRS", "thinking"),
    ("think+V;V.PTCP;PST", "thought"),
    # --- take ---
    ("take+V;NFIN", "take"),
    ("take+V;PRS;3;SG", "takes"),
    ("take+V;PST", "took"),
    ("take+V;V.PTCP;PRS", "taking"),
    ("take+V;V.PTCP;PST", "taken"),
    # --- see ---
    ("see+V;NFIN", "see"),
    ("see+V;PRS;3;SG", "sees"),
    ("see+V;PST", "saw"),
    ("see+V;V.PTCP;PRS", "seeing"),
    ("see+V;V.PTCP;PST", "seen"),
    # --- come ---
    ("come+V;NFIN", "come"),
    ("come+V;PRS;3;SG", "comes"),
    ("come+V;PST", "came"),
    ("come+V;V.PTCP;PRS", "coming"),
    ("come+V;V.PTCP;PST", "come"),
    # --- find ---
    ("find+V;NFIN", "find"),
    ("find+V;PRS;3;SG", "finds"),
    ("find+V;PST", "found"),
    ("find+V;V.PTCP;PRS", "finding"),
    ("find+V;V.PTCP;PST", "found"),
    # --- give ---
    ("give+V;NFIN", "give"),
    ("give+V;PRS;3;SG", "gives"),
    ("give+V;PST", "gave"),
    ("give+V;V.PTCP;PRS", "giving"),
    ("give+V;V.PTCP;PST", "given"),
    # --- tell ---
    ("tell+V;NFIN", "tell"),
    ("tell+V;PRS;3;SG", "tells"),
    ("tell+V;PST", "told"),
    ("tell+V;V.PTCP;PRS", "telling"),
    ("tell+V;V.PTCP;PST", "told"),
    # --- feel ---
    ("feel+V;NFIN", "feel"),
    ("feel+V;PRS;3;SG", "feels"),
    ("feel+V;PST", "felt"),
    ("feel+V;V.PTCP;PRS", "feeling"),
    ("feel+V;V.PTCP;PST", "felt"),
    # --- become ---
    ("become+V;NFIN", "become"),
    ("become+V;PRS;3;SG", "becomes"),
    ("become+V;PST", "became"),
    ("become+V;V.PTCP;PRS", "becoming"),
    ("become+V;V.PTCP;PST", "become"),
    # --- leave ---
    ("leave+V;NFIN", "leave"),
    ("leave+V;PRS;3;SG", "leaves"),
    ("leave+V;PST", "left"),
    ("leave+V;V.PTCP;PRS", "leaving"),
    ("leave+V;V.PTCP;PST", "left"),
    # --- put ---
    ("put+V;NFIN", "put"),
    ("put+V;PRS;3;SG", "puts"),
    ("put+V;PST", "put"),
    ("put+V;V.PTCP;PRS", "putting"),
    ("put+V;V.PTCP;PST", "put"),
    # --- mean ---
    ("mean+V;NFIN", "mean"),
    ("mean+V;PRS;3;SG", "means"),
    ("mean+V;PST", "meant"),
    ("mean+V;V.PTCP;PRS", "meaning"),
    ("mean+V;V.PTCP;PST", "meant"),
    # --- keep ---
    ("keep+V;NFIN", "keep"),
    ("keep+V;PRS;3;SG", "keeps"),
    ("keep+V;PST", "kept"),
    ("keep+V;V.PTCP;PRS", "keeping"),
    ("keep+V;V.PTCP;PST", "kept"),
    # --- let ---
    ("let+V;NFIN", "let"),
    ("let+V;PRS;3;SG", "lets"),
    ("let+V;PST", "let"),
    ("let+V;V.PTCP;PRS", "letting"),
    ("let+V;V.PTCP;PST", "let"),
    # --- begin ---
    ("begin+V;NFIN", "begin"),
    ("begin+V;PRS;3;SG", "begins"),
    ("begin+V;PST", "began"),
    ("begin+V;V.PTCP;PRS", "beginning"),
    ("begin+V;V.PTCP;PST", "begun"),
    # --- hear ---
    ("hear+V;NFIN", "hear"),
    ("hear+V;PRS;3;SG", "hears"),
    ("hear+V;PST", "heard"),
    ("hear+V;V.PTCP;PRS", "hearing"),
    ("hear+V;V.PTCP;PST", "heard"),
    # --- run ---
    ("run+V;NFIN", "run"),
    ("run+V;PRS;3;SG", "runs"),
    ("run+V;PST", "ran"),
    ("run+V;V.PTCP;PRS", "running"),
    ("run+V;V.PTCP;PST", "run"),
    # --- hold ---
    ("hold+V;NFIN", "hold"),
    ("hold+V;PRS;3;SG", "holds"),
    ("hold+V;PST", "held"),
    ("hold+V;V.PTCP;PRS", "holding"),
    ("hold+V;V.PTCP;PST", "held"),
    # --- bring ---
    ("bring+V;NFIN", "bring"),
    ("bring+V;PRS;3;SG", "brings"),
    ("bring+V;PST", "brought"),
    ("bring+V;V.PTCP;PRS", "bringing"),
    ("bring+V;V.PTCP;PST", "brought"),
    # --- write ---
    ("write+V;NFIN", "write"),
    ("write+V;PRS;3;SG", "writes"),
    ("write+V;PST", "wrote"),
    ("write+V;V.PTCP;PRS", "writing"),
    ("write+V;V.PTCP;PST", "written"),
    # --- sit ---
    ("sit+V;NFIN", "sit"),
    ("sit+V;PRS;3;SG", "sits"),
    ("sit+V;PST", "sat"),
    ("sit+V;V.PTCP;PRS", "sitting"),
    ("sit+V;V.PTCP;PST", "sat"),
    # --- stand ---
    ("stand+V;NFIN", "stand"),
    ("stand+V;PRS;3;SG", "stands"),
    ("stand+V;PST", "stood"),
    ("stand+V;V.PTCP;PRS", "standing"),
    ("stand+V;V.PTCP;PST", "stood"),
    # --- lose ---
    ("lose+V;NFIN", "lose"),
    ("lose+V;PRS;3;SG", "loses"),
    ("lose+V;PST", "lost"),
    ("lose+V;V.PTCP;PRS", "losing"),
    ("lose+V;V.PTCP;PST", "lost"),
    # --- pay ---
    ("pay+V;NFIN", "pay"),
    ("pay+V;PRS;3;SG", "pays"),
    ("pay+V;PST", "paid"),
    ("pay+V;V.PTCP;PRS", "paying"),
    ("pay+V;V.PTCP;PST", "paid"),
    # --- meet ---
    ("meet+V;NFIN", "meet"),
    ("meet+V;PRS;3;SG", "meets"),
    ("meet+V;PST", "met"),
    ("meet+V;V.PTCP;PRS", "meeting"),
    ("meet+V;V.PTCP;PST", "met"),
    # --- lead ---
    ("lead+V;NFIN", "lead"),
    ("lead+V;PRS;3;SG", "leads"),
    ("lead+V;PST", "led"),
    ("lead+V;V.PTCP;PRS", "leading"),
    ("lead+V;V.PTCP;PST", "led"),
    # --- understand ---
    ("understand+V;NFIN", "understand"),
    ("understand+V;PRS;3;SG", "understands"),
    ("understand+V;PST", "understood"),
    ("understand+V;V.PTCP;PRS", "understanding"),
    ("understand+V;V.PTCP;PST", "understood"),
    # --- set ---
    ("set+V;NFIN", "set"),
    ("set+V;PRS;3;SG", "sets"),
    ("set+V;PST", "set"),
    ("set+V;V.PTCP;PRS", "setting"),
    ("set+V;V.PTCP;PST", "set"),
    # --- grow ---
    ("grow+V;NFIN", "grow"),
    ("grow+V;PRS;3;SG", "grows"),
    ("grow+V;PST", "grew"),
    ("grow+V;V.PTCP;PRS", "growing"),
    ("grow+V;V.PTCP;PST", "grown"),
    # --- read ---
    ("read+V;NFIN", "read"),
    ("read+V;PRS;3;SG", "reads"),
    ("read+V;PST", "read"),
    ("read+V;V.PTCP;PRS", "reading"),
    ("read+V;V.PTCP;PST", "read"),
    # --- spend ---
    ("spend+V;NFIN", "spend"),
    ("spend+V;PRS;3;SG", "spends"),
    ("spend+V;PST", "spent"),
    ("spend+V;V.PTCP;PRS", "spending"),
    ("spend+V;V.PTCP;PST", "spent"),
    # --- win ---
    ("win+V;NFIN", "win"),
    ("win+V;PRS;3;SG", "wins"),
    ("win+V;PST", "won"),
    ("win+V;V.PTCP;PRS", "winning"),
    ("win+V;V.PTCP;PST", "won"),
    # --- build ---
    ("build+V;NFIN", "build"),
    ("build+V;PRS;3;SG", "builds"),
    ("build+V;PST", "built"),
    ("build+V;V.PTCP;PRS", "building"),
    ("build+V;V.PTCP;PST", "built"),
    # --- fall ---
    ("fall+V;NFIN", "fall"),
    ("fall+V;PRS;3;SG", "falls"),
    ("fall+V;PST", "fell"),
    ("fall+V;V.PTCP;PRS", "falling"),
    ("fall+V;V.PTCP;PST", "fallen"),
    # --- cut ---
    ("cut+V;NFIN", "cut"),
    ("cut+V;PRS;3;SG", "cuts"),
    ("cut+V;PST", "cut"),
    ("cut+V;V.PTCP;PRS", "cutting"),
    ("cut+V;V.PTCP;PST", "cut"),
    # --- buy ---
    ("buy+V;NFIN", "buy"),
    ("buy+V;PRS;3;SG", "buys"),
    ("buy+V;PST", "bought"),
    ("buy+V;V.PTCP;PRS", "buying"),
    ("buy+V;V.PTCP;PST", "bought"),
    # --- send ---
    ("send+V;NFIN", "send"),
    ("send+V;PRS;3;SG", "sends"),
    ("send+V;PST", "sent"),
    ("send+V;V.PTCP;PRS", "sending"),
    ("send+V;V.PTCP;PST", "sent"),
    # --- rise ---
    ("rise+V;NFIN", "rise"),
    ("rise+V;PRS;3;SG", "rises"),
    ("rise+V;PST", "rose"),
    ("rise+V;V.PTCP;PRS", "rising"),
    ("rise+V;V.PTCP;PST", "risen"),
    # --- speak ---
    ("speak+V;NFIN", "speak"),
    ("speak+V;PRS;3;SG", "speaks"),
    ("speak+V;PST", "spoke"),
    ("speak+V;V.PTCP;PRS", "speaking"),
    ("speak+V;V.PTCP;PST", "spoken"),
    # --- draw ---
    ("draw+V;NFIN", "draw"),
    ("draw+V;PRS;3;SG", "draws"),
    ("draw+V;PST", "drew"),
    ("draw+V;V.PTCP;PRS", "drawing"),
    ("draw+V;V.PTCP;PST", "drawn"),
    # --- break ---
    ("break+V;NFIN", "break"),
    ("break+V;PRS;3;SG", "breaks"),
    ("break+V;PST", "broke"),
    ("break+V;V.PTCP;PRS", "breaking"),
    ("break+V;V.PTCP;PST", "broken"),
    # --- drive ---
    ("drive+V;NFIN", "drive"),
    ("drive+V;PRS;3;SG", "drives"),
    ("drive+V;PST", "drove"),
    ("drive+V;V.PTCP;PRS", "driving"),
    ("drive+V;V.PTCP;PST", "driven"),
    # --- eat ---
    ("eat+V;NFIN", "eat"),
    ("eat+V;PRS;3;SG", "eats"),
    ("eat+V;PST", "ate"),
    ("eat+V;V.PTCP;PRS", "eating"),
    ("eat+V;V.PTCP;PST", "eaten"),
    # --- drink ---
    ("drink+V;NFIN", "drink"),
    ("drink+V;PRS;3;SG", "drinks"),
    ("drink+V;PST", "drank"),
    ("drink+V;V.PTCP;PRS", "drinking"),
    ("drink+V;V.PTCP;PST", "drunk"),
    # --- fly ---
    ("fly+V;NFIN", "fly"),
    ("fly+V;PRS;3;SG", "flies"),
    ("fly+V;PST", "flew"),
    ("fly+V;V.PTCP;PRS", "flying"),
    ("fly+V;V.PTCP;PST", "flown"),
    # --- sing ---
    ("sing+V;NFIN", "sing"),
    ("sing+V;PRS;3;SG", "sings"),
    ("sing+V;PST", "sang"),
    ("sing+V;V.PTCP;PRS", "singing"),
    ("sing+V;V.PTCP;PST", "sung"),
    # --- swim ---
    ("swim+V;NFIN", "swim"),
    ("swim+V;PRS;3;SG", "swims"),
    ("swim+V;PST", "swam"),
    ("swim+V;V.PTCP;PRS", "swimming"),
    ("swim+V;V.PTCP;PST", "swum"),
    # --- ring ---
    ("ring+V;NFIN", "ring"),
    ("ring+V;PRS;3;SG", "rings"),
    ("ring+V;PST", "rang"),
    ("ring+V;V.PTCP;PRS", "ringing"),
    ("ring+V;V.PTCP;PST", "rung"),
    # --- sleep ---
    ("sleep+V;NFIN", "sleep"),
    ("sleep+V;PRS;3;SG", "sleeps"),
    ("sleep+V;PST", "slept"),
    ("sleep+V;V.PTCP;PRS", "sleeping"),
    ("sleep+V;V.PTCP;PST", "slept"),
    # --- wear ---
    ("wear+V;NFIN", "wear"),
    ("wear+V;PRS;3;SG", "wears"),
    ("wear+V;PST", "wore"),
    ("wear+V;V.PTCP;PRS", "wearing"),
    ("wear+V;V.PTCP;PST", "worn"),
    # --- teach ---
    ("teach+V;NFIN", "teach"),
    ("teach+V;PRS;3;SG", "teaches"),
    ("teach+V;PST", "taught"),
    ("teach+V;V.PTCP;PRS", "teaching"),
    ("teach+V;V.PTCP;PST", "taught"),
    # --- catch ---
    ("catch+V;NFIN", "catch"),
    ("catch+V;PRS;3;SG", "catches"),
    ("catch+V;PST", "caught"),
    ("catch+V;V.PTCP;PRS", "catching"),
    ("catch+V;V.PTCP;PST", "caught"),
    # --- throw ---
    ("throw+V;NFIN", "throw"),
    ("throw+V;PRS;3;SG", "throws"),
    ("throw+V;PST", "threw"),
    ("throw+V;V.PTCP;PRS", "throwing"),
    ("throw+V;V.PTCP;PST", "thrown"),
    # --- choose ---
    ("choose+V;NFIN", "choose"),
    ("choose+V;PRS;3;SG", "chooses"),
    ("choose+V;PST", "chose"),
    ("choose+V;V.PTCP;PRS", "choosing"),
    ("choose+V;V.PTCP;PST", "chosen"),
    # --- fight ---
    ("fight+V;NFIN", "fight"),
    ("fight+V;PRS;3;SG", "fights"),
    ("fight+V;PST", "fought"),
    ("fight+V;V.PTCP;PRS", "fighting"),
    ("fight+V;V.PTCP;PST", "fought"),
    # --- forget ---
    ("forget+V;NFIN", "forget"),
    ("forget+V;PRS;3;SG", "forgets"),
    ("forget+V;PST", "forgot"),
    ("forget+V;V.PTCP;PRS", "forgetting"),
    ("forget+V;V.PTCP;PST", "forgotten"),
    # --- sell ---
    ("sell+V;NFIN", "sell"),
    ("sell+V;PRS;3;SG", "sells"),
    ("sell+V;PST", "sold"),
    ("sell+V;V.PTCP;PRS", "selling"),
    ("sell+V;V.PTCP;PST", "sold"),
    # --- blow ---
    ("blow+V;NFIN", "blow"),
    ("blow+V;PRS;3;SG", "blows"),
    ("blow+V;PST", "blew"),
    ("blow+V;V.PTCP;PRS", "blowing"),
    ("blow+V;V.PTCP;PST", "blown"),
    # --- lie (recline) ---
    ("lie+V;NFIN", "lie"),
    ("lie+V;PRS;3;SG", "lies"),
    ("lie+V;PST", "lay"),
    ("lie+V;V.PTCP;PRS", "lying"),
    ("lie+V;V.PTCP;PST", "lain"),
    # --- shake ---
    ("shake+V;NFIN", "shake"),
    ("shake+V;PRS;3;SG", "shakes"),
    ("shake+V;PST", "shook"),
    ("shake+V;V.PTCP;PRS", "shaking"),
    ("shake+V;V.PTCP;PST", "shaken"),
    # --- bite ---
    ("bite+V;NFIN", "bite"),
    ("bite+V;PRS;3;SG", "bites"),
    ("bite+V;PST", "bit"),
    ("bite+V;V.PTCP;PRS", "biting"),
    ("bite+V;V.PTCP;PST", "bitten"),
    # --- hide ---
    ("hide+V;NFIN", "hide"),
    ("hide+V;PRS;3;SG", "hides"),
    ("hide+V;PST", "hid"),
    ("hide+V;V.PTCP;PRS", "hiding"),
    ("hide+V;V.PTCP;PST", "hidden"),
    # --- feed ---
    ("feed+V;NFIN", "feed"),
    ("feed+V;PRS;3;SG", "feeds"),
    ("feed+V;PST", "fed"),
    ("feed+V;V.PTCP;PRS", "feeding"),
    ("feed+V;V.PTCP;PST", "fed"),
    # --- shoot ---
    ("shoot+V;NFIN", "shoot"),
    ("shoot+V;PRS;3;SG", "shoots"),
    ("shoot+V;PST", "shot"),
    ("shoot+V;V.PTCP;PRS", "shooting"),
    ("shoot+V;V.PTCP;PST", "shot"),
    # --- freeze ---
    ("freeze+V;NFIN", "freeze"),
    ("freeze+V;PRS;3;SG", "freezes"),
    ("freeze+V;PST", "froze"),
    ("freeze+V;V.PTCP;PRS", "freezing"),
    ("freeze+V;V.PTCP;PST", "frozen"),
    # --- steal ---
    ("steal+V;NFIN", "steal"),
    ("steal+V;PRS;3;SG", "steals"),
    ("steal+V;PST", "stole"),
    ("steal+V;V.PTCP;PRS", "stealing"),
    ("steal+V;V.PTCP;PST", "stolen"),
    # --- dig ---
    ("dig+V;NFIN", "dig"),
    ("dig+V;PRS;3;SG", "digs"),
    ("dig+V;PST", "dug"),
    ("dig+V;V.PTCP;PRS", "digging"),
    ("dig+V;V.PTCP;PST", "dug"),
    # --- wake ---
    ("wake+V;NFIN", "wake"),
    ("wake+V;PRS;3;SG", "wakes"),
    ("wake+V;PST", "woke"),
    ("wake+V;V.PTCP;PRS", "waking"),
    ("wake+V;V.PTCP;PST", "woken"),
    # --- hang ---
    ("hang+V;NFIN", "hang"),
    ("hang+V;PRS;3;SG", "hangs"),
    ("hang+V;PST", "hung"),
    ("hang+V;V.PTCP;PRS", "hanging"),
    ("hang+V;V.PTCP;PST", "hung"),
    # --- sweep ---
    ("sweep+V;NFIN", "sweep"),
    ("sweep+V;PRS;3;SG", "sweeps"),
    ("sweep+V;PST", "swept"),
    ("sweep+V;V.PTCP;PRS", "sweeping"),
    ("sweep+V;V.PTCP;PST", "swept"),
    # --- stick ---
    ("stick+V;NFIN", "stick"),
    ("stick+V;PRS;3;SG", "sticks"),
    ("stick+V;PST", "stuck"),
    ("stick+V;V.PTCP;PRS", "sticking"),
    ("stick+V;V.PTCP;PST", "stuck"),
    # --- strike ---
    ("strike+V;NFIN", "strike"),
    ("strike+V;PRS;3;SG", "strikes"),
    ("strike+V;PST", "struck"),
    ("strike+V;V.PTCP;PRS", "striking"),
    ("strike+V;V.PTCP;PST", "struck"),
    # --- shine ---
    ("shine+V;NFIN", "shine"),
    ("shine+V;PRS;3;SG", "shines"),
    ("shine+V;PST", "shone"),
    ("shine+V;V.PTCP;PRS", "shining"),
    ("shine+V;V.PTCP;PST", "shone"),
    # --- bend ---
    ("bend+V;NFIN", "bend"),
    ("bend+V;PRS;3;SG", "bends"),
    ("bend+V;PST", "bent"),
    ("bend+V;V.PTCP;PRS", "bending"),
    ("bend+V;V.PTCP;PST", "bent"),
    # --- lend ---
    ("lend+V;NFIN", "lend"),
    ("lend+V;PRS;3;SG", "lends"),
    ("lend+V;PST", "lent"),
    ("lend+V;V.PTCP;PRS", "lending"),
    ("lend+V;V.PTCP;PST", "lent"),
    # --- lay ---
    ("lay+V;NFIN", "lay"),
    ("lay+V;PRS;3;SG", "lays"),
    ("lay+V;PST", "laid"),
    ("lay+V;V.PTCP;PRS", "laying"),
    ("lay+V;V.PTCP;PST", "laid"),
    # --- deal ---
    ("deal+V;NFIN", "deal"),
    ("deal+V;PRS;3;SG", "deals"),
    ("deal+V;PST", "dealt"),
    ("deal+V;V.PTCP;PRS", "dealing"),
    ("deal+V;V.PTCP;PST", "dealt"),
    # --- seek ---
    ("seek+V;NFIN", "seek"),
    ("seek+V;PRS;3;SG", "seeks"),
    ("seek+V;PST", "sought"),
    ("seek+V;V.PTCP;PRS", "seeking"),
    ("seek+V;V.PTCP;PST", "sought"),
    # --- hit ---
    ("hit+V;NFIN", "hit"),
    ("hit+V;PRS;3;SG", "hits"),
    ("hit+V;PST", "hit"),
    ("hit+V;V.PTCP;PRS", "hitting"),
    ("hit+V;V.PTCP;PST", "hit"),
    # --- shut ---
    ("shut+V;NFIN", "shut"),
    ("shut+V;PRS;3;SG", "shuts"),
    ("shut+V;PST", "shut"),
    ("shut+V;V.PTCP;PRS", "shutting"),
    ("shut+V;V.PTCP;PST", "shut"),
    # --- split ---
    ("split+V;NFIN", "split"),
    ("split+V;PRS;3;SG", "splits"),
    ("split+V;PST", "split"),
    ("split+V;V.PTCP;PRS", "splitting"),
    ("split+V;V.PTCP;PST", "split"),
    # --- spread ---
    ("spread+V;NFIN", "spread"),
    ("spread+V;PRS;3;SG", "spreads"),
    ("spread+V;PST", "spread"),
    ("spread+V;V.PTCP;PRS", "spreading"),
    ("spread+V;V.PTCP;PST", "spread"),
    # --- quit ---
    ("quit+V;NFIN", "quit"),
    ("quit+V;PRS;3;SG", "quits"),
    ("quit+V;PST", "quit"),
    ("quit+V;V.PTCP;PRS", "quitting"),
    ("quit+V;V.PTCP;PST", "quit"),
]

# =============================================================================
# IRREGULAR NOUN PLURALS
# =============================================================================
IRREGULAR_NOUNS = [
    ("man+N;SG", "man"),       ("man+N;PL", "men"),
    ("woman+N;SG", "woman"),   ("woman+N;PL", "women"),
    ("child+N;SG", "child"),   ("child+N;PL", "children"),
    ("foot+N;SG", "foot"),     ("foot+N;PL", "feet"),
    ("tooth+N;SG", "tooth"),   ("tooth+N;PL", "teeth"),
    ("goose+N;SG", "goose"),   ("goose+N;PL", "geese"),
    ("mouse+N;SG", "mouse"),   ("mouse+N;PL", "mice"),
    ("louse+N;SG", "louse"),   ("louse+N;PL", "lice"),
    ("ox+N;SG", "ox"),         ("ox+N;PL", "oxen"),
    ("person+N;SG", "person"), ("person+N;PL", "people"),
    # f/fe -> ves
    ("knife+N;SG", "knife"),   ("knife+N;PL", "knives"),
    ("wife+N;SG", "wife"),     ("wife+N;PL", "wives"),
    ("life+N;SG", "life"),     ("life+N;PL", "lives"),
    ("leaf+N;SG", "leaf"),     ("leaf+N;PL", "leaves"),
    ("shelf+N;SG", "shelf"),   ("shelf+N;PL", "shelves"),
    ("half+N;SG", "half"),     ("half+N;PL", "halves"),
    ("wolf+N;SG", "wolf"),     ("wolf+N;PL", "wolves"),
    ("calf+N;SG", "calf"),     ("calf+N;PL", "calves"),
    ("thief+N;SG", "thief"),   ("thief+N;PL", "thieves"),
    ("loaf+N;SG", "loaf"),     ("loaf+N;PL", "loaves"),
    ("elf+N;SG", "elf"),       ("elf+N;PL", "elves"),
    ("dwarf+N;SG", "dwarf"),   ("dwarf+N;PL", "dwarves"),
    ("scarf+N;SG", "scarf"),   ("scarf+N;PL", "scarves"),
    # Unchanged plurals
    ("sheep+N;SG", "sheep"),   ("sheep+N;PL", "sheep"),
    ("deer+N;SG", "deer"),     ("deer+N;PL", "deer"),
    ("fish+N;SG", "fish"),     ("fish+N;PL", "fish"),
    ("series+N;SG", "series"), ("series+N;PL", "series"),
    ("species+N;SG", "species"), ("species+N;PL", "species"),
    ("aircraft+N;SG", "aircraft"), ("aircraft+N;PL", "aircraft"),
    # Latin/Greek plurals
    ("criterion+N;SG", "criterion"), ("criterion+N;PL", "criteria"),
    ("phenomenon+N;SG", "phenomenon"), ("phenomenon+N;PL", "phenomena"),
    ("analysis+N;SG", "analysis"), ("analysis+N;PL", "analyses"),
    ("basis+N;SG", "basis"),   ("basis+N;PL", "bases"),
    ("crisis+N;SG", "crisis"), ("crisis+N;PL", "crises"),
    ("thesis+N;SG", "thesis"), ("thesis+N;PL", "theses"),
    ("focus+N;SG", "focus"),   ("focus+N;PL", "foci"),
    ("fungus+N;SG", "fungus"), ("fungus+N;PL", "fungi"),
    ("cactus+N;SG", "cactus"), ("cactus+N;PL", "cacti"),
    ("nucleus+N;SG", "nucleus"), ("nucleus+N;PL", "nuclei"),
    ("radius+N;SG", "radius"), ("radius+N;PL", "radii"),
    ("stimulus+N;SG", "stimulus"), ("stimulus+N;PL", "stimuli"),
    ("appendix+N;SG", "appendix"), ("appendix+N;PL", "appendices"),
    ("index+N;SG", "index"),   ("index+N;PL", "indices"),
    ("matrix+N;SG", "matrix"), ("matrix+N;PL", "matrices"),
]

# =============================================================================
# IRREGULAR ADJECTIVE COMPARATIVES/SUPERLATIVES
# =============================================================================
IRREGULAR_ADJECTIVES = [
    ("good+ADJ", "good"),       ("good+ADJ;CMPR", "better"),
    ("good+ADJ;SPRL", "best"),
    ("bad+ADJ", "bad"),         ("bad+ADJ;CMPR", "worse"),
    ("bad+ADJ;SPRL", "worst"),
    ("far+ADJ", "far"),         ("far+ADJ;CMPR", "farther"),
    ("far+ADJ;SPRL", "farthest"),
    ("little+ADJ", "little"),   ("little+ADJ;CMPR", "less"),
    ("little+ADJ;SPRL", "least"),
    ("much+ADJ", "much"),       ("much+ADJ;CMPR", "more"),
    ("much+ADJ;SPRL", "most"),
    ("many+ADJ", "many"),       ("many+ADJ;CMPR", "more"),
    ("many+ADJ;SPRL", "most"),
    ("old+ADJ", "old"),         ("old+ADJ;CMPR", "elder"),
    ("old+ADJ;SPRL", "eldest"),
]

# =============================================================================
# CONSONANT DOUBLING cases (handled as irregular since pattern is complex)
# These are regular verbs where the final consonant doubles before -ing/-ed
# =============================================================================
DOUBLING_VERBS = [
    # stop
    ("stop+V;NFIN", "stop"), ("stop+V;PRS;3;SG", "stops"),
    ("stop+V;PST", "stopped"), ("stop+V;V.PTCP;PRS", "stopping"),
    ("stop+V;V.PTCP;PST", "stopped"),
    # drop
    ("drop+V;NFIN", "drop"), ("drop+V;PRS;3;SG", "drops"),
    ("drop+V;PST", "dropped"), ("drop+V;V.PTCP;PRS", "dropping"),
    ("drop+V;V.PTCP;PST", "dropped"),
    # plan
    ("plan+V;NFIN", "plan"), ("plan+V;PRS;3;SG", "plans"),
    ("plan+V;PST", "planned"), ("plan+V;V.PTCP;PRS", "planning"),
    ("plan+V;V.PTCP;PST", "planned"),
    # shop
    ("shop+V;NFIN", "shop"), ("shop+V;PRS;3;SG", "shops"),
    ("shop+V;PST", "shopped"), ("shop+V;V.PTCP;PRS", "shopping"),
    ("shop+V;V.PTCP;PST", "shopped"),
    # slip
    ("slip+V;NFIN", "slip"), ("slip+V;PRS;3;SG", "slips"),
    ("slip+V;PST", "slipped"), ("slip+V;V.PTCP;PRS", "slipping"),
    ("slip+V;V.PTCP;PST", "slipped"),
    # step
    ("step+V;NFIN", "step"), ("step+V;PRS;3;SG", "steps"),
    ("step+V;PST", "stepped"), ("step+V;V.PTCP;PRS", "stepping"),
    ("step+V;V.PTCP;PST", "stepped"),
    # trip
    ("trip+V;NFIN", "trip"), ("trip+V;PRS;3;SG", "trips"),
    ("trip+V;PST", "tripped"), ("trip+V;V.PTCP;PRS", "tripping"),
    ("trip+V;V.PTCP;PST", "tripped"),
    # wrap
    ("wrap+V;NFIN", "wrap"), ("wrap+V;PRS;3;SG", "wraps"),
    ("wrap+V;PST", "wrapped"), ("wrap+V;V.PTCP;PRS", "wrapping"),
    ("wrap+V;V.PTCP;PST", "wrapped"),
    # nod
    ("nod+V;NFIN", "nod"), ("nod+V;PRS;3;SG", "nods"),
    ("nod+V;PST", "nodded"), ("nod+V;V.PTCP;PRS", "nodding"),
    ("nod+V;V.PTCP;PST", "nodded"),
    # rob
    ("rob+V;NFIN", "rob"), ("rob+V;PRS;3;SG", "robs"),
    ("rob+V;PST", "robbed"), ("rob+V;V.PTCP;PRS", "robbing"),
    ("rob+V;V.PTCP;PST", "robbed"),
    # grab
    ("grab+V;NFIN", "grab"), ("grab+V;PRS;3;SG", "grabs"),
    ("grab+V;PST", "grabbed"), ("grab+V;V.PTCP;PRS", "grabbing"),
    ("grab+V;V.PTCP;PST", "grabbed"),
    # drag
    ("drag+V;NFIN", "drag"), ("drag+V;PRS;3;SG", "drags"),
    ("drag+V;PST", "dragged"), ("drag+V;V.PTCP;PRS", "dragging"),
    ("drag+V;V.PTCP;PST", "dragged"),
    # snap
    ("snap+V;NFIN", "snap"), ("snap+V;PRS;3;SG", "snaps"),
    ("snap+V;PST", "snapped"), ("snap+V;V.PTCP;PRS", "snapping"),
    ("snap+V;V.PTCP;PST", "snapped"),
    # chat
    ("chat+V;NFIN", "chat"), ("chat+V;PRS;3;SG", "chats"),
    ("chat+V;PST", "chatted"), ("chat+V;V.PTCP;PRS", "chatting"),
    ("chat+V;V.PTCP;PST", "chatted"),
    # pat
    ("pat+V;NFIN", "pat"), ("pat+V;PRS;3;SG", "pats"),
    ("pat+V;PST", "patted"), ("pat+V;V.PTCP;PRS", "patting"),
    ("pat+V;V.PTCP;PST", "patted"),
    # tap
    ("tap+V;NFIN", "tap"), ("tap+V;PRS;3;SG", "taps"),
    ("tap+V;PST", "tapped"), ("tap+V;V.PTCP;PRS", "tapping"),
    ("tap+V;V.PTCP;PST", "tapped"),
    # hug
    ("hug+V;NFIN", "hug"), ("hug+V;PRS;3;SG", "hugs"),
    ("hug+V;PST", "hugged"), ("hug+V;V.PTCP;PRS", "hugging"),
    ("hug+V;V.PTCP;PST", "hugged"),
    # beg
    ("beg+V;NFIN", "beg"), ("beg+V;PRS;3;SG", "begs"),
    ("beg+V;PST", "begged"), ("beg+V;V.PTCP;PRS", "begging"),
    ("beg+V;V.PTCP;PST", "begged"),
    # stir
    ("stir+V;NFIN", "stir"), ("stir+V;PRS;3;SG", "stirs"),
    ("stir+V;PST", "stirred"), ("stir+V;V.PTCP;PRS", "stirring"),
    ("stir+V;V.PTCP;PST", "stirred"),
    # occur
    ("occur+V;NFIN", "occur"), ("occur+V;PRS;3;SG", "occurs"),
    ("occur+V;PST", "occurred"), ("occur+V;V.PTCP;PRS", "occurring"),
    ("occur+V;V.PTCP;PST", "occurred"),
    # prefer
    ("prefer+V;NFIN", "prefer"), ("prefer+V;PRS;3;SG", "prefers"),
    ("prefer+V;PST", "preferred"), ("prefer+V;V.PTCP;PRS", "preferring"),
    ("prefer+V;V.PTCP;PST", "preferred"),
    # refer
    ("refer+V;NFIN", "refer"), ("refer+V;PRS;3;SG", "refers"),
    ("refer+V;PST", "referred"), ("refer+V;V.PTCP;PRS", "referring"),
    ("refer+V;V.PTCP;PST", "referred"),
    # admit
    ("admit+V;NFIN", "admit"), ("admit+V;PRS;3;SG", "admits"),
    ("admit+V;PST", "admitted"), ("admit+V;V.PTCP;PRS", "admitting"),
    ("admit+V;V.PTCP;PST", "admitted"),
    # permit
    ("permit+V;NFIN", "permit"), ("permit+V;PRS;3;SG", "permits"),
    ("permit+V;PST", "permitted"), ("permit+V;V.PTCP;PRS", "permitting"),
    ("permit+V;V.PTCP;PST", "permitted"),
    # regret
    ("regret+V;NFIN", "regret"), ("regret+V;PRS;3;SG", "regrets"),
    ("regret+V;PST", "regretted"), ("regret+V;V.PTCP;PRS", "regretting"),
    ("regret+V;V.PTCP;PST", "regretted"),
]

# Consonant doubling adjectives
DOUBLING_ADJECTIVES = [
    ("big+ADJ", "big"),       ("big+ADJ;CMPR", "bigger"),
    ("big+ADJ;SPRL", "biggest"),
    ("hot+ADJ", "hot"),       ("hot+ADJ;CMPR", "hotter"),
    ("hot+ADJ;SPRL", "hottest"),
    ("thin+ADJ", "thin"),     ("thin+ADJ;CMPR", "thinner"),
    ("thin+ADJ;SPRL", "thinnest"),
    ("fat+ADJ", "fat"),       ("fat+ADJ;CMPR", "fatter"),
    ("fat+ADJ;SPRL", "fattest"),
    ("wet+ADJ", "wet"),       ("wet+ADJ;CMPR", "wetter"),
    ("wet+ADJ;SPRL", "wettest"),
    ("sad+ADJ", "sad"),       ("sad+ADJ;CMPR", "sadder"),
    ("sad+ADJ;SPRL", "saddest"),
    ("mad+ADJ", "mad"),       ("mad+ADJ;CMPR", "madder"),
    ("mad+ADJ;SPRL", "maddest"),
    ("red+ADJ", "red"),       ("red+ADJ;CMPR", "redder"),
    ("red+ADJ;SPRL", "reddest"),
    ("dim+ADJ", "dim"),       ("dim+ADJ;CMPR", "dimmer"),
    ("dim+ADJ;SPRL", "dimmest"),
    ("fit+ADJ", "fit"),       ("fit+ADJ;CMPR", "fitter"),
    ("fit+ADJ;SPRL", "fittest"),
    ("flat+ADJ", "flat"),     ("flat+ADJ;CMPR", "flatter"),
    ("flat+ADJ;SPRL", "flattest"),
]

# =============================================================================
# ALL IRREGULARS COMBINED
# =============================================================================
ALL_IRREGULARS = (
    IRREGULAR_VERBS +
    IRREGULAR_NOUNS +
    IRREGULAR_ADJECTIVES +
    DOUBLING_VERBS +
    DOUBLING_ADJECTIVES
)
