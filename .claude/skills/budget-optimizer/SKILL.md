---
name: budget-optimizer
description: Ajuda a definir o orcamento ideal para campanhas de lead gen e ajusta diretamente na plataforma Meta Ads via API. Calcula CPL estimado, recomenda distribuicao e faz alteracoes com confirmacao do usuario.
---

# Budget Optimizer — Orcamento de Campanhas

## Quando Usar

- Quando o usuario nao sabe quanto investir
- Quando o usuario quiser redistribuir orcamento entre campanhas
- Quando o heartbeat recomendar ajuste de budget
- Quando o usuario perguntar "quanto devo investir?"

## Processo

### Passo 1: Entender o Cenario

Perguntar ao usuario:

```
Para recomendar o melhor orcamento, preciso entender seu cenario:

1. Qual seu objetivo de leads por mes? (ex: 100 leads)
2. Qual seu orcamento maximo mensal? (em BRL)
3. Ja rodou campanhas antes? (se sim, vou buscar seu CPL historico)
4. Qual o valor de cada lead para voce? (ex: "cada lead vale R$50 em receita potencial")
```

### Passo 2: Calcular com Base em Benchmarks

Se o usuario NAO tem historico, usar benchmarks Brasil para lead gen tech:

| Metrica | Cenario Conservador | Cenario Medio | Cenario Otimista |
|---------|-------------------|---------------|-----------------|
| CPL | R$25-30 | R$15-20 | R$8-12 |
| CTR | 0.8-1.2% | 1.2-2.0% | 2.0-3.5% |
| Taxa de conversao | 5-8% | 8-15% | 15-25% |
| CPM | R$35-50 | R$20-35 | R$10-20 |

**Formula base:**
```
Orcamento mensal = Meta de leads x CPL estimado

Exemplo:
- Meta: 100 leads/mes
- CPL estimado (medio): R$18
- Orcamento recomendado: 100 x R$18 = R$1.800/mes
- Orcamento diario: R$1.800 / 30 = R$60/dia
```

Se o usuario TEM historico, buscar via MCP:
```
GET /{ad_account_id}/insights
  ?fields=spend,actions,cost_per_action_type
  &date_preset=last_30d
  &filtering=[{"field":"action_type","operator":"IN","value":["lead"]}]
```

### Passo 3: Apresentar Recomendacao

```
## Recomendacao de Orcamento

**Meta:** {n} leads/mes
**CPL estimado:** R$ {cpl}

| Plano | Orcamento/mes | Orcamento/dia | Leads estimados |
|-------|--------------|--------------|-----------------|
| Conservador | R$ {x} | R$ {x/30} | {leads_min} |
| Recomendado | R$ {y} | R$ {y/30} | {leads_medio} |
| Agressivo | R$ {z} | R$ {z/30} | {leads_max} |

**Distribuicao sugerida:**
- 70% para campanha principal (publico validado)
- 20% para testes de novos publicos
- 10% para retargeting

Qual plano deseja seguir?
```

### Passo 4: Aplicar na Plataforma

Apos o usuario escolher, aplicar via MCP:

#### 4.1 Definir orcamento em campanha nova
Usar `meta_create_adset` com `daily_budget` em centavos:
```
daily_budget = orcamento_diario_brl * 100
Exemplo: R$60/dia = 6000
```

#### 4.2 Ajustar orcamento de campanha existente
```
POST /{adset_id}
{
  "daily_budget": "{novo_valor_centavos}"
}
```

Ou se usar Advantage Campaign Budget (orcamento no nivel da campanha):
```
POST /{campaign_id}
{
  "daily_budget": "{novo_valor_centavos}"
}
```

#### 4.3 Trocar de diario para lifetime (e vice-versa)
**ATENCAO:** Nao e possivel trocar tipo de budget apos criacao. Se necessario:
1. Criar novo ad set com o tipo desejado
2. Pausar o ad set antigo
3. Informar o usuario sobre a limitacao

### Passo 5: Confirmacao Obrigatoria

**SEMPRE** mostrar preview antes de aplicar:

```
## Alteracao de Orcamento

Campanha: {nome}
Ad Set: {nome_adset}

Orcamento atual: R$ {atual}/dia
Novo orcamento: R$ {novo}/dia
Variacao: {+/-}{percentual}%

Gasto estimado mensal: R$ {novo * 30}

Confirma a alteracao? (sim/nao)
```

So executar apos "sim" explicito.

### Passo 6: Regras de Escalamento

Quando o heartbeat ou campaign-analyzer sugerir escalar:

