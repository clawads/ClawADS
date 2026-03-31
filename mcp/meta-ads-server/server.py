"""
MCP Server para Meta Marketing API v21.0

Fornece tools para gerenciar campanhas, ad sets, ads, criativos,
lead forms e insights via Meta Graph API.
"""

import os
import json
import urllib.request
import urllib.parse
import urllib.error
from typing import Any

# Meta API config
META_API_VERSION = "v21.0"
META_API_BASE = f"https://graph.facebook.com/{META_API_VERSION}"


def get_env(key: str, required: bool = True) -> str | None:
    value = os.environ.get(key)
    if required and not value:
        raise ValueError(
            f"Variavel de ambiente '{key}' nao configurada. "
            f"Execute /onboarding para configurar."
        )
    return value


def meta_api_request(
    endpoint: str,
    method: str = "GET",
    params: dict | None = None,
    data: dict | None = None,
) -> dict[str, Any]:
    """Faz requisicao para a Meta Graph API."""
    token = get_env("META_ACCESS_TOKEN")

    url = f"{META_API_BASE}/{endpoint}"

    if params is None:
        params = {}
    params["access_token"] = token

    if method == "GET":
        query_string = urllib.parse.urlencode(params, doseq=True)
        url = f"{url}?{query_string}"
        req = urllib.request.Request(url, method="GET")
    else:
        if data:
            data.update(params)
        else:
            data = params
        encoded_data = urllib.parse.urlencode(data, doseq=True).encode("utf-8")
        req = urllib.request.Request(url, data=encoded_data, method=method)

    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            error_json = json.loads(error_body)
            error_msg = error_json.get("error", {}).get("message", error_body)
        except json.JSONDecodeError:
            error_msg = error_body
        raise RuntimeError(f"Meta API Error ({e.code}): {error_msg}") from e


# --- Campanhas ---


def meta_list_campaigns(
    status_filter: str = "ACTIVE,PAUSED",
    fields: str = "id,name,objective,status,daily_budget,lifetime_budget,bid_strategy,start_time,stop_time",
) -> dict:
    """Lista campanhas da conta de anuncios."""
    account_id = get_env("META_AD_ACCOUNT_ID")
    params = {"fields": fields}
    if status_filter:
        filtering = json.dumps(
            [{"field": "status", "operator": "IN", "value": status_filter.split(",")}]
        )
        params["filtering"] = filtering
    return meta_api_request(f"{account_id}/campaigns", params=params)


def meta_get_campaign(campaign_id: str) -> dict:
    """Obtem detalhes de uma campanha especifica."""
    fields = "id,name,objective,status,daily_budget,lifetime_budget,bid_strategy,start_time,stop_time,created_time,updated_time"
    return meta_api_request(campaign_id, params={"fields": fields})


def meta_create_campaign(
    name: str,
    objective: str = "OUTCOME_LEADS",
    status: str = "PAUSED",
    special_ad_categories: str = "[]",
    bid_strategy: str = "LOWEST_COST_WITHOUT_CAP",
    daily_budget: str | None = None,
    lifetime_budget: str | None = None,
) -> dict:
    """Cria nova campanha. Sempre criada como PAUSED por seguranca."""
    account_id = get_env("META_AD_ACCOUNT_ID")
    data = {
        "name": name,
        "objective": objective,
        "status": "PAUSED",  # Forcado PAUSED por seguranca
        "special_ad_categories": special_ad_categories,
        "bid_strategy": bid_strategy,
    }
    if daily_budget:
        data["daily_budget"] = daily_budget
    if lifetime_budget:
        data["lifetime_budget"] = lifetime_budget
    return meta_api_request(f"{account_id}/campaigns", method="POST", data=data)


def meta_update_campaign(campaign_id: str, **kwargs) -> dict:
    """Atualiza uma campanha existente."""
    return meta_api_request(campaign_id, method="POST", data=kwargs)


