---
name: imagens-agnes
description: Gera IMAGENS avulsas com a API Agnes AI (agnes-image-2.1-flash) a custo US$ 0, com todos os parâmetros e armadilhas já MEDIDOS. Use SEMPRE que o usuário pedir "gera uma imagem", "cria uma arte/ilustração", "imagem de X", "thumbnail", "capa", "mockup", ou quiser text2img/img2img/edição via Agnes. Cobre proporções, resoluções 1K-4K, referência de imagem (img2img), e as regras que evitam os defeitos conhecidos (texto, cauda/cabeça dupla, contaminação de estilo, filtro de conteúdo em PT). NÃO use para transformar história em filme (aí é videos-agnes).
---

# imagens-agnes — geração de imagem (Agnes AI, US$ 0)

Projeto: `~/projetos/imagens-agnes/` · CLI: `gerar.py`

```bash
cd ~/projetos/imagens-agnes
python3 gerar.py "a red fox in a snowy forest, cinematic" -o fox.png
python3 gerar.py "..." --ratio 1:1 --size 2K
python3 gerar.py "..." --ref base.png                 # img2img (1-2 refs; PNG local vira base64)
```

## Fatos MEDIDOS (fonte: `~/projetos/agnes-nei/NOTAS-API.md`, ~70 chamadas reais)

**Endpoint** `POST /v1/images/generations` · modelo `agnes-image-2.1-flash` · **US$ 0, sem créditos**.
Corpo: `model`, `prompt`, `size`, `ratio`, `extra_body.{image,response_format}`.

| Regra | Porquê |
|---|---|
| **Prompt em INGLÊS** | PT dispara o filtro de conteúdo → HTTP 400 em prompt legítimo |
| **`size` em pixels** (`1312x736`) | em img2img o `ratio` é IGNORADO (vira 1024²); pixels não |
| **Máx. 2 referências** | 3+ satura; 5 = confete + prompt ignorado |
| **Ref ≤ 10 MB** | 4K (23 MB) é rejeitada como entrada |
| **Base64 funciona** | PNG local vira `data:` URI — não precisa hospedar |
| **Retry com backoff** | ~34% de 503; retry recupera quase sempre |
| **Baixar na hora** | a URL de saída é temporária |

## Defeitos conhecidos e como evitar

- **Texto:** só curto e grande funciona (título, uma palavra). Texto denso vira sopa de letras.
  Sempre revisar a grafia à mão (já escreveu "SUU" por "SEU").
- **Cauda/cabeça dupla:** em pose **frontal simétrica**. Evitar frontal; usar perfil/três-quartos.
  E pedir `exactly one tail, one head` (POSITIVO — nunca "no two tails", que vira atrator).
- **Estilo sequestra o assunto:** "futurista" deixou esquilo ruivo prateado. Reforçar o atributo.
- **Descritor de estilo contamina cenário:** "expressive eyes/fur/children's book" injeta
  personagem numa paisagem. No estilo, só luz/cor/render.
- **Consistência entre imagens:** não há `seed`. Para o mesmo personagem, usar img2img com
  1-2 âncoras (não trava 100%, mas ajuda muito). Model sheet: derivar vistas de uma âncora-mãe.

## Estilos testados (matriz 10×2)
Pixar = mais obediente ao conteúdo · realista/cinematográfico = ótimos em cena · aquarela = lindo
em close mas erra personagem secundário · futurista = sequestra cor. Avatar humano fotorrealista
funciona bem (usar `--ratio 1:1` ou `3:4`).

## Resoluções
1K (`1312x736`, ~32s) = padrão. 2K = mais nitidez. 3K/4K = lento e mais 503, **e 4K não serve
de referência** depois (>10 MB). Ratios: `1:1 16:9 9:16 4:3 3:4 2:3 3:2 21:9`.

Pré-requisito: `AGNES_API_KEY` em `~/projetos/agnes-nei/.env`.
