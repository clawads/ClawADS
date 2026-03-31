---
name: lead-gen-creator
description: Cria campanhas completas de lead generation no Meta Ads para Instagram, seguindo a hierarquia Campaign > Ad Set > Ad com formularios instantaneos otimizados para captura de leads.
---

# Lead Gen Creator — Criacao de Campanhas de Leads

## Quando Usar

- Quando o usuario quiser criar uma nova campanha de lead generation
- Quando o campaign-analyzer recomendar criar uma nova campanha
- Quando o usuario pedir para criar anuncios para captar leads

## Processo

### Passo 1: Verificar Credenciais

Verificar se as credenciais estao configuradas. Se nao, executar `/onboarding`.

### Passo 2: Briefing com o Usuario

Coletar informacoes essenciais via chat:

```
Para criar sua campanha de leads, preciso de algumas informacoes:

1. Nome da campanha (ou posso sugerir um)
2. Orcamento diario ou total (em BRL)
3. Data de inicio e fim (ou campanha continua?)
4. Publico-alvo especifico (ou usar segmentacao padrao para devs BR?)
5. Qual produto promover?
   a) Teste Gratis do Claude Code + Comunidade (entrada do funil — recomendado)
   b) Comunidade Mensal (R$200/mes)
   c) Acervo Completo (R$997 a vista ou 6x R$166)
6. Campos do formulario de lead (padrao: nome, email, telefone)
```

### Passo 3: Criar Campanha

```json
POST /{ad_account_id}/campaigns
{
  "name": "{nome_campanha}",
  "objective": "OUTCOME_LEADS",
  "status": "PAUSED",
  "special_ad_categories": [],
  "bid_strategy": "LOWEST_COST_WITHOUT_CAP"
}
```

**IMPORTANTE:** Sempre criar com status PAUSED. So ativar com autorizacao explicita.

### Passo 4: Criar Lead Form (Formulario Instantaneo)

```json
POST /{page_id}/leadgen_forms
{
  "name": "Lead Form - Claude Code - {data}",
  "follow_up_action_url": "https://claude.ai/code",
  "questions": [
    {
      "type": "FULL_NAME",
      "key": "full_name"
    },
    {
      "type": "EMAIL",
      "key": "email"
    },
    {
      "type": "PHONE",
      "key": "phone_number"
    },
    {
      "type": "CUSTOM",
      "key": "experience_level",
      "label": "Qual seu nivel de experiencia com IA?",
      "options": [
        {"value": "iniciante", "key": "beginner"},
        {"value": "intermediario", "key": "intermediate"},
        {"value": "avancado", "key": "advanced"}
      ]
    }
  ],
  "context_card": {
    "title": "Teste Gratis — Claude Code + Comunidade",
    "content": [
      "Acesso gratis ao Claude Code mais potente (Opus) compartilhado",
      "Comunidade ativa de devs BR que usam IA para ganhar mais",
      "Prompts, workflows e automacoes prontos para usar",
      "Sem compromisso — teste antes de decidir"
    ],
    "style": "PARAGRAPH_STYLE"
  },
  "privacy_policy": {
    "url": "{url_politica_privacidade}",
    "link_text": "Politica de Privacidade"
  },
  "thank_you_page": {
    "title": "Voce esta dentro!",
    "body": "Em breve voce recebera acesso ao Claude Code compartilhado e a comunidade. Prepare-se para transformar sua produtividade e seus resultados!",
    "button_text": "Acessar a Comunidade",
    "button_type": "VIEW_WEBSITE",
    "website_url": "{url_comunidade}"
  }
}
```

### Passo 5: Criar Ad Set

