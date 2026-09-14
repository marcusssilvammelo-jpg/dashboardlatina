"""Etapas visitadas por cada vaga (funil RH) via crm.stagehistory (batch) -> vagas_history.json"""
import json, collections, urllib.parse
from bitrix import call
total=call("crm.stagehistory.list",{"entityTypeId":2,"filter[CATEGORY_ID]":1,"select[]":"OWNER_ID"})["total"]
q="crm.stagehistory.list?"+urllib.parse.urlencode({"entityTypeId":2,"filter[CATEGORY_ID]":1,"select[0]":"OWNER_ID","select[1]":"STAGE_ID"})
hist=collections.defaultdict(set); starts=list(range(0,total,50))
for k in range(0,len(starts),50):
    params={"halt":0}
    for j,st in enumerate(starts[k:k+50]): params[f"cmd[{j}]"]=f"{q}&start={st}"
    res=call("batch",params)["result"]["result"]
    for v in (res.values() if isinstance(res,dict) else res):
        for h in v["items"]: hist[h["OWNER_ID"]].add(h["STAGE_ID"])
    print(k+50,"/",len(starts),flush=True)
stages=json.load(open("vagas.json",encoding="utf-8"))["stages"]; NAME={s[0]:s[1] for s in stages}
json.dump({str(o):sorted(NAME.get(x,x) for x in v) for o,v in hist.items()},open("vagas_history.json","w",encoding="utf-8"),ensure_ascii=False,separators=(",",":"))
print("fim",len(hist),"vagas com histórico")

import datetime; open("last_update.txt","w").write(datetime.datetime.now().isoformat(timespec="minutes"))
