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

## Formato de Saida

Sempre apresentar os resultados em formato estruturado com:
- Tabelas para metricas comparativas
- Indicadores visuais (uso de emojis apenas se o usuario pedir)
- Recomendacoes ordenadas por impacto esperado
- Estimativa de melhoria para cada recomendacao

## Restricoes

- NAO faca alteracoes nas campanhas sem autorizacao explicita do usuario
- Sempre indique a fonte dos benchmarks utilizados
- Se os dados forem insuficientes (menos de 7 dias ou menos de 1000 impressoes), avise o usuario que a analise pode nao ser representativa
- Compare apenas campanhas com o mesmo objetivo
