"""Roda uma historia de ponta a ponta: ancoras -> imagens -> narracao -> clipes -> filme -> Telegram.

  python3 rodar.py alien
  python3 rodar.py diabrotic
  python3 rodar.py xbox

Idempotente em cada etapa: reexecutar so refaz o que falta.
"""
import importlib, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # chamável de qualquer cwd
import pipeline as P
from revisao import revisar   # revisão de dicção ANTES do TTS (preserva a voz da criança)

nome = sys.argv[1] if len(sys.argv) > 1 else 'alien'
H = importlib.import_module(f'historias.{nome}')
D = f'/home/nmaldaner/projetos/output/videos-agnes/{nome}'
for sub in ('', '/video', '/narracao'):
    os.makedirs(D + sub, exist_ok=True)

est = f'{D}/estado.json'
S = json.load(open(est)) if os.path.exists(est) else {'urls': {}, 'dur': {}}


def salvar():
    json.dump(S, open(est, 'w'), indent=2)


print(f'\n{"="*60}\n{H.TITULO}\n{"="*60}', flush=True)

# ---------- 1. MODEL SHEET (mae em text2img; demais DERIVADAS) ----------
print('\n[1/5] ÂNCORAS', flush=True)
for i, (aid, prompt, deriva_de) in enumerate(H.ANCORAS):
    png = f'{D}/{aid}.png'
    if aid in S['urls'] and os.path.exists(png):
        print(f'  [{aid}] ok', flush=True)
        continue
    refs = [S['urls'][deriva_de]] if deriva_de and deriva_de in S['urls'] else None
    u = P.gerar_imagem(png, prompt, refs)
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
    u = P.gerar_imagem(png, prompt, refs or None)
    if u:
        S['urls'][cid] = u
        salvar()

# ---------- 3. NARRAÇÃO (define a duração dos clipes) ----------
print('\n[3/5] NARRAÇÃO (revisada antes do TTS)', flush=True)
S.setdefault('revisao', {})
for c, texto in sorted(H.NARRACAO.items()):
    wav = f'{D}/narracao/cena-{c:02d}.wav'
    if os.path.exists(wav) and str(c) in S['dur']:
        continue
    # REVISÃO: só o que a locução erra (número/moeda/abreviação/pontuação). Nunca o português.
    texto_rev, mudancas = revisar(texto)
    if mudancas:
        print(f'  [cena {c:02d}] revisão:', '; '.join(f'"{a}"→"{b}"' for a, b in mudancas), flush=True)
        S['revisao'][str(c)] = [[a, b] for a, b in mudancas]
        salvar()
    d = P.narrar(wav, texto_rev, voz=getattr(H, 'VOZ', 'bella'))
    if d:
        S['dur'][str(c)] = d
        salvar()
        print(f'  [cena {c:02d}] {d:.1f}s', flush=True)
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
filme = P.montar(D, max(H.NARRACAO), f'filme-{nome}')
if filme:
    P.enviar_telegram(filme, H.LEGENDA)
print('\nFIM', flush=True)
