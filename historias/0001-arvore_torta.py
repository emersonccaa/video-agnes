# historias/arvore_torta.py
# Canal: Vozes de Serenidade (TikTok / Kwai)
# Duração alvo: ~90s (6 cenas, narração pausada e contemplativa)

TITULO = "A Árvore Torta"

LEGENDA = (
    "🌳 A árvore que ninguém queria virou a única que ficou de pé. "
    "Talvez sua história torta também tenha raízes fortes. "
    "Comenta aqui: qual foi a sua tempestade? "
    "#vozesdeserenidade #motivacao #resiliencia #reflexao #forcainterior"
)

# ---------------------------------------------------------------------------
# Personagem fixo — repetir ESTE bloco, literal, em toda cena que ele aparece.
# (Rosto humano é frágil na deriva de identidade — descrição estável ajuda.)
# ---------------------------------------------------------------------------
JARDINEIRO = (
    "an elderly gardener, deeply tanned weathered skin, thick white beard, "
    "kind warm eyes, wearing a faded green canvas apron over a simple brown "
    "linen shirt with rolled sleeves, calloused hands, exactly one man, one head"
)

# ---------------------------------------------------------------------------
# ANCORAS — model sheet do personagem. Mãe em text2img, derivada em img2img
# para permanecer o MESMO indivíduo (nunca pose frontal simétrica).
# ---------------------------------------------------------------------------
ANCORAS = [
    (
        "anc-jardineiro",
        f"{JARDINEIRO}, three-quarter body reference sheet, standing at a "
        "slight angle, calm natural stance, plain neutral gray background, "
        "soft even studio lighting, size:\"1312x736\"",
        None,
    ),
    (
        "anc-jardineiro-perfil",
        f"{JARDINEIRO}, turned slightly further to the side, same clothing "
        "and stance, plain neutral gray background, soft even studio "
        "lighting, size:\"1312x736\"",
        "anc-jardineiro",
    ),
]

# ---------------------------------------------------------------------------
# CENAS — 2 imagens por cena (a=início, b=fim), refs sempre <= 2.
# Prompts em INGLÊS (API bloqueia PT).
# ---------------------------------------------------------------------------
CENAS = [
    # Cena 01 — a descoberta
    (
        "cena-01-a",
        "wide shot of a plant nursery, dozens of straight young tree "
        "saplings in neat rows of pots, warm morning light, one small "
        "visibly crooked twisted sapling standing apart in a corner, "
        "size:\"1312x736\"",
        [],
    ),
    (
        "cena-01-b",
        f"{JARDINEIRO}, kneeling down in the nursery, gently holding the "
        "small crooked sapling in cupped hands, looking at it thoughtfully, "
        "rows of straight saplings blurred in the background, warm morning "
        "light, size:\"1312x736\"",
        ["anc-jardineiro"],
    ),
    # Cena 02 — o cuidado paciente
    (
        "cena-02-a",
        f"{JARDINEIRO}, digging a small hole in a quiet corner of a large "
        "garden, the crooked sapling resting on the ground beside him, "
        "soft afternoon light, size:\"1312x736\"",
        ["anc-jardineiro"],
    ),
    (
        "cena-02-b",
        f"{JARDINEIRO}, gently patting soil around the newly planted "
        "crooked sapling, holding an old metal watering can, peaceful "
        "expression, soft afternoon light, size:\"1312x736\"",
        ["anc-jardineiro"],
    ),
    # Cena 03 — os anos passam, a tempestade se anuncia
    (
        "cena-03-a",
        f"{JARDINEIRO}, watering the now taller crooked tree, tall proud "
        "straight trees growing nearby, lush green garden, bright sunny "
        "day, size:\"1312x736\"",
        ["anc-jardineiro"],
    ),
    (
        "cena-03-b",
        "wide shot of the garden, dark storm clouds rolling in overhead, "
        "wind starting to bend the grass, tall straight trees and the "
        "crooked tree standing side by side, dramatic lighting, "
        "size:\"1312x736\"",
        [],
    ),
    # Cena 04 — a tempestade testa cada tronco
    (
        "cena-04-a",
        "heavy storm, strong wind, the crooked tree bending flexibly in "
        "the gale, leaves whipping through the air, dark dramatic sky, "
        "size:\"1312x736\"",
        [],
    ),
    (
        "cena-04-b",
        "storm subsiding, one tall straight tree trunk snapped and fallen "
        "on the ground nearby, the crooked tree still standing bent but "
        "unbroken, first light breaking through clouds, size:\"1312x736\"",
        [],
    ),
    # Cena 05 — depois da tempestade
    (
        "cena-05-a",
        f"{JARDINEIRO}, walking slowly through fallen broken tree trunks "
        "and debris scattered across the garden, soft golden sunrise "
        "light, size:\"1312x736\"",
        ["anc-jardineiro"],
    ),
    (
        "cena-05-b",
        f"{JARDINEIRO}, close up, gently touching the trunk of the crooked "
        "tree, deep exposed roots visible gripping the earth, moved "
        "peaceful expression, golden sunrise light, size:\"1312x736\"",
        ["anc-jardineiro"],
    ),
    # Cena 06 — fechamento emocional
    (
        "cena-06-a",
        f"{JARDINEIRO}, sitting peacefully on a wooden stool under the "
        "crooked tree's canopy, warm golden hour sunlight filtering "
        "through the leaves, size:\"1312x736\"",
        ["anc-jardineiro"],
    ),
    (
        "cena-06-b",
        "wide pulled-back shot, the crooked tree standing tall and alone "
        "against a glowing sunset sky, warm cinematic light, silhouettes "
        "of the garden around it, size:\"1312x736\"",
        [],
    ),
]

