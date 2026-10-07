# Design System — Dashboards Latina Group

Referência completa da identidade visual, tokens, componentes e estrutura usados no
**Plataforma Latina — Indicadores de RH** (`dashboardlatina`). Serve de base para
implementar outros painéis com a mesma cara.

> **Princípio geral:** shell de aplicativo (sidebar + header fixo + área de conteúdo),
> superfícies claras com sombra suave, **verde-lima da Latina como única cor de acento**,
> neutros levemente azulados, tipografia Manrope com pesos altos nos números.
> Nada de gradiente decorativo, nada de cor por enfeite: cor = significado.

---

## 1. Fundamentos

### 1.1 Tipografia

Fonte única: **Manrope** (Google Fonts), pesos 400/500/600/700/800.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap">
```

```css
font-family: "Manrope", ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
```

| Papel | Tamanho | Peso | Tracking | Observação |
|---|---|---|---|---|
| Corpo / base | 14px | 400 | — | `line-height:1.5` |
| Título de página | 22px | 800 | `-.02em` | `text-wrap:balance` |
| Subtítulo de página | 13.5px | 400 | — | `color:var(--muted-foreground)`, `max-width:66ch` |
| Título de card/gráfico | 13px | 800 | `-.01em` | |
| Legenda de card (`.chsub`) | 11.5px | 400 | — | muted |
| **Valor de KPI** | 27px | 800 | `-.03em` | `font-variant-numeric: tabular-nums` |
| Rótulo de KPI | 11.5px | 700 | `.07em` | UPPERCASE, muted |
| Rótulo de seção/sidebar | 11px | 700 | `.09em` | UPPERCASE, muted |
| Item de navegação | 13.5px | 500 (700 ativo) | — | |
| Label de filtro | 11px | 700 | `.06em` | UPPERCASE, muted |
| Tabela — cabeçalho | 11px | 800 | `.07em` | UPPERCASE, muted |
| Tabela — célula | 13px | 500 (700 na 1ª col.) | — | |
| Chip | 11.5px | 700 | — | |
| Microtexto / meta | 11–12px | 500–600 | — | muted |

**Regra dos números:** todo dígito que aparece em coluna, eixo, tabela ou KPI leva
`font-variant-numeric: tabular-nums`. Números grandes usam peso 800 e tracking negativo.

### 1.2 Cor — tokens (oklch)

Paleta construída em **oklch** com o matiz do lima da Latina (~128–134) como acento,
e neutros com leve viés azul (250–260) para não competir com o verde.

```css
:root{
  /* superfícies */
  --background: oklch(0.985 0.005 240);
  --card:       oklch(1 0 0);
  --muted:      oklch(0.965 0.008 250);
  --border:     oklch(0.92 0.012 250);

  /* tinta */
  --foreground:       oklch(0.22 0.04 250);
  --card-foreground:  oklch(0.22 0.04 250);
  --muted-foreground: oklch(0.52 0.03 255);

  /* acento (verde Latina) */
  --primary:            oklch(0.52 0.17 132);
  --primary-foreground: oklch(0.99 0.005 250);
  --ring:               oklch(0.62 0.20 128);
  --accent:             oklch(0.95 0.06 128);
  --accent-foreground:  oklch(0.36 0.11 132);

  /* sidebar */
  --sidebar:            oklch(1 0 0);
  --sidebar-foreground: oklch(0.30 0.04 255);
  --sidebar-primary:    oklch(0.52 0.17 132);
  --sidebar-accent:     oklch(0.965 0.03 128);

  /* marca (lima puro — só no logo e selos) */
  --brand:     oklch(0.90 0.24 128);
  --brand-ink: oklch(0.42 0.13 128);

  /* semânticos */
  --success: oklch(0.44 0.13 134);  --success-bg: oklch(0.95 0.06 128);
  --warning: oklch(0.62 0.14 75);   --warning-bg: oklch(0.96 0.055 85);
  --danger:  oklch(0.56 0.19 25);   --danger-bg:  oklch(0.95 0.04 25);

  /* rampa sequencial para etapas/séries (claro → escuro) */
  --st1: oklch(0.85 0.16 128);
  --st2: oklch(0.72 0.18 130);
  --st3: oklch(0.58 0.17 132);
  --st4: oklch(0.44 0.13 134);
  --st-ok:   oklch(0.90 0.24 128);   /* desfecho positivo = lima da marca */
  --st-fail: oklch(0.70 0.02 255);   /* desfecho negativo = cinza, nunca vermelho */

  /* elevação e raio */
  --shadow-card: 0 1px 2px oklch(0.30 0.05 255 / .06), 0 8px 24px oklch(0.30 0.05 255 / .06);
  --radius: 0.6rem;
}
```

**Tema escuro** — mesmos papéis, re-escalados (não é inversão automática):

```css
/* bloco repetido em @media (prefers-color-scheme: dark) + [data-theme="dark"] */
--background: oklch(0.16 0.03 260);  --foreground: oklch(0.94 0.01 250);
--card:       oklch(0.22 0.04 260);  --card-foreground: oklch(0.94 0.01 250);
--primary:    oklch(0.78 0.20 128);  --primary-foreground: oklch(0.16 0.04 134);
--ring:       oklch(0.82 0.21 128);
--accent:     oklch(0.30 0.07 132);  --accent-foreground: oklch(0.90 0.16 128);
--muted:      oklch(0.24 0.035 260); --muted-foreground: oklch(0.70 0.03 255);
--border:     oklch(0.31 0.04 260);
--sidebar:    oklch(0.14 0.03 260);  --sidebar-foreground: oklch(0.86 0.02 250);
--sidebar-primary: oklch(0.82 0.21 128); --sidebar-accent: oklch(0.22 0.04 134);
--brand: oklch(0.88 0.23 128);       --brand-ink: oklch(0.88 0.23 128);
--success: oklch(0.80 0.20 128);     --success-bg: oklch(0.30 0.07 132);
--warning: oklch(0.80 0.13 85);      --warning-bg: oklch(0.32 0.06 80);
--danger:  oklch(0.70 0.16 25);      --danger-bg:  oklch(0.31 0.08 25);
--shadow-card: 0 1px 2px oklch(0 0 0 / .3), 0 8px 24px oklch(0 0 0 / .28);
--st1: oklch(0.88 0.20 128); --st2: oklch(0.76 0.19 130);
--st3: oklch(0.64 0.17 132); --st4: oklch(0.52 0.14 134);
--st-ok: oklch(0.93 0.24 128); --st-fail: oklch(0.55 0.02 255);
```

### 1.3 Os três estados de tema (obrigatório)

O usuário pode estar em "sistema" (sem atributo), claro ou escuro explícito.
Declare **todos** os tokens no `:root` nu e redefina nos dois escopos:

```css
:root { /* paleta clara completa */ }
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]) { /* só os tokens, re-escalados */ }
}
:root[data-theme="dark"] { /* mesmos tokens do bloco acima */ }
```

Toggle no header, com persistência e aplicação **antes do primeiro paint**:

```html
<script>(function(){try{const t=localStorage.getItem("app-theme");if(t)document.documentElement.dataset.theme=t}catch(e){}})();</script>
```

```js
btn.onclick = () => {
  const r = document.documentElement;
  const cur = r.dataset.theme || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  const next = cur === "dark" ? "light" : "dark";
  r.dataset.theme = next;
  try { localStorage.setItem("app-theme", next) } catch(e) {}
};
```

### 1.4 Espaçamento, raio e elevação

- **Gap único de 16px** entre blocos, entre cards da grade e entre KPIs. Entre funil e painel lateral: 20px.
- Padding: shell `24px` · card de gráfico `18px` · KPI `16px 18px` · filtros `14px 16px` · header `0 24px`.
- Raio: card `12px` · controles `var(--radius)` = 9.6px · trilhos de barra `4–6px` · chips/pills `999px`.
- Elevação: **só** `--shadow-card`. Nunca sombra mais forte, exceto overlays (drawer/tela cheia).
- Borda: `1px solid var(--border)` em cards, inputs e divisores. Sem bordas grossas.

---

## 2. Layout

### 2.1 Shell

```
┌────────────┬─────────────────────────────────────────────┐
│ sidebar    │ header (sticky, 60px)                        │
│ 248px      ├─────────────────────────────────────────────┤
│ sticky     │ shell (padding 24, flex column, gap 16)      │
│ 100vh      │   ├ title row                                │
│            │   ├ card de filtros                          │
│ logo       │   ├ .kpis (auto-fit minmax(180px,1fr))       │
│ grupos de  │   └ .dash-grid (3 col ≥1000px, 1 col abaixo) │
│ navegação  │                                              │
│ powered by │                                              │
└────────────┴─────────────────────────────────────────────┘
```

```css
.app{display:grid;grid-template-columns:248px 1fr;min-height:100vh}
.sidebar{position:sticky;top:0;height:100vh;overflow-y:auto;
  background:var(--sidebar);border-right:1px solid var(--border);
  display:flex;flex-direction:column;gap:2px}
