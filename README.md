# videos-agnes

História → filme animado narrado via **Agnes AI** (custo US$ 0). Você dá o conto e os
personagens; o pipeline devolve o MP4 narrado.

Guia: https://inematds.github.io/videos-agnes/guia/ · Skills: `videos-agnes` (filme) e `imagens-agnes` (imagem avulsa).

```bash
python3 rodar.py exemplo          # gera o filme de exemplo (âncoras→cenas→narração→clipes→montagem→Telegram)
cp historias/exemplo.py historias/minha.py   # e preencha
python3 rodar.py minha
```

---

# Documentação da API Agnes AI (medida na prática)

> Tudo abaixo saiu de **~70 chamadas reais**, não da documentação oficial. Onde a doc e a
> prática divergem, está marcado. Gateway: `apihub.agnes-ai.com` (roda **litellm** sobre **one-api**).
> Custo atual: **US$ 0** para imagem, vídeo e texto. Sem créditos.

## As 6 regras que valem dinheiro

1. **Prompts em INGLÊS.** Não por qualidade (é empatada) — porque em **português a API bloqueia
   conteúdo legítimo** com HTTP 400 (filtro de conteúdo). Ex.: "usar um galho como alavanca" foi
   recusado 4× em PT, passou de primeira em EN.
2. **No máximo 2 referências por imagem.** 5 destroem a saída (confete de pixels + o prompt é
   ignorado, vira cópia das âncoras). 1+1 (personagens diferentes) foi o melhor resultado.
3. **Retry com backoff é obrigatório.** ~34% das chamadas retornam **503**; o retry recupera quase 100%.
4. **Descritor de estilo só com estética.** Palavras como `fur`, `expressive eyes`, `children's book`
   **injetam personagens** em prompts de cenário (uma paisagem veio com uma menina no meio).
5. **1K para volume.** 4K custa ~150s/imagem e falha muito; 1K sai em ~32s. E **4K (23 MB) não serve
   como referência** depois (teto de 10 MB por imagem de entrada).
6. **Baixar o PNG na hora** — a URL de saída é temporária.

## Imagem — `agnes-image-2.1-flash`

`POST /v1/images/generations`

```bash
curl https://apihub.agnes-ai.com/v1/images/generations \
  -H "Authorization: Bearer $AGNES_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"agnes-image-2.1-flash","prompt":"...","size":"1312x736",
       "extra_body":{"response_format":"url"}}'
```

| Parâmetro | Notas |
|---|---|
| `model` | `agnes-image-2.1-flash` |
| `prompt` | **em inglês** |
| `size` | `1K`..`4K` **ou pixels exatos** (`1312x736`). Ver o ponto do `ratio` abaixo |
| `ratio` | `1:1 16:9 9:16 4:3 3:4 2:3 3:2 21:9`. Default `1:1` |
| `extra_body.image` | array de refs (URL pública ou **data URI base64**) → img2img |
| `extra_body.response_format` | `url` \| `b64_json`. **Não** pôr no nível raiz (HTTP 400) |

**Não existe `seed` nem LoRA** na imagem. Params desconhecidos são **descartados em silêncio**
(litellm `drop_params`) — HTTP 200 **não** prova que o parâmetro foi usado.

### Contradições medidas (doc × prática)

- ⚠️ **`ratio` é IGNORADO em img2img.** Pedir `1K`+`ratio:16:9` com referência volta **1024×1024**.
  **Contorno:** `size` em **pixels explícitos** (`"1312x736"`), sem `ratio`.
- ⚠️ O guia diz "3K/4K = 1 img/min". **Não observei esse limite** — duas chamadas 4K consecutivas
  passaram, sem 429.
- ⚠️ Não há **cota real** consultável. `/v1/dashboard/billing/*` devolve valores de preenchimento
  (`hard_limit_usd: 100000000`, `total_usage: 0`). O único medidor de saturação é a taxa de 503.

### Referências (`extra_body.image`) — o que preserva e o que não

- Preserva **estilo e composição** ✅. **NÃO** trava **identidade de personagem** com 1 ref (o rosto
  muda). Com **2 refs** a identidade melhora muito.
- **Model sheet:** gerar N vistas independentes em text2img dá N personagens diferentes. O certo é
  **1 âncora-mãe em text2img** e as demais vistas **derivadas dela via img2img** (mesmo indivíduo).
- Teto: **2 refs úteis**, **10 MB por imagem**.

### Defeitos do modelo e como evitar

- **Cauda/cabeça dupla** em **pose frontal simétrica** (bug de espelhamento). Evitar frontal (usar
  perfil/três-quartos) e pedir `exactly one tail, one head` — **positivo**; nunca "no two tails"
  (a negação vira atrator e o bug volta).
- **Texto:** curto e grande funciona (título, uma palavra); denso vira sopa de letras. Revisar a
  grafia à mão (o modelo já escreveu "SUU" por "SEU").
- **Estilo sequestra o assunto:** "futurista" deixou um esquilo ruivo prateado; "castanha" virou
  cupcake em 7/10 estilos. Reforçar o atributo no prompt.
- Modelo **forte em cenário/paisagem, fraco em personagem**. Avatar humano fotorrealista sai bem.

## Vídeo — `agnes-video-v2.0`

Assíncrono: `POST /v1/videos` → `GET /agnesapi?video_id=<ID>` (`queued`→`in_progress`→`completed`|`failed`).

