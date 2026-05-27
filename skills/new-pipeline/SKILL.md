---
name: new-pipeline
description: Use ao desenhar uma nova ICM workspace que é um PIPELINE MULTI-ESTÁGIO com revisão humana em loops (content workflows, research→script→design→review→publish, código→PR→merge, qualquer fluxo sequencial com gates de aprovação granulares). Vai além do `/icm:set-up pipeline` simples — ensina o padrão de salas numeradas, sub-estágios com markers próprios, gates configuráveis em config.json, sidecar revisao.json, rejeição granular (sub-estágio rejeitado não bumpa v<N+1>), protocolo mecânico do revisor (escreve markers em dois lugares), state-detection logic, separação think-vs-execute (writer descreve O QUÊ, executor decide COMO), plano-antes-de-gerar pra operações caras, tier de modelo por retorno_esperado, e subagent dispatch pra auto-review. Inclui exemplo genérico inline de pipeline 3-estágios.
---

# new-pipeline — Padrão de Pipeline Multi-Estágio com Gates Granulares

> Skill complementar a `/icm:set-up`. Use quando o workspace é um pipeline sequencial **com revisão humana em múltiplos pontos** e os estágios têm sub-fases internas que merecem ser revisadas independentemente.
>
> Reference implementation: `achadoempar-workspace` (Instagram afiliados, 5 salas pipeline numeradas + 2 off-pipeline, sub-N markers no Roteiro, plano+iNN+montagem no Edicao, 9 gates configuráveis, schemas validados).

## Quando usar (vs. `/icm:set-up pipeline` simples)

Use `/icm:set-up` quando:
- Pipeline tem ≤5 estágios e cada um é atômico (não subdivide)
- Revisão é um estágio único no final OU não há revisão humana intermediária
- Cost de execução de cada estágio é baixo (sem gerar imagens/vídeos caros)

Use **este padrão** (`new-pipeline`) quando:
- Pelo menos 1 estágio tem sub-fases que merecem revisão própria (ex: estratégia → copy → visual brief no estágio "escrita")
- Há review humano humano-no-loop em múltiplos pontos
- Custo de operações é alto e merece **plano antes de gastar** (geração IA, chamadas pagas, deploys)
- Quer afrouxar/apertar gates por config (mudar de "human" pra "auto" quando o agente aprender)
- Quer rejeição granular (refazer só o pedaço rejeitado, não o estágio inteiro)
- Quer separar **think** (criativo) de **execute** (técnico) com contrato explícito entre eles

## Decisões arquitetônicas que esta skill ajuda a tomar

Antes de scaffold, o agente deve ter respostas pra:

1. **Quantos estágios** (salas)? E quais? Use numeração visual `1.1-`, `1.2-`, ... pra ordem do pipeline.
2. **Quais estágios subdividem?** Estágios "criativos" geralmente sim (estratégia → copy → brief); estágios "técnicos" também (plano → execução → montagem). Estágios mecânicos (pesquisa, publicação) geralmente não.
3. **Onde estão os gates?** Lista exaustiva. Ex: `[pesquisa, n1_estrategia, n2_copy, n3_brief, roteiro_final, edicao_plano, edicao_item, edicao_montagem, publicacao]`.
4. **Como o gate é configurado?** Em `<arquivos-da-página>/config.json` sob `pipeline.gates.<gate>: "human" | "auto" | "agent"`. Default MVP = todos "human" (humano-no-loop).
5. **Como o revisor escreve markers?** Em **dois lugares**: no folder próprio (decisão + correções) E no folder revisado (marker `_concluido` ou `_rejeitado`). Detalhes em `docs/handoff_protocol.md` §protocolo do revisor.
6. **Como o agente principal sabe onde retomar?** Lê markers em ordem causal (state-detection table). Detalhes em `docs/handoff_protocol.md` §state-detection.
7. **Qual o contrato think-vs-execute?** O upstream (criativo) entrega O QUÊ — descrição precisa do output desejado, refs disponíveis, posições, elementos obrigatórios. O downstream (técnico) decide COMO — ferramentas, prompts, parâmetros, ordem de execução. Esquema enforced pelos schemas.
8. **Como controlar custo de execução IA?** Sub-estágio "plano" antes de "execução" — plano lista chain decidida, custos estimados por item, total. Aprovado o plano, executa. Plano rejeitado, refaz plano (sem desperdiçar gerações).
9. **Como escalar modelo por valor?** Briefing declara `retorno_esperado: baixo|medio|alto|critico`. Config tem `cost_tiers.{tier}.{role}: model_id` mapeando tier → modelo (writer haiku pra baixo, opus pra crítico). Agente lê tier ao escolher modelo.
10. **Como aprendizado fluir?** Per-sala `memoria/learnings.jsonl` (append-only via lockfile) populated apenas por rejeições humanas + auto-reviews aplicadas. Auto-review via skill genérica `convocar-subagente`.