#### Escalar para cima (campanha performando bem):
- **Regra:** Aumentar no maximo 20% por vez
- **Frequencia:** Esperar pelo menos 3 dias entre aumentos
- **Condicao:** CPL < benchmark E CTR > benchmark por 3 dias consecutivos

#### Escalar para baixo (campanha com problemas):
- **Regra:** Reduzir 20-30% se CPL > 2x benchmark por 2 dias
- **Emergencia:** Pausar se CPL > 3x benchmark por 24h

#### Redistribuir entre ad sets:
- Mover budget de ad sets com CPL alto para ad sets com CPL baixo
- Manter minimo de R$20/dia por ad set (limite Meta para otimizacao)

```
## Sugestao de Redistribuicao

| Ad Set | Budget Atual | CPL | Novo Budget | Motivo |
|--------|-------------|-----|-------------|--------|
| Devs 22-35 | R$40/dia | R$12 | R$55/dia | Melhor CPL, escalar |
| Tech 28-45 | R$40/dia | R$28 | R$25/dia | CPL alto, reduzir |

Aplicar redistribuicao? (sim/nao)
```

## Forecasting de Leads — Projecao Realista

Quando o usuario perguntar "quantos leads vou conseguir?" ou "quanto preciso investir para bater X leads?", usar projecao baseada em dados reais da campanha.

### Coleta de Dados para Projecao

Buscar dados dos ultimos 7, 14 e 30 dias separadamente via MCP:

```
GET /{ad_account_id}/insights
  ?fields=spend,impressions,reach,clicks,actions,cost_per_action_type,ctr,cpc,cpm
  &time_range={"since":"{7_dias_atras}","until":"{hoje}"}
  &level=campaign
  &time_increment=1
```

Com os dados diarios, calcular:

#### Metricas Reais da Campanha
```
CPL_real = spend_total / leads_total
CTR_real = clicks / impressions * 100
Conv_rate = leads / clicks * 100
CPM_real = (spend / impressions) * 1000
Leads_por_dia = leads_total / dias_ativos
Spend_por_dia = spend_total / dias_ativos
```

#### Tendencia (a campanha esta melhorando ou piorando?)
```
CPL_semana_1 vs CPL_semana_2:
- Se CPL caiu: campanha otimizando (learning phase saindo)
- Se CPL subiu: possivel fadiga ou saturacao
- Se estavel: campanha madura

Velocidade de leads:
- Leads/dia ultimos 7d vs Leads/dia ultimos 30d
- Acelerando, desacelerando ou estavel?
```

### Modelo de Projecao

Usar 3 cenarios baseados nos dados REAIS (nao benchmarks genericos):

```
CPL_otimista = CPL_real * 0.85   (melhoria de 15% com otimizacoes)
CPL_realista = CPL_real           (mantem performance atual)
CPL_pessimista = CPL_real * 1.25  (degradacao de 25% por saturacao)
```

**Ajustar o CPL projetado pela tendencia:**
- Se CPL esta caindo nos ultimos 7 dias: usar CPL_otimista como realista
- Se CPL esta subindo: usar CPL_pessimista como realista
- Se CPL esta estavel: manter CPL_real

**Fator de escala (ao aumentar budget, CPL tende a subir):**
```
Se aumento de budget < 20%: fator = 1.0 (sem impacto)
Se aumento de budget 20-50%: fator = 1.10 (CPL sobe ~10%)
Se aumento de budget 50-100%: fator = 1.20 (CPL sobe ~20%)
Se aumento de budget > 100%: fator = 1.35 (CPL sobe ~35%)
```

### Apresentacao: "Quantos leads vou conseguir?"

```
## Projecao de Leads — {nome_campanha}

**Dados reais (ultimos {n} dias):**
- Gasto total: R$ {spend}
- Leads captados: {leads}
- CPL medio: R$ {cpl}
- Leads/dia: {leads_dia}
- Tendencia CPL: {subindo/estavel/descendo} ({var}%)

**Projecao para os proximos 30 dias (budget atual: R$ {budget}/dia):**

| Cenario | CPL Projetado | Leads Estimados | Confianca |
|---------|--------------|-----------------|-----------|
| Otimista | R$ {cpl_o} | {leads_o} | {conf_o}% |
| Realista | R$ {cpl_r} | {leads_r} | {conf_r}% |
| Pessimista | R$ {cpl_p} | {leads_p} | {conf_p}% |

*Baseado em {n} dias de dados reais. Confianca aumenta com mais dias de historico.
```

**Nivel de confianca da projecao:**
- Menos de 3 dias de dados: 30% (muito incerto — campanha em learning phase)
- 3-7 dias: 50% (indicativo)
- 7-14 dias: 70% (confiavel)
- 14-30 dias: 85% (alta confianca)
- 30+ dias: 90% (muito confiavel)

