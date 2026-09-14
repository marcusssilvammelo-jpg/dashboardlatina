# Plataforma Latina — Indicadores de RH (Bitrix24)

Dashboard estático (`controle-curriculos.html`) gerado a partir do Bitrix24 + servidor mínimo em Python (`serve.py`)
com login, botão **Atualizar dados** e página de acesso.

## Rodar local
    python serve.py            # abre http://localhost:8765
Credenciais em `auth.json` (ou variáveis DASH_USER / DASH_PASSWORD). Webhook do Bitrix em `.env`
(`BITRIX24_WEBHOOK_URL=...`) ou variável de ambiente.

## Hospedar (Render, Railway, Fly, qualquer host com Docker)
1. Suba esta pasta num repositório **privado** no GitHub (o `.gitignore` já exclui `.env`, `auth.json` e dados brutos).
2. No Render: *New → Web Service → conectar o repo*. O `render.yaml` já descreve o serviço (Docker, plano free).
3. Em *Environment*, defina:
   - `BITRIX24_WEBHOOK_URL` — a URL do webhook de entrada (permissão CRM)
   - `DASH_USER` / `DASH_PASSWORD` — acesso ao painel
4. Deploy. A URL pública fica algo como `https://latina-dashboard.onrender.com`.

Os dados versionados (`*.json`, `controle-curriculos.html`) são o snapshot inicial; o botão **Atualizar dados**
regenera tudo no servidor (cerca de 2 min; geocodificação usa o `geocache.json` versionado).
No plano free do Render o disco é efêmero: a cada novo deploy volta ao snapshot do repositório — clique em Atualizar.

## Segurança
- Sem login o servidor entrega só a página de acesso; arquivos `.json/.py/.txt` nunca são servidos.
- Cookie de sessão HttpOnly (+Secure em produção). Sessões vivem na memória do processo.
- Nunca faça commit de `.env` ou `auth.json`.
