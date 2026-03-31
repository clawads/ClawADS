---
name: campaign-analyzer
description: Analisa campanhas existentes no Meta Ads e propoe melhorias baseadas em metricas de performance. Gera diagnostico completo com score de saude e recomendacoes acionaveis.
---

# Campaign Analyzer — Analise de Campanhas Meta Ads

## Quando Usar

- Quando o usuario quiser analisar performance das campanhas existentes
- Quando o usuario pedir sugestoes de otimizacao
- Quando o heartbeat detectar anomalias e precisar de analise profunda
- Quando o usuario perguntar "como estao minhas campanhas?"

## Processo

### Passo 1: Verificar Credenciais

Antes de qualquer analise, verifique se as credenciais estao configuradas. Se nao estiverem, execute `/onboarding`.

### Passo 2: Coletar Dados das Campanhas

Use o MCP server para buscar dados via Meta Marketing API:

#### 2.1 Listar Campanhas Ativas
```
GET /{ad_account_id}/campaigns
  ?fields=id,name,objective,status,daily_budget,lifetime_budget,bid_strategy,start_time,stop_time
  &filtering=[{"field":"status","operator":"IN","value":["ACTIVE","PAUSED"]}]
```

#### 2.2 Buscar Ad Sets de Cada Campanha
```
GET /{campaign_id}/adsets
  ?fields=id,name,targeting,optimization_goal,billing_event,bid_amount,daily_budget,status,promoted_object,instagram_actor_id
```

#### 2.3 Buscar Ads de Cada Ad Set
```
GET /{adset_id}/ads
  ?fields=id,name,status,creative{id,name,title,body,image_url,thumbnail_url,link_url,call_to_action_type}
```

#### 2.4 Buscar Insights (ultimos 30 dias)
```
GET /{ad_account_id}/insights
  ?fields=campaign_id,campaign_name,impressions,reach,clicks,cpc,cpm,ctr,spend,actions,cost_per_action_type,frequency
  &time_range={"since":"YYYY-MM-DD","until":"YYYY-MM-DD"}
  &level=campaign
  &time_increment=1
```

Para lead gen especificamente, buscar tambem:
```
GET /{ad_account_id}/insights
  ?fields=campaign_id,actions,cost_per_action_type
  &action_breakdowns=action_type
  &filtering=[{"field":"action_type","operator":"IN","value":["lead","onsite_conversion.lead_grouped"]}]
```

### Passo 3: Calcular Metricas-Chave

Para cada campanha, calcular:

| Metrica | Formula | Benchmark Lead Gen BR |
|---------|---------|----------------------|
| **CPL** (Custo por Lead) | Spend / Leads | < R$15 bom, < R$30 aceitavel |
| **CTR** (Taxa de Clique) | Clicks / Impressions * 100 | > 1.5% bom, > 1% aceitavel |
| **CPC** (Custo por Clique) | Spend / Clicks | < R$2 bom, < R$5 aceitavel |
| **CPM** (Custo por 1000 imp.) | (Spend / Impressions) * 1000 | < R$30 bom, < R$50 aceitavel |
| **Frequencia** | Impressions / Reach | < 3 bom, < 5 aceitavel |
| **Taxa de Conversao** | Leads / Clicks * 100 | > 10% bom, > 5% aceitavel |

### Passo 4: Score de Saude

Atribua um score de 0-100 para cada campanha:

- **90-100:** Excelente — Manter e escalar
- **70-89:** Bom — Pequenos ajustes podem melhorar
- **50-69:** Regular — Precisa de otimizacao
- **30-49:** Ruim — Revisao urgente necessaria
- **0-29:** Critico — Pausar e reestruturar

Criterios de pontuacao:
- CPL dentro do benchmark: +25 pontos
- CTR dentro do benchmark: +20 pontos
- Frequencia saudavel: +15 pontos
- Taxa de conversao dentro do benchmark: +20 pontos
- Estrutura correta (objetivo, targeting, placement): +20 pontos

### Passo 5: Diagnostico e Recomendacoes

Para cada campanha, apresentar:

```
## Campanha: {nome}
**Status:** {status} | **Score:** {score}/100 | **Classificacao:** {classificacao}

### Metricas (ultimos 30 dias)
- Investimento: R$ {spend}
- Leads: {leads}
- CPL: R$ {cpl}
- CTR: {ctr}%
- CPC: R$ {cpc}
- Frequencia: {freq}

### Diagnostico
{lista de problemas identificados}

### Recomendacoes
{lista de acoes concretas ordenadas por impacto}

### Prioridade
1. {acao mais urgente}
2. {segunda acao}
3. {terceira acao}
```

### Passo 6: Resumo Executivo

Ao final, apresentar um resumo geral:

```
## Resumo da Conta
- Total de campanhas analisadas: {n}
- Score medio: {media}/100
- Investimento total (30d): R$ {total}
- Total de leads (30d): {leads}
- CPL medio: R$ {cpl_medio}
- Campanha com melhor performance: {nome}
- Campanha que precisa de mais atencao: {nome}
```

## Decisoes de Otimizacao: Pausar, Remover ou Escalar

Apos a analise, classificar CADA elemento (campanha, ad set, ad, criativo) em uma acao recomendada.

### Regras para PAUSAR Campanha/Ad Set