.main{display:flex;flex-direction:column;min-width:0}
.header{position:sticky;top:0;z-index:20;height:60px;display:flex;align-items:center;gap:14px;
  padding:0 24px;background:var(--card);border-bottom:1px solid var(--border)}
.shell{padding:24px;display:flex;flex-direction:column;gap:16px;min-width:0}
.shell>section{display:flex;flex-direction:column;gap:16px;min-width:0}
.shell>section[hidden]{display:none}
```

### 2.2 Grades

```css
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px}

.dash-grid{display:grid;grid-template-columns:1fr;gap:16px}
.dash-grid .span3{grid-column:1/-1}
@media (min-width:1000px){
  .dash-grid{grid-template-columns:repeat(3,1fr)}
  .dash-grid .span2{grid-column:span 2}
}
```

> **Mobile-first obrigatório:** comece em 1 coluna e **expanda** com `min-width`.
> Fazer o contrário (3 colunas + `max-width`) estoura a largura em telas estreitas.

### 2.3 Responsivo

| Breakpoint | Comportamento |
|---|---|
| `≥1000px` | Grade de 3 colunas; `.span2` ocupa 2 |
| `<1100px` | Funil + painel lateral viram coluna única |
| `<900px` | Sidebar colapsa para 64px (só ícones); shell com padding 16px |
| `<640px` | Drawer ocupa 100% da largura; listas de definição em 1 coluna |

Conteúdo largo (tabelas, mapas) sempre dentro de container com `overflow-x:auto` —
o `body` nunca rola na horizontal.

---

## 3. Componentes

### 3.1 Sidebar

```css
.sb-head{padding:18px 16px 14px;display:flex;align-items:center;justify-content:center;min-height:72px}
.logo{display:block;width:100%;max-width:150px;height:auto}
.sb-group{padding:14px 12px 2px}
.sb-label{font-size:11px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;
  color:var(--muted-foreground);padding:0 8px 6px}