# --- Ad Sets ---


def meta_list_adsets(
    campaign_id: str,
    fields: str = "id,name,targeting,optimization_goal,billing_event,bid_amount,daily_budget,status,promoted_object",
) -> dict:
    """Lista ad sets de uma campanha."""
    return meta_api_request(f"{campaign_id}/adsets", params={"fields": fields})


def meta_get_adset(adset_id: str) -> dict:
    """Obtem detalhes de um ad set."""
    fields = "id,name,targeting,optimization_goal,billing_event,bid_amount,daily_budget,lifetime_budget,status,promoted_object,start_time,end_time"
    return meta_api_request(adset_id, params={"fields": fields})


def meta_create_adset(
    campaign_id: str,
    name: str,
    daily_budget: str,
    targeting: str,
    optimization_goal: str = "LEAD_GENERATION",
    billing_event: str = "IMPRESSIONS",
    bid_strategy: str = "LOWEST_COST_WITHOUT_CAP",
    status: str = "PAUSED",
    promoted_object: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
) -> dict:
    """Cria novo ad set."""
    account_id = get_env("META_AD_ACCOUNT_ID")
    data = {
        "campaign_id": campaign_id,
        "name": name,
        "daily_budget": daily_budget,
        "targeting": targeting,
        "optimization_goal": optimization_goal,
        "billing_event": billing_event,
        "bid_strategy": bid_strategy,
        "status": "PAUSED",
    }
    if promoted_object:
        data["promoted_object"] = promoted_object
    if start_time:
        data["start_time"] = start_time
    if end_time:
        data["end_time"] = end_time
    return meta_api_request(f"{account_id}/adsets", method="POST", data=data)


def meta_update_adset(adset_id: str, **kwargs) -> dict:
    """Atualiza um ad set existente."""
    return meta_api_request(adset_id, method="POST", data=kwargs)


# --- Ads ---


def meta_list_ads(
    adset_id: str,
    fields: str = "id,name,status,creative{id,name,title,body,image_url,thumbnail_url,call_to_action_type}",
) -> dict:
    """Lista ads de um ad set."""
    return meta_api_request(f"{adset_id}/ads", params={"fields": fields})


def meta_get_ad(ad_id: str) -> dict:
    """Obtem detalhes de um ad."""
    fields = "id,name,status,creative{id,name,title,body,image_url,thumbnail_url,link_url,call_to_action_type},created_time,updated_time"
    return meta_api_request(ad_id, params={"fields": fields})


def meta_create_ad(
    adset_id: str,
    name: str,
    creative_id: str,
    status: str = "PAUSED",
) -> dict:
    """Cria novo ad."""
    account_id = get_env("META_AD_ACCOUNT_ID")
    data = {
        "adset_id": adset_id,
        "name": name,
        "creative": json.dumps({"creative_id": creative_id}),
        "status": "PAUSED",
    }
    return meta_api_request(f"{account_id}/ads", method="POST", data=data)


def meta_update_ad(ad_id: str, **kwargs) -> dict:
    """Atualiza um ad existente."""
    return meta_api_request(ad_id, method="POST", data=kwargs)


# --- Criativos ---


def meta_create_creative(
    name: str,
    page_id: str | None = None,
    instagram_user_id: str | None = None,
    message: str = "",
    headline: str = "",
    description: str = "",
    link: str = "https://claude.ai/code",
    call_to_action_type: str = "SIGN_UP",
    image_hash: str | None = None,
    leadgen_form_id: str | None = None,
) -> dict:
    """Cria ad creative para lead gen."""
    account_id = get_env("META_AD_ACCOUNT_ID")
    if not page_id:
        page_id = get_env("META_PAGE_ID")
    if not instagram_user_id:
        instagram_user_id = get_env("META_INSTAGRAM_ACCOUNT_ID", required=False)

    link_data = {
        "message": message,
        "name": headline,
        "description": description,
        "link": link,
        "call_to_action": {"type": call_to_action_type},
    }

    if image_hash:
        link_data["image_hash"] = image_hash
    if leadgen_form_id:
        link_data["call_to_action"]["value"] = {"lead_gen_form_id": leadgen_form_id}

    object_story_spec = {"page_id": page_id, "link_data": link_data}
    if instagram_user_id:
        object_story_spec["instagram_user_id"] = instagram_user_id

    data = {
        "name": name,
        "object_story_spec": json.dumps(object_story_spec),
    }
    return meta_api_request(f"{account_id}/adcreatives", method="POST", data=data)


