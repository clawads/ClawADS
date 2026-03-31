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

## Calculadora Rapida

Se o usuario so quiser uma estimativa rapida:

```
Orcamento rapido:
- R$30/dia (~R$900/mes) → ~45-60 leads/mes
- R$60/dia (~R$1.800/mes) → ~90-120 leads/mes
- R$100/dia (~R$3.000/mes) → ~150-200 leads/mes
- R$200/dia (~R$6.000/mes) → ~300-400 leads/mes

*Estimativas baseadas em CPL medio de R$15-20 para tech/devs Brasil
```

## Restricoes

- NUNCA altere orcamento sem confirmacao explicita do usuario
- NUNCA aumente mais de 20% de uma vez (causa instabilidade no leilao)
- SEMPRE informe o gasto mensal estimado antes de confirmar
- Orcamento minimo por ad set: R$20/dia (recomendacao Meta para learning phase)
- Se o usuario definir um budget muito baixo (< R$15/dia), avisar que pode nao sair da learning phase
- NUNCA defina lifetime_budget sem data de termino
