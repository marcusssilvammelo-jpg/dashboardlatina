"""Exporta os candidatos do Banco de Talentos (SPA 1040) com ficha completa + histórico -> talentos.json"""
import json, re, urllib.parse
from bitrix import call, call_all, flat

ETID = 1040; STAGE = "DT1040_31:UC_F117FW"; PORTAL = "https://gruposuporte.bitrix24.com.br"
USERS = {1539: "Fabio Gomes", 1537: "Laís Fernanda Luz de Sousa", 1715: "Diana Marinho De Barros",
         1543: "Vinicius Paulo Mazola", 1551: "Jéssica Meregalli De Lima", 1: "Administrador"}
F = {  # campos do smart process
    "nasc": "ufCrm13_1734052920838", "email": "ufCrm13_1734052961", "bairro": "ufCrm13_1734053040865",
    "cidade": "ufCrm13_1734053058846", "cv": "ufCrm13_1734055567818", "estado": "ufCrm13_1734116469",
    "ensino": "ufCrm13_1740083519505", "area": "ufCrm13_1748441858628", "contato": "ufCrm13_1734052619",
    "vaga1": "ufCrm13_1789496394", "vaga2": "ufCrm13_1789496567", "vaga3": "ufCrm13_1789583413",
    "areaInd": "ufCrm13_1789747332010", "adequacao": "ufCrm13_1789747355721", "faixa": "ufCrm13_1790087750",
}
fields = call("crm.item.fields", {"entityTypeId": ETID})["result"]["fields"]
enums = {n: {str(i["ID"]): i["VALUE"] for i in f["items"]} for n, f in fields.items() if f.get("type") == "enumeration"}
STAGES = {s["STATUS_ID"]: s["NAME"] for s in call("crm.status.list", flat({"filter": {"ENTITY_ID": f"DYNAMIC_{ETID}_STAGE_31"}}))["result"]}

sel = ["id", "title", "assignedById", "createdTime", "movedTime", "updatedTime", "stageId", "contactId"] + list(F.values())
items = call_all("crm.item.list", flat({"entityTypeId": ETID, "filter": {"stageId": STAGE}, "select": sel}), "items")
ids = [i["id"] for i in items]

# --- contatos ---
cids = sorted({i["contactId"] for i in items if i.get("contactId")})
contacts = {}
for k in range(0, len(cids), 50):
    for c in call("crm.contact.list", flat({"filter": {"ID": cids[k:k+50]}, "select": ["ID", "NAME", "LAST_NAME", "PHONE", "EMAIL"]}))["result"]:
        contacts[int(c["ID"])] = c

# --- vagas vinculadas (campos "D_<id>" ou "<id>") ---
def deal_id(v):
    if not v: return None
    m = re.search(r"(\d+)", str(v)); return int(m.group(1)) if m else None
dids = sorted({d for i in items for d in [deal_id(i.get(F["vaga1"])), deal_id(i.get(F["vaga2"])), deal_id(i.get(F["vaga3"]))] if d})
deals = {}
for k in range(0, len(dids), 50):
    for d in call("crm.deal.list", flat({"filter": {"ID": dids[k:k+50]}, "select": ["ID", "TITLE", "STAGE_ID", "COMPANY_ID"]}))["result"]:
        deals[int(d["ID"])] = d

# --- histórico: etapas + atividades (em lote) ---
def batch(cmds):
    out = {}
    keys = list(cmds)
    for k in range(0, len(keys), 50):
        p = {"halt": 0}
        for j, key in enumerate(keys[k:k+50]): p[f"cmd[{j}]"] = cmds[key]
        res = call("batch", p)["result"]["result"]
        vals = res.values() if isinstance(res, dict) else res
        for j, v in enumerate(vals): out[keys[k+j]] = v
    return out

q_st = {i: "crm.stagehistory.list?" + urllib.parse.urlencode({"entityTypeId": ETID, "filter[OWNER_ID]": i, "select[0]": "CREATED_TIME", "select[1]": "STAGE_ID", "order[ID]": "ASC"}) for i in ids}
q_ac = {i: "crm.activity.list?" + urllib.parse.urlencode({"filter[OWNER_ID]": i, "filter[OWNER_TYPE_ID]": ETID, "select[0]": "SUBJECT", "select[1]": "CREATED", "select[2]": "TYPE_ID", "select[3]": "PROVIDER_ID", "select[4]": "AUTHOR_ID", "select[5]": "COMPLETED", "order[CREATED]": "ASC"}) for i in ids}
hist_st, hist_ac = batch(q_st), batch(q_ac)
ACT = {"1": "Reunião", "2": "Ligação", "3": "Tarefa", "4": "E-mail", "6": "Atividade"}