.sb-link{position:relative;display:flex;align-items:center;gap:11px;width:100%;
  padding:8px 10px;margin:1px 0;border:0;background:none;cursor:pointer;
  border-radius:var(--radius);color:inherit;text-align:left;font-size:13.5px;font-weight:500}
.sb-link:hover{background:var(--sidebar-accent)}
.sb-link[data-active="true"]{font-weight:700;color:var(--sidebar-primary);background:var(--sidebar-accent)}
.sb-link[data-active="true"]::before{content:"";position:absolute;left:0;top:6px;bottom:6px;
  width:3px;border-radius:0 3px 3px 0;background:var(--sidebar-primary)}
.sb-link .ico{flex:none;width:18px;height:18px;stroke:currentColor;fill:none;
  stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.sb-count{margin-left:auto;font-size:11px;font-weight:700;padding:1px 7px;border-radius:999px;
  background:var(--muted);color:var(--muted-foreground);font-variant-numeric:tabular-nums}
.sb-foot{margin-top:auto;padding:12px 16px;border-top:1px solid var(--border);
  display:flex;justify-content:center;align-items:center;gap:7px}
```

**Assinaturas:**
- Barra vertical de 3px à esquerda do item ativo (marca registrada do sistema).
- Contador em pílula à direita de cada item.
- Rodapé `powered by` + logo Abstrato em 9px, opacidade .85, com troca de arte por tema
  (`.dark-hide` / `.light-hide`).

**Ícones:** SVG inline 18×18, `stroke:currentColor`, `fill:none`, `stroke-width:1.7`,
pontas e junções arredondadas. Família única (estilo Lucide). Nunca emoji na navegação.

### 3.2 Header

```html
<header class="header">
  <div class="crumb">Plataforma Latina <span aria-hidden="true">/</span> Indicadores
       <span aria-hidden="true">/</span> <b id="crumb">Seção atual</b></div>
  <div class="spacer"></div>
  <button class="icon-btn" id="theme-btn" aria-label="Alternar tema">…</button>
  <span class="chip" id="hdr-date">Última atualização: 07/10/2026 06:00</span>
  <button class="icon-btn" id="logout-btn" aria-label="Sair">…</button>
</header>
```

- Breadcrumb à esquerda com o nível atual em negrito; a seção muda ao navegar.
- Direita: tema, chip de "Última atualização", ações.
- `.icon-btn`: 34×34, borda 1px, raio do token, ícone 17px.

### 3.3 Card

```css
.card{background:var(--card);color:var(--card-foreground);border:1px solid var(--border);
  border-radius:12px;box-shadow:var(--shadow-card);min-width:0}
.chart-card{padding:18px}
.chart-card .chead{display:flex;align-items:baseline;gap:8px;margin-bottom:10px;flex-wrap:wrap}
.chart-card h3{margin:0;font-size:13px;font-weight:800;letter-spacing:-.01em}
.chart-card .chsub{font-size:11.5px;color:var(--muted-foreground)}
```

Cabeçalho padrão: **título (800) + legenda curta (muted) + ⓘ + controles à direita**
(empurrados por `.spacer`).

### 3.4 KPI

```html
<div class="card kpi">
  <span class="k-label">Em aberto <button class="info" data-info="Como é calculado…">ⓘ</button></span>
  <span class="k-value">2.235</span>
  <span class="k-foot"><span class="delta up">▲ +21% <small>ago vs jul</small></span></span>
</div>
```

```css
.kpi{padding:16px 18px;display:flex;flex-direction:column;gap:5px}
.kpi .k-label{font-size:11.5px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;
  color:var(--muted-foreground);display:flex;align-items:center}
.kpi .info{margin-left:auto}
.kpi .k-value{font-size:27px;font-weight:800;letter-spacing:-.03em;font-variant-numeric:tabular-nums}
.kpi .k-foot{font-size:12px;color:var(--muted-foreground)}
.delta{display:inline-flex;align-items:center;gap:4px;font-size:12px;font-weight:700;
  font-variant-numeric:tabular-nums}
.delta.up{color:var(--success)} .delta.down{color:var(--danger)} .delta.flat{color:var(--muted-foreground)}
.delta small{font-weight:600;color:var(--muted-foreground)}
```

**Regra do rodapé do KPI:** nunca texto explicativo (isso vai no ⓘ) — sempre a
**variação versus o período anterior**, com seta pelo sinal e cor pelo que é bom/ruim
(num indicador onde cair é bom, a queda é verde).

### 3.5 Ícone de ajuda ⓘ

Em **todo** KPI, gráfico e tabela. Explica como o número é calculado, em uma frase.

```css
.info{display:inline-flex;align-items:center;justify-content:center;width:16px;height:16px;
  border:0;background:none;padding:0;color:var(--muted-foreground);cursor:help;
  vertical-align:-3px;margin-left:6px;opacity:.75}
.info:hover{color:var(--primary);opacity:1}
.info svg{width:15px;height:15px;stroke:currentColor;fill:none;stroke-width:1.9}
```

Tooltip reaproveitado do dos gráficos, via delegação:

```js
document.addEventListener("mouseover", e => { const b = e.target.closest(".info"); if (b) showTip(e, b.dataset.info) });
document.addEventListener("mousemove", e => { const b = e.target.closest(".info"); if (b) showTip(e, b.dataset.info) });
document.addEventListener("mouseout",  e => { if (e.target.closest(".info")) hideTip() });
```

### 3.6 Chips, botões, segmented

```css
.chip{display:inline-flex;align-items:center;gap:5px;padding:2px 9px;border-radius:999px;
  font-size:11.5px;font-weight:700;background:var(--muted);color:var(--muted-foreground);white-space:nowrap}
.chip.blue{background:var(--accent);color:var(--accent-foreground)}      /* informativo */
.chip.ok  {background:var(--success-bg);color:var(--success)}
.chip.warn{background:var(--warning-bg);color:var(--warning)}
.chip.brand{background:var(--brand);color:oklch(0.30 0.09 128)}          /* selo lima */
.chip.x{cursor:pointer;border:1px solid var(--border);background:var(--accent);color:var(--accent-foreground)}
.chip.x:hover{background:var(--danger-bg);color:var(--danger);border-color:transparent}  /* remover filtro */

.btn{display:inline-flex;align-items:center;gap:7px;padding:8px 14px;border-radius:var(--radius);
  border:1px solid var(--border);background:var(--card);color:var(--foreground);
  font-size:13px;font-weight:700;cursor:pointer;white-space:nowrap}
.btn:hover{background:var(--muted)}
.btn.sm{padding:5px 10px;font-size:12px}

.segmented{display:inline-flex;padding:2px;background:var(--muted);border:1px solid var(--border);
  border-radius:var(--radius)}
.segmented button{padding:4px 10px;border:0;background:none;cursor:pointer;
  border-radius:calc(var(--radius) - 3px);font-size:12px;font-weight:700;color:var(--muted-foreground)}
.segmented button[aria-pressed="true"]{background:var(--card);color:var(--foreground);box-shadow:var(--shadow-card)}
```

> **Botões são sempre discretos** (fundo da superfície + borda). Não existe botão
> primário sólido preenchido de verde — o verde é da informação, não da interface.

### 3.7 Barra de filtros

```html
<div class="card filtros">
  <div class="row">
    <div class="field fmini grow"><label for="f-nome">Candidato</label>
      <input class="input" id="f-nome" type="search" placeholder="Buscar por nome"></div>
    <div class="field fmini"><label for="f-filial">Filial</label>
      <select class="input" id="f-filial"><option value="">Todas</option></select></div>
    <div class="field fmini"><label for="f-d1">De</label><input class="input" id="f-d1" type="date"></div>
  </div>
  <div class="row ftags">
    <span class="fcount"><b>56</b> de <span>56</span> registros</span>
    <div class="spacer"></div>
    <button class="btn sm" id="f-clear">Limpar filtros</button>
  </div>
</div>
```

```css
.filtros{padding:14px 16px;display:flex;flex-direction:column;gap:12px}
.field{display:flex;flex-direction:column;gap:6px}
.field label{font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--muted-foreground)}
.input{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);
  padding:6px 9px;font-size:12.5px;width:100%;font:inherit;color:inherit}
