# "A Maldição da Família Diabrotic"
# Amora (cabelo roxo fluorescente) e Lila (cabelo azul marinho), irmas lacadoras.
# Nota: a historia tem clima de terror leve (potreiro macabro, maldicao) — mantido, mas
# tratado como conto de fadas: sem horror grafico.

TITULO = 'A Maldição da Família Diabrotic'
LEGENDA = ('A Maldicao da Familia Diabrotic\n'
           '12 cenas · imagens agnes-image-2.1-flash · video keyframes agnes-video-v2.0 · '
           'narracao bella local. Custo US$ 0.')

IRMAS = ('Amora, a young woman with bright fluorescent purple hair; and Lila, her sister, a young woman with '
         'navy blue hair. Two sisters in rodeo clothing with lassos, boots and hats')
RAPAZES = ('Pietro, a handsome young man with black hair; and Matheus, his friend, also a young man with black hair. '
           'Both in rodeo clothing')

ANCORAS = [
    ('anc-irmas', f'Character reference sheet: {IRMAS}, standing side by side holding their lassos, '
                  f'three-quarter view, full body. Plain soft background.', None),
    ('anc-rapazes', f'Character reference sheet: {RAPAZES}, standing side by side, three-quarter view, full body. '
                    f'Plain soft background.', 'anc-irmas'),
]

CENAS = [
    ('cena-01-a', f'{IRMAS} riding horses and throwing their lassos in a sunny arena, skilled and joyful, wide shot.',
     ['anc-irmas']),
    ('cena-01-b', 'Close-up of two ornate old lassos and saddles hanging in a barn, heirloom objects, '
                  'faint magical purple and blue glow around them, mysterious.', []),
    ('cena-02-a', 'An old family portrait on a wall showing generations of lasso riders, dusty, '
                  'the heirloom saddles passed down, sense of legacy and burden.', []),
    ('cena-02-b', f'Close-up of {IRMAS} looking at each other with worry, the weight of the family curse on their faces.',
     ['anc-irmas']),
    ('cena-03-a', 'A beautiful clean rodeo park in Madrid, Spain, flags, green grass, elegant arena, sunny, wide shot.', []),
    ('cena-03-b', f'{IRMAS} signing up at a registration desk for the sibling lasso competition, nervous but decided.',
     ['anc-irmas']),
    ('cena-04-a', f'{IRMAS} waiting at the gate before their turn, afraid, holding hands, tense.', ['anc-irmas']),
    ('cena-04-b', 'Amora, a young woman with bright fluorescent purple hair, on horseback throwing her lasso perfectly, '
                  'hitting the target, precise and strong.', ['anc-irmas']),
    ('cena-05-a', 'Lila, a young woman with navy blue hair, on horseback throwing her lasso and missing, '
                  'frustration on her face.', ['anc-irmas']),
    ('cena-05-b', f'{IRMAS} leaving the arena with heads down, knowing the curse will come, dread.', ['anc-irmas']),
    ('cena-06-a', 'A macabre eerie horse paddock at dusk, dead bare trees, insects, fog, like a horror film set, '
                  'empty and unsettling.', []),
    ('cena-06-b', f'{IRMAS} leading their horses into the eerie paddock, looking around uneasily, dead trees around them.',
     ['anc-irmas']),
    ('cena-07-a', f'{IRMAS} suddenly surrounded by swirling magical smoke, bright purple and navy blue, '
                  f'the colors of their hair, the curse arriving, dramatic.', ['anc-irmas']),
    ('cena-07-b', 'A young calf and a young filly standing where the sisters were, in the eerie paddock, '
                  'purple and blue smoke fading around them, sad and strange.', []),
    ('cena-08-a', 'A calf and a filly grazing together in a field, two months have passed, seasons changed, '
                  'they stay close to each other, melancholy.', []),
    ('cena-08-b', 'Close-up of the filly eyes, intelligent and human behind the animal face, longing.', []),
    ('cena-09-a', 'Pietro, a handsome young man with black hair, appearing in the field, speaking strange words, '
                  'hand raised, magic beginning.', ['anc-rapazes']),
    ('cena-09-b', f'The same purple and blue smoke swirling around the animals and {IRMAS} standing human again, '
                  f'astonished and grateful.', ['anc-irmas', 'anc-rapazes']),
    ('cena-10-a', f'{RAPAZES} meeting {IRMAS}, Pietro introducing his friend Matheus, four young people together, warm.',
     ['anc-irmas', 'anc-rapazes']),
    ('cena-10-b', 'The four of them laughing together at a rodeo, becoming a quartet, friendship growing, golden light.',
     ['anc-irmas', 'anc-rapazes']),
    ('cena-11-a', 'Matheus and Lila, the young woman with navy blue hair, walking together and falling in love, '
                  'shy smiles, sunset.', ['anc-irmas', 'anc-rapazes']),
    ('cena-11-b', 'Pietro and Amora, the young woman with fluorescent purple hair, riding side by side, '
                  'falling in love, warm light.', ['anc-irmas', 'anc-rapazes']),
    ('cena-12-a', 'A joyful double wedding of the two couples at a rodeo ranch, flowers, horses, celebration, wide shot.',
     ['anc-irmas', 'anc-rapazes']),
    ('cena-12-b', 'The two couples riding together into a golden sunset at a rodeo, lassos in hand, happy ending.',
     ['anc-irmas', 'anc-rapazes']),
]

