---
name: videos-agnes
description: Transforma uma HISTÓRIA/conto em FILME animado narrado (imagens + vídeo keyframe + narração PT-BR) usando a API Agnes AI (custo US$ 0), e entrega no Telegram do openpcbot. Use SEMPRE que o usuário der uma história, conto, roteiro infantil ou pedir "faz um filme dessa história", "transforma em vídeo", "vídeo animado do conto", "manda o filme no bot", ou passar personagens + enredo querendo um vídeo narrado. Cobre da história ao MP4 final: model sheet de personagens, 2 imagens por cena (início/fim), clipes de vídeo interpolando cada par, narração local (inemavox bella) e montagem. NÃO use para imagem avulsa (aí é imagens-agnes) nem vídeo sem história/personagens.
---

# videos-agnes — história → filme narrado (Agnes AI, US$ 0)

Projeto: `~/projetos/videos-agnes/` · Saída: `~/projetos/output/videos-agnes/<nome>/`

## Fluxo

Cada história é **um arquivo de spec** em `~/projetos/videos-agnes/historias/<nome>.py`.
Rodar de ponta a ponta (idempotente — reexecutar só refaz o que falta):

```bash
cd ~/projetos/videos-agnes && python3 rodar.py <nome>
```

Faz: **âncoras** (model sheet) → **cenas** (2 imgs/cena) → **revisão de dicção** → **narração** → **clipes** (keyframe A→B, duração casada com a fala) → **montagem** → **envio ao Telegram** (openpcbot).

## REGRA: revisar o texto antes da narração (`revisao.py`, automático)

As histórias vêm de **crianças**. Antes do TTS, `revisar(texto)` corrige **só o que a locução
erra**, nunca o português:
- **número/moeda por extenso** — `R$60` → "sessenta reais", `2 amigos` → "dois amigos"
  (senão o chatterbox lê "erre cifrão sessenta").
- abreviações de digitação (`vc`→você, `pq`→porque), pontuação de fala, reticências.

**Preserva a voz da criança** — não mexe em concordância, estilo ou grafia que não atrapalhe a fala.
Toda mudança é **registrada e impressa** (diff em `estado.json['revisao']`) — nada é editado em silêncio.
Se quiser corrigir o português também, é decisão explícita do usuário, não o default.

## Para uma história NOVA

1. Ler a história e o elenco. Traduzir personagens/cenas para prompts **em INGLÊS**.
2. Copiar `historias/alien.py` como molde e preencher:
   - `TITULO`, `LEGENDA`
   - blocos de personagem (descrição fixa, repetida literal em toda cena)
   - `ANCORAS` = `[(id, prompt, deriva_de)]` — 1 âncora-mãe em text2img (`deriva_de=None`),
     as demais **derivadas** dela (`deriva_de='anc-...'`) para serem o MESMO indivíduo.
   - `CENAS` = `[(id, prompt, [refs_ids])]` — id no formato `cena-NN-a`/`cena-NN-b`.
   - `NARRACAO` = `{n: texto_pt}` — o texto do conto fatiado por cena.
   - `MOVIMENTO` = `{n: descrição do movimento A→B em inglês}`.
3. Rodar. Conferir as folhas de contato ANTES de dar por pronto.

## Regras não-óbvias (medidas — ver `~/projetos/agnes-nei/NOTAS-API.md`)

- **Prompts em INGLÊS.** Em PT a API bloqueia conteúdo legítimo (HTTP 400 do filtro).
- **No máximo 2 referências por imagem.** 5 destroem a imagem (confete + prompt ignorado).
  Muitos personagens numa cena → usar **1 âncora de GRUPO** (várias pessoas juntas = 1 ref).
- **`size:"1312x736"` explícito**, nunca `ratio` (é ignorado em img2img → vira quadrado).
- **Model sheet: derivar, não gerar em paralelo.** Mãe em text2img, resto por img2img.
- **Nada de pose frontal simétrica** e sempre `exactly one ... one head` (positivo, nunca "no two").
- **Descritor de estilo só estético** (nada de "eyes"/"hair"/"fur" — injeta personagem no cenário).
- **Vídeo:** rate limit REAL 5 req/min (HTTP 429) — o pipeline já pausa. Base64 nos keyframes
  funciona. `num_frames ≤ 441` (18,4s @24fps), regra 8n+1. O `size` da resposta MENTE (mede com ffprobe).
- **~34% de 503** na geração — retry com backoff já embutido.
- **Narração define a duração:** gera a voz primeiro, cada clipe dura a fala da cena.

## Limitações conhecidas (avisar o usuário, não esconder)

- **Deriva de identidade:** personagem pode mudar de rosto entre cenas; não há seed na imagem.
- **Rosto humano** é mais frágil que animal/criatura.
- **Ação forte** (empurrar, alavanca) sai amenizada.
- Sempre revisar as folhas de contato e relatar o que saiu torto.

## Pré-requisitos

- `AGNES_API_KEY` em `~/projetos/agnes-nei/.env`
- inemavox daemon em `localhost:8010` (narração `bella` chatterbox)
- openpcbot `.env` com `TELEGRAM_BOT_TOKEN` + `ALLOWED_CHAT_ID` (envio)
- `ffmpeg`/`ffprobe` no PATH