def meta_upload_image(image_path: str) -> dict:
    """Faz upload de imagem para a conta de anuncios."""
    account_id = get_env("META_AD_ACCOUNT_ID")
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    import base64

    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    data = {"bytes": image_b64}
    return meta_api_request(f"{account_id}/adimages", method="POST", data=data)


# --- Lead Forms ---


def meta_list_leadgen_forms() -> dict:
    """Lista formularios de lead da pagina."""
    page_id = get_env("META_PAGE_ID")
    return meta_api_request(
        f"{page_id}/leadgen_forms",
        params={"fields": "id,name,status,created_time,questions"},
    )


def meta_create_leadgen_form(
    name: str,
    questions: str,
    context_card: str | None = None,
    privacy_policy_url: str = "",
    thank_you_page: str | None = None,
    follow_up_action_url: str = "https://claude.ai/code",
) -> dict:
    """Cria formulario de lead (instant form)."""
    page_id = get_env("META_PAGE_ID")
    data = {
        "name": name,
        "questions": questions,
        "follow_up_action_url": follow_up_action_url,
        "privacy_policy": json.dumps({"url": privacy_policy_url}),
    }
    if context_card:
        data["context_card"] = context_card
    if thank_you_page:
        data["thank_you_page"] = thank_you_page
    return meta_api_request(f"{page_id}/leadgen_forms", method="POST", data=data)


def meta_get_leads(form_id: str) -> dict:
    """Busca leads captados de um formulario."""
    return meta_api_request(
        f"{form_id}/leads",
        params={"fields": "id,created_time,field_data"},
    )


# --- Insights ---


def meta_get_insights(
    object_id: str,
    fields: str = "impressions,reach,clicks,cpc,cpm,ctr,spend,actions,cost_per_action_type,frequency",
    time_range: str | None = None,
    level: str = "campaign",
    time_increment: str = "1",
    breakdowns: str | None = None,
) -> dict:
    """Busca metricas de performance de qualquer objeto (conta, campanha, adset, ad)."""
    params: dict[str, str] = {
        "fields": fields,
        "level": level,
        "time_increment": time_increment,
    }
    if time_range:
        params["time_range"] = time_range
    if breakdowns:
        params["breakdowns"] = breakdowns
    return meta_api_request(f"{object_id}/insights", params=params)


def meta_get_account_insights(
    date_preset: str = "last_30d",
    level: str = "account",
) -> dict:
    """Busca metricas gerais da conta de anuncios."""
    account_id = get_env("META_AD_ACCOUNT_ID")
    return meta_api_request(
        f"{account_id}/insights",
        params={
            "fields": "impressions,reach,clicks,spend,actions,cost_per_action_type",
            "date_preset": date_preset,
            "level": level,
        },
    )


# --- Budget / Orcamento ---


def meta_update_daily_budget(object_id: str, daily_budget_brl: float) -> dict:
    """Atualiza orcamento diario de uma campanha ou ad set.

    Args:
        object_id: ID da campanha ou ad set
        daily_budget_brl: Orcamento diario em BRL (ex: 60.00 para R$60/dia)

    O valor e convertido para centavos automaticamente (Meta exige centavos).
    """
    budget_centavos = str(int(daily_budget_brl * 100))
    return meta_api_request(
        object_id, method="POST", data={"daily_budget": budget_centavos}
    )


