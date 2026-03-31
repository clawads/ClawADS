# Heartbeat Checklist — Meta Ads Lead Generation

Leia este checklist a cada execucao. Siga estritamente.
Se nada precisar de atencao, responda apenas: HEARTBEAT_OK

## Checklist

### 1. Validar Conexao
- [ ] Token de acesso esta valido? (`GET /me`)
- [ ] Conta de anuncios esta acessivel? (`GET /{account_id}`)
- Se falhar: alertar usuario sobre token expirado

### 2. Verificar Campanhas Ativas
- [ ] Listar campanhas com status ACTIVE
- [ ] Para cada campanha, verificar `effective_status`
- Se alguma campanha parou de entregar: ALERTA CRITICO

### 3. Metricas de Performance (ultimas 24h)
- [ ] Buscar insights de todas as campanhas ativas
- [ ] Calcular: CPL, CTR, CPC, CPM, Frequencia

### 4. Avaliar Thresholds
- [ ] CPL > R$30? → ALERTA ALTO
- [ ] CTR < 0.8%? → ALERTA ALTO
- [ ] CPC > R$5? → ALERTA MEDIO
- [ ] Frequencia > 4? → ALERTA MEDIO
- [ ] 0 leads com spend > R$50? → ALERTA CRITICO
- [ ] Spend > 80% do orcamento diario? → ALERTA INFO

### 5. Fadiga Criativa
- [ ] CTR caiu >15% vs media 3 dias? → Sugerir refresh de criativos
- [ ] Frequencia > 3 E CTR caindo? → Publico saturado

### 6. Quality Ranking
- [ ] Verificar quality_ranking, engagement_rate_ranking, conversion_rate_ranking
- [ ] Algum ranking "below_average_35"? → ALERTA ALTO

### 7. Projecao de Fechamento
- [ ] Calcular leads acumulados no mes
- [ ] Projetar leads ate fim do mes no ritmo atual
- [ ] Se meta definida: comparar projecao vs meta
- [ ] Se projecao < 80% da meta? → ALERTA: "No ritmo atual, vai fechar com X leads (meta: Y)"
- [ ] Se projecao > meta? → INFO: "Campanha no ritmo para bater a meta"
- [ ] Se CPL subindo e projecao em risco? → Sugerir aumento de budget com simulacao

### 8. Auto-Melhoria (a cada 7 execucoes)
- [ ] Comparar metricas atuais vs BENCHMARKS.md
- [ ] Se diferenca > 15%: atualizar benchmarks com dados reais
- [ ] Registrar qualquer aprendizado novo no LEARNINGS.md
- [ ] Verificar se alguma estrategia em teste no PLAYBOOK.md tem dados suficientes para validar
- [ ] Comparar projecao anterior vs resultado real: calcular erro e ajustar modelo

### 9. Relatorio
- Se houver alertas: apresentar relatorio completo
- Se nao houver alertas: responder HEARTBEAT_OK