## Receita — passos pra scaffold um pipeline assim

### 1. Esqueleto base (use `/icm:set-up pipeline` se workspace ainda não existe)

Salas numeradas em `salas/`:
```
salas/
├── 1.1-<sala-1>/                    (e.g., sala-de-pesquisa)
├── 1.2-<sala-2>/                    (e.g., sala-de-roteiro)
├── 1.3-<sala-revisao-1>/            (e.g., sala-de-revisao-roteiro)
├── 1.4-<sala-3>/                    (e.g., sala-de-edicao)
├── 1.5-<sala-revisao-2>/            (e.g., sala-de-revisao-edicao)
└── (off-pipeline: dev, CEO, etc — sem prefixo numérico)
```

### 2. Estrutura da unidade-de-trabalho (campanha, ticket, projeto)

Em `<arquivos>/instances/Em_execução/<id>/`:
```
<id>/
├── manifest.json
├── _stage.json                       { campaign_id, estagio_atual, versao_atual, sub_gates{...} }
├── <Estagio1>/
│   └── output... + _handoff.md + _concluido
├── <Estagio2>/v<N>/
│   ├── <sub_a>/                      output do sub-estágio + revisao.json + _handoff.md + marker
│   ├── <sub_b>/
│   ├── <sub_c>/
│   ├── <output_merged>.json
│   ├── _handoff.md
│   └── _concluido
├── <Revisao1>/v<N>/                  decisoes + correcoes_<gate>.md + marker
├── ... (continua)
└── <Finalizado>/_publicado
```

### 3. Markers + sidecar

| Marker | Quem escreve | Quando |
|---|---|---|
| `_handoff.md` | Agente da sala | Sempre, descrevendo o output |
| `_concluido` | Agente (gate=auto) OR revisor (gate=human, aprovação) | Sub-estágio aprovado |
| `_aguardando_revisao` | Agente | Antes de pausar pra revisão humana |
| `_rejeitado` | Revisor | Quando rejeita |
| `revisao.json` (sidecar) | Agente principal + revisor (atualiza) | Toda transição |

Schema do sidecar `revisao.json`:
```json
{
  "self_assessment": "string | null",
  "auto_review": [{"ts","model","tipo":"reviewer","feedback","aplicado","diff_resumido"}],
  "aguardando": "humano" | null
}
```

Idempotência: criar `_concluido` sobre `_concluido` é no-op. `_rejeitado` sobre `_concluido` é erro (não tente reverter; isso é bug).

### 4. Gates config

Em `<arquivos>/config.json`:
```json
"pipeline": {
  "gates": {
    "<gate1>": "human",
    "<gate2>": "human",
    ...
  }
}
```

Semântica:
- `"human"` → agente cria `_aguardando_revisao` e pausa
- `"auto"` → agente cria `_concluido` direto e prossegue
- `"agent"` → reservado pra agent reviewer especialista (futuro)

Mudança mid-execução só afeta transições **futuras** — markers já escritos não replay.

### 5. State-detection (resume logic)

Tabela canônica que o agente checa ao entrar numa instância:

| Estado | Ação |
|---|---|
| nenhum `v<N>/` | começar `v01/` |
| `<sub_a>/_concluido` ausente | começar/retomar sub_a |
| `<sub_a>/_concluido` OK, `<sub_b>/_concluido` ausente | retomar sub_b |
| `<sub_X>/_rejeitado` + `correcoes_<sub_X>.md` em Revisão | refazer sub_X + descendentes (cascata) |
| `v<N>/_aguardando_revisao` | esperar (não avançar); pode sair com `icm-compact` |
| `<Revisao>/v<N>/_concluido` (gate final aprovado) | propagar `<Estagio>/v<N>/_concluido` (idempotente), atualizar `_stage.json`, sair pra próxima sala |
| `<Revisao>/v<N>/_rejeitado` (gate final rejeitado) | bump `v<N+1>`, recomeçar do primeiro sub |

Análogo pra cada estágio com sub-fases.

### 6. Rejeição granular (regra)

