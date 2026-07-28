# PROGRESS

Registro do que foi feito no projeto `videos-agnes`, na ordem em que aconteceu.
**Entradas mais recentes no topo.** Serve pra qualquer sessão (sua ou de uma IA) saber
onde as coisas pararam sem precisar reconstruir tudo de novo pelo `git log`.

Cada entrada: **o que mudou** → **valor que agrega** (por quê importa).

---

## 2026-07-27 21:00–21:05 — Capa nova sem marca de terceiro

**O que mudou:**
- A entrada anterior já tinha purgado `capa/capa.png` do histórico por ter a marca
  "INEMA.CLUB" **composta nos pixels da imagem** (não era texto pesquisável — só foi
  achada revisando a imagem manualmente, não por grep). O arquivo tinha ficado sem
  substituto.
- Gerada capa nova: mesma foto do `guia/assets/hero.png` (já sem marca), composta com
  título "videos-agnes" e um selo neutro "IA · VÍDEO" — nada de branding de terceiro,
  só o nome do próprio projeto. Composição feita com PIL local (fundo + foto + texto),
  não pela API Agnes, pra ter texto nítido garantido.
- A capa também **não tinha uso** (não aparecia nem no `guia/index.html` nem no
  `README.md`). Agora está referenciada no topo do `README.md`.

**Valor agregado:** fecha o último resquício visual da marca antiga que tinha escapado
da limpeza de texto; e o arquivo `capa/capa.png` deixa de ser um PNG órfão no repo —
agora cumpre o papel de capa/preview do projeto de fato.

**Commit:** `cbab931`.

---

## 2026-07-27 20:00–21:00 — Migração de dono do repo + publicação

**O que mudou:**
- Removidas todas as referências a "Nei"/"inema" do código e da documentação:
  `Bot_Telegram.md` (token exposto na raiz), branding INEMA.CLUB/PRO no `guia/index.html`,
  paths hardcoded pra `~/projetos/agnes-nei` e `~/projetos/openpcbot`, menções a
  "inemavox/chatterbox/bella" (TTS antigo) em textos residuais.
- Histórico do git **reescrito**: os 7 commits que estavam com autoria `inematds
  <inematds@gmail.com>` (dono original do projeto) agora são `Emerson Resende
  <emerson.ccaa@gmail.com>`.
- `capa/capa.png` — imagem de capa com a marca "INEMA.CLUB" **desenhada nos pixels**
  (não era texto, por isso passou batida na primeira limpeza) — removida do diretório
  de trabalho **e purgada de todos os commits do histórico** (não é recuperável nem
  pelos commits antigos no GitHub).
- Remote do git migrado de `github.com/inematds/videos-agnes` (sem permissão de escrita
  pra essa conta) para `github.com/emersonccaa/video-agnes` (repo novo, criado pelo usuário).
- Repositório novo publicado: descrição adicionada, `git push` feito.
- GitHub Pages habilitado (não vinha ligado por padrão num repo novo) e o guia
  publicado com sucesso em `https://emersonccaa.github.io/video-agnes/guia/`.

**Valor agregado:** projeto deixou de depender da conta/infra de terceiros (Nei/inematds)
pra existir — dono, remote, autoria do histórico e branding agora são 100% do Emerson.
Sem isso, qualquer push, deploy do Pages ou clone continuava travado ou emprestado.

**Commits:** `6847dd1` (pipeline), `0a94874` (limpeza Nei/inema) — histórico completo
reescrito, hashes de todos os 7 commits mudaram nesta sessão.

---

## 2026-07-23/24 — Pipeline portável + Edge TTS + duas histórias novas

*(trabalho de uma sessão anterior que ficou sem commitar até 2026-07-27 — reconstruído
por timestamps de arquivo e diff, não por log de sessão.)*

**O que mudou:**
- `pipeline.py` / `rodar.py` refatorados: paths deixaram de ser hardcoded pra
  `/home/nmaldaner/projetos/...` (só funcionava numa máquina específica).
- TTS trocado de local (inemavox/chatterbox, exigia daemon rodando) pra **Edge TTS**
  (online, gratuito, sem GPU/daemon).
- Pasta de saída passou a ser **numerada automaticamente** (`output/0001-nome`,
  `0002-nome`, ...) e reaproveitada em reexecuções, em vez de fixa.
- `montar()` ganhou: mixagem de música/ambiente do clipe com a narração, e legendas
  queimadas no vídeo por cena (SRT gerado a partir do texto revisado).
- Histórias podem sobrescrever `STYLE` (ex: `cinematic realistic photography` em vez
  do Pixar 3D padrão) — usado pela primeira vez em `banco_da_praca.py`.
- Duas histórias novas geradas **ponta a ponta com sucesso**:
  - `historias/0001-arvore_torta.py` → `output/0001-arvore_torta/filme-0001-arvore_torta.mp4` (77,9s, 6 cenas)
  - `historias/banco_da_praca.py` → `output/0002-banco_da_praca/filme-banco_da_praca.mp4` (46,5s, 5 cenas, com legendas queimadas)

**Valor agregado:** pipeline saiu de "só roda na máquina do Nei" pra portável (qualquer
clone funciona com `config/*.env` local); narração não depende mais de um daemon externo
rodando; vídeos agora saem com legenda embutida, melhor pra quem assiste sem som.

**Commits:** `6847dd1` (ficou como *unstaged* até esta sessão seguinte consolidar e commitar).

---

## 2026-07-17/18 — Base do projeto (herdada, autoria reescrita em 27/07)

**O que mudou:** pipeline inicial história→filme (model sheet, cenas, clipes keyframe,
narração, montagem, envio Telegram), skills `videos-agnes` e `imagens-agnes`, landing
+ guia publicados via GitHub Pages Actions, documentação da API Agnes AI medida na
prática (regras de prompt, referências, rate limits) incorporada ao README.

**Commits:** `97c240c`, `0b514d2`, `a8dfdb0`, `9bee3c0`, `58c6301`.

---

## Como continuar a partir daqui

- Pipeline funcional e publicado; não há trabalho pendente conhecido no código.
- Se for gerar uma história nova: `python3 rodar.py <nome>` (ver `skills/videos-agnes/SKILL.md`).
- Pré-requisitos de config vivem em `config/agnes.env` e `config/telegram.env` (fora do
  git, cada máquina precisa criar os seus).
- Ao terminar uma sessão de trabalho com mudanças relevantes, **adicionar uma entrada
  no topo deste arquivo** (data/hora, o que mudou, valor agregado) antes de encerrar.