```bash
curl -X POST https://apihub.agnes-ai.com/v1/videos \
  -H "Authorization: Bearer $AGNES_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"agnes-video-v2.0","prompt":"Smooth cinematic transition between the keyframes...",
       "num_frames":81,"frame_rate":24,"width":1312,"height":736,
       "extra_body":{"image":["<A>","<B>"],"mode":"keyframes"}}'
```

| Fato | Status |
|---|---|
| `mode: "keyframes"` com par A→B | ✅ interpola de verdade, personagem consistente no movimento |
| 3+ keyframes | ✅ aceito |
| **`seed`** | ✅ **existe no vídeo** (na imagem não!) · **`negative_prompt`** também |
| `num_frames` | ≤ **441** (18,4s @24fps), regra **8n+1**; `seconds = num_frames / frame_rate` |
| `mode: "ti2vid"` | ✅ imagem única + movimento sutil (uma âncora, deriva menos que A→B) |
| **RATE LIMIT — criação** | **5 requisições/min** no `POST /v1/videos` → HTTP 429 |
| **RATE LIMIT — status** | ⚠️ o **polling** (`GET /agnesapi`) TAMBÉM é limitado (`video status query rate limit`). Espaçar as consultas (≥15s), não só a criação |
| Keyframes por **base64** | ✅ funciona — a doc diz que exige URL pública, **mentira** |
| ⚠️ `size` da resposta **mente** | pede `1312x736`, entrega **1280x704** (nem 16:9 exato). **Medir com ffprobe** |
| Tempo | 19–50s por clipe de ~3,4s |

## Técnica multi-plano (FUTURO — parada por causa dos rate limits)

**Independente de modelo** — vale pra qualquer gerador de vídeo por keyframe (Agnes, Kling, Veo…),
não é específico da Agnes. Fica documentada aqui para adoção quando os limites de vídeo afrouxarem.

O problema: a interpolação A→B tem **dois defeitos distintos**.
1. **Defeito de vídeo** (dentro do clipe): o morph inventa o "entre" — objetos se atravessam,
   movimento vaza (o pássaro voa e a barraca "bate asas"), coisas surgem/caem sem razão, a roupa
   se deforma durante o gesto. Piora quanto mais **longo** o clipe (esticar pra 18s é onde desmorona).
2. **Defeito de imagem** (no corte entre clipes): `cena-N-b` e `cena-(N+1)-a` são gerados
   separadamente → derivam → a roupa/rosto **muda no corte**.

A técnica ataca os dois:
- **Planos curtos + corte seco** — quebrar cada beat da narração em 3–4 planos de ~3,4s
  (o ponto doce do modelo) em vez de 1 morph longo. Corte não interpola → zero defeito de vídeo.
  Mistura `keyframes` (A→B onde há ação) com `ti2vid` (imagem viva onde é só atmosfera).
- **Referência encadeada** — cada plano gera usando o **plano anterior** como referência
  (`extra_body.image=[frame_anterior]`), não só a âncora. A roupa/estado carrega adiante →
  mata o defeito de imagem no corte. (Testado: 3 planos da "noite gelada", figurino idêntico.)

Por que está **parada**: multiplica as chamadas de vídeo (1 clipe/cena → 3–4), e os **três** rate
limits de vídeo (criação 5/min + status query) tornam o forno longo demais hoje. Quando os limites
afrouxarem — ou num modelo sem esse gargalo — vira o default. Comprovado num teste de uma cena
(morph de 13s × 4 planos curtos cortados, mesma narração): o figurino se manteve e o movimento
ficou mais limpo.

## Modelos disponíveis (`GET /v1/models`)

`agnes-image-2.1-flash` · `agnes-image-2.0-flash` · `agnes-2.0-flash` (texto/visão) ·
`agnes-1.5-flash` · `agnes-video-v2.0`.

## Riscos

Sem SLA no plano gratuito; cotas e políticas podem mudar. No free, **seus dados podem treinar os
modelos** (salvo opt-out). Usar como camada gratuita de alto volume com fallback — nunca como
fornecedor único crítico.

---

## Como o pipeline aplica isso

`historias/<nome>.py` (spec) → `rodar.py`:

1. **Âncoras** — model sheet derivado (mãe em text2img, resto por img2img).
2. **Cenas** — 2 imagens por cena (A abre / B fecha), ≤ 2 refs, `size` em pixels.
3. **Revisão de dicção** (`revisao.py`) — número/moeda por extenso etc. antes do TTS, preservando o texto original.
4. **Narração** — inemavox `bella` (chatterbox) local; a fala define a duração de cada clipe.
5. **Clipes** — keyframe A→B, `num_frames` casado com a narração, throttle de 5/min.
6. **Montagem** — concatena, casa áudio/vídeo sem cortar fala, comprime, envia ao Telegram.

## Pré-requisitos

- `AGNES_API_KEY` em `~/projetos/agnes-nei/.env` (lida em runtime; nunca versionada)
- inemavox em `localhost:8010` (narração) · `ffmpeg`/`ffprobe` no PATH
- openpcbot `.env` com `TELEGRAM_BOT_TOKEN` + `ALLOWED_CHAT_ID` (envio)

## Estrutura

```
pipeline.py            motor (imagem, vídeo, TTS, montagem, envio)
rodar.py               orquestra uma história de ponta a ponta (idempotente)
revisao.py             revisão de dicção antes do TTS
historias/exemplo.py   molde comentado — copie para criar a sua
skills/                videos-agnes e imagens-agnes (as skills do projeto)
```
