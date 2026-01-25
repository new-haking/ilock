# AuthLook - Sistema de Autenticação e Licenciamento

## 📋 Visão Geral

**AuthLook** é uma plataforma completa de autenticação e gerenciamento de licenças para aplicações, similar ao KeyAuth, mas com funcionalidades exclusivas e melhorias significativas. O sistema permite que desenvolvedores controlem acesso a seus softwares através de autenticação de usuários, gerenciamento de licenças, proteção HWID, e muito mais.

### Objetivo Principal
Criar uma solução robusta e escalável para autenticação e licenciamento de software, com dashboard administrativo completo, API pública para integração, e suporte a OAuth social (Google e Discord).

### Problema que Resolve
- **Autenticação centralizada**: Fornece sistema de login seguro para aplicações
- **Gerenciamento de licenças**: Controle de acesso baseado em chaves de licença
- **Proteção contra pirataria**: HWID Block, blacklists, validação de tokens
- **Dashboard administrativo**: Interface completa para gerenciar usuários, licenças, anúncios
- **API pública**: Integração fácil com qualquer aplicação (C#, C++, Python, JavaScript, etc.)
- **OAuth social**: Login via Google e Discord
- **Estatísticas em tempo real**: Monitoramento de usuários online, licenças usadas, receita

---

## 🏗️ Arquitetura

### Estrutura do Projeto

```
AuthLook/
│
├── Frontend (Cliente Web)
│   ├── home.html          → Página inicial/landing
│   ├── login.html          → Página de login (email, Google, Discord)
│   ├── index.html          → Dashboard administrativo
│   ├── styles.css          → Estilos dark theme
│   ├── login.css           → Estilos da página de login
│   ├── script.js           → Lógica principal do frontend
│   └── api.js              → Helper para comunicação com backend
│
├── Backend (API Python)
│   ├── backend/
│   │   ├── app.py          → Aplicação FastAPI principal
│   │   ├── config.py       → Configurações (DB, OAuth, CORS)
│   │   ├── database.py     → Modelos SQLAlchemy
│   │   ├── auth.py         → Lógica de autenticação
│   │   ├── schemas.py      → Schemas Pydantic
│   │   └── routes/
│   │       ├── auth.py     → Rotas de autenticação
│   │       ├── api.py      → API pública (para integração)
│   │       └── dashboard.py → Rotas do dashboard (autenticadas)
│   │
│   ├── requirements.txt   → Dependências Python
│   ├── run_server.py       → Script para iniciar servidor
│   └── .env                → Variáveis de ambiente
│
└── Documentação
    ├── README.md                    → Este arquivo
    ├── PROJETO_DNA_UNIVERSAL.md     → DNA completo do projeto
    ├── DOCUMENTACAO_DE_PROGRESSO.md → Registro de mudanças
    ├── CONFIGURACAO_PRODUCAO.md     → Guia de produção
    ├── INSTALL.md                    → Guia de instalação
    └── project_progress_log.md      → Log automático de progresso
```

### Fluxo de Dados

1. **Login Flow:**
   - Usuário acessa `login.html` → preenche credenciais ou clica em OAuth
   - Frontend envia requisição para `/auth/login` ou `/auth/google/authorize` ou `/auth/discord/authorize`
   - Backend valida credenciais, verifica HWID se necessário
   - Backend gera JWT token e retorna
   - Frontend salva token em localStorage
   - Redireciona para `index.html` (dashboard)

2. **Dashboard Flow:**
   - `index.html` verifica token no localStorage
   - Se válido, exibe dashboard
   - Todas as requisições incluem token no header `Authorization: Bearer <token>`
   - Backend valida token em cada requisição autenticada

3. **API Integration Flow:**
   - Aplicação cliente chama `/api/init` com `name`, `seller_id`, `version`
   - Backend retorna `sessionid` e `enckey`
   - Aplicação usa `/api/login`, `/api/register`, `/api/license` com `sessionid`
   - Backend valida e retorna dados

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.14+** - Linguagem principal
- **FastAPI** - Framework web assíncrono
- **SQLAlchemy** - ORM para banco de dados
- **Pydantic** - Validação de dados
- **JWT (python-jose)** - Autenticação stateless
- **OAuth 2.0** - Google e Discord
- **SQLite** (dev) / **PostgreSQL** (prod) - Banco de dados
- **Uvicorn** - Servidor ASGI
- **SlowAPI** - Rate limiting
- **Bcrypt** - Hash de senhas

### Frontend
- **HTML5** - Estrutura
- **CSS3** - Estilos (tema dark customizado)
- **JavaScript ES6+** - Lógica
- **LocalStorage** - Fallback quando API não disponível
- **Fetch API** - Comunicação com backend

### Segurança
- **Bcrypt** - Hash de senhas
- **JWT tokens** - Autenticação stateless
- **CORS** - Configurado para domínios permitidos
- **HWID** - Hardware ID para proteção de dispositivo
- **Rate Limiting** - Proteção contra abuso

---

## 📦 Instalação

### Pré-requisitos
- Python 3.14+
- pip (gerenciador de pacotes Python)
- PostgreSQL (para produção) ou SQLite (para desenvolvimento)

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone <repository-url>
   cd AuthLook
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure variáveis de ambiente:**
   ```bash
   cp env.example .env
   # Edite .env com suas credenciais
   ```

4. **Inicie o servidor:**
   ```bash
   python run_server.py
   ```

5. **Acesse:**
   - Frontend: `http://localhost:3000` (ou servidor web estático)
   - Backend API: `http://localhost:8000`
   - Documentação: `http://localhost:8000/docs`

Para instruções detalhadas, veja [INSTALL.md](INSTALL.md).

---

## 🚀 Como Rodar

### Desenvolvimento
```bash
# Modo desenvolvimento (com reload automático)
python run_server.py
# ou
uvicorn backend.app:app --reload
```

### Produção
```bash
# Configure ENVIRONMENT=production no .env
export ENVIRONMENT=production
python run_server.py
# ou
gunicorn backend.app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

Para configuração completa de produção, veja [CONFIGURACAO_PRODUCAO.md](CONFIGURACAO_PRODUCAO.md).

---

## 📚 Estrutura de Pastas e Funções

### Backend

#### `backend/app.py`
- Aplicação FastAPI principal
- Configuração de CORS
- Rate limiting
- Inclusão de rotas
- Eventos de startup

#### `backend/config.py`
- Configurações centralizadas
- Variáveis de ambiente
- Settings Pydantic
- CORS origins

#### `backend/database.py`
- Modelos SQLAlchemy:
  - `User` - Usuários
  - `Application` - Aplicações
  - `License` - Licenças
  - `Token` - Tokens de sessão
  - `Subscription` - Assinaturas
  - `Webhook` - Webhooks
  - `Variable` - Variáveis customizadas
  - `Blacklist` / `Whitelist` - Listas de bloqueio/permissão
  - `Log` - Logs de ações
  - `Session` - Sessões ativas
  - `File` - Arquivos
  - `Chat` - Mensagens de chat
  - `Announcement` - Anúncios
  - `Cooldown` - Configurações de cooldown
  - `LiveStat` - Estatísticas em tempo real

#### `backend/auth.py`
- `verify_password()` - Verifica senha
- `get_password_hash()` - Gera hash de senha
- `create_access_token()` - Cria token JWT
- `verify_token()` - Verifica token JWT
- `authenticate_user()` - Autentica usuário
- `get_user_by_email()` - Busca usuário por email
- `get_user_by_seller_id()` - Busca usuário por seller_id
- `generate_seller_id()` - Gera seller_id único
- `get_google_user_info()` - Obtém info do Google OAuth
- `get_discord_user_info()` - Obtém info do Discord OAuth
- `exchange_discord_code()` - Troca código Discord por token
- `create_or_get_oauth_user()` - Cria/obtém usuário OAuth

#### `backend/routes/auth.py`
- `POST /auth/login` - Login com email/senha
- `POST /auth/register` - Registro de usuário
- `POST /auth/google` - Login com Google OAuth
- `POST /auth/discord` - Login com Discord OAuth
- `GET /auth/google/authorize` - Redireciona para Google OAuth
- `GET /auth/discord/authorize` - Redireciona para Discord OAuth
- `GET /auth/google/callback` - Callback do Google OAuth
- `GET /auth/discord/callback` - Callback do Discord OAuth

#### `backend/routes/api.py`
- `POST /api/init` - Inicializa API (integração)
- `POST /api/login` - Login via API (integração)
- `POST /api/register` - Registro via API (integração)
- `POST /api/license` - Validar licença (integração)
- `GET /api/variable` - Obter variável customizada
- `GET /api/custom` - Obter mensagem customizada de login

#### `backend/routes/dashboard.py`
- `GET /dashboard/users` - Listar usuários
- `POST /dashboard/users` - Criar usuário
- `PUT /dashboard/users/{id}` - Atualizar usuário
- `DELETE /dashboard/users/{id}` - Deletar usuário
- `GET /dashboard/applications` - Listar aplicações
- `POST /dashboard/applications` - Criar aplicação
- `PUT /dashboard/applications/{id}` - Atualizar aplicação
- `GET /dashboard/licenses` - Listar licenças
- `POST /dashboard/licenses` - Criar licença
- `GET /dashboard/announcements` - Listar anúncios
- `POST /dashboard/announcements` - Criar anúncio
- `PUT /dashboard/announcements/{id}` - Atualizar anúncio
- `DELETE /dashboard/announcements/{id}` - Deletar anúncio
- `GET /dashboard/cooldowns` - Listar cooldowns
- `PUT /dashboard/cooldowns/{type}` - Atualizar cooldown
- `GET /dashboard/live-stats` - Estatísticas em tempo real

### Frontend

#### `index.html`
- Dashboard administrativo principal
- Sidebar com navegação
- Seções: App, Licenses, Users, Tokens, Subscriptions, Webhooks, Variables, Blacklists, Logs, Sessions, Files, Chats, Cooldowns, Settings
- Script de força de dashboard (garante exibição após login)

#### `login.html`
- Página de login
- Formulário email/senha
- Botões OAuth (Google e Discord)
- Validação HWID
- Redirecionamento após login

#### `script.js`
- `DataManager` - Gerenciamento de dados local (localStorage)
- `AuthLookAPI` - SDK para desenvolvedores
- `LocalStorage` - Helper para localStorage
- `generateHWID()` - Gera Hardware ID único
- `getCurrentHWID()` - Obtém HWID atual
- Funções de carregamento: `loadUsers()`, `loadLicenses()`, `loadAnnouncements()`, etc.
- Funções de criação: `createUser()`, `createLicense()`, etc.
- Funções de atualização: `updateUser()`, `updateLicense()`, etc.
- Funções de exclusão: `deleteUser()`, `deleteLicense()`, etc.
- Funções de UI: `showSection()`, `showModal()`, `closeModal()`, etc.

#### `api.js`
- `APIHelper` - Classe helper para comunicação com backend
- Detecção automática de URL (dev/prod)
- Métodos: `login()`, `register()`, `getUsers()`, `createUser()`, etc.
- Gerenciamento de token JWT

---

## 🔄 Fluxos Internos Detalhados

### Sistema de Autenticação

1. **Login com Email/Senha:**
   ```
   Frontend (login.html) 
   → Coleta email, senha, HWID
   → POST /auth/login
   → Backend valida credenciais
   → Backend verifica HWID Block se necessário
   → Backend gera JWT token
   → Frontend salva token em localStorage
   → Redireciona para index.html
   ```

2. **Login com OAuth (Google/Discord):**
   ```
   Frontend (login.html)
   → Clique em botão OAuth
   → GET /auth/google/authorize ou /auth/discord/authorize
   → Backend redireciona para provedor OAuth
   → Usuário autoriza no provedor
   → Provedor redireciona para /auth/google/callback ou /auth/discord/callback
   → Backend troca código por access_token
   → Backend obtém informações do usuário
   → Backend cria/obtém usuário
   → Backend gera JWT token
   → Backend redireciona para frontend com token
   → Frontend salva token e redireciona para dashboard
   ```

3. **Validação de Token:**
   ```
   Frontend (index.html)
   → Lê token do localStorage
   → Inclui em header Authorization: Bearer <token>
   → Backend (get_current_user)
   → Verifica token JWT
   → Extrai user_id do payload
   → Busca usuário no banco
   → Retorna usuário ou erro 401
   ```

### Sistema de Proteção HWID

1. **Primeiro Login:**
   ```
   Usuário faz login
   → Frontend gera HWID único
   → Envia HWID no login
   → Backend salva HWID no banco
   → Próximos logins comparam HWID
   ```

2. **HWID Block Ativo:**
   ```
   Usuário com hwid_locked = true
   → Frontend envia HWID atual
   → Backend compara com HWID salvo
   → Se diferente → Erro 403 (acesso negado)
   → Se igual → Login permitido
   ```

### Sistema de Licenças

1. **Criação de Licença:**
   ```
   Admin no dashboard
   → Clica em "Nova Licença"
   → Preenche dados (chave, aplicação, expiração)
   → POST /dashboard/licenses
   → Backend cria licença no banco
   → Frontend atualiza lista
   ```

2. **Validação de Licença (API):**
   ```
   Aplicação cliente
   → POST /api/license com key
   → Backend busca licença
   → Verifica status (active/used/expired/banned)
   → Verifica expiração
   → Verifica blacklist
   → Retorna sucesso/erro
   ```

### Sistema de Live Stats

1. **Atualização de Estatísticas:**
   ```
   Frontend (dashboard)
   → GET /dashboard/live-stats
   → Backend calcula:
     - Usuários online (sessões ativas)
     - Licenças usadas hoje
     - Receita mensal
     - Logins últimas 24h
   → Retorna dados
   → Frontend atualiza gráficos
   ```

---

## 🔌 APIs e Integrações

### API Pública (para integração)

**Base URL:** `https://api.authlook.cc` (produção) ou `http://localhost:8000` (dev)

#### Endpoints:

1. **POST /api/init**
   - Inicializa API
   - Parâmetros: `name`, `seller_id`, `version`
   - Retorna: `sessionid`, `enckey`

2. **POST /api/login**
   - Login via API
   - Parâmetros: `name`, `seller_id`, `username`, `password`, `hwid`
   - Retorna: `success`, `message`, `info`

3. **POST /api/register**
   - Registro via API
   - Parâmetros: `name`, `seller_id`, `username`, `password`, `email`, `hwid`
   - Retorna: `success`, `message`, `info`

4. **POST /api/license**
   - Validar licença
   - Parâmetros: `name`, `seller_id`, `key`, `hwid`
   - Retorna: `success`, `message`, `info`

5. **GET /api/variable**
   - Obter variável customizada
   - Parâmetros: `name`, `seller_id`, `var_name`
   - Retorna: `success`, `value`

6. **GET /api/custom**
   - Obter mensagem customizada
   - Parâmetros: `name`, `seller_id`
   - Retorna: `custom_login_message`, `maintenance_mode`, etc.

### OAuth Providers

- **Google OAuth:** Configurado via `GOOGLE_CLIENT_ID` e `GOOGLE_CLIENT_SECRET`
- **Discord OAuth:** Configurado via `DISCORD_CLIENT_ID` e `DISCORD_CLIENT_SECRET`

---

## 🧪 Como Testar

### Testar Login
1. Acesse `login.html`
2. Use credenciais: `admin@authlook.com` / `admin123` (ou crie usuário)
3. Deve redirecionar para `index.html`

### Testar OAuth
1. Acesse `login.html`
2. Clique em "Login com Google" ou "Login com Discord"
3. Autorize no provedor
4. Deve redirecionar para dashboard

### Testar API
```bash
# Inicializar
curl -X POST http://localhost:8000/api/init \
  -H "Content-Type: application/json" \
  -d '{"name": "MyApp", "seller_id": "abc123", "version": "1.0"}'

# Login
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"name": "MyApp", "seller_id": "abc123", "username": "user", "password": "pass"}'
```

---

## 🐛 Como Debugar

### Backend
- Logs aparecem no console
- Acesse `/docs` para Swagger UI
- Verifique logs do uvicorn

### Frontend
- Abra DevTools (F12)
- Console mostra logs detalhados
- Network tab mostra requisições
- Verifique localStorage para tokens

### Problemas Comuns

1. **Dashboard não aparece após login:**
   - Verifique token no localStorage
   - Verifique console para erros
   - Verifique se `authlook_logged_in` está como `'true'`

2. **Erro 401 Unauthorized:**
   - Token expirado ou inválido
   - Faça login novamente

3. **Erro CORS:**
   - Verifique `CORS_ORIGINS` no `.env`
   - Adicione origem do frontend

---

## 🔧 Como Modificar

### Adicionar Nova Rota
1. Crie função em `backend/routes/[arquivo].py`
2. Adicione decorador `@router.get/post/put/delete("/endpoint")`
3. Importe router em `backend/app.py`
4. Inclua com `app.include_router()`

### Adicionar Novo Modelo
1. Crie classe em `backend/database.py`
2. Herde de `Base`
3. Defina `__tablename__` e colunas
4. Crie schema em `backend/schemas.py`
5. Banco será criado automaticamente

### Adicionar Nova Funcionalidade no Frontend
1. Adicione HTML em `index.html`
2. Adicione função em `script.js`
3. Adicione método em `api.js` se necessário
4. Atualize estilos em `styles.css` se necessário

---

## 📈 Como Estender

### Adicionar Novo Provedor OAuth
1. Configure credenciais no `.env`
2. Adicione funções em `backend/auth.py`
3. Adicione rotas em `backend/routes/auth.py`
4. Adicione botão em `login.html`

### Adicionar Novo Tipo de Proteção
1. Adicione campo no modelo `Application`
2. Adicione validação em `backend/routes/api.py`
3. Adicione configuração no dashboard

### Adicionar Novo Tipo de Estatística
1. Adicione campo em `LiveStat`
2. Atualize cálculo em `backend/routes/dashboard.py`
3. Atualize frontend para exibir

---

## 🔐 Segurança

### Boas Práticas Implementadas
- ✅ Senhas hasheadas com bcrypt
- ✅ Tokens JWT com expiração
- ✅ CORS configurado
- ✅ Rate limiting
- ✅ Validação de entrada (Pydantic)
- ✅ Proteção HWID
- ✅ Blacklists/Whitelists

### Configurações Importantes
- **SECRET_KEY:** Gere com `openssl rand -hex 32`
- **DATABASE_URL:** Use PostgreSQL em produção
- **CORS_ORIGINS:** Configure domínios permitidos
- **HTTPS:** Obrigatório em produção

---

## 📝 Decisões de Design

### Por que FastAPI?
- Performance superior (assíncrono)
- Validação automática com Pydantic
- Documentação automática (Swagger)
- Type hints nativos

### Por que JWT?
- Stateless (não precisa de sessões)
- Escalável
- Seguro com HTTPS

### Por que Sistema Híbrido (API + localStorage)?
- Permite desenvolvimento offline
- Transição suave para produção
- Fallback automático se API falhar

---

## 🚧 Integrações Futuras

- [ ] Sistema de pagamentos (Stripe, PayPal)
- [ ] Notificações push
- [ ] Exportação de dados (CSV, JSON)
- [ ] Relatórios avançados
- [ ] API webhooks para eventos
- [ ] Suporte a mais provedores OAuth
- [ ] Sistema de 2FA
- [ ] Auditoria completa

---

## 📞 Suporte

Para mais informações:
- Veja [PROJETO_DNA_UNIVERSAL.md](PROJETO_DNA_UNIVERSAL.md) para DNA completo
- Veja [DOCUMENTACAO_DE_PROGRESSO.md](DOCUMENTACAO_DE_PROGRESSO.md) para histórico
- Veja [CONFIGURACAO_PRODUCAO.md](CONFIGURACAO_PRODUCAO.md) para produção

---

## 📄 Licença

Este projeto é proprietário. Todos os direitos reservados.

---

**Última atualização:** 2025-01-XX  
**Versão:** 1.0.0  
**Status:** ✅ Pronto para Produção


