"""Pipeline generico: historia -> filme narrado.

Encapsula TUDO que foi aprendido sobre a API Agnes AI, medido na pratica:

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

narracao (Edge TTS)
- TTS online (Microsoft), gratuito, sem GPU — sem daemon local, sem clonagem de voz.
- Usa vozes prontas PT-BR (default: pt-BR-FranciscaNeural).
- Requer pacote `edge-tts` (pip install edge-tts) e conexao com a internet.

--- Configuracao (env vars, com fallback pra config/ dentro do proprio projeto) ---
AGNES_ENV_PATH      caminho do .env com AGNES_API_KEY   (default: <projeto>/config/agnes.env)
TELEGRAM_ENV_PATH   caminho do .env do bot do Telegram   (default: <projeto>/config/telegram.env)
EDGE_TTS_VOICE      voz do Edge TTS a usar               (default: pt-BR-FranciscaNeural)
"""

import base64, json, os, shutil, subprocess, time, urllib.request, urllib.error

# ---------------------------------------------------------------- config ---

_PROJETO = os.path.dirname(os.path.abspath(__file__))


def _cfg_path(env_var, default):
    return os.path.expanduser(os.environ.get(env_var, default))

AGNES_ENV_PATH = _cfg_path('AGNES_ENV_PATH', os.path.join(_PROJETO, 'config', 'agnes.env'))
TELEGRAM_ENV_PATH = _cfg_path('TELEGRAM_ENV_PATH', os.path.join(_PROJETO, 'config', 'telegram.env'))
EDGE_TTS_VOICE = os.environ.get('EDGE_TTS_VOICE', 'pt-BR-FranciscaNeural')

IMG_API = 'https://apihub.agnes-ai.com/v1/images/generations'
VID_API = 'https://apihub.agnes-ai.com/v1/videos'
VID_GET = 'https://apihub.agnes-ai.com/agnesapi?video_id='

FPS, SEED = 24, 12345

STYLE_PADRAO = ('Pixar-style 3D animated feature film render, soft cinematic lighting, warm color palette, '
         'shallow depth of field, restrained natural saturation')
SO_UM = 'Exactly one of each character, one head each, no duplicates, natural anatomy.'
MESMO = ('Keep exactly the same characters as in the reference images: same faces, same hair color, '
         'same eye color, same clothes, same proportions.')


def _parse_env_file(path):
    """Le um .env simples: KEY=VALUE, ignora comentarios/linhas vazias, tira aspas e espacos."""
    if not os.path.exists(path):
        raise FileNotFoundError(
            f'arquivo de configuracao nao encontrado: {path}\n'
            f'  crie o arquivo (ex: echo "CHAVE=valor" > {path}) '
            f'ou aponte para o local certo via variavel de ambiente.')
    env = {}
    for line in open(path):
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def _check_ffmpeg():
    faltando = [b for b in ('ffmpeg', 'ffprobe') if shutil.which(b) is None]
    if faltando:
        raise RuntimeError(
            f'binarios ausentes no PATH: {", ".join(faltando)}. '
            f'Instale com: sudo apt install -y ffmpeg')


def _check_edge_tts():
    try:
        import edge_tts  # noqa: F401
    except ImportError:
        raise RuntimeError(
            'pacote "edge-tts" nao instalado. Instale com: '
            'pip install edge-tts --break-system-packages')


_check_ffmpeg()
_check_edge_tts()

_agnes_env = _parse_env_file(AGNES_ENV_PATH)
KEY = _agnes_env.get('AGNES_API_KEY')
if not KEY:
    raise RuntimeError(f'AGNES_API_KEY nao encontrada em {AGNES_ENV_PATH}')


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


def gerar_imagem(dest, prompt, refs=None, tentativas=5, estilo=None):
    """text2img (refs=None) ou img2img (<=2 refs). Devolve a URL publica.
    `estilo`: sobrescreve STYLE_PADRAO (ex: uma historia pode definir STYLE proprio)."""
    if refs and len(refs) > 2:
        raise ValueError(f'{len(refs)} refs — o teto util e 2 (NOTAS §5.1)')
    estilo = estilo or STYLE_PADRAO
    texto = f'{prompt} {MESMO} {SO_UM} {estilo}' if refs else f'{prompt} {SO_UM} {estilo}'
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
            print(f' [{os.path.basename(dest)}] {w}x{h} {len(b)//1024}KB · {len(refs) if refs else 0} refs', flush=True)
            return u
        except Exception as e:
            print(f' falha {t}: {str(e)[:80]}', flush=True)
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
            print(f' HTTP {e.code}: {msg}', flush=True)
            time.sleep(70 if e.code == 429 else 6 * t)  # 429 = rate limit 5/min
        except Exception as e:
            print(f' erro: {str(e)[:80]}', flush=True)
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
                print(f' [{os.path.basename(dest)}] {dur(dest):.1f}s', flush=True)
                return dest
            if st == 'failed':
                print(f' falhou: {json.dumps(d)[:150]}', flush=True)
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


