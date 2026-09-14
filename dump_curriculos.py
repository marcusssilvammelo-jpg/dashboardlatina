"""Exporta os itens do Controle de Currículos (SPA 1040) para curriculos.json."""
import json, re
from bitrix import call, call_all, flat

ETID = 1040
fields = call("crm.item.fields", {"entityTypeId": ETID})["result"]["fields"]
enums = {name: {str(i["ID"]): i["VALUE"] for i in f["items"]}
         for name, f in fields.items() if f.get("type") == "enumeration"}
stages = {}
for c in call("crm.category.list", {"entityTypeId": ETID})["result"]["categories"]:
    for s in call("crm.status.list", flat({"filter": {"ENTITY_ID": f"DYNAMIC_{ETID}_STAGE_{c['id']}"}}))["result"]:
        stages[s["STATUS_ID"]] = {"name": s["NAME"], "sort": s["SORT"], "semantics": s.get("SEMANTICS")}

sel = ["id", "title", "stageId", "previousStageId", "createdTime", "movedTime", "updatedTime",
       "assignedById", "sourceId", "parentId1032",
       "ufCrm13_1734053058846", "ufCrm13_1734116469", "ufCrm13_1748441858628",
       "ufCrm13_1740083519505", "ufCrm13_1734052920838", "ufCrm13_1734055567818"]
items = call_all("crm.item.list", flat({"entityTypeId": ETID, "select": sel}), "items")
out = []
for i in items:
    out.append({
        "id": i["id"], "nome": i["title"],
        "etapa": stages.get(i["stageId"], {}).get("name", i["stageId"]),
        "etapaId": i["stageId"],
        "etapaAnterior": stages.get(i.get("previousStageId") or "", {}).get("name"),
        "criadoEm": i["createdTime"], "movidoEm": i.get("movedTime"), "atualizadoEm": i["updatedTime"],
        "responsavel": i.get("assignedById"), "vagaId": i.get("parentId1032"),
        "cidade": (i.get("ufCrm13_1734053058846") or "").strip().title() or None,
        "estado": enums["ufCrm13_1734116469"].get(str(i.get("ufCrm13_1734116469"))),
        "area": [enums["ufCrm13_1748441858628"].get(str(a), str(a)) for a in (i.get("ufCrm13_1748441858628") or [])],
        "ensinoMedio": enums["ufCrm13_1740083519505"].get(str(i.get("ufCrm13_1740083519505"))),
        "nascimento": i.get("ufCrm13_1734052920838"),
        "temCurriculo": bool(i.get("ufCrm13_1734055567818")),
    })
def _tc(v): return " ".join(w.capitalize() if len(w)>2 else w.lower() for w in re.sub(r"\s+"," ",(v or "")).strip().split())
json.dump({i["id"]:[_tc(i.get("ufCrm13_1734053058846")),_tc(i.get("ufCrm13_1734053040865"))] for i in items},open("geo_fields.json","w",encoding="utf-8"),ensure_ascii=False)
json.dump({"stages": stages, "items": out}, open("curriculos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "itens exportados")
