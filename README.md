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
