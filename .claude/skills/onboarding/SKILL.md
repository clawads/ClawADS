---
name: onboarding
description: Guia interativo para configuracao de credenciais da Meta Marketing API. Solicita e valida todas as chaves necessarias diretamente no chat.
---

# Onboarding — Configuracao Meta Ads

## Quando Usar

- Na primeira interacao com o usuario
- Quando qualquer operacao falhar por falta de credenciais
- Quando o usuario pedir para reconfigurar as credenciais

## Processo

### Passo 1: Boas-vindas

Apresente-se e explique o objetivo:

```
Ola! Sou seu agente especialista em Meta Ads para geracao de leads.
Antes de comecarmos, preciso configurar o acesso a sua conta do Meta Ads.
Vou te guiar passo a passo — e rapido!
```

### Passo 2: Verificar Variaveis de Ambiente

Verifique se as seguintes variaveis de ambiente ja estao configuradas:

- `META_ACCESS_TOKEN`
- `META_AD_ACCOUNT_ID`
- `META_PAGE_ID`
- `META_INSTAGRAM_ACCOUNT_ID`
- `META_APP_ID`
- `META_APP_SECRET`

Para cada variavel ausente, solicite ao usuario.

### Passo 3: Solicitar Credenciais

Para cada credencial faltante, explique ao usuario como obter:

#### META_ACCESS_TOKEN
```
1. Acesse https://developers.facebook.com/tools/explorer/
2. Selecione seu app
3. Clique em "Generate Access Token"
4. Selecione as permissoes: ads_management, ads_read, leads_retrieval, pages_show_list, pages_read_engagement, instagram_basic
5. Copie o token gerado
```

#### META_AD_ACCOUNT_ID
```
1. Acesse https://business.facebook.com/settings/ad-accounts
2. Selecione sua conta de anuncios
3. O ID esta no formato act_XXXXXXXXX
4. Copie o ID completo incluindo o prefixo "act_"
```

#### META_PAGE_ID
```
1. Acesse https://business.facebook.com/settings/pages
2. Selecione a pagina vinculada aos anuncios
3. O ID numerico aparece na URL ou nas configuracoes da pagina
```

#### META_INSTAGRAM_ACCOUNT_ID
```
1. Acesse https://business.facebook.com/settings/instagram-accounts
2. Selecione a conta do Instagram vinculada
3. Copie o ID numerico da conta
```

#### META_APP_ID e META_APP_SECRET
```
1. Acesse https://developers.facebook.com/apps/
2. Selecione seu app (ou crie um novo do tipo "Business")
3. Va em Configuracoes > Basico
4. Copie o "ID do Aplicativo" (APP_ID) e "Chave Secreta" (APP_SECRET)
```

### Passo 4: Instrucoes de Configuracao

Depois de coletar todas as credenciais, instrua o usuario a configura-las como variaveis de ambiente:

```bash
export META_ACCESS_TOKEN="seu_token_aqui"
export META_AD_ACCOUNT_ID="act_XXXXXXXXX"
export META_PAGE_ID="XXXXXXXXXXXXXXX"
export META_INSTAGRAM_ACCOUNT_ID="XXXXXXXXXXXXXXX"
export META_APP_ID="XXXXXXXXXXXXXXX"
export META_APP_SECRET="XXXXXXXXXXXXXXXXXXXXXXX"
```

Recomende adicionar ao `.bashrc`, `.zshrc` ou usar um `.env` local (fora do versionamento).

### Passo 5: Validacao

Apos a configuracao, valide o token fazendo uma chamada de teste:

```
GET https://graph.facebook.com/v21.0/me?access_token={TOKEN}
```

Se retornar o nome do usuario, o token esta valido. Em seguida, valide o acesso a conta de anuncios:

```
GET https://graph.facebook.com/v21.0/{AD_ACCOUNT_ID}?fields=name,account_status&access_token={TOKEN}
```

### Passo 6: Confirmacao

Confirme ao usuario que tudo esta configurado e sugira os proximos passos:

```
Tudo configurado! Sua conta esta pronta para usar.

Proximos passos sugeridos:
- /campaign-analyzer — Para analisar suas campanhas existentes
- /lead-gen-creator — Para criar uma nova campanha de leads
- /creative-generator — Para gerar copies e criativos
```

## Restricoes

- NUNCA armazene credenciais em arquivos do projeto
- NUNCA exiba tokens completos no chat — mostre apenas os primeiros e ultimos 4 caracteres
- Se o usuario colar um token no chat, avise que e inseguro e oriente a usar variaveis de ambiente
- Tokens devem ser tratados como dados sensiveis em todas as interacoes