.fmini{min-width:150px} .fmini.grow{flex:1;min-width:220px}
.ftags{padding-top:10px;border-top:1px solid var(--border);gap:8px}
.fcount{font-size:12px;color:var(--muted-foreground);font-variant-numeric:tabular-nums}
.fcount b{color:var(--foreground);font-weight:800}
```

Padrão: **uma linha de filtros no topo**, contador de resultados + "Limpar" num rodapé
separado por hairline. Todos os painéis abaixo reagem ao mesmo estado.

### 3.8 Tabela

```css
.tablewrap{overflow-x:auto;border-radius:12px;border:1px solid var(--border);
  background:var(--card);box-shadow:var(--shadow-card);position:relative}
table{width:100%;border-collapse:collapse;font-size:13px}
th{text-align:right;font-size:11px;font-weight:800;letter-spacing:.07em;text-transform:uppercase;
  color:var(--muted-foreground);padding:11px 14px;border-bottom:1px solid var(--border);white-space:nowrap}
td{padding:9px 14px;border-bottom:1px solid var(--border);text-align:right;font-variant-numeric:tabular-nums}
th:first-child,td:first-child{text-align:left;font-weight:700}
tbody tr:hover{background:var(--muted)}
tfoot td{font-weight:800;border-top:2px solid var(--border);border-bottom:0;background:var(--muted)}
td.dim{color:var(--muted-foreground)}
/* variante de texto (listas de pessoas/itens) */
table.tal th, table.tal td{text-align:left}
table.tal td{font-weight:500;vertical-align:top}
table.tal td.nm{font-weight:700}
table.tal .sub{font-size:11px;color:var(--muted-foreground);font-weight:600}
/* rolagem interna com cabeçalho fixo */
.scrollwrap{max-height:320px;overflow:auto;box-shadow:none}
.scrollwrap thead th{position:sticky;top:0;background:var(--muted);z-index:1}
```

Números à direita, rótulos à esquerda, total em `tfoot` com fundo `--muted`.
Célula vazia = `·` em `td.dim`, nunca "0" nem em branco.

### 3.9 Drawer de detalhe

Abre da direita ao clicar numa linha. Fecha com Esc, clique no fundo ou ✕.

```css
.drawer-bd{position:fixed;inset:0;z-index:160;background:oklch(0.22 0.04 250 / .42);
  opacity:0;pointer-events:none;transition:opacity var(--d-base) var(--ease-out)}
