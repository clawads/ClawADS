---
name: heartbeat
description: Monitoramento periodico automatizado de campanhas Meta Ads. Analisa performance, detecta anomalias, e propoe otimizacoes proativamente em intervalos regulares.
---

# Heartbeat — Monitoramento de Campanhas

## Quando Usar

- Ativado pelo usuario para monitoramento continuo
- Executado periodicamente (configuravel: a cada 1h, 6h, 12h ou 24h)
- Quando o usuario quiser acompanhamento automatico das campanhas

## Processo

### Passo 1: Configuracao Inicial

Perguntar ao usuario:

```
Vou configurar o monitoramento automatico das suas campanhas.

1. Frequencia de verificacao:
   a) A cada 1 hora (recomendado para campanhas novas)
   b) A cada 6 horas (recomendado para campanhas estabilizadas)
   c) A cada 12 horas
   d) A cada 24 horas

2. Quais campanhas monitorar?
   a) Todas as campanhas ativas
   b) Campanhas especificas (listar IDs)

3. Alertas — me notifique quando:
   a) CPL subir mais de 20% em relacao a media
   b) CTR cair abaixo de 1%
   c) Orcamento diario atingir 80%
   d) Frequencia ultrapassar 3
   e) Todas as opcoes acima (recomendado)

4. Limites de orcamento:
   - Gasto maximo diario total: R$ ___
   - Gasto maximo por campanha: R$ ___
```

### Passo 2: Coleta de Metricas

A cada execucao, coletar via MCP / Meta API:

#### Metricas de Performance (periodo: ultimas 24h e acumulado 7d)
```
GET /{ad_account_id}/insights
  ?fields=campaign_id,campaign_name,impressions,reach,clicks,cpc,cpm,ctr,spend,
          actions,cost_per_action_type,frequency,quality_ranking,
          engagement_rate_ranking,conversion_rate_ranking
  &level=campaign
  &filtering=[{"field":"campaign.delivery_status","operator":"IN","value":["active"]}]
  &time_range={"since":"{ontem}","until":"{hoje}"}
```

#### Status de Entrega
```
GET /{ad_account_id}/campaigns
  ?fields=id,name,effective_status,issues_info
  &filtering=[{"field":"effective_status","operator":"IN","value":["ACTIVE","CAMPAIGN_PAUSED","ADSET_PAUSED"]}]
```

### Passo 3: Analise de Anomalias

Comparar metricas atuais com:
- **Media movel dos ultimos 7 dias**
- **Benchmarks definidos no campaign-analyzer**
- **Limites configurados pelo usuario**

#### Regras de Deteccao de Anomalias

| Anomalia | Condicao | Severidade | Acao Sugerida |
|----------|----------|-----------|---------------|
| CPL Elevado | CPL > media_7d * 1.3 | ALTA | Revisar targeting e criativos |
| CTR Baixo | CTR < 0.8% | ALTA | Testar novos criativos |
| Frequencia Alta | Freq > 4 | MEDIA | Expandir publico ou pausar |
| CPC Elevado | CPC > media_7d * 1.5 | MEDIA | Revisar relevancia do anuncio |
| Sem Leads | 0 leads em 24h com spend > R$50 | CRITICA | Verificar formulario e tracking |
| Budget Quase Esgotado | Spend > 80% do orcamento | INFO | Informar usuario |
| Quality Ranking Baixo | below_average_35 | ALTA | Melhorar criativo e copy |
| Entrega Parada | effective_status != ACTIVE | CRITICA | Verificar rejeicoes e erros |

### Passo 4: Relatorio de Heartbeat

Formato do relatorio periodico:

```
## Heartbeat — {data} {hora}

### Status Geral
- Campanhas ativas: {n}
- Gasto total (24h): R$ {spend}
- Leads captados (24h): {leads}
- CPL medio (24h): R$ {cpl}

### Alertas
{lista de alertas detectados, se houver}

### Performance por Campanha (24h)
| Campanha | Spend | Leads | CPL | CTR | Status |
|----------|-------|-------|-----|-----|--------|
| {nome}   | R${x} | {n}  | R${y}| {z}%| {ok/alerta} |

### Tendencias (7 dias)
- CPL: {subindo/estavel/descendo} ({variacao}%)
- CTR: {subindo/estavel/descendo} ({variacao}%)
- Volume de leads: {subindo/estavel/descendo} ({variacao}%)

### Recomendacoes
{lista de acoes sugeridas baseadas na analise, se houver}
```

### Passo 5: Acoes Automaticas (com autorizacao previa)

Se o usuario autorizar acoes automaticas, o heartbeat pode:

#### Autorizacao Nivel 1 (Somente Leitura — padrao):
- Coletar metricas
- Gerar relatorios
- Enviar alertas

#### Autorizacao Nivel 2 (Otimizacao Leve — requer aprovacao):
- Ajustar orcamento em ate 20% para cima ou para baixo
- Pausar ads com performance muito ruim (CPL > 3x benchmark)

#### Autorizacao Nivel 3 (Gestao Ativa — requer aprovacao explicita):
- Pausar/ativar ad sets
- Ajustar targeting
- Criar novos ads com criativos sugeridos

**IMPORTANTE:** O nivel padrao e sempre Nivel 1. Qualquer acao que envolva alteracao requer confirmacao explicita.

### Passo 6: Historico

Manter historico das execucoes do heartbeat para:
- Identificar tendencias de longo prazo
- Comparar performance semana a semana
- Gerar relatorio semanal consolidado

## Protocolo HEARTBEAT_OK

Quando executado via `/loop` ou schedule, seguir o protocolo padrao:

- Se **todas as metricas estiverem normais** e nao houver alertas, responder apenas: `HEARTBEAT_OK`
- Se **houver alertas**, apresentar o relatorio completo do Passo 4
- Se **houver alerta CRITICO**, apresentar relatorio + solicitar acao imediata do usuario

Isso evita poluir o chat com relatorios desnecessarios quando tudo esta ok.

## Configuracao de Schedule

Existem 3 formas de ativar o heartbeat:

### Opcao 1: /loop (sessao ativa — recomendado para comecar)
```
/loop 1h /heartbeat
```
Roda a cada 1 hora enquanto a sessao estiver ativa. Auto-expira apos 72h.

### Opcao 2: /schedule (cloud — roda mesmo offline)
Acessar `claude.ai/code/scheduled` e criar uma tarefa com:
- **Prompt:** "Execute /heartbeat para verificar campanhas Meta Ads"
- **Frequencia:** A cada 1h, 6h, diario, etc.
- Roda na nuvem mesmo com a maquina desligada.

### Opcao 3: Cron local
```bash
# A cada 6 horas
0 */6 * * * claude-code --skill heartbeat --auto
```

## Deteccao de Fadiga Criativa

Alem das anomalias padrao, monitorar fadiga criativa:

- **CTR decay:** Se CTR cair >15% em media movel de 3 dias, sugerir refresh de criativos
- **Frequencia + CTR:** Se frequencia > 3.0 E CTR caindo, o publico esta saturado
- **Acao:** Sugerir ao usuario executar `/creative-generator` para novas variacoes

## Restricoes

- NUNCA altere campanhas sem autorizacao (nivel padrao e somente leitura)
- Se detectar gasto anomalo (>2x do esperado), SEMPRE alerte imediatamente
- Mantenha logs de todas as execucoes e alertas
- Se a API retornar erro, tente novamente uma vez. Se persistir, alerte o usuario
- Nao gere relatorio se nao houver dados novos desde a ultima execucao
