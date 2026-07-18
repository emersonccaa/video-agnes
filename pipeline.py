"""Pipeline generico: historia -> filme narrado.

Encapsula TUDO que foi aprendido em 2026-07-17 (ver ~/projetos/agnes-nei/NOTAS-API.md):

  imagem (agnes-image-2.1-flash)
    - prompts em INGLES (o PT apanha do filtro de conteudo -> HTTP 400)
    - `size` em pixels explicitos ("1312x736"); `ratio` e IGNORADO em img2img
    - NO MAXIMO 2 referencias — 5 destroem a imagem (confete + prompt ignorado)
    - descritor de estilo so estetico (senao injeta personagem em cenario)
    - nada de pose frontal simetrica (duplica cauda/cabeca)
    - "exactly one" POSITIVO; nunca "never two" (negacao vira atrator)
    - ~34% de 503 -> retry com backoff obrigatorio
    - salvar a URL publica (o video precisa dela; base64 tambem serve)

  model sheet
    - ancora-mae em text2img; demais vistas DERIVADAS dela por img2img
      (gerar em paralelo produz personagens diferentes)

  video (agnes-video-v2.0)
    - mode "keyframes" com [A, B]; base64 funciona (a doc diz que nao)
    - RATE LIMIT REAL: 5 req/min -> HTTP 429. Unico limite real da API
    - `seed` existe aqui (na imagem nao)
    - num_frames <= 441 (18.4s @24fps), regra 8n+1
    - o `size` da resposta MENTE: pede 1312x736, entrega 1280x704 -> conferir com ffprobe

  montagem
    - narracao PRIMEIRO: a duracao da fala define num_frames de cada clipe
"""
import base64, json, os, subprocess, time, urllib.request, urllib.error

KEY = None
for line in open('/home/nmaldaner/projetos/agnes-nei/.env'):
    if line.startswith('AGNES_API_KEY='):
        KEY = line.strip().split('=', 1)[1]
IMG_API = 'https://apihub.agnes-ai.com/v1/images/generations'
VID_API = 'https://apihub.agnes-ai.com/v1/videos'
VID_GET = 'https://apihub.agnes-ai.com/agnesapi?video_id='
VOX = 'http://localhost:8010'
FPS, SEED = 24, 12345

STYLE = ('Pixar-style 3D animated feature film render, soft cinematic lighting, warm color palette, '
         'shallow depth of field, restrained natural saturation')
SO_UM = 'Exactly one of each character, one head each, no duplicates, natural anatomy.'
MESMO = ('Keep exactly the same characters as in the reference images: same faces, same hair color, '
         'same eye color, same clothes, same proportions.')


def _post(url, body, timeout=400):
    r = urllib.request.Request(url, data=json.dumps(body).encode())
    r.add_header('Authorization', 'Bearer ' + KEY)
    r.add_header('Content-Type', 'application/json')
    return json.loads(urllib.request.urlopen(r, timeout=timeout).read())


def _get(url, timeout=120):
    r = urllib.request.Request(url)
    r.add_header('Authorization', 'Bearer ' + KEY)
    return json.loads(urllib.request.urlopen(r, timeout=timeout).read())


def dur(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                        '-of', 'csv=p=0', p], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def gerar_imagem(dest, prompt, refs=None, tentativas=5):
    """text2img (refs=None) ou img2img (<=2 refs). Devolve a URL publica."""
    if refs and len(refs) > 2:
        raise ValueError(f'{len(refs)} refs — o teto util e 2 (NOTAS §5.1)')
    texto = f'{prompt} {MESMO} {SO_UM} {STYLE}' if refs else f'{prompt} {SO_UM} {STYLE}'
    body = {'model': 'agnes-image-2.1-flash', 'prompt': texto,
            'size': '1312x736', 'extra_body': {'response_format': 'url'}}
    if refs:
        body['extra_body']['image'] = refs
    for t in range(1, tentativas + 1):
        try:
            d = _post(IMG_API, body)
            u = d['data'][0]['url']
            b = urllib.request.urlopen(u, timeout=180).read()
            open(dest, 'wb').write(b)
            import struct
            w, h = struct.unpack('>II', b[16:24])
            print(f'  [{os.path.basename(dest)}] {w}x{h} {len(b)//1024}KB · {len(refs) if refs else 0} refs', flush=True)
            return u
        except Exception as e:
            print(f'    falha {t}: {str(e)[:80]}', flush=True)
            time.sleep(4 * t)
    return None