# ---------------------------------------------------------------------------
# NARRACAO — texto em PT-BR, fatiado por cena. A duração do clipe é definida
# pela fala, então o texto já está calibrado pra ~90s no total (fala pausada).
# ---------------------------------------------------------------------------
NARRACAO = {
    1: (
        "Um velho jardineiro encontrou, entre mudas perfeitas, uma pequena "
        "árvore torta. Diziam: essa não presta, jogue fora. Mas ele olhou "
        "mais de perto e enxergou o que ninguém mais quis ver."
    ),
    2: (
        "Plantou-a sozinha, num canto quieto do jardim. Regava todos os "
        "dias, sem pressa, sem cobrar que crescesse igual às outras. Só "
        "cuidava, com a paciência de quem sabe que toda raiz precisa de "
        "tempo."
    ),
    3: (
        "Os anos passaram. As árvores retas cresceram altas e orgulhosas "
        "ao lado dela. Um dia o céu escureceu: uma tempestade forte se "
        "aproximava, pronta pra testar cada tronco daquele jardim."
    ),
    4: (
        "O vento foi implacável. As árvores retas, tão certinhas, "
        "quebraram uma a uma. A árvore torta se curvou, dobrou, resistiu "
        "— porque suas raízes tinham aprendido a se agarrar fundo."
    ),
    5: (
        "Na manhã seguinte, o jardineiro caminhou entre os troncos "
        "caídos. No meio da destruição, só uma árvore seguia de pé: a "
        "torta. Aquela chamada de imperfeita era, agora, a mais forte de "
        "todas."
    ),
    6: (
        "Talvez o que te fez diferente não seja o que te quebra — é o "
        "que te mantém de pé quando tudo desaba. Sua história torta "
        "também tem raízes fortes. Não desista dela. Comenta aqui: qual "
        "foi a sua tempestade?"
    ),
}

# ---------------------------------------------------------------------------
# MOVIMENTO — descrição do movimento A -> B por cena, em inglês.
# ---------------------------------------------------------------------------
MOVIMENTO = {
    1: "slow push-in from the wide nursery shot toward the gardener kneeling and cradling the small crooked sapling",
    2: "gentle handheld feel, gardener digging then patting soil around the planted sapling, calm continuous motion",
    3: "smooth transition from sunny watering to gathering storm clouds rolling across the sky, wind picking up",
    4: "dynamic wind motion, tree bending and swaying, then settling as the storm passes and light breaks through",
    5: "slow tracking shot following the gardener walking through debris, ending in a close-up on his hand touching the trunk",
    6: "slow pull-back crane shot from the gardener sitting in the shade to a wide sunset silhouette of the standing tree",
}
