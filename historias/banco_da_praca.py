# Vozes de Serenidade — vídeo motivacional/reflexão para TikTok e Kwai.
# Roda com:  python3 rodar.py banco_da_praca
#
# Pesquisa (jul/2026): conteúdo de reflexão que viraliza segue o arco
# situação difícil -> gesto/frase inesperada -> virada emocional, com temas
# universais (solidão, gentileza, presença entre gerações, "continuar
# aparecendo"). Texto de legenda/narração curto, close nos rostos, silêncio
# como recurso dramático.

TITULO = 'O Banco da Praça'
LEGENDA = ('🌅 O Banco da Praça | Vozes de Serenidade\n'
           'Às vezes a força que você precisa está em continuar aparecendo. 💛\n'
           '#VozesDeSerenidade #motivação #reflexão #paz #forçainterior')
VOZ = 'pt-BR-AntonioNeural'   # voz grave, tom contemplativo
TAMANHO = '736x1312'   # vertical 9:16, padrão TikTok/Kwai (mesma resolução testada, só rotacionada)

# Caminho pra uma trilha instrumental (mp3/wav) — calma, sem letra, royalty-free.
# Se o arquivo não existir, o vídeo sai sem música de fundo (só narração).
MUSICA = '~/Workspace/videos-agnes/musicas/reflexiva.mp3'

# Estilo cinematográfico realista — mais adequado a um público adulto de reflexão
# do que o Pixar 3D padrão do projeto (esse é usado só nesta história).
STYLE = ('cinematic realistic photography, soft golden hour lighting, shallow depth of field, '
         '35mm film grain, warm muted color grading, emotional and contemplative mood')

# Descrição fixa dos personagens — repetida literal em toda cena que aparecem.
VELHO = ('an elderly man in his 70s, kind weathered face, short white hair, wearing a simple '
         'beige cardigan over a light shirt')
JOVEM = ('a tired young woman in her late 20s, dark hair tied back, wearing a grey hoodie, '
         'carrying visible exhaustion in her posture')

# ANCORAS: model sheet. Cada personagem tem sua própria mãe (deriva_de=None);
# as demais vistas do MESMO personagem derivam dela.
ANCORAS = [
    ('anc-velho', f'Character reference of {VELHO}, sitting on a park bench, three-quarter view, '
                  f'full body, soft natural background.', None),
    ('anc-jovem', f'Character reference of {JOVEM}, standing, three-quarter view, full body, '
                  f'plain soft background.', None),
]

# CENAS: (id, prompt EN, [ids das refs — no máximo 2]). id no formato cena-NN-a / cena-NN-b.
CENAS = [
    # 1 — o velho, sozinho, todo dia no mesmo banco
    ('cena-01-a', f'{VELHO} sitting alone on a park bench in the early morning light, smiling gently '
                  f'at people passing by who do not notice him.', ['anc-velho']),
    ('cena-01-b', f'Close-up of {VELHO} face, warm patient smile, morning light, a quiet dignity.',
     ['anc-velho']),

    # 2 — a jovem, exausta, quase desistindo
    ('cena-02-a', f'{JOVEM} walking alone at dusk through the same park, looking down at her phone, '
                  f'shoulders slumped, visibly overwhelmed.', ['anc-jovem']),
    ('cena-02-b', f'Close-up of {JOVEM} face, eyes tired and holding back tears, streetlights blurred '
                  f'behind her.', ['anc-jovem']),

    # 3 — ela senta ao lado dele, silêncio, o dia se apaga
    ('cena-03-a', f'{JOVEM} sitting down on the same park bench next to {VELHO}, both looking forward '
                  f'in silence as the sunset colors the sky.', ['anc-velho', 'anc-jovem']),
    ('cena-03-b', f'Wide shot of {VELHO} and {JOVEM} sitting together on the bench, silhouetted against '
                  f'a warm orange sunset, peaceful stillness.', ['anc-velho', 'anc-jovem']),

    # 4 — a frase, a virada emocional
    ('cena-04-a', f'Close-up of {VELHO} turning his head gently to speak to {JOVEM}, warm compassionate '
                  f'expression, golden hour light on his face.', ['anc-velho']),
    ('cena-04-b', f'Close-up of {JOVEM} listening, a single tear on her cheek catching the light, the '
                  f'beginning of a soft relieved smile.', ['anc-jovem']),

    # 5 — o dia seguinte, ela volta
    ('cena-05-a', f'{JOVEM} walking back into the park the next morning under soft sunrise light, '
                  f'a small hopeful smile, posture lighter than before.', ['anc-jovem']),
    ('cena-05-b', f'Wide shot of {VELHO} and {JOVEM} sitting together on the bench at sunrise, both '
                  f'looking at the horizon, calm and connected.', ['anc-velho', 'anc-jovem']),
]

# NARRAÇÃO: texto PT por cena (passa pela revisão de dicção antes do TTS).
NARRACAO = {
    1: 'Todos os dias, seu Joaquim se sentava no mesmo banco da praça e sorria para quem passava. '
       'Quase ninguém parava.',
    2: 'Numa noite qualquer, Marina caminhava exausta, o coração pesado, prestes a desistir de tudo '
       'o que um dia sonhou.',
    3: 'Sem saber bem por quê, ela sentou-se ao lado dele. Os dois ficaram em silêncio, olhando o dia '
       'se apagar no horizonte.',
    4: 'Então ele disse: "Ninguém aplaude o sol nascendo todos os dias. Mas ele nunca deixou de nascer." '
       'Marina chorou, e por dentro, algo se acendeu.',
    5: 'No dia seguinte, ela voltou. E descobriu que a coragem, às vezes, mora só em continuar '
       'aparecendo.',
}

# MOVIMENTO: o que acontece entre o keyframe A e o B (em inglês).
MOVIMENTO = {
    1: 'the camera slowly pushes in on the old man smiling at passersby, morning light warming the scene',
    2: 'the young woman walks slowly through the park at dusk, the camera drifts closer to her tired face',
    3: 'she sits down next to him, the camera pulls back to a wide shot as the sunset deepens',
    4: 'he turns to speak, the camera cuts between his compassionate face and her welling tears',
    5: 'she walks back into the park at sunrise, camera settles on the two of them sitting together, still',
}
