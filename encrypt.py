"""Gera site/index.html: página de acesso + dashboard criptografado (AES-256-GCM, PBKDF2-SHA256 600k).

Credenciais: DASH_USER / DASH_PASSWORD (env) ou auth.json. A chave é derivada de "usuário:senha";
sem ela o conteúdo publicado é ilegível. Saída pensada para hospedagem estática (GitHub Pages).
"""
import base64, json, os, re, secrets, gzip
from pathlib import Path
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

HERE = Path(__file__).parent
ITER = 600_000
if os.environ.get("DASH_USER"):
    user, pw = os.environ["DASH_USER"], os.environ.get("DASH_PASSWORD", "")
else:
    a = json.loads((HERE / "auth.json").read_text(encoding="utf-8")); user, pw = a["user"], a["password"]

html = (HERE / "controle-curriculos.html").read_text(encoding="utf-8")
# marca o contexto estático: sem overlay de login (a página só existe decifrada) e botão Atualizar aponta p/ o workflow
html = html.replace("<div id=\"login\" hidden>", "<script>window.__STATIC__=true;window.__ACTIONS_URL__=%s;</script>\n<div id=\"login\" hidden>" % json.dumps(os.environ.get("ACTIONS_URL", "")), 1)

salt = secrets.token_bytes(16); nonce = secrets.token_bytes(12)
key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(f"{user}:{pw}".encode())
ct = AESGCM(key).encrypt(nonce, gzip.compress(html.encode("utf-8"), 9), None)
b64 = lambda b: base64.b64encode(b).decode()

login = (HERE / "login.html").read_text(encoding="utf-8")
# reaproveita a tela de acesso; troca o script de POST /login por decifração local
login = re.sub(r"<script>\n\(function\(\)\{const f=document\.getElementById\(\"login-form\"\).*?</script>", "", login, flags=re.S)
loader = """<script>
(function(){
const SALT="%s",NONCE="%s",CT="%s",ITER=%d,KEY="dashlatina-key";
const f=document.getElementById("login-form"),err=document.getElementById("lg-err"),L=document.getElementById("login"),btn=f.querySelector("button");
const b64=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0));
async function derive(u,p){const km=await crypto.subtle.importKey("raw",new TextEncoder().encode(u+":"+p),"PBKDF2",false,["deriveKey"]);
  return crypto.subtle.deriveKey({name:"PBKDF2",salt:b64(SALT),iterations:ITER,hash:"SHA-256"},km,{name:"AES-GCM",length:256},true,["decrypt"])}
async function open(key){const pt=await crypto.subtle.decrypt({name:"AES-GCM",iv:b64(NONCE)},key,b64(CT));
  const ds=new DecompressionStream("gzip");const html=await new Response(new Blob([pt]).stream().pipeThrough(ds)).text();
  L.classList.add("out");setTimeout(()=>{document.open();document.write(html);document.close()},240)}
(async()=>{try{const raw=sessionStorage.getItem(KEY);if(raw){const key=await crypto.subtle.importKey("raw",b64(raw),"AES-GCM",true,["decrypt"]);await open(key)}}catch(e){sessionStorage.removeItem(KEY)}})();
f.onsubmit=async e=>{e.preventDefault();btn.disabled=true;btn.textContent="Verificando…";
  const u=document.getElementById("lg-user").value.trim(),p=document.getElementById("lg-pass").value;
  try{const key=await derive(u,p);const raw=await crypto.subtle.exportKey("raw",key);try{sessionStorage.setItem(KEY,btoa(String.fromCharCode(...new Uint8Array(raw))))}catch(x){}await open(key);return}
  catch(x){sessionStorage.removeItem(KEY)}
  btn.disabled=false;btn.textContent="Entrar";err.textContent="Usuário ou senha incorretos.";document.getElementById("lg-pass").value="";document.getElementById("lg-pass").focus();L.classList.remove("shake");void L.offsetWidth;L.classList.add("shake")};
setTimeout(()=>document.getElementById("lg-user").focus(),50);
})();
</script>""" % (b64(salt), b64(nonce), b64(ct), ITER)
out = login.replace("</body>", loader + "\n</body>")
(HERE / "site").mkdir(exist_ok=True)
(HERE / "site" / "index.html").write_text(out, encoding="utf-8")
(HERE / "site" / ".nojekyll").write_text("")
print("site/index.html", len(out), "bytes; payload", len(ct), "bytes cifrados")
