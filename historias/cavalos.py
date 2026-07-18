# "A Menina que Adorava Cavalos" — Aurora
# Elenco conforme a autora (roupas incluidas, que sao parte da identidade visual).

TITULO = 'A Menina que Adorava Cavalos — Aurora'
LEGENDA = ('A Menina que Adorava Cavalos\n'
           '10 cenas · imagens agnes-image-2.1-flash · video keyframes agnes-video-v2.0 · '
           'narracao bella local. Custo US$ 0.')

AURORA = ('Aurora, a girl about ten years old with straight red hair and greenish-blue eyes, '
          'wearing dark blue jeans, a plaid shirt, a dark blue denim jacket and light leather boots')
PAI = ('Aurora\'s father, an adult man with red hair and blue eyes, wearing jeans, a red shirt and leather shoes')
MAE = ('Aurora\'s mother, an adult woman with wavy dark brown hair and brown eyes, wearing jeans, '
       'a plaid shirt and leather boots')
IRMA = ('Aurora\'s older sister, a teenage girl wearing bell-bottom trousers, a Stranger Things t-shirt and sneakers')
INDIO = 'Índio, a strong brown horse'
ESTRELA = 'Estrela, a fast elegant mare'

ANCORAS = [
    ('anc-aurora', f'Character reference of {AURORA}, standing in a stable yard, three-quarter view, full body. '
                   f'Plain soft background.', None),
    ('anc-familia', f'Character reference sheet: {PAI}, {MAE} and {IRMA} standing side by side on a farm, '
                    f'three-quarter view, full body.', 'anc-aurora'),
]

CENAS = [
    ('cena-01-a', f'{AURORA} hugging a goat and surrounded by farm animals, chickens and a dog, sunny farm, '
                  f'she adores them, wide shot.', ['anc-aurora']),
    ('cena-01-b', f'Close-up of {AURORA} smiling with a puppy in her arms, pure affection for animals.', ['anc-aurora']),
    ('cena-02-a', f'{PAI} standing proudly beside {INDIO} in a paddock, holding the reins.', ['anc-familia']),
    ('cena-02-b', f'{AURORA} trying to ride {INDIO} clumsily, wobbling in the saddle, unsure, her father steadying her.',
     ['anc-aurora', 'anc-familia']),
    ('cena-03-a', f'{PAI} and {MAE} talking together in the kitchen, having an idea, warm light.', ['anc-familia']),
    ('cena-03-b', f'{AURORA} arriving at a riding school, looking up at the big arena, nervous and excited.', ['anc-aurora']),
    ('cena-04-a', f'{IRMA} introducing her friend, a girl who rides well, to {AURORA} at the riding school.',
     ['anc-aurora', 'anc-familia']),
    ('cena-04-b', f'The friend showing {AURORA} how to hold the reins properly, teaching, patient.', ['anc-aurora']),
    ('cena-05-a', f'{AURORA} practicing riding in the arena, still awkward, determined, dust in the light.', ['anc-aurora']),
    ('cena-05-b', f'{AURORA} riding confidently now, posture perfect, time has passed, proud.', ['anc-aurora']),
    ('cena-06-a', f'{AURORA} meeting {ESTRELA} for the first time, touching her nose gently, connection.', ['anc-aurora']),
    ('cena-06-b', f'{AURORA} galloping fast on {ESTRELA} across an open field, hair flying, joy and speed.', ['anc-aurora']),
    ('cena-07-a', f'{AURORA} studying at a desk with books, focused, improving at school, lamp light.', ['anc-aurora']),
    ('cena-07-b', f'{AURORA} holding a good school report, her parents proud behind her.', ['anc-aurora', 'anc-familia']),
    ('cena-08-a', f'A riding competition arena full of people, flags, other riders warming up, big day.', []),
    ('cena-08-b', f'{AURORA} riding {ESTRELA} in the competition, jumping an obstacle, intense focus.', ['anc-aurora']),
    ('cena-09-a', f'{AURORA} on the podium receiving the second place ribbon, smiling, {ESTRELA} beside her.', ['anc-aurora']),
    ('cena-09-b', f'{AURORA} hugging {ESTRELA} neck, medal on her chest, her family cheering, emotional.',
     ['anc-aurora', 'anc-familia']),
    ('cena-10-a', f'{AURORA} riding {ESTRELA} at golden hour along a country trail, peaceful, free.', ['anc-aurora']),
    ('cena-10-b', f'Wide shot of {AURORA} and {ESTRELA} silhouetted riding into a golden sunset, she still rides, ending.',
     ['anc-aurora']),
]

NARRACAO = {
    1: 'Uma menina muito linda e legal adorava os animais. Ela se chamava Aurora.',
    2: 'Seu pai tinha um cavalo chamado Índio. Ela ainda não sabia andar muito bem a cavalo.',
    3: 'Então, seu pai e sua mãe tiveram a ideia de colocá-la em uma escola de equitação.',
    4: 'A irmã de Aurora tinha uma amiga que sabia cavalgar e era muito legal.',
    5: 'O tempo passou, e Aurora aprendeu a andar a cavalo.',
    6: 'Ela cavalgava uma égua chamada Estrela, que era muito veloz.',
    7: 'Aurora também melhorou nos estudos.',
    8: 'E participou de uma competição de montaria.',
    9: 'Na qual conquistou o segundo lugar.',
    10: 'Ela ainda cavalga por aí.',
}

MOVIMENTO = {
    1: 'the girl plays among the farm animals, the camera pushes in as she hugs a puppy',
    2: 'the father stands with his horse, then the girl wobbles clumsily in the saddle',
    3: 'the parents talk and decide, then the girl arrives at the riding school looking up in awe',
    4: 'the sister introduces her friend, who shows the girl how to hold the reins',
    5: 'the girl practices awkwardly, then rides with confidence, time passing',
    6: 'the girl meets the mare gently, then gallops fast across the open field, hair flying',
    7: 'the girl studies at her desk, then proudly shows her report to her parents',
    8: 'the competition arena fills with people, then the girl jumps an obstacle with intense focus',
    9: 'the girl receives the second place ribbon on the podium, then hugs her mare, emotional',
    10: 'the girl rides along the trail at golden hour and into the sunset, peaceful and free',
}