.drawer-bd.show{opacity:1;pointer-events:auto}
.drawer{position:fixed;top:0;right:0;bottom:0;width:min(520px,100%);z-index:161;
  background:var(--card);border-left:1px solid var(--border);display:flex;flex-direction:column;
  transform:translateX(100%);transition:transform 220ms var(--ease-out)}
.drawer.open{transform:none}
.dw-head{display:flex;align-items:flex-start;gap:12px;padding:18px 20px 14px;border-bottom:1px solid var(--border)}
.dw-body{padding:18px 20px 24px;overflow-y:auto;display:flex;flex-direction:column;gap:20px}
.dw-sec>h3{margin:0 0 10px;font-size:11px;font-weight:800;letter-spacing:.08em;
  text-transform:uppercase;color:var(--muted-foreground)}
.dl{display:grid;grid-template-columns:132px 1fr;gap:9px 14px;font-size:13px}
.dl dt{color:var(--muted-foreground);font-weight:600}
.dl dd{margin:0;font-weight:600;word-break:break-word}
.dl dd.empty{color:var(--muted-foreground);font-weight:500}
.dw-foot{padding:12px 20px;border-top:1px solid var(--border);display:flex;gap:8px;flex-wrap:wrap}
```

**Linha do tempo** dentro do drawer:

```css
.tl-item{display:grid;grid-template-columns:14px 1fr;gap:10px;padding:0 0 14px;position:relative}
.tl-item::before{content:"";position:absolute;left:6px;top:14px;bottom:0;width:1px;background:var(--border)}
.tl-item:last-child::before{display:none}
.tl-dot{width:9px;height:9px;border-radius:999px;background:var(--primary);margin-top:4px;justify-self:center}
.tl-txt{font-weight:600;line-height:1.35}
.tl-meta{color:var(--muted-foreground);font-size:11.5px;margin-top:2px;font-weight:500}
```

### 3.10 Botão de tela cheia (por card)

Ícone 22×22 translúcido no canto superior direito de cada gráfico/tabela.

```css
.chart-card,.tablewrap{position:relative}
.fs-btn{position:absolute;top:8px;right:8px;width:22px;height:22px;border:0;background:transparent;
  color:var(--muted-foreground);border-radius:6px;display:inline-flex;align-items:center;
  justify-content:center;cursor:pointer;opacity:.55;z-index:2}
.fs-btn:hover{opacity:1;background:var(--muted);color:var(--foreground)}
.fs-on{position:fixed!important;inset:14px!important;z-index:150;overflow:auto;
  padding:24px 28px!important;box-shadow:0 30px 80px rgba(0,0,0,.35)!important;
  max-height:none!important;display:flex;flex-direction:column}
```

### 3.11 Tooltip e toast

```css
.chart-tip{position:fixed;z-index:80;pointer-events:none;background:var(--foreground);
  color:var(--background);padding:7px 10px;border-radius:8px;font-size:12px;font-weight:600;
  opacity:0;transform:translate(-50%,calc(-100% + 3px));max-width:320px;line-height:1.4;
  transition:opacity 90ms var(--ease-out),transform 90ms var(--ease-out)}
.chart-tip.show{opacity:1;transform:translate(-50%,-100%)}

.rf-toast{position:fixed;left:50%;bottom:26px;transform:translate(-50%,8px);z-index:90;
  background:var(--foreground);color:var(--background);padding:10px 16px;border-radius:12px;
  font-size:12.5px;font-weight:600;max-width:min(560px,92vw);box-shadow:var(--shadow-card);
  opacity:0;pointer-events:none;transition:opacity var(--d-base) var(--ease-out),transform var(--d-base) var(--ease-out)}
