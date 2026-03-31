---
name: strategy-engine
description: Motor de estrategias de otimizacao para maximizar leads qualificados e minimizar custo. Combina testes de criativos, segmentacao de publico, retargeting, lookalike, otimizacao de funil e foco em ROI.
---

# Strategy Engine — Estrategias de Otimizacao com Foco em ROI

## Quando Usar

- Quando o usuario quiser mais leads pagando menos
- Quando o usuario perguntar sobre estrategias de otimizacao
- Quando o campaign-analyzer detectar oportunidades de melhoria
- Quando o usuario quiser melhorar a qualidade dos leads
- Quando o foco for retorno sobre investimento

## Metricas Centrais de ROI

Antes de qualquer estrategia, calcular e apresentar:

```
## Dashboard de ROI

**Investimento (30d):** R$ {spend}
**Leads totais:** {leads}
**CPL (Custo por Lead):** R$ {cpl}
**Leads qualificados:** {leads_qualificados} ({taxa_qualificacao}%)
**CPQL (Custo por Lead Qualificado):** R$ {cpql}
**Valor medio do lead:** R$ {valor_lead}
**ROI:** {(receita_leads - spend) / spend * 100}%
**ROAS:** {receita_leads / spend}x

Meta de ROI: Cada R$1 investido deve retornar R$ {meta_roas}
```

---

## ESTRATEGIA 1: Teste Sistematico de Criativos

### Framework de Testes A/B/C

Nunca rodar apenas 1 criativo. Sempre testar em camadas:

#### Fase 1 — Teste de Dor (semana 1)
Criar 4 ads com DORES diferentes, MESMO publico:
```
Ad A: Medo de demissao ("Programadores estao sendo demitidos")
Ad B: Estagnacao ("3 anos no mesmo cargo. Ate quando?")
Ad C: Burnout ("12h por dia e nunca da conta?")
Ad D: Ambicao ("Tem dev cobrando R$300/hora com IA")

Budget: dividir igualmente
Duracao: 5-7 dias
Metrica de decisao: CPL + Taxa de qualificacao
Vencedor: menor CPQL (nao apenas menor CPL)

REGRA: 80% da copy sobre a DOR. Produto aparece so no final.
```

#### Fase 2 — Teste de Formato (semana 2)
Com o angulo vencedor, testar formatos:
```
Ad A: Imagem estatica (1080x1080 Feed)
Ad B: Carrossel (3-5 slides)
Ad C: Video curto (15s Stories/Reels)
Ad D: Video longo (30-60s Reels)

Budget: dividir igualmente
Duracao: 5-7 dias
Metrica: CPL + engajamento
```

#### Fase 3 — Teste de Copy (semana 3)
Com angulo + formato vencedor, testar variações de copy:
```
Ad A: Copy curta (direto ao ponto)
Ad B: Copy media (problema-solucao)
Ad C: Copy longa (storytelling)

Budget: dividir igualmente
Duracao: 5 dias
Metrica: CTR + conversao
```

#### Fase 4 — Teste de CTA (semana 4)
```
Ad A: "Cadastre-se" (SIGN_UP)
Ad B: "Saiba Mais" (LEARN_MORE)
Ad C: "Comece Agora" (APPLY_NOW)
```

#### Regra de Corte Rapido
- Se um ad tem CPL > 2x da media apos 3 dias e 500+ impressoes: pausar
- Realocar budget para os vencedores
- Documentar aprendizados para proximos testes

### Rotacao de Criativos (Anti-Fadiga)
```
Regra: A cada 2-3 semanas, mesmo criativos vencedores precisam de refresh
Sinais de fadiga: CTR caiu 20% + Frequencia > 3
Acao: Gerar variacao do vencedor (mesmo angulo, nova abordagem visual/copy)
```

---

## ESTRATEGIA 2: Segmentacao Inteligente de Publico

### Camada 1: Publicos de Interesse (Topo de Funil)

