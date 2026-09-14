"""Servidor local do dashboard Latina.

  python serve.py            -> abre http://localhost:8765 no navegador
  Botão "Atualizar dados" na página chama POST /refresh, que roda as extrações do Bitrix e regenera o HTML.
"""
import http.server, json, os, subprocess, sys, threading, time, webbrowser, hashlib, secrets, hmac
from pathlib import Path

HERE = Path(__file__).parent
PORT = int(os.environ.get("PORT", 8765))
STEPS = [("Candidatos", "dump_curriculos.py"), ("Histórico de etapas", "dump_history.py"),
         ("Banco de Talentos", "dump_talentos.py"), ("Vagas", "dump_vagas.py"),
         ("Histórico de vagas", "dump_vagas_history.py"), ("Geocodificação (novos endereços)", "geocode.py"),
         ("Montagem da página", "build.py")]
# credenciais em auth.json ({"user": "...", "password": "..."}); padrão criado no primeiro uso
AUTH_FILE = HERE / "auth.json"
if not AUTH_FILE.exists() and not os.environ.get("DASH_USER"):
    AUTH_FILE.write_text(json.dumps({"user": "latinaabstrato", "password": "latina2026"}, indent=1), encoding="utf-8")
SESSIONS = set()
HOST = os.environ.get("HOST", "127.0.0.1" if not os.environ.get("PORT") else "0.0.0.0")
SECURE = os.environ.get("COOKIE_SECURE", "1" if os.environ.get("PORT") else "0") == "1"
def creds():
    if os.environ.get("DASH_USER"): return os.environ["DASH_USER"], os.environ.get("DASH_PASSWORD", "")
    a = json.loads(AUTH_FILE.read_text(encoding="utf-8")); return a["user"], a["password"]
def check_login(u, p):
    cu, cp = creds()
    return hmac.compare_digest(u, cu) and hmac.compare_digest(p, cp)
state = {"running": False, "step": "", "log": [], "ok": None, "finished": None}

def refresh():
    state.update(running=True, log=[], ok=None, finished=None)
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    try:
        for label, script in STEPS:
            state["step"] = label; state["log"].append(f"▶ {label}")
            r = subprocess.run([sys.executable, script], cwd=HERE, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
            tail = (r.stdout.strip().splitlines() or [""])[-1]
            if r.returncode != 0:
                state["log"].append(f"✕ {label}: {(r.stderr.strip().splitlines() or ['erro'])[-1]}"); state["ok"] = False; return
            state["log"].append(f"✓ {label} — {tail}")
        state["ok"] = True
    finally:
        state["running"] = False; state["step"] = ""; state["finished"] = time.strftime("%d/%m/%Y %H:%M")

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=str(HERE), **k)
    def log_message(self, *a): pass
    def _json(self, obj, code=200):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json; charset=utf-8"); self.send_header("Cache-Control", "no-store"); self.send_header("Content-Length", len(b)); self.end_headers(); self.wfile.write(b)
    def _authed(self):
        c = self.headers.get("Cookie", "")
        tok = next((x.split("=",1)[1] for x in c.split(";") if x.strip().startswith("sid=")), "").strip()
        return tok in SESSIONS
    def do_GET(self):
        if self.path in ("/", "/index.html"): self.path = "/controle-curriculos.html"
        if self.path == "/auth": return self._json({"ok": self._authed()})
        if self.path == "/status": return self._json(state)
        if self.path == "/logout":
            self.send_response(302); self.send_header("Set-Cookie", "sid=; Max-Age=0; Path=/"); self.send_header("Location", "/"); self.end_headers(); return
        if self.path.startswith("/controle-curriculos.html"):
            # sem cache, para o reload pós-atualização pegar a versão nova; sem login, entrega só a tela de acesso
            f = HERE / ("controle-curriculos.html" if self._authed() else "login.html"); b = f.read_bytes()
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.send_header("Cache-Control", "no-store"); self.send_header("Content-Length", len(b)); self.end_headers(); self.wfile.write(b); return
        if not self._authed() or self.path.split("?")[0].endswith((".py", ".json", ".txt", ".env", ".log", ".err", ".bat", ".md", ".yaml", ".toml")):
            return self.send_error(404)
        return super().do_GET()
    def do_POST(self):
        if self.path == "/login":
            n = int(self.headers.get("Content-Length", 0)); body = json.loads(self.rfile.read(n) or b"{}")
            if check_login(str(body.get("u", "")), str(body.get("p", ""))):
                tok = secrets.token_urlsafe(24); SESSIONS.add(tok)
                b = b'{"ok": true}'; self.send_response(200); self.send_header("Content-Type", "application/json"); self.send_header("Set-Cookie", f"sid={tok}; Path=/; HttpOnly; SameSite=Lax" + ("; Secure" if SECURE else "")); self.send_header("Content-Length", len(b)); self.end_headers(); self.wfile.write(b); return
            time.sleep(0.6); return self._json({"ok": False}, 401)
        if self.path == "/refresh":
            if not self._authed(): return self._json({"error": "login"}, 401)
            if not state["running"]: threading.Thread(target=refresh, daemon=True).start()
            return self._json({"started": True})
        self.send_error(404)

if __name__ == "__main__":
    srv = http.server.ThreadingHTTPServer((HOST, PORT), H)
    print(f"Dashboard em http://localhost:{PORT}  (Ctrl+C para encerrar)")
    if HOST == "127.0.0.1": threading.Timer(0.8, lambda: webbrowser.open(f"http://localhost:{PORT}")).start()
    try: srv.serve_forever()
    except KeyboardInterrupt: pass