.rf-toast.show{opacity:1;transform:translate(-50%,0);pointer-events:auto}
```

Tooltip/toast usam **tinta invertida** (fundo `--foreground`, texto `--background`).

---

## 4. Gráficos (SVG próprio, sem biblioteca)

Todos desenhados à mão em SVG com `viewBox` fixo e `width:100%`, herdando os tokens.
Única dependência externa é o Leaflet, e só no mapa.

### 4.1 Regras comuns

- Cor vem dos tokens; texto do gráfico usa `--muted-foreground` (eixos) e `--foreground` (destaques).
- Grade horizontal tracejada `stroke-dasharray:2 3` em `--border`; linha de base sólida.
- Rótulo de valor **só no ponto de máximo** — nunca número em cima de toda barra.
- Hover sempre presente: crosshair + tooltip em linha/área; tooltip por marca em barra/bolha.
- Transição de dados por FLIP (ver §5.3).

```css
.bars-svg, .line-svg, .cfunnel{display:block;width:100%;height:auto;overflow:visible}
.bars-svg text, .line-svg text, .cfunnel text{font-family:"Manrope",sans-serif}
text.axis{fill:var(--muted-foreground);font-size:11px;font-weight:600}
text.axis.yr{fill:var(--foreground);font-weight:800}   /* marcação de ano */
text.val{fill:var(--foreground);font-size:12px;font-weight:800;font-variant-numeric:tabular-nums}
line.grid{stroke:var(--border);stroke-width:1;stroke-dasharray:2 3}
line.base{stroke:var(--border);stroke-width:1}
```

### 4.2 Linha com área em degradê (série temporal)

`viewBox 1100×230`, margens `pl:44 pr:16 pt:18 pb:30`. Curva Catmull-Rom suavizada,
área fechada até a base com gradiente vertical do `--primary` (32% → 0).

```js
<linearGradient id="g" x1="0" x2="0" y1="0" y2="1">
  <stop offset="0" stop-color="var(--primary)" stop-opacity=".32"/>
  <stop offset="1" stop-color="var(--primary)" stop-opacity="0"/>
</linearGradient>
```

```css
.line-svg .line{fill:none;stroke:var(--primary);stroke-width:2.5;stroke-linejoin:round;stroke-linecap:round}
.line-svg .xh{stroke:var(--muted-foreground);stroke-width:1;stroke-dasharray:3 3}
.line-svg .dot{fill:var(--card);stroke:var(--primary);stroke-width:2.5}
.line-svg .cap{cursor:crosshair}   /* retângulo invisível que captura o mouse */
```

Interação: um `<rect>` transparente cobre a área de plotagem, acha o ponto mais próximo
do cursor e move crosshair + ponto; o tooltip mostra valor **e a diferença para o ponto anterior**.

### 4.3 Barras (empilhadas ou simples)

`viewBox 1100×220`, barras com `rx:3`, largura 70% do passo. Eixo X rotula o mês;
janeiro (ou o primeiro ponto) aparece com ano em peso 800. Em séries longas,
rotula a cada 2.

```css
.bars-svg .bar{fill:var(--primary);cursor:pointer;transition:opacity .12s}
.bars-svg .bar:hover{opacity:.82}
.bars-svg .seg:hover{opacity:.8}   /* segmento de barra empilhada */
```

### 4.4 Funil de faixas curvas

Assinatura visual do sistema. Cada etapa é uma faixa centralizada cuja meia-largura é
`MINW + (MAXW-MINW)*sqrt(n/max)` (raiz quadrada para etapas pequenas não sumirem),
com pescoço curvo em Bézier até a largura da etapa seguinte.

```
viewBox 580×(n*56+8) · L=160 R=420 · RH=56 · MINW=22
rótulo à esquerda (+ grupo abaixo) · valor e % à direita · linhas-guia em --border
```

```css
.cfunnel .band{cursor:pointer;transition:d var(--d-data) var(--ease-out),opacity var(--d-base),filter var(--d-fast)}
.cfunnel .band:hover{filter:brightness(1.08)}
.cfunnel.has-active .band:not(.active){opacity:.35}
.cfunnel .band.active{stroke:var(--foreground);stroke-width:1.5}
.cfunnel .nm{font-size:14px;font-weight:700;fill:var(--foreground)}
.cfunnel .grp{font-size:11.5px;font-weight:600;fill:var(--muted-foreground)}
.cfunnel .val{font-size:15px;font-weight:800;fill:var(--foreground);font-variant-numeric:tabular-nums}
.cfunnel .pc{font-size:12px;font-weight:600;fill:var(--muted-foreground);font-variant-numeric:tabular-nums}
```

**Regra conceitual:** status de insucesso (reprovado, perdido, cancelado) **não entra no
funil** — vira painel lateral `.side-stat` com total, percentuais e botão de filtro.
O funil representa o caminho, não os desfechos.

Dois funis lado a lado quando faz sentido: *situação atual* (cada registro conta uma vez)
e *conversão histórica* (conta em toda etapa por onde passou, com % da etapa anterior).

```css
.fwrap{display:grid;grid-template-columns:1fr 1fr 180px;gap:20px;align-items:center}
@media (max-width:1100px){.fwrap{grid-template-columns:1fr}}
.side-stat{border-left:1px solid var(--border);padding:8px 0 8px 20px;
  display:flex;flex-direction:column;gap:6px}