```json
POST /{ad_account_id}/adsets
{
  "name": "AdSet - Devs BR - Instagram - {data}",
  "campaign_id": "{campaign_id}",
  "status": "PAUSED",
  "daily_budget": "{orcamento_diario_centavos}",
  "billing_event": "IMPRESSIONS",
  "optimization_goal": "LEAD_GENERATION",
  "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
  "targeting": {
    "geo_locations": {
      "countries": ["BR"]
    },
    "age_min": 22,
    "age_max": 45,
    "locales": [{"key": 24, "name": "Portuguese"}],
    "flexible_spec": [
      {
        "interests": [
          {"id": "6003139266461", "name": "Artificial intelligence"},
          {"id": "6003384248805", "name": "Computer programming"},
          {"id": "6003397425735", "name": "Software development"},
          {"id": "6003017847882", "name": "Python (programming language)"},
          {"id": "6003277229371", "name": "JavaScript"},
          {"id": "6003402857620", "name": "GitHub"},
          {"id": "6003322286148", "name": "Visual Studio Code"},
          {"id": "6003325434582", "name": "Open-source software"}
        ]
      }
    ],
    "exclusions": {
      "flexible_spec": [
        {
          "interests": [
            {"id": "6003246841461", "name": "Anthropic"}
          ]
        }
      ]
    },
    "publisher_platforms": ["instagram"],
    "instagram_positions": ["stream", "story", "reels"]
  },
  "promoted_object": {
    "page_id": "{page_id}",
    "leadgen_form_id": "{form_id}"
  }
}
```

### Passo 6: Criar Ad Creative

```json
POST /{ad_account_id}/adcreatives
{
  "name": "Creative - Claude Code Lead Gen - {data}",
  "object_story_spec": {
    "page_id": "{page_id}",
    "instagram_user_id": "{instagram_account_id}",
    "link_data": {
      "message": "{copy_principal}",
      "name": "{headline}",
      "description": "{descricao}",
      "link": "https://claude.ai/code",
      "call_to_action": {
        "type": "SIGN_UP",
        "value": {
          "lead_gen_form_id": "{form_id}"
        }
      },
      "image_hash": "{image_hash}"
    }
  }
}
```

### Passo 7: Criar Ad

```json
POST /{ad_account_id}/ads
{
  "name": "Ad - Claude Code - {variacao}",
  "adset_id": "{adset_id}",
  "creative": {"creative_id": "{creative_id}"},
  "status": "PAUSED"
}
```

### Passo 8: Preview e Confirmacao

Antes de ativar, apresentar um resumo completo:

```
## Resumo da Campanha

**Campanha:** {nome}
**Objetivo:** Lead Generation
**Status:** PAUSADA (aguardando sua aprovacao)

**Ad Set:**
- Orcamento: R$ {orcamento}/dia
- Publico: Devs e profissionais de tech, 22-45 anos, Brasil
- Posicionamento: Instagram (Feed, Stories, Reels)
- Interesses: IA, Programacao, GitHub, VS Code

**Anuncio:**
- Headline: {headline}
- Copy: {copy}
- CTA: Cadastre-se

**Formulario de Lead:**
- Campos: Nome, Email, Telefone, Nivel de experiencia com IA
- Pagina de agradecimento configurada

Deseja que eu ative a campanha? (sim/nao)
```

### Passo 9: Ativacao (apenas com autorizacao)

Somente apos confirmacao explicita do usuario:

```
POST /{campaign_id}
{"status": "ACTIVE"}

POST /{adset_id}
{"status": "ACTIVE"}

POST /{ad_id}
{"status": "ACTIVE"}
```

## Templates de Segmentacao

### Publico 1: Desenvolvedores Early Adopters
- Idade: 22-35
- Interesses: IA, GitHub, VS Code, Python, JavaScript, Open Source
- Comportamento: Early technology adopters

### Publico 2: Tech Leads e Seniors
- Idade: 28-45
- Interesses: Software development, Cloud computing, DevOps, Tech startups
- Cargos: Software Engineer, Tech Lead, CTO, Developer

### Publico 3: Entusiastas de IA
- Idade: 20-40
- Interesses: ChatGPT, Machine Learning, AI tools, Automation
- Comportamento: Technology early adopters

## Restricoes

- NUNCA crie campanhas com status ACTIVE diretamente
- SEMPRE apresente preview completo antes de ativar
- SEMPRE confirme o orcamento com o usuario antes de criar
- Valide se o token tem permissao ads_management antes de criar
- Nao crie mais de 3 variacoes de ad sem aprovacao do usuario
