"""imagens-agnes — CLI de geração de imagem (Agnes AI, agnes-image-2.1-flash, US$ 0).

Uso:
  python3 gerar.py "a red fox in a snowy forest, cinematic"           # text2img 16:9
  python3 gerar.py "..." -o saida.png --ratio 1:1 --size 2K           # quadro/resolução
  python3 gerar.py "..." --ref base.png                               # img2img (1-2 refs)
  python3 gerar.py "..." --ref a.png --ref b.png -o out.png           # 2 refs (teto útil)

Tudo que este CLI aplica foi MEDIDO (ver ~/projetos/agnes-nei/NOTAS-API.md). Ver README.
"""
import argparse, base64, json, os, struct, sys, time, urllib.request, urllib.error

ENV = '/home/nmaldaner/projetos/agnes-nei/.env'
API = 'https://apihub.agnes-ai.com/v1/images/generations'

# tabela de dimensões (16:9 e 1:1 confirmados por medição; demais conforme doc)
DIMS = {
    '1:1': {'1K': '1024x1024', '2K': '2048x2048', '3K': '3072x3072', '4K': '4096x4096'},
    '16:9': {'1K': '1312x736', '2K': '2624x1472', '3K': '3936x2208', '4K': '5248x2944'},
    '9:16': {'1K': '736x1312', '2K': '1472x2624', '3K': '2208x3936', '4K': '2944x5248'},
    '4:3': {'1K': '1152x864', '2K': '2304x1728', '3K': '3456x2592', '4K': '4608x3456'},
    '3:4': {'1K': '864x1152', '2K': '1728x2304', '3K': '2592x3456', '4K': '3456x4608'},
}


def key():
    for line in open(ENV):
        if line.startswith('AGNES_API_KEY='):
            return line.strip().split('=', 1)[1]
    raise SystemExit('AGNES_API_KEY não encontrada em ' + ENV)


def data_uri(path):
    return 'data:image/png;base64,' + base64.b64encode(open(path, 'rb').read()).decode()


def gerar(prompt, dest, ratio='16:9', size='1K', refs=None, tent=6):
    if refs and len(refs) > 2:
        print('⚠️  mais de 2 refs saturam e destroem a imagem (teto útil = 2). Usando as 2 primeiras.')
        refs = refs[:2]
    # size em pixels explícitos: em img2img o `ratio` é ignorado; pixels não são.
    px = DIMS.get(ratio, DIMS['16:9']).get(size, DIMS[ratio]['1K'])
    body = {'model': 'agnes-image-2.1-flash', 'prompt': prompt,
            'size': px, 'extra_body': {'response_format': 'url'}}
    if refs:
        body['extra_body']['image'] = [data_uri(r) if os.path.exists(r) else r for r in refs]
    r = urllib.request.Request(API, data=json.dumps(body).encode())
    r.add_header('Authorization', 'Bearer ' + key())
    r.add_header('Content-Type', 'application/json')
    for t in range(1, tent + 1):
        t0 = time.time()
        try:
            d = json.loads(urllib.request.urlopen(r, timeout=400).read())
            u = d['data'][0]['url']
            b = urllib.request.urlopen(u, timeout=180).read()
            open(dest, 'wb').write(b)
            w, h = struct.unpack('>II', b[16:24])
            print(f'✅ {dest}  {w}x{h}  {len(b)//1024}KB  {round(time.time()-t0)}s'
                  f'{"  ("+str(len(refs))+" refs)" if refs else ""}')
            print(f'   url: {u}')
            return u
        except urllib.error.HTTPError as e:
            msg = e.read()[:120].decode(errors='ignore')
            print(f'   tent {t}: HTTP {e.code} {msg}')
            if e.code == 400:      # filtro de conteúdo ou prompt inválido — retry não ajuda
                print('   ⚠️ 400 costuma ser o filtro de conteúdo (pior em PT). Tente reformular em INGLÊS.')
                return None
            time.sleep(4 * t)
        except Exception as e:
            print(f'   tent {t}: {str(e)[:90]}')
            time.sleep(4 * t)
    print('❌ falhou após', tent, 'tentativas (a API teve ~34% de 503 no dia do teste)')
    return None


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('prompt', help='descrição em INGLÊS (PT apanha do filtro de conteúdo)')
    ap.add_argument('-o', '--out', default='saida.png')
    ap.add_argument('--ratio', default='16:9', choices=list(DIMS) + ['2:3', '3:2', '21:9'])
    ap.add_argument('--size', default='1K', choices=['1K', '2K', '3K', '4K'])
    ap.add_argument('--ref', action='append', help='imagem de referência (PNG local ou URL). Até 2.')
    a = ap.parse_args()
    if a.size in ('3K', '4K'):
        print('⚠️  3K/4K: mais lento e com mais 503; 4K (>10MB) NÃO serve como referência depois.')
    gerar(a.prompt, a.out, a.ratio, a.size, a.ref)