| Condicao | Tempo minimo | Acao |
|----------|-------------|------|
| CPL > 3x benchmark por 48h | 2 dias | Pausar e reestruturar |
| 0 leads com spend > R$100 | 3 dias | Pausar, verificar formulario e tracking |
| CTR < 0.5% por 7 dias | 7 dias | Pausar, criativos nao ressoam |
| Quality ranking "below_average_10" | 3 dias | Pausar, criativo penalizado |
| Frequencia > 5 e CPL subindo | 5 dias | Pausar, publico saturado |
| Score < 30/100 | 7 dias | Pausar e reestruturar completamente |

**IMPORTANTE:** Nunca recomendar pausar antes de 48h — a learning phase precisa de tempo.

### Regras para REMOVER Criativo/Ad

| Condicao | Tempo minimo | Acao |
|----------|-------------|------|
| CTR < 50% da media dos outros ads do mesmo ad set | 5 dias | Remover (pausar ad) |
| CPL > 2x da media dos outros ads | 5 dias | Remover |
| 0 cliques com > 1000 impressoes | 3 dias | Remover imediatamente |
| Engagement rate ranking "below_average_10" | 5 dias | Remover e substituir |
| Conversion rate ranking "below_average_10" | 5 dias | Remover e substituir |
| Frequencia do ad > 6 com CTR caindo | 7 dias | Fadiga criativa — substituir |

### Regras para ESCALAR

| Condicao | Tempo minimo | Acao |
|----------|-------------|------|
| CPL < benchmark e estavel por 5 dias | 5 dias | Escalar +20% budget |
| CTR > 2x benchmark | 3 dias | Criar lookalike do publico |
| Score > 85/100 por 7 dias | 7 dias | Escalar agressivamente (+30%) |
| Melhor ad do ad set (CPL mais baixo) | 5 dias | Duplicar em novo ad set com mais budget |

### Apresentacao das Decisoes

```
## Plano de Otimizacao

### PAUSAR (acao urgente)
| Elemento | Tipo | Motivo | Dados |
|----------|------|--------|-------|
| {nome} | Campanha | CPL 3x acima do benchmark por 3 dias | CPL R$45 (bench R$15) |
| {nome} | Ad Set | Frequencia 5.2 + CPL subindo | Freq 5.2, CPL +30% 7d |

### REMOVER CRIATIVOS (substituir)
| Ad | Ad Set | Motivo | Performance vs Media |
|----|--------|--------|---------------------|
| {nome} | {adset} | CTR 60% abaixo da media | CTR 0.4% (media 1.2%) |
| {nome} | {adset} | 0 leads em 5 dias | 2000 imp, 0 conversoes |

**Sugestao:** Executar /creative-generator para criar substitutos antes de remover.

### ESCALAR (oportunidade)
| Elemento | Tipo | Motivo | Acao Sugerida |
|----------|------|--------|---------------|
| {nome} | Ad Set | CPL R$10 (bench R$15) estavel 7d | +20% budget |
| {nome} | Ad | Melhor CTR do grupo (2.5%) | Duplicar em novo ad set |

### MANTER (sem alteracao)
| Elemento | Motivo |
|----------|--------|
| {nome} | Performance dentro do esperado |

---

Deseja que eu execute as acoes? Posso:
1. Pausar os elementos listados
2. Gerar novos criativos para substituir os removidos
3. Escalar os budgets recomendados

Escolha uma opcao ou "tudo" para executar o plano completo.
```

### Execucao das Acoes

Apos confirmacao do usuario:

#### Pausar:
```
POST /{object_id}
{"status": "PAUSED"}
```

#### Remover criativo (pausar o ad, manter o criativo para referencia):
```
POST /{ad_id}
{"status": "PAUSED"}
```

#### Escalar:
Usar `/budget-optimizer` para ajustar orcamento com regra de max 20%.

### Ciclo de Otimizacao Continuo

Recomendar ao usuario o ciclo:

```
Ciclo semanal de otimizacao:
1. /campaign-analyzer → identifica o que pausar/remover/escalar
2. Pausar e remover o que nao funciona
3. /creative-generator → criar substitutos
4. /lead-gen-creator → criar novos ads com os criativos
5. /budget-optimizer → redistribuir budget
6. /heartbeat → monitorar resultados
7. Repetir na proxima semana
```

## Formato de Saida

Sempre apresentar os resultados em formato estruturado com:
- Tabelas para metricas comparativas
- Classificacao clara: PAUSAR / REMOVER / ESCALAR / MANTER para cada elemento
- Recomendacoes ordenadas por impacto esperado
- Estimativa de melhoria para cada recomendacao
- Plano de acao executavel com confirmacao do usuario

## Restricoes

- NAO faca alteracoes nas campanhas sem autorizacao explicita do usuario
- NUNCA recomendar pausar antes de 48h (learning phase)
- NUNCA remover criativo sem sugerir substituto antes
- Sempre mostrar os dados que justificam a decisao
- Sempre indique a fonte dos benchmarks utilizados
- Se os dados forem insuficientes (menos de 7 dias ou menos de 1000 impressoes), avise o usuario que a analise pode nao ser representativa
- Compare apenas campanhas com o mesmo objetivo
- Ao remover/pausar, SEMPRE perguntar se o usuario quer executar ou apenas anotar