def narrar(dest, texto, voz=None, tentativas=3):
    """TTS via Edge TTS (online, gratuito, sem GPU). Sem clonagem de voz —
    usa uma voz neural PT-BR pronta (default: pt-BR-FranciscaNeural).

    Vozes PT-BR disponiveis (as mais comuns): pt-BR-FranciscaNeural (feminina,
    tom caloroso — boa pra contos infantis), pt-BR-AntonioNeural (masculina).
    Lista completa: `edge-tts --list-voices | grep pt-BR`
    """
    import asyncio
    import edge_tts

    voz = voz or EDGE_TTS_VOICE

    async def _gerar():
        communicate = edge_tts.Communicate(texto, voz)
        await communicate.save(dest)

    for t in range(1, tentativas + 1):
        try:
            asyncio.run(_gerar())
            if os.path.exists(dest) and os.path.getsize(dest) > 0:
                return dur(dest)
        except Exception as e:
            print(f' falha narracao {t}: {str(e)[:80]}', flush=True)
            time.sleep(3 * t)
    return None


def frames_para(segundos):
    """8n+1, teto 441 (18.4s @24fps)."""
    n = round((segundos * FPS - 1) / 8)
    return max(9, min(441, int(n * 8 + 1)))


def _sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(' ffmpeg:', r.stderr[-200:])
    return r.returncode == 0


def _tem_audio(p):
    """True se o arquivo de video tiver alguma faixa de audio (musica/ambiente gerado pela Agnes)."""
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a',
                         '-show_entries', 'stream=index', '-of', 'csv=p=0', p],
                        capture_output=True, text=True)
    return bool(r.stdout.strip())


def _tempo_srt(t):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    ms = int(round((s - int(s)) * 1000))
    return f'{int(h):02d}:{int(m):02d}:{int(s):02d},{ms:03d}'


def _gerar_srt(dest, blocos):
    """blocos: lista de (inicio_seg, fim_seg, texto)"""
    linhas = []
    for i, (ini, fim, texto) in enumerate(blocos, 1):
        linhas.append(str(i))
        linhas.append(f'{_tempo_srt(ini)} --> {_tempo_srt(fim)}')
        linhas.append(texto)
        linhas.append('')
    open(dest, 'w', encoding='utf-8').write('\n'.join(linhas))