### Apresentacao: "Quanto preciso investir para bater X leads?"

```
## Simulador de Investimento — Meta: {meta} leads/mes

**Performance atual da campanha:**
- CPL real: R$ {cpl}
- Tendencia: {tendencia}
- Leads atuais/mes: {leads_atual}
- Budget atual: R$ {budget}/dia

**Para atingir {meta} leads/mes:**

| Cenario | CPL Ajustado | Budget Necessario/dia | Budget/mes | Aumento vs atual |
|---------|-------------|----------------------|-----------|-----------------|
| Otimista | R$ {cpl_o} | R$ {bud_o} | R$ {bud_o*30} | +{var_o}% |
| Realista | R$ {cpl_r} | R$ {bud_r} | R$ {bud_r*30} | +{var_r}% |
| Pessimista | R$ {cpl_p} | R$ {bud_p} | R$ {bud_p*30} | +{var_p}% |

**Formula:**
Budget necessario = meta_leads x CPL_ajustado / 30 dias

**Alertas:**
{se aumento > 100%: "Aumento superior a 100%. Recomendo escalar gradualmente em 20% a cada 3-5 dias para evitar reset da learning phase."}
{se meta > reach estimado: "Atencao: a meta pode ser superior ao tamanho do publico. Considere expandir targeting."}
{se CPL subindo: "CPL em tendencia de alta. Recomendo otimizar criativos antes de escalar."}
```

### Apresentacao: "Qual a projecao ate o fim do mes?"

Calcular com base nos dias restantes do mes:

```
## Projecao para Fechamento do Mes

**Hoje:** {data} ({dia_do_mes}/{dias_no_mes})
**Dias restantes:** {dias_restantes}

**Acumulado ate agora:**
- Leads: {leads_acumulados}
- Gasto: R$ {spend_acumulado}
- CPL: R$ {cpl_acumulado}

**Projecao ate fim do mes (mantendo budget atual):**
- Leads estimados total: {leads_acumulados + (leads_dia * dias_restantes)}
- Gasto estimado total: R$ {spend_acumulado + (spend_dia * dias_restantes)}

**Para bater a meta de {meta} leads ate fim do mes:**
- Faltam: {meta - leads_acumulados} leads em {dias_restantes} dias
- Necessario: {leads_faltantes / dias_restantes} leads/dia
- Budget necessario: R$ {(leads_faltantes / dias_restantes) * cpl_ajustado}/dia
- vs budget atual: R$ {budget_atual}/dia ({diferenca}%)

{se viavel: "Meta alcancavel com ajuste de budget de {x}%."}
{se dificil: "Meta desafiadora. Alem de aumentar budget, recomendo otimizar criativos e expandir publico."}
{se inviavel: "Meta provavelmente inviavel com os dias restantes. Seria necessario {y} leads/dia, mas a campanha entrega {z}/dia. Considere revisar a meta ou estender o prazo."}
```

### Alertas Automaticos do Forecasting

O heartbeat pode usar o forecasting para alertas proativos:

```
Alertas de projecao:
- "No ritmo atual, voce vai fechar o mes com ~{x} leads (meta: {meta}). Faltam {y}."
- "Se aumentar o budget em {z}%, provavelmente bate a meta."
- "CPL subiu 20% esta semana. Se continuar, vai fechar com {x} leads a menos."
- "Otimo ritmo! Campanha deve bater a meta {n} dias antes do prazo."
```

## Calculadora Rapida

Se o usuario so quiser uma estimativa rapida sem dados historicos:

```
Estimativa rapida (sem historico):
- R$30/dia (~R$900/mes) → ~45-60 leads/mes
- R$60/dia (~R$1.800/mes) → ~90-120 leads/mes
- R$100/dia (~R$3.000/mes) → ~150-200 leads/mes
- R$200/dia (~R$6.000/mes) → ~300-400 leads/mes

*Benchmarks CPL R$15-20 para tech/devs Brasil. Resultados reais podem variar.
Use /campaign-analyzer para projecoes baseadas em dados reais.
```

## Restricoes

- NUNCA altere orcamento sem confirmacao explicita do usuario
- NUNCA aumente mais de 20% de uma vez (causa instabilidade no leilao)
- SEMPRE informe o gasto mensal estimado antes de confirmar
- Orcamento minimo por ad set: R$20/dia (recomendacao Meta para learning phase)
- Se o usuario definir um budget muito baixo (< R$15/dia), avisar que pode nao sair da learning phase
- NUNCA defina lifetime_budget sem data de termino
