"""Exporta os candidatos do Banco de Talentos (SPA 1040) com contato vinculado -> talentos.json"""
import json, re
from bitrix import call, call_all, flat

ETID=1040; STAGE="DT1040_31:UC_F117FW"; PORTAL="https://gruposuporte.bitrix24.com.br"
USERS={1539:"Fabio Gomes",1537:"Laís Fernanda Luz de Sousa",1715:"Diana Marinho De Barros",14035:"Usuário #14035",32231:"Usuário #32231"}
fields=call("crm.item.fields",{"entityTypeId":ETID})["result"]["fields"]
enums={n:{str(i["ID"]):i["VALUE"] for i in f["items"]} for n,f in fields.items() if f.get("type")=="enumeration"}
sel=["id","title","assignedById","createdTime","movedTime","contactId","ufCrm13_1734053040865","ufCrm13_1734052920838","ufCrm13_1734055567818","ufCrm13_1734053058846","ufCrm13_1734116469","ufCrm13_1748441858628"]
items=call_all("crm.item.list",flat({"entityTypeId":ETID,"filter":{"stageId":STAGE},"select":sel}),"items")
ids=sorted({i["contactId"] for i in items if i.get("contactId")})
contacts={}
for k in range(0,len(ids),50):
    for c in call("crm.contact.list",flat({"filter":{"ID":ids[k:k+50]},"select":["ID","NAME","LAST_NAME"]}))["result"]:
        contacts[int(c["ID"])]=c
def clean(s): return re.sub(r"\s+"," ",(s or "")).strip()
def tc(s): return " ".join(w.capitalize() if len(w)>2 else w.lower() for w in clean(s).split())
UF={"Santa Catarina":"Matriz (Florianópolis)","Rio de Janeiro":"Rio de Janeiro","São Paulo":"São Paulo"}
out=[]
for i in items:
    c=contacts.get(i.get("contactId"),{})
    nome=tc(f"{c.get('NAME','')} {c.get('LAST_NAME') or ''}") or clean(i["title"])
    estado=enums["ufCrm13_1734116469"].get(str(i.get("ufCrm13_1734116469")))
    f=i.get("ufCrm13_1734055567818") or {}
    out.append({
        "id":i["id"],"nome":nome,
        "filial":UF.get(estado,"Outra região"),
        "estado":estado or "Não informado",
        "cidade":tc(i.get("ufCrm13_1734053058846")) or "Não informada",
        "bairro":tc(i.get("ufCrm13_1734053040865")) or "—",
        "nascimento":(i.get("ufCrm13_1734052920838") or "")[:10] or None,
        "area":[enums["ufCrm13_1748441858628"].get(str(a),str(a)) for a in (i.get("ufCrm13_1748441858628") or [])],
        "responsavel":USERS.get(i.get("assignedById"),f"Usuário #{i.get('assignedById')}"),
        "desde":(i.get("movedTime") or i["createdTime"])[:10],
        "cv":f.get("url"),   # link de sessão do portal (exige login no Bitrix); urlMachine NUNCA é exportado
        "card":f"{PORTAL}/crm/type/{ETID}/details/{i['id']}/",
    })
out.sort(key=lambda x:x["nome"])
json.dump(out,open("talentos.json","w",encoding="utf-8"),ensure_ascii=False,separators=(",",":"))
print(len(out),"talentos")
