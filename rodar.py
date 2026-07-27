"""Roda uma historia de ponta a ponta: ancoras -> imagens -> narracao -> clipes -> filme -> Telegram.

  python3 rodar.py alien
  python3 rodar.py diabrotic
  python3 rodar.py xbox

Idempotente em cada etapa: reexecutar so refaz o que falta.

Saida: OUTPUT_DIR/NNNN-<nome> (env var OUTPUT_DIR, default: <pasta do projeto>/output)
Cada historia ganha uma pasta numerada sequencialmente (0001-, 0002-, ...). Rodar de novo
o mesmo <nome> reaproveita a pasta ja numerada — nao cria uma nova a cada execucao.
"""
import importlib, json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # chamável de qualquer cwd
import pipeline as P
from revisao import revisar   # revisão de dicção ANTES do TTS (preserva a voz da criança)

nome = sys.argv[1] if len(sys.argv) > 1 else 'alien'
H = importlib.import_module(f'historias.{nome}')

_PROJETO = os.path.dirname(os.path.abspath(__file__))
_OUTPUT_BASE = os.path.expanduser(os.environ.get('OUTPUT_DIR', os.path.join(_PROJETO, 'output')))


def _diretorio_numerado(base, nome):
    """Acha a pasta NNNN-<nome> ja existente (reaproveita) ou cria a proxima numerada."""
    os.makedirs(base, exist_ok=True)
    existentes = [d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))]
    padrao_este = re.compile(r'^(\d{4})-' + re.escape(nome) + r'$')
    for d in existentes:
        if padrao_este.match(d):
            return os.path.join(base, d)
    numeros = [int(m.group(1)) for d in existentes if (m := re.match(r'^(\d{4})-', d))]
    proximo = max(numeros, default=0) + 1
    return os.path.join(base, f'{proximo:04d}-{nome}')


D = _diretorio_numerado(_OUTPUT_BASE, nome)
print(f'📁 pasta: {D}', flush=True)
for sub in ('', '/video', '/narracao'):
    os.makedirs(D + sub, exist_ok=True)

est = f'{D}/estado.json'
S = json.load(open(est)) if os.path.exists(est) else {'urls': {}, 'dur': {}}


def salvar():
    json.dump(S, open(est, 'w'), indent=2)


print(f'\n{"="*60}\n{H.TITULO}\n{"="*60}', flush=True)
_estilo = getattr(H, 'STYLE', None)

# ---------- 1. MODEL SHEET (mae em text2img; demais DERIVADAS) ----------
print('\n[1/5] ÂNCORAS', flush=True)
for i, (aid, prompt, deriva_de) in enumerate(H.ANCORAS):
    png = f'{D}/{aid}.png'
    if aid in S['urls'] and os.path.exists(png):
        print(f'  [{aid}] ok', flush=True)
        continue
    refs = [S['urls'][deriva_de]] if deriva_de and deriva_de in S['urls'] else None
    u = P.gerar_imagem(png, prompt, refs, estilo=_estilo)
    if u:
        S['urls'][aid] = u
        salvar()

# ---------- 2. CENAS ----------
print('\n[2/5] CENAS', flush=True)
for cid, prompt, refs_ids in H.CENAS:
    png = f'{D}/{cid}.png'
    if cid in S['urls'] and os.path.exists(png):
        print(f'  [{cid}] ok', flush=True)
        continue
    refs = [S['urls'][r] for r in refs_ids if r in S['urls']][:2]   # teto util = 2
    u = P.gerar_imagem(png, prompt, refs or None, estilo=_estilo)
    if u:
        S['urls'][cid] = u
        salvar()

# ---------- 3. NARRAÇÃO (define a duração dos clipes) ----------
print('\n[3/5] NARRAÇÃO (revisada antes do TTS)', flush=True)
S.setdefault('revisao', {})
S.setdefault('textos', {})
for c, texto in sorted(H.NARRACAO.items()):
    wav = f'{D}/narracao/cena-{c:02d}.wav'
    # REVISÃO: só o que a locução erra (número/moeda/abreviação/pontuação). Nunca o português.
    texto_rev, mudancas = revisar(texto)
    S['textos'][str(c)] = texto_rev
    if os.path.exists(wav) and str(c) in S['dur']:
        continue
    if mudancas:
        print(f'  [cena {c:02d}] revisão:', '; '.join(f'"{a}"→"{b}"' for a, b in mudancas), flush=True)
        S['revisao'][str(c)] = [[a, b] for a, b in mudancas]
        salvar()
    # voz: usa H.VOZ se a história definir (ex: 'pt-BR-AntonioNeural'), senao o default do Edge TTS
    d = P.narrar(wav, texto_rev, voz=getattr(H, 'VOZ', None))
    if d:
        S['dur'][str(c)] = d
        salvar()
        print(f'  [cena {c:02d}] {d:.1f}s', flush=True)
salvar()
total = sum(S['dur'].values())
print(f'  narração total: {total:.0f}s', flush=True)

# ---------- 4. CLIPES (keyframe A->B, duração casada com a fala) ----------
print('\n[4/5] CLIPES', flush=True)
feitos = 0
for c in sorted(H.NARRACAO):
    mp4 = f'{D}/video/clipe-{c:02d}.mp4'
    if os.path.exists(mp4):
        continue
    a, b = f'cena-{c:02d}-a', f'cena-{c:02d}-b'
    if not (os.path.exists(f'{D}/{a}.png') and os.path.exists(f'{D}/{b}.png')):
        print(f'  [clipe {c:02d}] sem keyframe', flush=True)
        continue
    fr = P.frames_para(S['dur'].get(str(c), 3.4))
    if feitos and feitos % 4 == 0:      # rate limit REAL do video: 5/min
        print('  ... pausa 65s (rate limit 5/min)', flush=True)
        time.sleep(65)
    P.gerar_video(mp4, P.keyframe(f'{D}/{a}.png', S['urls'].get(a)),
                  P.keyframe(f'{D}/{b}.png', S['urls'].get(b)),
                  H.MOVIMENTO[c], fr)
    feitos += 1

# ---------- 5. MONTAGEM + ENVIO ----------
print('\n[5/5] MONTAGEM', flush=True)
legendas = {int(c): t for c, t in S.get('textos', {}).items()}
filme = P.montar(D, max(H.NARRACAO), f'filme-{nome}', legendas=legendas)
if filme:
    P.enviar_telegram(filme, H.LEGENDA)
print('\nFIM', flush=True)