def gerar_video(dest, kf_a, kf_b, prompt, frames, tentativas=4):
    body = {'model': 'agnes-video-v2.0',
            'prompt': f'Smooth cinematic transition between the keyframes: {prompt}. '
                      f'Natural motion, consistent characters and style, cinematic camera.',
            'num_frames': frames, 'frame_rate': FPS, 'seed': SEED,
            'width': 1312, 'height': 736,
            'extra_body': {'image': [kf_a, kf_b], 'mode': 'keyframes'}}
    vid = None
    for t in range(1, tentativas + 1):
        try:
            d = _post(VID_API, body, timeout=300)
            vid = d.get('video_id') or d.get('task_id') or d.get('id')
            break
        except urllib.error.HTTPError as e:
            msg = e.read()[:120].decode(errors='ignore')
            print(f'    HTTP {e.code}: {msg}', flush=True)
            time.sleep(70 if e.code == 429 else 6 * t)   # 429 = rate limit 5/min
        except Exception as e:
            print(f'    erro: {str(e)[:80]}', flush=True)
            time.sleep(6 * t)
    if not vid:
        return None
    t0 = time.time()
    while time.time() - t0 < 1800:
        try:
            d = _get(VID_GET + vid)
            st = d.get('status')
            if st == 'completed':
                u = d.get('url') or (d.get('data') or [{}])[0].get('url') or d.get('video_url')
                if not u:
                    return None
                open(dest, 'wb').write(urllib.request.urlopen(u, timeout=300).read())
                print(f'  [{os.path.basename(dest)}] {dur(dest):.1f}s', flush=True)
                return dest
            if st == 'failed':
                print(f'    falhou: {json.dumps(d)[:150]}', flush=True)
                return None
        except Exception:
            pass
        time.sleep(12)
    return None


def keyframe(png, url=None):
    """URL publica, ou data URI base64 do PNG local (funciona, apesar da doc dizer que nao)."""
    if url:
        return url
    return 'data:image/png;base64,' + base64.b64encode(open(png, 'rb').read()).decode()


def narrar(dest, texto, voz='bella', ref_dir='/home/nmaldaner/projetos/timesmkt3/media/voice-refs'):
    """TTS local (inemavox chatterbox). bella = tom de storytelling."""
    import uuid
    ref = f'{ref_dir}/{voz}.wav'
    cfg = {'text': texto, 'engine': 'chatterbox', 'voice': voz, 'lang': 'pt'}
    b = '----inema' + uuid.uuid4().hex
    partes = [f'--{b}\r\nContent-Disposition: form-data; name="config_json"\r\n\r\n{json.dumps(cfg)}\r\n'.encode(),
              f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="{voz}.wav"\r\n'
              f'Content-Type: audio/wav\r\n\r\n'.encode() + open(ref, 'rb').read() + b'\r\n',
              f'--{b}--\r\n'.encode()]
    r = urllib.request.Request(f'{VOX}/api/jobs/tts/upload', data=b''.join(partes))
    r.add_header('Content-Type', f'multipart/form-data; boundary={b}')
    j = json.loads(urllib.request.urlopen(r, timeout=120).read())
    jid = j.get('job_id') or j.get('id')
    t0 = time.time()
    while time.time() - t0 < 900:
        d = json.loads(urllib.request.urlopen(f'{VOX}/api/jobs/{jid}', timeout=30).read())
        if d.get('status') in ('completed', 'done', 'finished'):
            open(dest, 'wb').write(urllib.request.urlopen(f'{VOX}/api/jobs/{jid}/audio', timeout=180).read())
            return dur(dest)
        if d.get('status') in ('failed', 'error'):
            return None
        time.sleep(5)
    return None


