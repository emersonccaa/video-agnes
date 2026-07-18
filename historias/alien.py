# "O Mistério do Alien"
# Elenco e características conforme a autora.

TITULO = 'O Mistério do Alien'
LEGENDA = ('O Misterio do Alien — uma historia infantil\n'
           '14 cenas · imagens agnes-image-2.1-flash · video keyframes agnes-video-v2.0 · '
           'narracao bella local. Custo US$ 0.')

TRIO = ('Lívia, a girl with brown skin, dark brown hair and brown eyes; '
        'Maria, a girl with blonde hair and blue eyes; '
        'Lucas, a boy with black hair and green eyes. Three children, about ten years old')
ALIEN = ('a small friendly alien with bright green skin, a large oversized head and very large dark eyes, '
         'small slender body')
MAE = "Lívia's mother, an adult woman with brown skin, dark brown hair and brown eyes, warm and kind"
CIENT = 'a tall adult scientist in a white lab coat with round glasses, sinister expression'

# (id, prompt, deriva_de) — a mae do elenco em text2img, o resto DERIVADO (mesmo mundo/estilo)
ANCORAS = [
    ('anc-trio', f'Character reference sheet: {TRIO}, standing together side by side in a sunny backyard, '
                 f'three-quarter view, full body, friendly. Plain soft background.', None),
    ('anc-alien', f'Character reference of {ALIEN}, standing in a forest clearing, three-quarter view, '
                  f'full body. Plain soft background.', None),
    ('anc-mae', f'Character reference of {MAE}, standing in a kitchen, three-quarter view, full body.', 'anc-trio'),
    ('anc-cient', f'Character reference of {CIENT}, standing in a laboratory, three-quarter view, full body.', 'anc-trio'),
]

CENAS = [
    ('cena-01-a', f'{TRIO} playing together in a sunny backyard, laughing, wide shot.', ['anc-trio']),
    ('cena-01-b', f'Close-up of Lívia, a girl with brown skin, dark brown hair and brown eyes, sitting on the grass '
                  f'looking at a book about aliens with wonder in her eyes.', ['anc-trio']),
    ('cena-02-a', f'{TRIO} freeze mid-play and all turn their heads toward a dark thicket of woods, alarmed.', ['anc-trio']),
    ('cena-02-b', 'A dark dense thicket of woods, something moving among the leaves, mysterious, nobody visible.', []),
    ('cena-03-a', 'Lucas, a boy with black hair and green eyes, walking alone into the dark woods, determined, '
                  'seen from behind.', ['anc-trio']),
    ('cena-03-b', 'Lívia and Maria waiting at the edge of the woods, growing worried, glancing at each other.', ['anc-trio']),
    ('cena-04-a', 'Lívia and Maria stepping into the woods searching for their friend, worried.', ['anc-trio']),
    ('cena-04-b', 'The girls find Lucas among the trees; he waves at them to follow him, excited.', ['anc-trio']),
    ('cena-05-a', 'A small crashed alien spaceship lying among the trees in the woods, smoke rising, discovery.', []),
    ('cena-05-b', f'{ALIEN}, injured, lying on the ground beside the crashed spaceship, the three children '
                  f'kneeling around him, worried.', ['anc-trio', 'anc-alien']),
    ('cena-06-a', f'The three children carrying {ALIEN} carefully toward a house at dusk.', ['anc-trio', 'anc-alien']),
    ('cena-06-b', f'{ALIEN} resting in a childs bed with a bandage, the three children caring for him, '
                  f'warm lamp light, cozy bedroom.', ['anc-trio', 'anc-alien']),
    ('cena-07-a', f'{ALIEN} standing up healed and smiling, arms raised, happy.', ['anc-alien']),
    ('cena-07-b', f'The three children and {ALIEN} together, all happy, celebrating in the bedroom.', ['anc-trio', 'anc-alien']),
    ('cena-08-a', f'The three children and {ALIEN} working on repairing the crashed spaceship in the woods, tools, daylight.',
     ['anc-trio', 'anc-alien']),
    ('cena-08-b', f'{CIENT} hiding behind a tree, spying on them through the leaves, sinister, unnoticed.', ['anc-cient']),
    ('cena-09-a', f'{CIENT} grabbing {ALIEN}, the alien struggling, dramatic, tense.', ['anc-alien', 'anc-cient']),
    ('cena-09-b', 'The three children arriving too late at the empty clearing, the spaceship alone, '
                  'their friend gone, shock and despair.', ['anc-trio']),
    ('cena-10-a', f'Days later, {CIENT} walking down a street carrying a case, seen from across the road.', ['anc-cient']),
    ('cena-10-b', 'The three children following him, hiding behind a wall, peeking out, stealthy.', ['anc-trio', 'anc-cient']),
    ('cena-11-a', 'A sinister laboratory building at night, cold light in the windows, ominous.', []),
    ('cena-11-b', f'{ALIEN} trapped inside a glass capsule in the laboratory, sad, hands against the glass.', ['anc-alien']),
    ('cena-12-a', f'The three children opening the glass capsule and freeing {ALIEN}, rescue, hopeful.', ['anc-trio', 'anc-alien']),
    ('cena-12-b', f'The three children and {ALIEN} running out of the laboratory together, escaping, night.', ['anc-trio', 'anc-alien']),
    ('cena-13-a', f'{MAE} in a warm kitchen handing out a big tray of fresh cookies, smiling.', ['anc-mae']),
    ('cena-13-b', f'The three children and {ALIEN} sitting around the kitchen table eating cookies together, joyful, warm.',
     ['anc-trio', 'anc-alien']),
    ('cena-14-a', f'{ALIEN} trying to repair his spaceship and failing, disappointed, the children beside him.',
     ['anc-trio', 'anc-alien']),
    ('cena-14-b', 'A big alien mother ship descending from the night sky over the woods, warm lights, '
                  'the children and the little alien waving goodbye, bittersweet.', ['anc-trio', 'anc-alien']),
]