def montar(D, n_cenas, saida_base, musica_fundo=0.45, legendas=None):
    """Concatena os clipes; casa cada fala com seu clipe (padding, nunca corta fala).

    Os clipes de video da Agnes costumam vir com musica/ambiente proprios. Quando ha
    narracao, mixamos as duas faixas (narracao em volume cheio, musica em `musica_fundo`,
    0.0-1.0) em vez de descartar o audio original do clipe.

    `legendas`: dict opcional {numero_da_cena: texto} — se fornecido, queima legendas
    no video final, uma por cena, com o timing casado ao clipe.
    """
    T = f'{D}/tmp'
    os.makedirs(T, exist_ok=True)
    partes = []
    offset = 0.0
    blocos_srt = []
    for c in range(1, n_cenas + 1):
        vp, ap = f'{D}/video/clipe-{c:02d}.mp4', f'{D}/narracao/cena-{c:02d}.wav'
        if not os.path.exists(vp):
            continue
        dv = dur(vp)
        out = f'{T}/p{c:02d}.mp4'
        tem_narracao = os.path.exists(ap)
        tem_musica = _tem_audio(vp)
        dur_pedaco = dv  # duracao final desse pedaco, ajustada abaixo se houver narracao

        if tem_narracao and tem_musica:
            da = dur(ap)
            alvo = max(dv, da + 0.4)
            dur_pedaco = alvo
            ok = _sh(['ffmpeg', '-loglevel', 'error', '-i', vp, '-i', ap, '-filter_complex',
                      f'[0:v]tpad=stop_mode=clone:stop_duration={max(0,alvo-dv):.2f},'
                      f'trim=0:{alvo:.2f},setpts=PTS-STARTPTS[v];'
                      f'[0:a]volume={musica_fundo},apad=pad_dur={max(0,alvo-dv):.2f},'
                      f'atrim=0:{alvo:.2f},asetpts=PTS-STARTPTS[bg];'
                      f'[1:a]apad=pad_dur={max(0,alvo-da):.2f},atrim=0:{alvo:.2f},asetpts=PTS-STARTPTS[voice];'
                      f'[bg][voice]amix=inputs=2:duration=first:dropout_transition=0:normalize=0[a]',
                      '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '20',
                      '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-y', out])
        elif tem_narracao:
            da = dur(ap)
            alvo = max(dv, da + 0.4)
            dur_pedaco = alvo
            ok = _sh(['ffmpeg', '-loglevel', 'error', '-i', vp, '-i', ap, '-filter_complex',
                      f'[0:v]tpad=stop_mode=clone:stop_duration={max(0,alvo-dv):.2f},'
                      f'trim=0:{alvo:.2f},setpts=PTS-STARTPTS[v];'
                      f'[1:a]apad=pad_dur={max(0,alvo-da):.2f},atrim=0:{alvo:.2f},asetpts=PTS-STARTPTS[a]',
                      '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '20',
                      '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-y', out])
        elif tem_musica:
            ok = _sh(['ffmpeg', '-loglevel', 'error', '-i', vp, '-c', 'copy', '-y', out])
        else:
            ok = _sh(['ffmpeg', '-loglevel', 'error', '-i', vp, '-f', 'lavfi',
                      '-i', 'anullsrc=r=44100:cl=stereo', '-shortest', '-map', '0:v', '-map', '1:a',
                      '-c:v', 'copy', '-c:a', 'aac', '-y', out])
        if ok:
            partes.append(out)
            if legendas and legendas.get(c):
                blocos_srt.append((offset, offset + dur_pedaco, legendas[c]))
            offset += dur_pedaco
    if not partes:
        return None
    lst = f'{T}/lista.txt'
    open(lst, 'w').write('\n'.join(f"file '{p}'" for p in partes))
    final = f'{D}/{saida_base}.mp4'
    concat_dest = final
    if legendas and blocos_srt:
        concat_dest = f'{T}/concat-sem-legenda.mp4'
    _sh(['ffmpeg', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst,
         '-c:v', 'libx264', '-crf', '27', '-preset', 'slow', '-pix_fmt', 'yuv420p',
         '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', '-y', concat_dest])

    if legendas and blocos_srt:
        srt_path = f'{T}/legendas.srt'
        _gerar_srt(srt_path, blocos_srt)
        srt_escapado = srt_path.replace('\\', '\\\\').replace(':', '\\:').replace("'", "\\'")
        estilo = ("FontName=DejaVu Sans,FontSize=13,PrimaryColour=&H00FFFFFF,"
                  "OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=0,"
                  "Alignment=2,MarginV=60")
        ok_legenda = _sh(['ffmpeg', '-loglevel', 'error', '-i', concat_dest, '-vf',
                          f"subtitles='{srt_escapado}':force_style='{estilo}'",
                          '-c:v', 'libx264', '-crf', '23', '-preset', 'medium',
                          '-c:a', 'copy', '-movflags', '+faststart', '-y', final])
        if not ok_legenda:
            print(' falha ao queimar legenda — usando video sem legenda', flush=True)
            shutil.copy(concat_dest, final)

    mb = os.path.getsize(final) / 1048576
    print(f'>> {saida_base}: {dur(final):.1f}s · {mb:.1f}MB' + (' ⚠️ >50MB, Telegram recusa' if mb > 50 else ''))
    return final


def enviar_telegram(path, legenda):
    import uuid
    env = _parse_env_file(TELEGRAM_ENV_PATH)
    TOKEN, CHAT = env.get('TELEGRAM_BOT_TOKEN'), env.get('ALLOWED_CHAT_ID') or env.get('CHAT_ID')
    if not TOKEN or not CHAT:
        raise RuntimeError(f'TELEGRAM_BOT_TOKEN / ALLOWED_CHAT_ID ausentes em {TELEGRAM_ENV_PATH}')
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
        print(f' {"✅ enviado" if d.get("ok") else "❌"} {os.path.basename(path)} ({len(dados)//1048576}MB)')
        return d.get('ok')
    except Exception as e:
        print(f' ❌ envio: {str(e)[:150]}')
        return False
