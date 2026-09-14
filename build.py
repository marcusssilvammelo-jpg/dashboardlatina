import json, datetime, os
try: LU=datetime.datetime.fromisoformat(open("last_update.txt").read().strip())
except Exception: LU=datetime.datetime.now()
rows=open("rows.json",encoding="utf-8").read()
d=json.load(open("curriculos.json",encoding="utf-8"))["items"]
ds=sorted(i["criadoEm"][:10] for i in d)
br=lambda s:f"{s[8:10]}/{s[5:7]}/{s[:4]}"
h=open("template.html",encoding="utf-8").read()
import unicodedata
geo=json.load(open("geo_fields.json",encoding="utf-8")); cache=json.load(open("geocache.json",encoding="utf-8"))
UF=["Acre","Alagoas","Amapá","Amazonas","Bahia","Ceará","Distrito Federal","Espírito Santo","Goiás","Maranhão","Mato Grosso","Mato Grosso do Sul","Minas Gerais","Pará","Paraíba","Paraná","Pernambuco","Piauí","Rio de Janeiro","Rio Grande do Norte","Rio Grande do Sul","Rondônia","Roraima","Santa Catarina","São Paulo","Sergipe","Tocantins"]
G={"estado":{},"cidade":{},"bairro":{}}
USERS={1539:"Fabio Gomes",1537:"Laís Fernanda Luz de Sousa",1715:"Diana Marinho De Barros",1543:"Vinicius Paulo Mazola",1551:"Jéssica Meregalli De Lima"}
HIST=json.load(open("history.json",encoding="utf-8"))
rows_l=[]
for i in d:
    c,bb=geo[str(i["id"])]; e=i["estado"] if i["estado"] in UF else ""
    est=i["estado"] or "Não informado"; cid=c or "Não informada"
    rows_l.append([i["etapa"],i["criadoEm"][:7],est,i["area"],cid,i["ensinoMedio"] or "Não informado",i["movidoEm"][:10] if i["movidoEm"] else None,bb or None,i["criadoEm"][:10],USERS.get(i["responsavel"],f"Usuário #{i['responsavel']}"),HIST[str(i["id"])]])
    if e and cache.get(f"{e}, Brasil"): G["estado"][e]=cache[f"{e}, Brasil"]
    if c:
        k=f"{c}, {e}, Brasil" if e else f"{c}, Brasil"
        if cache.get(k): G["cidade"][f"{c}|{est}"]=cache[k]
        if bb:
            k=f"{bb}, {c}, {e}, Brasil" if e else f"{bb}, {c}, Brasil"
            if cache.get(k): G["bairro"][f"{bb}|{c}|{est}"]=cache[k]
rows=json.dumps(rows_l,ensure_ascii=False,separators=(",",":"))
VGJ=json.load(open("vagas.json",encoding="utf-8"))
try: VH=json.load(open("vagas_history.json",encoding="utf-8"))
except FileNotFoundError: VH={}
FLOW=[st[1] for st in VGJ["stages"] if st[2]!="Perdida"]
for v in VGJ["vagas"]:
    cur=v[2]; vis={FLOW[0],cur}
    if str(v[0]) in VH: vis|=set(VH[str(v[0])])
    elif cur in FLOW: vis|=set(FLOW[:FLOW.index(cur)+1])
    v.append(sorted(vis,key=lambda x:([st[1] for st in VGJ["stages"]]).index(x) if x in [st[1] for st in VGJ["stages"]] else 99))
vagas_txt=json.dumps(VGJ,ensure_ascii=False,separators=(",",":"))
import hashlib
if os.environ.get("DASH_USER"): _u,_p=os.environ["DASH_USER"],os.environ.get("DASH_PASSWORD","")
else: _a=json.load(open("auth.json",encoding="utf-8")); _u,_p=_a["user"],_a["password"]
h=h.replace("%%AUTH_HASH%%",hashlib.sha256(f"{_u}:{_p}".encode()).hexdigest())
h=h.replace("%%ROWS%%",rows).replace("%%GEO%%",json.dumps(G,ensure_ascii=False,separators=(",",":"))).replace("%%VAGAS%%",vagas_txt).replace("%%TAL%%",open("talentos.json",encoding="utf-8").read()).replace("%%DATA%%",LU.strftime("%d/%m/%Y %H:%M")).replace("%%DATA_ISO%%",LU.date().isoformat()).replace("%%INI%%",br(ds[0])).replace("%%FIM%%",br(ds[-1]))
open("controle-curriculos.html","w",encoding="utf-8").write(h)
print(len(h))

# --- login.html standalone (servido pelo serve.py a quem não está autenticado) ---
import re as _re
head=h[:h.index("<div id=\"login\"")]
css_blocks=_re.findall(r"<style>.*?</style>",head,flags=_re.S)
fonts=_re.findall(r"<link[^>]+fonts[^>]*>",head)
login_block=h[h.index("<div id=\"login\" hidden>"):h.index("<div class=\"app\">")].replace("<div id=\"login\" hidden>","<div id=\"login\">",1)
login_js="""<script>
(function(){const f=document.getElementById("login-form"),err=document.getElementById("lg-err"),L=document.getElementById("login");
f.onsubmit=async e=>{e.preventDefault();const u=document.getElementById("lg-user").value.trim(),p=document.getElementById("lg-pass").value;
  try{const r=await fetch("/login",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({u,p})});if((await r.json()).ok){L.classList.add("out");setTimeout(()=>location.replace("/"),260);return}}catch(x){}
  err.textContent="Usuário ou senha incorretos.";document.getElementById("lg-pass").value="";document.getElementById("lg-pass").focus();L.classList.remove("shake");void L.offsetWidth;L.classList.add("shake")};
setTimeout(()=>document.getElementById("lg-user").focus(),50)})();
</script>"""
login_html="<!doctype html><html lang=\"pt-BR\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>Plataforma Latina — Acesso</title>"+"".join(fonts)+"".join(css_blocks)+"</head><body style=\"margin:0;background:#0a0f0b\">"+login_block+login_js+"</body></html>"
open("login.html","w",encoding="utf-8").write(login_html)