Testar publicos separados por PERSONA/DOR em ad sets diferentes:

```
Ad Set A — O Ameacado (medo de demissao):
  Interesses: AI, Machine Learning, ChatGPT, Layoffs, Career Development
  Idade: 20-35 (juniors e plenos mais vulneraveis)
  Copy: Foco em medo de substituicao

Ad Set B — O Estagnado (carreira parada):
  Interesses: Software Development, Career Growth, Tech Salary
  Idade: 25-40 (quem ja tem experiencia mas parou)
  Copy: Foco em estagnacao e frustacao

Ad Set C — O Sobrecarregado (burnout):
  Interesses: Productivity, Freelancing, Remote Work, Work-life balance
  Idade: 25-45 (freelancers e profissionais sobrecarregados)
  Copy: Foco em tempo e exaustao

Ad Set D — O Ambicioso (quer ganhar mais):
  Interesses: Entrepreneurship, Startup, SaaS, Tech Business, Side Projects
  Idade: 22-40 (quem busca crescimento financeiro)
  Copy: Foco em dinheiro e oportunidade
```

**Regra:** Usar exclusoes entre ad sets para evitar sobreposicao de publico.

### Camada 2: Lookalike Audiences (Escala)

Apos captar leads, criar publicos semelhantes:

```
Fonte: Lista de leads qualificados (os que converteram)
Lookalike 1%: Mais similar (menor, mais qualificado)
Lookalike 3%: Equilibrio
Lookalike 5%: Maior volume, menos preciso

Estrategia:
1. Comeca com Lookalike 1% (melhor CPQL)
2. Se escalar, expandir para 3%
3. Usar 5% apenas se 1% e 3% saturarem
```

Para criar via API:
```
POST /{ad_account_id}/customaudiences
{
  "name": "Lookalike 1% - Leads Qualificados",
  "subtype": "LOOKALIKE",
  "origin_audience_id": "{custom_audience_id}",
  "lookalike_spec": {
    "country": "BR",
    "ratio": 0.01
  }
}
```

### Camada 3: Custom Audiences (Retargeting)

```
Publico A — Visitantes do site (ultimos 30 dias):
  Quem visitou mas nao converteu
  Copy: "Ainda pensando? Veja o que mudou..."

Publico B — Engajamento Instagram (ultimos 60 dias):
  Quem interagiu com posts/stories
  Copy: "Voce ja nos conhece. Agora experimente."

Publico C — Video viewers (75%+):
  Quem assistiu 75%+ de videos de anuncio
  Copy: "Voce viu como funciona. Agora teste gratis."

Publico D — Lead form aberto mas nao enviado:
  Quem abriu o formulario mas desistiu
  Copy: "Faltou pouco! Complete seu cadastro em 10 segundos."

Publico E — Leads antigos (remarketing):
  Quem ja e lead mas nao converteu em cliente
  Copy: "Novidades no Claude Code que voce precisa ver."
```

### Exclusoes Essenciais

SEMPRE excluir:
- Leads ja captados (evitar pagar de novo pelo mesmo lead)
- Clientes ja convertidos
- Funcionarios / equipe interna

---

## ESTRATEGIA 3: Otimizacao de Formulario para Qualidade

### Formulario Otimizado para Qualidade

Ativar `is_optimized_for_quality=true` no lead form:
- Adiciona tela de revisao antes do envio
- Menos leads, porem mais qualificados
- Reduz leads falsos/acidentais

### Perguntas de Qualificacao

Adicionar perguntas que filtram leads ruins:

```
Pergunta obrigatoria: "Qual seu nivel de experiencia com IA?"
- Iniciante (baixa qualificacao para devs)
- Intermediario (media)
- Avancado (alta qualificacao)

Pergunta filtro: "Voce usa ferramentas de codigo com IA atualmente?"
- Sim, diariamente
- Sim, ocasionalmente
- Nao, mas quero comecar
- Nao tenho interesse (desqualifica)
```