```

### 4.5 Ranking horizontal (top N)

```css
.top5-row{display:grid;grid-template-columns:22px 130px 1fr 54px;align-items:center;gap:10px;padding:5px 0}
.top5-row .rk{font-size:11px;font-weight:800;color:var(--muted-foreground);font-variant-numeric:tabular-nums}
.top5-row .nm{font-size:12.5px;font-weight:700;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.top5-track{height:16px;border-radius:5px;background:var(--muted);overflow:hidden}
.top5-fill{height:100%;border-radius:5px;background:var(--primary);transition:width var(--d-data) var(--ease-out)}
.top5-n{font-size:12px;font-weight:800;text-align:right;font-variant-numeric:tabular-nums}
.top5-n small{font-weight:600;color:var(--muted-foreground);margin-left:3px}
```

Posição, nome, trilho, valor + % em `small` muted. Barra proporcional ao **maior** do recorte.

### 4.6 Curva ABC

Tabela rolável (`max-height:320px`, cabeçalho fixo) com chip de classe:
A = até 80% acumulado · B = até 95% · C = resto.

```css
.chip.A{background:var(--success-bg);color:var(--success)}
.chip.B{background:var(--warning-bg);color:var(--warning)}
.chip.C{background:var(--muted);color:var(--muted-foreground)}
```

### 4.7 Mapa (Leaflet + OpenStreetMap)

Bolhas proporcionais com raio `6 + sqrt(n/max)*k`, nível trocando com o zoom
(estado → cidade → bairro) e botões `.segmented` para travar o nível.

```css
#map{height:480px;border-radius:10px;border:1px solid var(--border);background:var(--muted);z-index:0}
.leaflet-container{font-family:"Manrope",sans-serif;font-size:12px}
.leaflet-tile-pane{filter:saturate(.35) contrast(.95)}            /* mapa dessaturado */
:root[data-theme="dark"] .leaflet-tile-pane{filter:invert(1) hue-rotate(180deg) saturate(.4) brightness(.85)}
.leaflet-tooltip{background:var(--foreground);color:var(--background);border:0;border-radius:8px;
  padding:7px 10px;font-weight:600;box-shadow:none}
.leaflet-control-zoom a{color:var(--foreground);background:var(--card);border-color:var(--border)}
```

Bolhas: `color/fillColor: var(--primary)`, `fillOpacity:.32`, `weight:1.5`.

> **Armadilha:** o Leaflet precisa de `map.invalidateSize()` depois que o container
> ganha tamanho real (fim do skeleton, troca de aba, tela cheia, resize) — senão
> os tiles saem desalinhados.

---

## 5. Motion

Baseado no skill `design-motion-principles` (lente **Emil Kowalski** primária —
restrição e velocidade; **Jakub Krehel** secundária — polimento), porque é um
painel de produtividade.

### 5.1 Tokens

```css
:root{
  --ease-out: cubic-bezier(.2,.8,.2,1);
  --ease-in:  cubic-bezier(.4,0,1,1);
  --ease-io:  cubic-bezier(.4,0,.2,1);
  --d-fast: 120ms;   /* hover, press, foco */
  --d-base: 180ms;   /* entrada/saída de blocos */
  --d-data: 260ms;   /* interpolação de dados */
}
```

Nada de `ease` puro, nada de spring com bounce em ação utilitária.

### 5.2 Entrada e saída

```css
.shell>section{transition:opacity var(--d-base) var(--ease-out),transform var(--d-base) var(--ease-out)}
.shell>section.entering{opacity:0;transform:translateY(6px)}
.shell>section.leaving{opacity:0;transform:translateY(-3px);
  transition-duration:var(--d-fast);transition-timing-function:var(--ease-in)}
```

Saída sempre **mais curta e mais sutil** que a entrada.

### 5.3 Dados que mudam (FLIP)

Ao filtrar, as formas **interpolam** do valor antigo para o novo em vez de piscar.
Guarde os atributos geométricos por chave, re-renderize, reaplique os antigos,
force reflow e devolva os novos — o CSS cuida da transição:

```js
function morph(container, sel, keyFn, props, build){
  const prev = new Map();
  if (!REDUCED) container.querySelectorAll(sel).forEach(el => prev.set(keyFn(el), props.map(p => el.getAttribute(p) ?? el.style[p])));
  build();
  if (REDUCED || !prev.size) return;
  const finals = [];
  container.querySelectorAll(sel).forEach(el => {
    const old = prev.get(keyFn(el)); if (!old) return;
    finals.push([el, props.map(p => el.getAttribute(p) ?? el.style[p])]);
    props.forEach((p,i) => el.style[p] = old[i]);
  });
  void container.offsetWidth;                       // reflow
  finals.forEach(([el, fin]) => props.forEach((p,i) => el.style[p] = fin[i]));
}
```

Propriedades animadas: `d` (funil), `y`/`height` (barras), `width` (rankings).
Valores de KPI trocam com micro-crossfade (sem count-up — filtro é ação frequente).

### 5.4 Skeleton e lazy loading

```css
.skel{position:relative;overflow:hidden;background:var(--muted);border-radius:8px;min-height:14px}
.skel::after{content:"";position:absolute;inset:0;transform:translateX(-100%);
  background:linear-gradient(90deg,transparent,oklch(1 0 0 / .45),transparent);
  animation:shimmer 1.4s var(--ease-io) infinite}
@keyframes shimmer{to{transform:translateX(100%)}}
.is-loading>*:not(.skeleton){display:none!important}
.skeleton{display:none}
.is-loading>.skeleton{display:flex;flex-direction:column;gap:16px}
```

- Cada aba nasce `is-loading`; renderiza na primeira abertura e troca skeleton → conteúdo.
- Mapa só inicializa quando entra na viewport (IntersectionObserver + fallback de scroll/timeout).
- Barra de progresso determinada no topo durante tarefas longas:

```css
#progress{position:fixed;top:0;left:0;height:2px;width:0;background:var(--primary);z-index:300;
  opacity:0;transition:width 600ms var(--ease-out),opacity var(--d-base) var(--ease-out)}
