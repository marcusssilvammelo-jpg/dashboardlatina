"""Cliente mínimo da REST API do Bitrix24 para Smart Processes (SPA).

Uso:
  python bitrix.py types                     # lista os smart processes (entityTypeId)
  python bitrix.py stages <entityTypeId>     # lista as etapas do pipeline
  python bitrix.py items  <entityTypeId>     # lista os itens (currículos) com etapa
  python bitrix.py fields <entityTypeId>     # lista os campos do smart process
  python bitrix.py move   <entityTypeId> <itemId> <stageId>   # move um item de etapa

A URL do webhook é lida de BITRIX24_WEBHOOK_URL ou do arquivo .env ao lado
(linha: BITRIX24_WEBHOOK_URL=https://SEU-PORTAL.bitrix24.com.br/rest/1/xxxx/).
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent


def _webhook() -> str:
    url = os.environ.get("BITRIX24_WEBHOOK_URL")
    if not url and (HERE / ".env").exists():
        for line in (HERE / ".env").read_text(encoding="utf-8").splitlines():
            if line.startswith("BITRIX24_WEBHOOK_URL="):
                url = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not url:
        sys.exit("Defina BITRIX24_WEBHOOK_URL (env ou .env ao lado do script).")
    return url.rstrip("/") + "/"


def call(method: str, params: dict | None = None):
    data = urllib.parse.urlencode(params or {}, doseq=True).encode()
    req = urllib.request.Request(_webhook() + method + ".json", data=data)
    with urllib.request.urlopen(req, timeout=60) as r:
        body = json.load(r)
    if "error" in body:
        sys.exit(f"{body['error']}: {body.get('error_description')}")
    return body


def call_all(method: str, params: dict, key: str):
    """Pagina automaticamente (50 por página)."""
    out, start = [], 0
    while True:
        body = call(method, {**params, "start": start})
        out.extend(body["result"][key])
        if "next" not in body:
            return out
        start = body["next"]


def flat(d: dict, prefix: str = "") -> dict:
    """Achata dicts aninhados p/ o urlencode: {'filter': {'a':1}} -> {'filter[a]':1}."""
    out = {}
    for k, v in d.items():
        name = f"{prefix}[{k}]" if prefix else k
        if isinstance(v, dict):
            out.update(flat(v, name))
        elif isinstance(v, list):
            for i, x in enumerate(v):
                out[f"{name}[{i}]"] = x
        else:
            out[name] = v
    return out


def cmd_types():
    for t in call_all("crm.type.list", {}, "types"):
        print(f"{t['entityTypeId']:>5}  {t['title']}")


def cmd_stages(etid):
    body = call("crm.status.list", flat({"filter": {"ENTITY_ID": f"DYNAMIC_{etid}_STAGE_%"}}))
    # categorias podem ter ENTITY_ID DYNAMIC_<id>_STAGE_<cat>
    stages = call("crm.category.list", {"entityTypeId": etid})["result"]["categories"]
    for c in stages:
        print(f"\n[Categoria {c['id']}] {c['name']}")
        for s in call("crm.status.list", flat({"filter": {"ENTITY_ID": f"DYNAMIC_{etid}_STAGE_{c['id']}"}}))["result"]:
            print(f"  {s['STATUS_ID']:<28} {s['NAME']}")


def cmd_fields(etid):
    for name, f in call("crm.item.fields", {"entityTypeId": etid})["result"]["fields"].items():
        print(f"{name:<32} {f.get('type',''):<12} {f.get('title','')}")


def cmd_items(etid):
    items = call_all("crm.item.list", flat({"entityTypeId": etid, "select": ["id", "title", "stageId", "createdTime"]}), "items")
    for i in items:
        print(f"{i['id']:>5}  {i['stageId']:<28} {i['createdTime'][:10]}  {i['title']}")
    print(f"\n{len(items)} itens")


def cmd_move(etid, item_id, stage_id):
    call("crm.item.update", flat({"entityTypeId": etid, "id": item_id, "fields": {"stageId": stage_id}}))
    print("ok")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    cmd, rest = args[0], args[1:]
    {"types": cmd_types, "stages": cmd_stages, "fields": cmd_fields,
     "items": cmd_items, "move": cmd_move}[cmd](*rest)