- `<sub_X>/_rejeitado` → refaz `sub_X` + descendentes (sub_X+1, sub_X+2, ...). Mantém upstream.
- `<Revisao>/v<N>/_rejeitado` (gate final do estágio) → bump `v<N+1>`, recomeça do primeiro sub.
- Versão (`v<N>`) só incrementa quando o gate **final** do estágio rejeita. Sub-rejeições ficam dentro da mesma versão.

### 7. Protocolo do revisor (mecânico)

Sala de revisão escreve em **dois lugares**:

1. No próprio folder (`<Revisao>/v<N>/`):
   - `<sub_X>_decisao.md` — notas detalhadas
   - `correcoes_<sub_X>.md` — feedback acionável (se rejeitado)
   - `_concluido` (no gate final aprovado)

2. No folder revisado (`<Estagio>/v<N>/<sub_X>/`):
   - `_concluido` (aprovação) OR `_rejeitado` (rejeição)
   - Atualiza `revisao.json.aguardando = null`

NÃO modifica outputs do agente (read-only); só anota markers + decisão + correções.

### 8. Schemas validados

Para cada output relevante:
- `<workspace>/salas/<sala-de-desenvolvimento>/docs/schemas/<nome>.schema.json`
- `$id`: `https://<projeto>.local/schemas/<nome>.schema.json`
- Schemas típicos: input briefing, sub-estagio output (cada um), merged output, sidecar revisão, plano (se houver fase de plano)

Agente VALIDA antes de marcar `_concluido` ou `_aguardando_revisao`. Falha de schema = falha cedo.

### 9. Catálogo de "identidade" (Layer 3 factory)

Pasta `<workspace>/voz-da-marca/` (ou equivalente — `identidade/`, `brand/`, `style-guide/`):
- `identidade.md` — tom, voz, persona
- `visual-*.md` — direção visual por contexto/universo
- `layouts.md` — catálogo de `layout_id`s canônicos (writer referencia por nome, executor mapeia pra implementação)
- `convencoes-nome.md` — convenções de naming
- READ-ONLY durante runs (Layer 3)

### 10. Briefing template (entry point do pipeline)

Em `modelo-pagina/template/briefing-template.md` (ou equivalente):
- YAML frontmatter validado por schema (`id`, `formato_sugerido`, `retorno_esperado`, recursos disponíveis, restrições)
- Markdown livre depois (ângulo criativo, hooks, refs, notas)
- Humano copia + edita ao criar nova unidade-de-trabalho

### 11. Skills custom recomendadas

- `convocar-subagente` — dispatch generalista pra auto-review pre-pass. Modelo por tier (haiku/sonnet/opus baseado em `retorno_esperado`). Subagent não cria junctions, não escreve markers, não compacta — output transitório.
- `icm-compact` — handoff entre salas (já existe no plugin ICM).
- `icm-workspace-guide` — mapa do workspace pra agentes em dúvida.
- Skills específicas do domínio (ex: `remotion-render` se renderizar vídeo; `n8n-deploy` se deployar workflow).

### 12. MCP wiring

Em `.mcp.json`: adicionar MCPs externos necessários. OAuth flows (Canva, Higgsfield, etc) ficam pra primeiro uso humano. API keys em `.env` (gitignored), documentadas em `.env.example`.

CapCut e similares 3rd-party MCPs: marcar como **research task** se pacote npm não confirmado.

### 13. Cost-aware execution

Em `config.json`:
```json
"cost_tiers": {
  "baixo":   { "writer": "haiku", "image_gen": "...schnell" },
  "medio":   { "writer": "sonnet", "image_gen": "...pro" },
  "alto":    { "writer": "sonnet", "image_gen": "...premium" },
  "critico": { "writer": "opus", "image_gen": "...top" }
},
"cost_estimates": {
  "<tool>/<model>": <usd_por_unidade>
}
```

Briefing declara `retorno_esperado` → agentes consultam tier ao escolher modelo. Editor estima custo no plano antes de executar. Humano aprova/rejeita plano.

## Anti-padrões (vistos durante o design — não repita)

