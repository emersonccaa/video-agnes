# Exemplo/molde de história. Copie este arquivo para historias/<nome>.py e preencha.
# Roda com:  python3 rodar.py exemplo

TITULO = 'O Pequeno Robô que Aprendeu a Sonhar (exemplo)'
LEGENDA = ('O Pequeno Robô que Aprendeu a Sonhar (exemplo)\n'
           'Gerado com videos-agnes · imagens + video keyframe + narracao local. Custo US$ 0.')
VOZ = 'bella'   # voz do inemavox (chatterbox)

# Descrição fixa dos personagens — repetida literal em toda cena que o personagem aparece.
ROBO = ('Biel, a small friendly round robot with a glowing blue screen face, short antenna, '
        'smooth white and orange body')

# ANCORAS: model sheet. A mãe em text2img (deriva_de=None); as demais DERIVADAS dela (mesmo indivíduo).
ANCORAS = [
    ('anc-robo', f'Character reference of {ROBO}, standing in a workshop, three-quarter view, full body. '
                 f'Plain soft background.', None),
]

# CENAS: (id, prompt EN, [ids das refs — no máximo 2]). id no formato cena-NN-a / cena-NN-b.
CENAS = [
    ('cena-01-a', f'{ROBO} sitting alone in a quiet workshop at night, looking at the stars through a window.', ['anc-robo']),
    ('cena-01-b', f'Close-up of {ROBO}, blue screen face showing a tiny dreaming star, wonder.', ['anc-robo']),
    ('cena-02-a', f'{ROBO} building a small paper rocket on a workbench, focused and hopeful.', ['anc-robo']),
    ('cena-02-b', f'{ROBO} launching the little rocket out the window into the starry sky, joyful.', ['anc-robo']),
]

# NARRAÇÃO: texto PT por cena (passa pela revisão de dicção antes do TTS).
NARRACAO = {
    1: 'Era uma vez um pequeno robô chamado Biel, que vivia sozinho numa oficina e olhava as estrelas.',
    2: 'Um dia, Biel construiu um foguete de papel e o lançou para o céu, aprendendo a sonhar.',
}

# MOVIMENTO: o que acontece entre o keyframe A e o B (em inglês).
MOVIMENTO = {
    1: 'the little robot looks up at the stars, the camera pushes in on its dreaming face',
    2: 'the robot builds a paper rocket and launches it out the window into the night sky',
}