### Formulario Longo vs Curto (Teste)
```
Form A (Curto - 3 campos): Nome, Email, Nivel IA
  → Mais leads, menos qualificados

Form B (Medio - 5 campos): Nome, Email, Telefone, Nivel IA, Ferramenta atual
  → Equilibrio

Form C (Longo - 7 campos): + Empresa, Cargo, Budget mensal para tools
  → Poucos leads, altamente qualificados

Metrica de decisao: CPQL (custo por lead QUALIFICADO), nao CPL
```

---

## ESTRATEGIA 4: Otimizacao de Lances e Budget

### Migrar de Lowest Cost para Cost Cap

```
Fase 1 (primeiros 7 dias): LOWEST_COST_WITHOUT_CAP
  → Deixar Meta encontrar o publico
  → Coletar dados de CPL real

Fase 2 (apos dados): COST_CAP
  → Definir cost cap = CPL medio real * 0.9
  → Forca Meta a buscar leads mais baratos
  → Se entrega cair muito, subir cap em 10%

Fase 3 (escala): BID_CAP
  → Definir bid maximo baseado no valor do lead
  → Formula: bid_cap = valor_medio_lead * taxa_conversao * margem_desejada
```

### Advantage Campaign Budget (ACB)

Quando tiver 3+ ad sets, ativar ACB:
```
POST /{campaign_id}
{"daily_budget": "{budget_total}", "bid_strategy": "LOWEST_COST_WITHOUT_CAP"}
```
Meta distribui automaticamente para os ad sets com melhor performance.

### Day Parting (Horarios)

Analisar insights por hora do dia:
```
GET /{campaign_id}/insights
  ?fields=spend,actions,cost_per_action_type
  &breakdowns=hourly_stats_aggregated_by_advertiser_time_zone
  &date_preset=last_14d
```

Se identificar horarios com CPL muito alto:
- Usar ad scheduling para pausar nesses horarios
- Concentrar budget nos horarios de melhor performance
- Tipicamente para tech BR: 8h-12h e 14h-18h (horario comercial)

---

## ESTRATEGIA 5: Retargeting Multi-Camada

### Funil de Retargeting

```
Camada 1 — Awareness (Topo):
  Publico: Interesses amplos
  Objetivo: Atrair cliques e engajamento
  Budget: 50% do total
  Formato: Video curto, carrossel informativo

Camada 2 — Consideracao (Meio):
  Publico: Quem engajou com Camada 1 (video 50%+, cliques, saves)
  Objetivo: Lead form
  Budget: 30% do total
  Formato: Depoimentos, demonstracao, comparacao
  Copy: Mais detalhada, prova social

Camada 3 — Conversao (Fundo):
  Publico: Quem abriu form mas nao enviou + visitantes site
  Objetivo: Lead form com urgencia
  Budget: 15% do total
  Formato: Oferta direta, escassez
  Copy: "Ultima chance", "Vagas limitadas"

Camada 4 — Reativacao:
  Publico: Leads antigos (30-90 dias) que nao converteram
  Objetivo: Reengajamento
  Budget: 5% do total
  Copy: "Novidades", "Novo recurso", "Preco especial"
```

### Sequencia de Impacto

```
Dia 1-3: Usuario ve anuncio de awareness
Dia 3-7: Se engajou, ve anuncio de consideracao
Dia 7-14: Se clicou/abriu form, ve anuncio de conversao
Dia 14-30: Se nao converteu, ve anuncio de reativacao
Dia 30+: Excluir (evitar queimar budget)
```

---

## ESTRATEGIA 6: Otimizacao por Dados e Sinais

### Breakdown Analysis

Analisar performance por dimensoes:
```
GET /{campaign_id}/insights
  ?fields=spend,actions,cost_per_action_type
  &breakdowns=age,gender
  &date_preset=last_30d
```

Identificar segmentos com melhor ROI:
- Qual faixa etaria tem menor CPQL?
- Qual genero converte melhor?
- Qual posicionamento (feed vs stories vs reels) tem menor CPL?
- Qual dispositivo (iOS vs Android)?
- Qual regiao do Brasil?