def clean(s): return re.sub(r"\s+", " ", (s or "")).strip()
def tc(s): return " ".join(w.capitalize() if len(w) > 2 else w.lower() for w in clean(s).split())
def split_name(c, fallback):
    nome, sob = tc(c.get("NAME")), tc(c.get("LAST_NAME"))
    if not nome and not sob: nome = clean(fallback)
    if not sob and " " in nome: p = nome.split(); nome, sob = p[0], " ".join(p[1:])
    return nome, sob
UF = {"Santa Catarina": "Matriz (Florianópolis)", "Rio de Janeiro": "Rio de Janeiro", "São Paulo": "São Paulo"}

out = []
for i in items:
    c = contacts.get(i.get("contactId"), {})
    nome, sob = split_name(c, i["title"])
    estado = enums[F["estado"]].get(str(i.get(F["estado"])))
    f = i.get(F["cv"]) or {}
    vagas = []
    for k in ("vaga1", "vaga2", "vaga3"):
        d = deals.get(deal_id(i.get(F[k])))
        if d and not any(v["id"] == int(d["ID"]) for v in vagas):
            vagas.append({"id": int(d["ID"]), "titulo": clean(d["TITLE"]), "url": f"{PORTAL}/crm/deal/details/{d['ID']}/"})
    ev = [{"t": i["createdTime"][:19], "tipo": "Criação", "txt": "Currículo cadastrado no pipeline"}]
    for h in (hist_st.get(i["id"]) or {}).get("items", []):
        ev.append({"t": h["CREATED_TIME"][:19], "tipo": "Etapa", "txt": "Movido para " + STAGES.get(h["STAGE_ID"], h["STAGE_ID"])})
    for a in (hist_ac.get(i["id"]) or []):
        ev.append({"t": a["CREATED"][:19], "tipo": ACT.get(str(a.get("TYPE_ID")), "Atividade"),
                   "txt": clean(a.get("SUBJECT")) or "(sem assunto)",
                   "quem": USERS.get(int(a.get("AUTHOR_ID") or 0), f"Usuário #{a.get('AUTHOR_ID')}")})
    ev.sort(key=lambda x: x["t"])
    tel = (c.get("PHONE") or [{}])[0].get("VALUE")
    out.append({
        "id": i["id"], "nome": (nome + " " + sob).strip(), "primeiro": nome, "sobrenome": sob or "—",
        "filial": UF.get(estado, "Outra região"), "estado": estado or "Não informado",
        "cidade": tc(i.get(F["cidade"])) or "Não informada", "bairro": tc(i.get(F["bairro"])) or "—",
        "nascimento": (i.get(F["nasc"]) or "")[:10] or None,
        "area": [enums[F["area"]].get(str(a), str(a)) for a in (i.get(F["area"]) or [])],
        "ensino": enums[F["ensino"]].get(str(i.get(F["ensino"]))) or "Não informado",
        "email": clean(i.get(F["email"])) or (c.get("EMAIL") or [{}])[0].get("VALUE") or "—",
        "telefone": tel or "—",
        "vagas": vagas,
        "areaIndicada": clean(i.get(F["areaInd"])) or None,
        "adequacao": clean(i.get(F["adequacao"])) or None,
        "faixa": enums[F["faixa"]].get(str(i.get(F["faixa"]))) or None,
        "responsavel": USERS.get(i.get("assignedById"), f"Usuário #{i.get('assignedById')}"),
        "criadoEm": i["createdTime"][:10], "desde": (i.get("movedTime") or i["createdTime"])[:10],
        "hist": ev,
        "cv": f.get("url"),
        "card": f"{PORTAL}/crm/type/{ETID}/details/{i['id']}/",
    })
out.sort(key=lambda x: x["nome"])
json.dump(out, open("talentos.json", "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(len(out), "talentos;", sum(len(t["hist"]) for t in out), "eventos;", sum(1 for t in out if t["vagas"]), "com vaga vinculada")