def frames_para(segundos):
    """8n+1, teto 441 (18.4s @24fps)."""
    n = round((segundos * FPS - 1) / 8)
    return max(9, min(441, int(n * 8 + 1)))


def _sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print('   ffmpeg:', r.stderr[-200:])
    return r.returncode == 0


def montar(D, n_cenas, saida_base):
    """Concatena os clipes; casa cada fala com seu clipe (padding, nunca corta fala)."""
    T = f'{D}/tmp'
    os.makedirs(T, exist_ok=True)
    partes = []
    for c in range(1, n_cenas + 1):
        vp, ap = f'{D}/video/clipe-{c:02d}.mp4', f'{D}/narracao/cena-{c:02d}.wav'
        if not os.path.exists(vp):
            continue
        dv = dur(vp)
        out = f'{T}/p{c:02d}.mp4'
        if os.path.exists(ap):
            da = dur(ap)
            alvo = max(dv, da + 0.4)
            ok = _sh(['ffmpeg', '-loglevel', 'error', '-i', vp, '-i', ap, '-filter_complex',
                      f'[0:v]tpad=stop_mode=clone:stop_duration={max(0,alvo-dv):.2f},'
                      f'trim=0:{alvo:.2f},setpts=PTS-STARTPTS[v];'
                      f'[1:a]apad=pad_dur={max(0,alvo-da):.2f},atrim=0:{alvo:.2f},asetpts=PTS-STARTPTS[a]',
                      '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '20',
                      '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-y', out])
        else:
            ok = _sh(['ffmpeg', '-loglevel', 'error', '-i', vp, '-f', 'lavfi',
                      '-i', 'anullsrc=r=44100:cl=stereo', '-shortest', '-c:v', 'copy',
                      '-c:a', 'aac', '-y', out])
        if ok:
            partes.append(out)
    if not partes:
        return None
    lst = f'{T}/lista.txt'
    open(lst, 'w').write('\n'.join(f"file '{p}'" for p in partes))
    final = f'{D}/{saida_base}.mp4'
    _sh(['ffmpeg', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst,
         '-c:v', 'libx264', '-crf', '27', '-preset', 'slow', '-pix_fmt', 'yuv420p',
         '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', '-y', final])
    mb = os.path.getsize(final) / 1048576
    print(f'>> {saida_base}: {dur(final):.1f}s · {mb:.1f}MB' + ('  ⚠️ >50MB, Telegram recusa' if mb > 50 else ''))
    return final


def enviar_telegram(path, legenda):
    import uuid
    env = {}
    for line in open('/home/nmaldaner/projetos/openpcbot/.env'):
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            env[k] = v.strip().strip('"').strip("'")
    TOKEN, CHAT = env.get('TELEGRAM_BOT_TOKEN'), env.get('ALLOWED_CHAT_ID') or env.get('CHAT_ID')
    b = '----tg' + uuid.uuid4().hex
    dados = open(path, 'rb').read()
    p = []
    for k, v in (('chat_id', CHAT), ('caption', legenda), ('supports_streaming', 'true')):
        p.append(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    p.append(f'--{b}\r\nContent-Disposition: form-data; name="video"; filename="{os.path.basename(path)}"\r\n'
             f'Content-Type: video/mp4\r\n\r\n'.encode() + dados + b'\r\n')
    p.append(f'--{b}--\r\n'.encode())
    r = urllib.request.Request(f'https://api.telegram.org/bot{TOKEN}/sendVideo', data=b''.join(p))
    r.add_header('Content-Type', f'multipart/form-data; boundary={b}')
    try:
        d = json.loads(urllib.request.urlopen(r, timeout=900).read())
        print(f'  {"✅ enviado" if d.get("ok") else "❌"} {os.path.basename(path)} ({len(dados)//1048576}MB)')
        return d.get('ok')
    except Exception as e:
        print(f'  ❌ envio: {str(e)[:150]}')
        return False
