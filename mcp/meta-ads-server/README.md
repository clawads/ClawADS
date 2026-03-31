# MCP Server — Meta Marketing API

Servidor MCP para integrar o picoclaw com a Meta Marketing API v21.0.

## Funcionalidades

### Tools Disponiveis

#### Campanhas
- `meta_list_campaigns` — Lista campanhas da conta
- `meta_get_campaign` — Detalhes de uma campanha
- `meta_create_campaign` — Cria nova campanha
- `meta_update_campaign` — Atualiza campanha existente

#### Ad Sets
- `meta_list_adsets` — Lista ad sets de uma campanha
- `meta_get_adset` — Detalhes de um ad set
- `meta_create_adset` — Cria novo ad set
- `meta_update_adset` — Atualiza ad set existente

#### Ads
- `meta_list_ads` — Lista ads de um ad set
- `meta_get_ad` — Detalhes de um ad
- `meta_create_ad` — Cria novo ad
- `meta_update_ad` — Atualiza ad existente

#### Criativos
- `meta_create_creative` — Cria ad creative
- `meta_upload_image` — Faz upload de imagem para a conta

#### Lead Forms
- `meta_list_leadgen_forms` — Lista formularios de lead
- `meta_create_leadgen_form` — Cria formulario de lead
- `meta_get_leads` — Busca leads captados

#### Insights & Relatorios
- `meta_get_insights` — Busca metricas de performance
- `meta_get_account_insights` — Metricas gerais da conta

#### Utilidades
- `meta_validate_token` — Valida token de acesso
- `meta_get_account_info` — Info da conta de anuncios
- `meta_search_interests` — Busca interesses para targeting

## Variaveis de Ambiente Necessarias

```
META_ACCESS_TOKEN — Token de acesso (obrigatorio)
META_AD_ACCOUNT_ID — ID da conta de anuncios (obrigatorio)
META_PAGE_ID — ID da pagina do Facebook (obrigatorio)
META_INSTAGRAM_ACCOUNT_ID — ID da conta Instagram (obrigatorio)
META_APP_ID — ID do app (opcional, para refresh de token)
META_APP_SECRET — Secret do app (opcional, para refresh de token)
```

## API Version

Este servidor usa a Meta Marketing API **v21.0**.

Referencia: https://developers.facebook.com/docs/marketing-api/

## Seguranca

- Todas as operacoes de escrita (create/update) requerem confirmacao do usuario
- Tokens nunca sao logados ou armazenados em disco
- Rate limiting automatico conforme limites da Meta API