#progress.on{opacity:1}
```

### 5.5 Acessibilidade de motion (não opcional)

```css
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;
    transition-duration:.01ms!important;scroll-behavior:auto!important}
  .skel::after{display:none}
}
```

**Nunca:** pulsar indicadores, hover-scale em todo card, stagger em lista,
blur em toda entrada, animação em texto estático.

### 5.6 Foco

```css
:focus-visible{outline:2px solid var(--ring);outline-offset:2px;border-radius:4px}
```

Linhas clicáveis recebem `tabindex="0"` e respondem a Enter/Espaço; overlays fecham com Esc
e devolvem o foco à origem.

---

## 6. Tela de login (quando houver)

Mundo visual próprio, sempre escuro, independente do tema do app.

- Fundo `#0a0f0b` com campo de estrelas em `radial-gradient` e um halo verde
  `radial-gradient(circle, oklch(0.55 0.18 130 / .18), transparent 62%)`.
- Cartão central estreito (`min(380px,92vw)`), moldura dupla: externa translúcida com
  raio 22px, interna `#0e150f` raio 14px, hairlines lima no topo e na base.
- Logo da marca, saudação curta, dois campos, **botão discreto** (verde translúcido com
  borda, nunca sólido/brilhante) e `powered by` no rodapé.
- Erro: mensagem curta + shake de 320ms na moldura.
- Saída: fade + `scale(.985)` em 240ms.

---

## 7. Estrutura do arquivo e do pipeline

### 7.1 HTML single-file

```
<meta charset> + <title>
<link> Manrope
<style> CSS de bibliotecas (ex.: Leaflet inline)
<style> tokens → base → shell → componentes → gráficos → motion
<script> (tema, antes do paint)
#login (overlay)
.app
  nav.sidebar
  .main > header.header + main.shell
    section#view-a / section#view-b … (cada aba com .skeleton)
overlays: #progress, .fs-backdrop, .drawer-bd, aside.drawer, .chart-tip, .rf-toast
<script src> dependências (CDN)
<script> DADOS (JSON embutido) + render
```

Dados embutidos como constantes JSON no topo do script — a página abre offline, sem fetch.
Linhas em **array posicional** (`[etapa, mês, estado, …]`), não objetos, para o arquivo
não inchar com milhares de registros.

### 7.2 Pipeline de build

```
dump_*.py   → extraem da fonte (API) para JSON
build.py    → injeta JSON + tokens no template.html → dashboard.html
encrypt.py  → (opcional) empacota cifrado para hospedagem estática
serve.py    → servidor local com login e botão "Atualizar dados"
```

Template com marcadores `%%ROWS%%`, `%%DATA%%` substituídos no build.
Hospedagem: GitHub Pages + Actions (cron diário) — custo zero.

---

## 8. Checklist de implementação

**Fundamentos**
- [ ] Manrope carregada com 400–800
- [ ] Tokens completos no `:root` nu + bloco dark no media query **e** em `[data-theme="dark"]`
- [ ] Script de tema antes do primeiro paint; toggle no header
- [ ] `tabular-nums` em todo número alinhado

**Layout**
- [ ] Sidebar 248px sticky com barra de 3px no item ativo e contadores em pílula
- [ ] Header 60px sticky com breadcrumb + "Última atualização"
- [ ] Gap 16px uniforme; grade mobile-first (`min-width`, nunca `max-width`)
- [ ] Rodapé `powered by` com logo

**Componentes**
- [ ] KPI com ⓘ e **variação vs. período anterior** no rodapé (nunca texto explicativo)
- [ ] ⓘ em todo gráfico e tabela
- [ ] Filtros numa linha + contador + "Limpar"
- [ ] Botão de tela cheia em cada card de gráfico e tabela
- [ ] Tabelas: números à direita, `·` para vazio, total em `tfoot`

**Gráficos**
- [ ] SVG próprio com tokens; rótulo de valor só no máximo
- [ ] Hover com tooltip em toda marca
- [ ] Funil em faixas curvas; insucesso fora do funil, em painel lateral
- [ ] FLIP ao filtrar

**Motion e carregamento**
- [ ] Tokens de easing/duração; saída mais sutil que entrada
- [ ] Skeleton por aba + render preguiçoso
- [ ] Barra de progresso em tarefa longa
- [ ] `prefers-reduced-motion` desligando tudo
- [ ] `:focus-visible` visível; Esc fecha overlays

---

## 9. O que **não** fazer

- Botão primário sólido verde brilhante com sombra colorida (lê como IA genérica).
- Vermelho para "perdido/reprovado" — use cinza `--st-fail`; vermelho só para erro real.
- Emoji como ícone de navegação ou marcador de seção.
- Texto explicativo no rodapé do KPI — isso é papel do ⓘ.
- Número em cima de toda barra; `scale(0)` como início de animação; `ease` puro.
- Dois eixos Y no mesmo gráfico.
- Animar `width`/`height`/`top`/`left` de layout (use `transform`, `opacity`, `filter`,
  ou atributos SVG como `d`/`y` que o navegador interpola).

---

*Documento gerado a partir do código em produção do `dashboardlatina`
(`template.html` + `build.py`). Última revisão: 07/10/2026.*