NARRACAO = {
    1: 'Era uma vez uma menina chamada Lívia. Ela tinha dois amigos que se chamavam Lucas e Maria. '
       'Lívia era uma menina que amava aliens, Maria amava filmes de terror, e Lucas gostava muito de animais.',
    2: 'Um certo dia, Lívia e seus amigos ouviram um barulho no mato.',
    3: 'Lucas achava que era um animal machucado, então foi ver o que era.',
    4: 'Um tempo depois elas ficaram preocupadas e foram ver o que tinha acontecido. Quando o acharam, '
       'ele disse para elas seguirem ele.',
    5: 'Ele mostrou que tinha uma nave alien, com um alienígena machucado.',
    6: 'Eles o levaram para casa e cuidaram dele.',
    7: 'Quando ele melhorou, ficaram todos muito felizes.',
    8: 'Foram consertar a nave. Só que o que eles não sabiam é que tinha um cientista os observando.',
    9: 'Quando eles viram, já era tarde: o cientista pegou e sumiu com o alien.',
    10: 'Dias depois eles viram o cientista caminhando, e o seguiram.',
    11: 'Logo acharam o laboratório.',
    12: 'E resgataram o alien, seu amigo.',
    13: 'Quando voltaram para casa, a mãe de Lívia fez um monte de biscoitos e distribuiu para as crianças e o alien.',
    14: 'Logo o alien foi consertar a sua nave, mas não conseguiu. Então chamou sua família, que os buscaram. '
        'E às vezes o alien os visita.',
}

MOVIMENTO = {
    1: 'the children play and laugh, the camera pushes in slowly toward Lívia and her book',
    2: 'the children stop playing and all turn toward the woods, the camera drifts into the dark thicket',
    3: 'Lucas walks away into the woods while the two girls watch, worry growing on their faces',
    4: 'the girls move through the woods and find Lucas, who waves them over excitedly',
    5: 'the camera reveals the crashed ship, then tilts down to the injured alien on the ground',
    6: 'the children carry the alien home and lay him gently in bed, warm lamp light rising',
    7: 'the alien stands up healed and smiles, the children celebrate around him',
    8: 'the group works on the ship, then the camera pans to the scientist hiding behind a tree',
    9: 'the scientist grabs the alien and vanishes, the children arrive to find the clearing empty',
    10: 'the scientist walks down the street, the children follow, hiding behind a wall',
    11: 'the camera approaches the sinister laboratory and finds the alien trapped in a glass capsule',
    12: 'the children free the alien and they all run out of the laboratory together',
    13: 'the mother hands out cookies, everyone gathers around the table eating happily',
    14: 'the alien fails to fix his ship, then a huge mother ship descends from the sky, everyone waves goodbye',
}
