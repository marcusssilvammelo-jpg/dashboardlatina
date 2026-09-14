"""Geocodifica estados, cidades e bairros dos candidatos via Nominatim (OSM). Cache em geocache.json."""
import json, time, urllib.parse, urllib.request, sys, unicodedata
from collections import Counter

items = json.load(open("curriculos.json", encoding="utf-8"))["items"]
geo = json.load(open("geo_fields.json", encoding="utf-8"))
try: cache = json.load(open("geocache.json", encoding="utf-8"))
except FileNotFoundError: cache = {}

def norm(s): return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower().strip()
UF = {"Acre":"AC","Alagoas":"AL","Amapá":"AP","Amazonas":"AM","Bahia":"BA","Ceará":"CE","Distrito Federal":"DF","Espírito Santo":"ES","Goiás":"GO","Maranhão":"MA","Mato Grosso":"MT","Mato Grosso do Sul":"MS","Minas Gerais":"MG","Pará":"PA","Paraíba":"PB","Paraná":"PR","Pernambuco":"PE","Piauí":"PI","Rio de Janeiro":"RJ","Rio Grande do Norte":"RN","Rio Grande do Sul":"RS","Rondônia":"RO","Roraima":"RR","Santa Catarina":"SC","São Paulo":"SP","Sergipe":"SE","Tocantins":"TO"}

def nominatim(q, extra=""):
    key = q
    if key in cache: return cache[key]
    t0 = time.time()
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({"q": q, "format": "json", "limit": 1, "countrycodes": "br", "accept-language": "pt-BR"}) + extra
    req = urllib.request.Request(url, headers={"User-Agent": "latina-dashboard/1.0 (geocoding candidate cities)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r: res = json.load(r)
        cache[key] = [float(res[0]["lat"]), float(res[0]["lon"])] if res else None
    except Exception as e:
        print("erro", q, e, file=sys.stderr); cache[key] = None
    time.sleep(max(0,1.05-(time.time()-t0)))
    return cache[key]

def save(): json.dump(cache, open("geocache.json", "w", encoding="utf-8"), ensure_ascii=False)

# 1. estados
for est in UF: nominatim(f"{est}, Brasil")
save()
# 2. cidades (cidade + estado quando houver)
cities = Counter()
for i in items:
    c, b = geo[str(i["id"])]
    if c: cities[(c, i["estado"] if i["estado"] in UF else "")] += 1
print("cidades", len(cities))
for n, ((c, e), cnt) in enumerate(cities.most_common()):
    nominatim(f"{c}, {e}, Brasil" if e else f"{c}, Brasil")
    if n % 25 == 0: save(); print("cidade", n, flush=True)
save()
# 3. bairros
pairs = Counter()
for i in items:
    c, b = geo[str(i["id"])]
    if c and b: pairs[(b, c, i["estado"] if i["estado"] in UF else "")] += 1
print("bairros", len(pairs))
for n, ((b, c, e), cnt) in enumerate(pairs.most_common()):
    nominatim(f"{b}, {c}, {e}, Brasil" if e else f"{b}, {c}, Brasil")
    if n % 25 == 0: save(); print("bairro", n, flush=True)
save()
print("fim", sum(1 for v in cache.values() if v), "de", len(cache), "resolvidos")
