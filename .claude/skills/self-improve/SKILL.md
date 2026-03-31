---
name: self-improve
description: Sistema de auto-melhoria continua. O agente aprende com resultados reais, atualiza seus proprios benchmarks, documenta aprendizados e evolui estrategias ao longo do tempo.
---

# Self-Improve — Auto-Melhoria Continua

## Quando Usar

- Automaticamente apos cada ciclo de analise do campaign-analyzer
- Quando o heartbeat completar 7 dias de dados
- Quando o usuario pedir para o agente "aprender" ou "melhorar"
- Apos pausar ou escalar campanhas (documentar o motivo e resultado)
- Semanalmente como parte do ciclo de otimizacao

## Arquitetura de Aprendizado

O agente mantem 3 arquivos de conhecimento na raiz do projeto:

```
LEARNINGS.md    — Registro de aprendizados (o que funcionou, o que nao funcionou)
BENCHMARKS.md   — Benchmarks reais da conta (atualizados com dados reais)
PLAYBOOK.md     — Playbook evolutivo (estrategias validadas por dados)
```

Esses arquivos sao lidos pelo agente em TODA interacao para informar decisoes.

---

## Processo

### Passo 1: Coletar Resultados

Apos cada acao significativa (criar campanha, pausar ad, escalar budget, trocar criativo), registrar:

```
Data: {data}
Acao: {o que foi feito}
Contexto: {por que foi feito}
Metricas antes: {CPL, CTR, CPC, CPQL antes da acao}
Metricas depois (7 dias): {CPL, CTR, CPC, CPQL depois}
Resultado: {melhorou / piorou / sem impacto}
Aprendizado: {o que aprendemos com isso}
```

### Passo 2: Atualizar LEARNINGS.md

Adicionar entrada no LEARNINGS.md com formato:

```markdown
### {data} — {titulo do aprendizado}

**Acao:** {descricao}
**Resultado:** {positivo/negativo/neutro}
**Impacto:** CPL {antes} → {depois} ({variacao}%)
**Aprendizado:** {insight acionavel}
**Aplicar em:** {quais skills/estrategias devem ser atualizadas}
```

Categorizar aprendizados por tipo:
- CRIATIVO: O que funciona em copies, angulos, formatos
- PUBLICO: Quais segmentos performam melhor
- BUDGET: Como orcamento afeta performance
- FORMULARIO: O que melhora taxa de conversao do lead form
- HORARIO: Melhores horarios/dias
- LANCE: Estrategias de bidding que funcionam
- GERAL: Outros insights

### Passo 3: Atualizar BENCHMARKS.md

Substituir benchmarks genericos por dados reais da conta:

```markdown
# Benchmarks — {nome_da_conta}
Ultima atualizacao: {data}

## Metricas Reais (baseadas em {n} dias de dados)

| Metrica | Benchmark Anterior | Valor Real | Atualizado em |
|---------|-------------------|------------|---------------|
| CPL | R$15-20 (generico) | R$ {cpl_real} | {data} |
| CTR | 1.2-2.0% (generico) | {ctr_real}% | {data} |
| CPC | R$2-5 (generico) | R$ {cpc_real} | {data} |
| CPM | R$20-35 (generico) | R$ {cpm_real} | {data} |
| Conv Rate | 8-15% (generico) | {conv_real}% | {data} |
| CPQL | N/A | R$ {cpql_real} | {data} |
| Frequencia ideal | < 3 (generico) | {freq_ideal} | {data} |

## Por Publico
| Publico | CPL | CTR | Conv Rate | Veredicto |
|---------|-----|-----|-----------|-----------|
| Devs IA | R$ {x} | {y}% | {z}% | {melhor/pior/medio} |
| Devs Tools | R$ {x} | {y}% | {z}% | {melhor/pior/medio} |
| Tech Leads | R$ {x} | {y}% | {z}% | {melhor/pior/medio} |

## Por Criativo
| Angulo | CPL Medio | CTR Medio | Melhor Formato | Veredicto |
|--------|----------|----------|----------------|-----------|
| Economia | R$ {x} | {y}% | {formato} | {melhor/pior} |
| Produtividade | R$ {x} | {y}% | {formato} | {melhor/pior} |
| Hack | R$ {x} | {y}% | {formato} | {melhor/pior} |
| FOMO | R$ {x} | {y}% | {formato} | {melhor/pior} |

## Por Horario
| Periodo | CPL Medio | Volume | Recomendacao |
|---------|----------|--------|-------------|
| 6h-10h | R$ {x} | {vol} | {investir/evitar} |
| 10h-14h | R$ {x} | {vol} | {investir/evitar} |
| 14h-18h | R$ {x} | {vol} | {investir/evitar} |
| 18h-22h | R$ {x} | {vol} | {investir/evitar} |
| 22h-6h | R$ {x} | {vol} | {investir/evitar} |

## Por Posicionamento
| Posicionamento | CPL | CTR | Recomendacao |
|---------------|-----|-----|-------------|
| Instagram Feed | R$ {x} | {y}% | {investir/evitar} |
| Instagram Stories | R$ {x} | {y}% | {investir/evitar} |
| Instagram Reels | R$ {x} | {y}% | {investir/evitar} |
```

