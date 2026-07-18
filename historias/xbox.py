# "O Menino que Queria um Xbox"
# Elenco conforme o autor: Titi (loiro amarelado, olhos verdes, camisa preta, calça jeans, tênis branco)
#                          Mãe (cabelo castanho, olhos castanhos, casaco verde peludo, calça jeans, chinelo)

TITULO = 'O Menino que Queria um Xbox'
LEGENDA = ('O Menino que Queria um Xbox — uma historia infantil\n'
           '10 cenas · imagens agnes-image-2.1-flash · video keyframes agnes-video-v2.0 · '
           'narracao bella local. Custo US$ 0.')

TITI = ('Titi, a boy about ten years old with yellowish blond hair and green eyes, '
        'wearing a black t-shirt, blue jeans and white sneakers')
MAE = ('Titi\'s mother, an adult woman with brown hair and brown eyes, wearing a fuzzy green coat, '
       'blue jeans and flip-flops')

ANCORAS = [
    ('anc-titi', f'Character reference of {TITI}, standing, three-quarter view, full body. Plain soft background.', None),
    ('anc-mae', f'Character reference of {MAE}, standing in a living room, three-quarter view, full body.', 'anc-titi'),
]

CENAS = [
    ('cena-01-a', f'{TITI} standing in front of a bright shop window, staring at an Xbox game console on display, '
                  f'longing on his face, city street.', ['anc-titi']),
    ('cena-01-b', f'Close-up of {TITI} pressing his hands against the shop glass, eyes wide with desire.', ['anc-titi']),
    ('cena-02-a', f'{TITI} at home asking {MAE}, hands together pleading, hopeful.', ['anc-titi', 'anc-mae']),
    ('cena-02-b', f'{MAE} explaining gently, shaking her head, kind but firm, in the living room.', ['anc-mae']),
    ('cena-03-a', f'Close-up of {TITI} thinking hard, an idea forming, looking at his old toys on a shelf.', ['anc-titi']),
    ('cena-03-b', f'{TITI} gathering his old toys into a cardboard box, determined, in his bedroom.', ['anc-titi']),
    ('cena-04-a', f'{TITI} setting up a small yard sale stand on the sidewalk with his toys laid out, sunny day.', ['anc-titi']),
    ('cena-04-b', f'{TITI} texting his friends on a phone, inviting them, sitting at his little stand.', ['anc-titi']),
    ('cena-05-a', f'Several children gathered around {TITI} little stand buying his toys, busy and cheerful.', ['anc-titi']),
    ('cena-05-b', f'Close-up of {TITI} counting money in his hands, sixty reais, proud smile.', ['anc-titi']),
    ('cena-06-a', 'A calendar on a wall with months flying past, seasons changing outside the window, time passing.', []),
    ('cena-06-b', f'{TITI} pouring a big pile of saved money out of a jar onto his bed, a whole year of saving, triumphant.',
     ['anc-titi']),
    ('cena-07-a', f'{TITI} and {MAE} searching in a busy electronics store, shelves empty of Xbox, disappointed.',
     ['anc-titi', 'anc-mae']),
    ('cena-07-b', f'{TITI} sitting sad at home, shoulders down, money beside him, nobody had the console.', ['anc-titi']),
    ('cena-08-a', f'{MAE} sitting beside {TITI} with a laptop, suggesting they look online, encouraging.',
     ['anc-titi', 'anc-mae']),
    ('cena-08-b', f'{TITI} and {MAE} looking at the laptop screen together, finding it, both excited.', ['anc-titi', 'anc-mae']),
    ('cena-09-a', f'{TITI} waiting by the front door looking out the window, impatient, days of waiting.', ['anc-titi']),
    ('cena-09-b', f'A delivery person handing a big box to {TITI} at the front door, the moment of arrival.', ['anc-titi']),
    ('cena-10-a', f'{TITI} tearing open the box on the living room floor, the Xbox inside, pure joy on his face.', ['anc-titi']),
    ('cena-10-b', f'{TITI} playing the Xbox on the TV with {MAE} smiling beside him on the sofa, warm happy ending.',
     ['anc-titi', 'anc-mae']),
]

NARRACAO = {
    1: 'Um dia, um menino chamado Titi viu um Xbox.',
    2: 'E falou para a mãe: mãe, me dá um! A mãe respondeu: é muito caro, não dá para comprar. '
       'Você pode começar a vender coisas.',
    3: 'Ele pensou e falou: vou vender meus brinquedos que não uso mais.',
    4: 'Ele montou uma barraquinha e mandou mensagem para os amigos.',
    5: 'E ganhou sessenta reais.',
    6: 'Depois de um ano, ele conseguiu todo o dinheiro.',
    7: 'Eles procuravam em todos os lugares e não achavam o Xbox. Em casa, triste,',
    8: 'a mãe falou: bora procurar na internet. Ele concordou. Procuraram, e acharam. Compraram.',
    9: 'Ele esperou.',
    10: 'Quando chegou, ele ficou muito feliz. Fim.',
}

MOVIMENTO = {
    1: 'the boy stares at the console through the shop window, the camera pushes in on his longing face',
    2: 'the boy pleads with his mother, she gently shakes her head explaining',
    3: 'the boy thinks, an idea lights his face, then he gathers his old toys into a box',
    4: 'the boy sets up his little stand and texts his friends, hopeful',
    5: 'children crowd around buying toys, then the boy counts his money proudly',
    6: 'time passes, the calendar flies, then the boy pours out a year of savings',
    7: 'the boy and his mother search the store shelves and find nothing, disappointment settles',
    8: 'the mother opens a laptop beside him, they search together and light up when they find it',
    9: 'the boy waits by the window, then the delivery arrives at the door',
    10: 'the boy tears open the box in joy, then plays happily with his mother beside him',
}
