# TechStore

MVP acadêmico de e-commerce com Flask, SQLAlchemy e PostgreSQL no Neon.

## Requisitos

- Python 3.10 ou superior;
- Node.js 20 ou superior, usado pela CLI e pela configuração do Neon;
- projeto Neon do Bloco 3;
- `DATABASE_URL` em `.env.local`.

O comando `neon link` já criou `.env.local` neste computador. Em outra máquina,
use `.env.example` como referência e nunca envie credenciais ao GitHub.

## Executar no Windows

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app app check-db
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m flask --app app run --debug
```

Acesse `http://127.0.0.1:5000`.

Não execute `init-db`: as tabelas e os dados iniciais já foram criados pelos
scripts do Bloco 3. O comando `check-db` apenas confere a conexão e conta os
registros existentes.

## Executar no macOS

O Python não cria ambientes virtuais em caminhos que contêm `:`. Como a pasta
`Facul 2026:2` contém esse caractere, crie o ambiente fora do projeto:

```bash
python3 -m venv "$HOME/.venvs/techstore"
"$HOME/.venvs/techstore/bin/python" -m pip install -r requirements.txt
npm install
npx --yes neon@latest auth
npx --yes neon@latest link
"$HOME/.venvs/techstore/bin/python" -m flask --app app check-db
"$HOME/.venvs/techstore/bin/python" -m unittest discover -s tests -v
"$HOME/.venvs/techstore/bin/python" -m flask --app app run --debug
```

No `neon link`, selecione o projeto `techstore-facamp-tai` e a branch
`production`. O comando cria `.neon` e `.env.local`, ambos ignorados pelo Git.
Se o projeto for movido para um caminho sem `:`, também é possível usar uma
`.venv` dentro dele normalmente.

## Configuração

Variáveis reconhecidas:

- `DATABASE_URL`: conexão PostgreSQL fornecida pela Neon;
- `SECRET_KEY`: chave forte usada para assinar a sessão do carrinho;
- `SESSION_COOKIE_SECURE`: use `true` no deploy com HTTPS.

Se `SECRET_KEY` não estiver definida durante o desenvolvimento, o aplicativo
gera uma chave temporária a cada inicialização. Para o deploy, configure uma
chave permanente no provedor.

## Deploy no Render

O arquivo `render.yaml` configura um Web Service Python gratuito na região da
Virgínia, com deploy automático da branch `main` e Gunicorn como servidor de
produção. O Render gera a `SECRET_KEY` e solicita apenas o valor secreto de
`DATABASE_URL` durante a criação do Blueprint.

1. Envie as alterações para a branch `main` no GitHub.
2. No Render, escolha **New > Blueprint** e conecte o repositório `TechStore`.
3. Confirme que o Blueprint encontrado é `render.yaml`.
4. Em `DATABASE_URL`, informe a URL pooled da branch `production` do Neon.
5. Aplique o Blueprint e acompanhe o primeiro deploy.

Não use `DATABASE_URL_UNPOOLED` na aplicação e nunca grave a URL de conexão no
repositório. O endpoint `/` é usado pelo Render para verificar simultaneamente
se a aplicação e o catálogo no Neon estão disponíveis.