### Passo 4: Atualizar PLAYBOOK.md

Manter um playbook evolutivo de estrategias validadas:

```markdown
# Playbook — Estrategias Validadas
Ultima atualizacao: {data}
Total de testes realizados: {n}
Taxa de acerto: {acertos/total}%

## Estrategias que FUNCIONAM (validadas por dados)

### 1. {nome_estrategia}
- **Testada em:** {data}
- **Resultado:** CPL reduziu {x}% / Leads aumentaram {y}%
- **Como replicar:** {passo a passo}
- **Quando usar:** {contexto ideal}
- **Confianca:** {alta/media} (testada {n} vezes)

## Estrategias que NAO FUNCIONAM (evitar)

### 1. {nome_estrategia}
- **Testada em:** {data}
- **Resultado:** {o que deu errado}
- **Por que nao funciona:** {explicacao}
- **Alternativa:** {o que fazer ao inves}

## Estrategias em TESTE (aguardando dados)

### 1. {nome_estrategia}
- **Iniciada em:** {data}
- **Hipotese:** {o que esperamos}
- **Resultado parcial:** {dados ate agora}
- **Decisao em:** {data prevista}
```

### Passo 5: Retroalimentar Skills

Com base nos aprendizados, o agente deve ATUALIZAR as skills existentes:

#### Atualizar creative-generator:
- Adicionar angulos que funcionaram
- Remover angulos que falharam
- Ajustar templates de copy com base nos vencedores

#### Atualizar campaign-analyzer:
- Substituir benchmarks genericos pelos reais (BENCHMARKS.md)
- Ajustar thresholds de alerta baseado no historico

#### Atualizar budget-optimizer:
- Usar CPL real para projecoes (nao benchmarks genericos)
- Ajustar fator de escala com base em dados reais de escalamento

#### Atualizar strategy-engine:
- Promover estrategias validadas para "recomendadas"
- Marcar estrategias que falharam como "evitar"
- Adicionar novas estrategias descobertas

#### Atualizar heartbeat:
- Ajustar thresholds de anomalia com base em desvio padrao real
- Adicionar novos checks baseados em problemas ja encontrados

### Passo 6: Auto-Avaliacao

Semanalmente, o agente deve avaliar sua propria performance:

```
## Auto-Avaliacao Semanal — {data}

### Precisao das Projecoes
- Leads projetados: {x}
- Leads reais: {y}
- Erro: {|x-y|/y * 100}%
- Tendencia do erro: {superestima/subestima/preciso}
- Ajuste: {como corrigir o vies}

### Qualidade das Recomendacoes
- Recomendacoes feitas: {n}
- Recomendacoes aceitas pelo usuario: {n}
- Recomendacoes que melhoraram performance: {n}
- Taxa de acerto: {acertos/total}%

### Decisoes de Pausar/Escalar
- Campanhas pausadas: {n}
- Pausas que foram corretas (CPL nao recuperou): {n}
- Escaladas realizadas: {n}
- Escaladas que mantiveram CPL: {n}

### Acoes de Melhoria
1. {acao concreta para melhorar}
2. {acao concreta para melhorar}
3. {acao concreta para melhorar}
```

---

## Regras de Atualizacao

### Quando atualizar benchmarks:
- Minimo 7 dias de dados novos
- Minimo 1000 impressoes
- Usar media ponderada: 70% dados recentes (14d) + 30% historico total
- Nunca descartar historico, apenas ponderar

### Quando promover estrategia para "validada":
- Testada pelo menos 2 vezes
- Resultado positivo em ambas
- Impacto > 10% de melhoria em metrica chave

### Quando marcar estrategia como "evitar":
- Testada pelo menos 2 vezes
- Resultado negativo em ambas
- OU resultado muito negativo 1 vez (CPL > 3x)

### Quando sugerir estrategia nova:
- Identificar padrao nos dados que nenhuma estrategia atual cobre
- Apresentar ao usuario como "hipotese a testar"
- So adicionar ao playbook apos validacao

## Formato de Commit

Ao atualizar arquivos de aprendizado, commitar com:
```
learn: {descricao do aprendizado}
```

Exemplos:
- `learn: angulo economia performa 40% melhor que FOMO para devs BR`
- `learn: CPL real da conta e R$12, atualizar benchmarks`
- `learn: stories converte 2x melhor que feed para lead gen`

## Restricoes

- NUNCA deletar aprendizados antigos — sao historico valioso
- NUNCA atualizar benchmarks com menos de 7 dias de dados
- SEMPRE manter backup do benchmark anterior ao atualizar
- SEMPRE apresentar ao usuario o que mudou e por que
- Se uma estrategia que funcionava parar de funcionar, investigar antes de marcar como "evitar"
- Aprendizados devem ser factuais (baseados em dados), nao opinativos