NARRACAO = {
    1: 'Era uma vez uma menina de cabelo roxo fluorescente, Amora, e sua irmã de cabelos azuis marinhos, Lila. '
       'Elas amavam laçar.',
    2: 'Porém sua família tinha uma maldição: em todo rodeio que elas iam, se elas não ganhassem, '
       'uma coisa horrível iria acontecer. A maldição era por causa de seus laços e encilhas, que não podiam ser '
       'vendidos ou dados para alguém que não fosse filho ou filha, porque era passado de geração em geração '
       'da família Diabrotic.',
    3: 'Até que, em um rodeio no parque mais bonito e limpo de laço, em Madrid, na Espanha, elas se inscreveram '
       'para laçar laço irmão, que só irmãos ou irmãs podiam ir.',
    4: 'Elas estavam com medo de não ganhar ou acertar, mas mesmo assim foram. Chegou a hora delas laçarem. '
       'De três, a Amora acertou as três.',
    5: 'Mas a Lila só acertou uma. Então elas sabiam que iriam pagar a maldição quando chegassem em casa.',
    6: 'Elas foram deixar os cavalos no potreiro, que era macabro. Parecia cena de filme de terror, '
       'com árvores mortas e insetos.',
    7: 'Mas a maldição chegou antes do esperado. Elas foram rodeadas por uma fumaça azul e roxa, '
       'da cor de seus cabelos. Lila foi transformada em uma bezerra, e Amora em uma potra.',
    8: 'Ali elas passaram dois meses na forma de animais.',
    9: 'Até que, do nada, um homem apareceu, falou umas palavras, e a mesma fumaça rodeou elas de novo '
       'e as transformou de volta em humanas.',
    10: 'Ele se chamava Pietro, era bem bonito, com cabelos pretos. Eles se tornaram um quarteto, pois Pietro '
        'as apresentou mais um amigo chamado Matheus, também com cabelos pretos.',
    11: 'Matheus e Lila foram se apaixonando, assim como Amora e Pietro.',
    12: 'Os casais se casaram e foram para muitos rodeios juntos.',
}

MOVIMENTO = {
    1: 'the sisters ride and throw their lassos joyfully, the camera pushes in on the glowing heirloom lassos',
    2: 'the camera drifts across the old family portrait, then finds the sisters worried faces',
    3: 'the camera sweeps across the beautiful rodeo park, then the sisters sign up at the desk',
    4: 'the sisters wait tensely at the gate, then Amora throws her lasso and hits the target perfectly',
    5: 'Lila throws and misses, frustration crossing her face, then the sisters leave the arena with dread',
    6: 'the camera moves through the eerie foggy paddock with dead trees, then the sisters lead their horses in',
    7: 'purple and blue smoke swirls violently around the sisters, then a calf and a filly stand where they were',
    8: 'the calf and filly graze together, seasons passing, the camera pushes in on the filly human eyes',
    9: 'Pietro appears and speaks the words, the smoke returns and the sisters become human again',
    10: 'Pietro introduces Matheus, the four meet and laugh together, friendship forming',
    11: 'Matheus and Lila walk together shyly, then Pietro and Amora ride side by side in love',
    12: 'the double wedding celebration, then the two couples ride into the golden sunset together',
}
