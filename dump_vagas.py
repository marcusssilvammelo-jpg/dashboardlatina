"""Exporta o funil 'Recursos Humanos' (Negócios, categoria 1) -> vagas.json"""
import json, re
from bitrix import call, flat

CAT = 1
GRUPO = {
    "C1:NEW": "Aberta", "C1:PREPARATION": "Aberta", "C1:PREPAYMENT_INVOICE": "Aberta",
    "C1:EXECUTING": "Onboarding", "C1:UC_5V8TGO": "Onboarding", "C1:FINAL_INVOICE": "Onboarding",
    "C1:UC_YFNUOH": "Fechada", "C1:WON": "Fechada",
    "C1:LOSE": "Perdida", "C1:UC_5I5PXB": "Perdida", "C1:UC_NY2F3L": "Perdida",
}
stages = call("crm.dealcategory.stage.list", {"id": CAT})["result"]
STAGE = {s["STATUS_ID"]: s["NAME"] for s in stages}

cf = call("crm.company.fields", {})["result"]
ESC = {str(i["ID"]): i["VALUE"] for i in cf["UF_CRM_1728336192993"]["items"]}
FILIAL = {"SEDE": "SC", "RJ": "RJ", "SP": "SP"}
UF_MAP = {"santa catarina": "SC", "sc": "SC", "rio de janeiro": "RJ", "rj": "RJ", "são paulo": "SP", "sao paulo": "SP", "sp": "SP"}

def paged(method, params):
    out, start = [], 0
    while True:
        b = call(method, {**params, "start": start})
        out += b["result"]
        if "next" not in b:
            return out
        start = b["next"]

sel = ["ID", "TITLE", "STAGE_ID", "DATE_CREATE", "CLOSEDATE", "COMPANY_ID", "MOVED_TIME",
       "UF_CRM_1756813479", "UF_CRM_1756813447", "UF_CRM_1727616025104", "UF_CRM_1756315926384"]
deals = paged("crm.deal.list", flat({"filter": {"CATEGORY_ID": CAT}, "select": sel}))
ids = sorted({int(d["COMPANY_ID"]) for d in deals if d.get("COMPANY_ID") and d["COMPANY_ID"] != "0"})
comp = {}
for k in range(0, len(ids), 50):
    for c in call("crm.company.list", flat({"filter": {"ID": ids[k:k+50]}, "select": ["ID", "TITLE", "UF_CRM_1728336192993", "UF_CRM_1731951962073"]}))["result"]:
        comp[c["ID"]] = c

def filial(c):
    e = ESC.get(str(c.get("UF_CRM_1728336192993") or ""))
    if e: return FILIAL[e]
    return UF_MAP.get((c.get("UF_CRM_1731951962073") or "").strip().lower(), "Não informada")

def d10(s): return (s or "")[:10] or None
out = []
for d in deals:
    c = comp.get(d.get("COMPANY_ID"), {})
    grupo = GRUPO.get(d["STAGE_ID"], "Outra")
    aberta = d10(d.get("UF_CRM_1756813479")) or d10(d["DATE_CREATE"])
    fim = d10(d.get("UF_CRM_1756813447")) or d10(d.get("UF_CRM_1727616025104")) or (d10(d.get("CLOSEDATE")) if grupo == "Fechada" else None)
    out.append([
        int(d["ID"]), re.sub(r"\s+", " ", d["TITLE"]).strip(), STAGE.get(d["STAGE_ID"], d["STAGE_ID"]), grupo,
        (c.get("TITLE") or "Sem cliente").strip(), filial(c) if c else "Não informada",
        aberta, fim if grupo == "Fechada" else None,
    ])
json.dump({"stages": [[s["STATUS_ID"], s["NAME"], GRUPO.get(s["STATUS_ID"], "Outra")] for s in stages], "vagas": out},
          open("vagas.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(len(out), "vagas;", len(comp), "clientes")
