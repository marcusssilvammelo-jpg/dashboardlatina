"""Etapas visitadas por cada currículo (histórico + fallback linear) -> history.json"""
import json, collections
from bitrix import call, flat
ETID=1040
ST={"DT1040_31:NEW":"Recebido","DT1040_31:PREPARATION":"Em Análise","DT1040_31:CLIENT":"Entrevista Agendada","DT1040_31:UC_F117FW":"Banco de Talentos","DT1040_31:SUCCESS":"Aprovado","DT1040_31:FAIL":"Reprovado"}
LINEAR=["Recebido","Em Análise","Entrevista Agendada","Aprovado"]
hist=collections.defaultdict(set); start=0
while True:
    b=call("crm.stagehistory.list",{**flat({"entityTypeId":ETID,"select":["OWNER_ID","STAGE_ID"]}),"start":start})
    for h in b["result"]["items"]: hist[h["OWNER_ID"]].add(ST.get(h["STAGE_ID"],h["STAGE_ID"]))
    if "next" not in b: break
    start=b["next"]
items=json.load(open("curriculos.json",encoding="utf-8"))["items"]
out={}; nh=0
for i in items:
    cur=i["etapa"]; prev=i.get("etapaAnterior")
    v={"Recebido",cur}
    if prev: v.add(prev)
    if i["id"] in hist: v|=hist[i["id"]]; nh+=1
    else:
        # fallback linear: etapas anteriores à atual (ou à anterior) na sequência principal
        ref=cur if cur in LINEAR else (prev if prev in LINEAR else None)
        if ref: v|=set(LINEAR[:LINEAR.index(ref)+1])
    out[i["id"]]=sorted(v,key=lambda x:(LINEAR+["Banco de Talentos","Reprovado"]).index(x))
json.dump(out,open("history.json","w",encoding="utf-8"),ensure_ascii=False,separators=(",",":"))
c=collections.Counter(s for v in out.values() for s in v)
print(len(out),"itens |",nh,"com histórico real |",c)