def meta_update_lifetime_budget(
    object_id: str, lifetime_budget_brl: float, end_time: str
) -> dict:
    """Atualiza orcamento total (lifetime) de uma campanha ou ad set.

    Args:
        object_id: ID da campanha ou ad set
        lifetime_budget_brl: Orcamento total em BRL (ex: 1800.00 para R$1.800)
        end_time: Data de termino obrigatoria (formato ISO 8601)
    """
    budget_centavos = str(int(lifetime_budget_brl * 100))
    return meta_api_request(
        object_id,
        method="POST",
        data={"lifetime_budget": budget_centavos, "end_time": end_time},
    )


def meta_get_budget_info(object_id: str) -> dict:
    """Busca informacoes de orcamento de uma campanha ou ad set."""
    return meta_api_request(
        object_id,
        params={
            "fields": "id,name,daily_budget,lifetime_budget,budget_remaining,spend_cap,bid_strategy,start_time,end_time"
        },
    )


def meta_get_spend_today(object_id: str | None = None) -> dict:
    """Busca gasto de hoje para a conta ou objeto especifico."""
    if not object_id:
        object_id = get_env("META_AD_ACCOUNT_ID")
    return meta_api_request(
        f"{object_id}/insights",
        params={
            "fields": "spend,impressions,actions,cost_per_action_type",
            "date_preset": "today",
        },
    )


# --- Forecasting / Projecoes ---


def meta_get_daily_breakdown(
    object_id: str | None = None,
    days: int = 30,
) -> dict:
    """Busca metricas diarias para forecasting de leads.

    Retorna dados dia a dia para calcular tendencias, media movel e projecoes.

    Args:
        object_id: ID da campanha, ad set ou conta. Se None, usa a conta.
        days: Numero de dias para buscar (padrao 30).
    """
    if not object_id:
        object_id = get_env("META_AD_ACCOUNT_ID")

    from datetime import datetime, timedelta

    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    return meta_api_request(
        f"{object_id}/insights",
        params={
            "fields": "spend,impressions,reach,clicks,actions,cost_per_action_type,ctr,cpc,cpm,frequency",
            "time_range": json.dumps({"since": start_date, "until": end_date}),
            "time_increment": "1",
            "level": "campaign",
        },
    )


def meta_get_reach_estimate(
    targeting_spec: str,
    optimization_goal: str = "LEAD_GENERATION",
) -> dict:
    """Estima o tamanho do publico para um targeting especifico.

    Util para verificar se a meta de leads e viavel para o tamanho do publico.

    Args:
        targeting_spec: JSON string com o targeting spec
        optimization_goal: Objetivo de otimizacao
    """
    account_id = get_env("META_AD_ACCOUNT_ID")
    return meta_api_request(
        f"{account_id}/reachestimate",
        params={
            "targeting_spec": targeting_spec,
            "optimization_goal": optimization_goal,
        },
    )


# --- Utilidades ---


def meta_validate_token() -> dict:
    """Valida o token de acesso atual."""
    return meta_api_request("me", params={"fields": "id,name"})


def meta_get_account_info() -> dict:
    """Obtem informacoes da conta de anuncios."""
    account_id = get_env("META_AD_ACCOUNT_ID")
    return meta_api_request(
        account_id,
        params={
            "fields": "id,name,account_status,currency,timezone_name,amount_spent,balance,spend_cap"
        },
    )


def meta_search_interests(query: str) -> dict:
    """Busca interesses para targeting."""
    return meta_api_request(
        "search",
        params={
            "type": "adinterest",
            "q": query,
        },
    )


if __name__ == "__main__":
    print("Meta Ads MCP Server")
    print(f"API Version: {META_API_VERSION}")
    print("Tools disponiveis: 28")
    print("Execute como MCP server para usar as tools no Claude Code.")