**Acao:** Criar ad sets especificos para os melhores segmentos e alocar mais budget.

### Sinais de Qualidade do Meta

Usar os rankings do Meta como guia:
```
quality_ranking: Qualidade percebida do anuncio
engagement_rate_ranking: Taxa de engajamento vs concorrentes
conversion_rate_ranking: Taxa de conversao vs concorrentes
```

Matriz de decisao:
| Quality | Engagement | Conversion | Acao |
|---------|-----------|------------|------|
| Acima media | Acima media | Acima media | ESCALAR |
| Acima media | Acima media | Abaixo media | Otimizar formulario |
| Acima media | Abaixo media | Acima media | Otimizar copy/visual |
| Abaixo media | Abaixo media | Abaixo media | PAUSAR e refazer |

---

## ESTRATEGIA 7: Growth Loops

### Lead Magnet Escalonado
```
Nivel 1 (Lead form simples):
  Oferta: "Guia: Como usar Claude Code no terminal"
  Esforco do lead: Baixo (nome + email)
  
Nivel 2 (Pos-captacao):
  Oferta: "Workshop gravado: Produtividade 3x com IA"
  Esforco: Medio (assistir conteudo)

Nivel 3 (Conversao):
  Oferta: "7 dias gratis de Claude Code via API"
  Esforco: Alto (setup da conta)
```

### Referral via Lead
```
Apos captacao:
"Indique 2 amigos devs e ganhe 30 dias extras"
→ Reduz CAC (custo de aquisicao) organicamente
→ Leads indicados convertem 3-5x melhor
```

---

## Plano de Execucao por Fase

### Fase 1 — Fundacao (Semana 1-2)
1. /lead-gen-creator → Criar campanha com 3-4 ad sets (publicos diferentes)
2. /creative-generator → 3 variacoes por ad set (teste de angulo)
3. /budget-optimizer → Definir budget inicial (LOWEST_COST)
4. /heartbeat → Ativar monitoramento a cada 6h

### Fase 2 — Otimizacao (Semana 3-4)
1. /campaign-analyzer → Identificar vencedores e perdedores
2. Pausar ads/ad sets com baixa performance
3. /creative-generator → Novos criativos baseados nos vencedores
4. /budget-optimizer → Redistribuir budget para vencedores
5. Implementar retargeting Camada 2

### Fase 3 — Escala (Mes 2)
1. Criar Lookalike audiences dos melhores leads
2. Migrar para COST_CAP com base no CPL real
3. Ativar Advantage Campaign Budget
4. Implementar retargeting multi-camada completo
5. Testar day parting

### Fase 4 — Maturidade (Mes 3+)
1. Breakdown analysis completa (idade, genero, regiao, dispositivo)
2. Criar ad sets micro-segmentados para melhores segmentos
3. Implementar growth loops (lead magnet + referral)
4. Formularios otimizados para qualidade
5. Automacao completa via heartbeat Nivel 2

## Metricas de Acompanhamento por Fase

```
| Fase | KPI Principal | Meta |
|------|--------------|------|
| Fundacao | CPL | Descobrir CPL base |
| Otimizacao | CPQL | Reduzir CPQL em 30% |
| Escala | Volume + CPQL | 2x leads mantendo CPQL |
| Maturidade | ROI | R$3+ retorno por R$1 investido |
```

## Restricoes

- NUNCA escalar antes de ter pelo menos 7 dias de dados
- NUNCA criar Lookalike com menos de 100 leads na fonte
- SEMPRE testar uma variavel por vez (nao mudar angulo E formato ao mesmo tempo)
- SEMPRE manter pelo menos 1 ad set de controle (sem alteracoes) para comparacao
- Retargeting so funciona com Pixel/CAPI instalado — verificar com usuario
- Growth loops (referral) requerem infraestrutura propria — sugerir mas nao prometer