- ❌ **Writer decidir production_chain.** Vaza domínio. Writer descreve "o que" (visual brief); executor escolhe ferramentas. Granularidade EXECUÇÃO no contrato (rich N3), não na chain.
- ❌ **Único marker `_aguardando_revisao_provisoria` separado do humano.** Use 1 marker + sidecar JSON `revisao.json` com campo `aguardando: "humano" | null` — schema-evoluível, CLI simples.
- ❌ **Versão (v<N>) incrementa em sub-rejeição.** Não — só no gate final. Sub-rejeição refaz dentro da mesma versão.
- ❌ **Process loops detalhados em `job_draft.md`.** `job_draft.md` é pra **persona/voz/estilo editorial**. Process loops mecânicos vão em `CONTEXT.md` (canon). Não duplicar.
- ❌ **Revisor escreve apenas no próprio folder.** Tem que escrever marker no folder revisado também — senão writer/editor não detecta state-detection.
- ❌ **Subagent reviewer criando junctions / escrevendo markers.** Subagent transitório lê via paths absolutos, escreve só `revisao_provisoria.md`, agente principal processa e remove.
- ❌ **Memory populada por self-judging.** Learnings só de rejeições humanas + auto-reviews aplicadas. Agente não inventa "lesson".
- ❌ **Bump v<N+1> automático quando sub-N rejeitado.** Só quando gate **final** do estágio rejeita.
- ❌ **`auto` gate como default em pipeline novo.** MVP humano-no-loop precisa de gates `human` em tudo. Afrouxe progressivamente conforme agente aprende.

## Verificação pós-scaffold (smoke checks)

- [ ] `AGENTS.md` routing table tem todas as salas listadas com paths numerados.
- [ ] `config.json` tem bloco `pipeline.gates.*` com todos os gates do pipeline.
- [ ] `config.json` tem `cost_tiers` (4 níveis) + `cost_estimates` (≥6 tools).
- [ ] Cada sala pipeline tem `CONTEXT.md` com seções: Purpose, Posição no pipeline, Inputs (tabela), Process (numerado), Outputs (tabela), Done when (checklist), Hand-off, Boundaries, Skills aceitas.
- [ ] Schemas JSON validam sintaticamente (`python -c "import json; json.load(open(...))"`).
- [ ] `docs/handoff_protocol.md` cobre: markers + responsabilidades, sidecar revisao.json, protocolo mecânico do revisor (2 lugares), state-detection table, rejeição granular, mudança mid-campanha, junctions, paralelismo, ordem de eventos, lockfiles.
- [ ] Grep `salas/<nome-antigo>` retorna zero matches (renames consistentes).
- [ ] EXEMPLO/template tem briefing.md com YAML frontmatter completo + estrutura completa de pastas com `.placeholder.md`.

## Exemplo (pipeline genérico 3-estágios)

Content workflow com 3 estágios principais e sub-estágios em 2 deles:

```
workspace/
├── AGENTS.md
├── config.json                              # gates + tiers
├── identidade/                              # Layer 3: identidade (read-only)
├── salas/
│   ├── 1.1-research/                        # estágio atômico (sem sub-fases)
│   ├── 1.2-write/                           # sub-staged: a (strategy) → b (copy) → c (brief)
│   ├── 1.3-review-write/                    # gate room (reviewer)
│   ├── 1.4-edit/                            # sub-staged: plan → items → assemble
│   └── 1.5-review-edit/                     # gate room (reviewer)
└── arquivos/instances/em-execucao/<id>/
    ├── _stage.json
    ├── Research/_concluido
    ├── Write/v01/
    │   ├── a/{output.json, revisao.json, _concluido}
    │   ├── b/{output.json, revisao.json, _concluido}
    │   ├── c/{output.json, revisao.json, _aguardando_revisao}   # paused here
    │   └── (merged.json + _concluido once all subs concluido)
    └── Review-write/v01/                                         # reviewer dual-writes
```

Gate config em `config.json`:
```json
"pipeline": {
  "gates": {
    "research":      "human",
    "write_a":       "human",
    "write_b":       "human",
    "write_c":       "human",
    "write_final":   "human",
    "edit_plan":     "human",
    "edit_item":     "human",
    "edit_assemble": "human",
    "publish":       "human"
  }
}
```

Cada gate pode virar `"auto"` (agente cria `_concluido` direto) ou `"agent"` (reviewer especialista) à medida que o sistema amadurece — sem mexer em estrutura de pasta.

Rejeição em `c/_rejeitado` (sub-stage rejeitado) → refaz só `c` + descendentes, mantém `a` e `b`. Rejeição em `Review-write/v01/_rejeitado` (gate final) → writer bumpa `v02`, recomeça do `a`.

## Comandos relacionados (já no plugin)

- `/icm:set-up` — scaffold inicial (use ANTES desta skill pra criar o esqueleto)
- `/icm:remap` — recompor routing table se estrutura mudou
- `/icm:debloat` — limpar folder oversized
- `/icm:new-tool` — adicionar skill nova ao workspace

Esta skill **não** scaffolda automaticamente — ela ensina o padrão. Se você quer scaffolding automático de pipelines multi-estágio com gates, isso seria uma extensão futura ao `/icm:set-up`.
