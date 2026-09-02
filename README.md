# TechStore

MVP acadêmico de e-commerce com Flask, SQLAlchemy e PostgreSQL no Neon.

## Requisitos

- Python 3.10 ou superior;
- projeto Neon do Bloco 3;
- `DATABASE_URL` em `.env.local`.

O comando `neon link` já criou `.env.local` neste computador. Em outra máquina,
use `.env.example` como referência e nunca envie credenciais ao GitHub.

## Executar no Windows

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app app check-db
.\.venv\Scripts\python.exe -m flask --app app run --debug
```

Acesse `http://127.0.0.1:5000`.

Não execute `init-db`: as tabelas e os dados iniciais já foram criados pelos
scripts do Bloco 3. O comando `check-db` apenas confere a conexão e conta os
registros existentes.

## Configuração

Variáveis reconhecidas:

- `DATABASE_URL`: conexão PostgreSQL fornecida pela Neon;
- `SECRET_KEY`: chave forte usada para assinar a sessão do carrinho;
- `SESSION_COOKIE_SECURE`: use `true` no deploy com HTTPS.

Se `SECRET_KEY` não estiver definida durante o desenvolvimento, o aplicativo
gera uma chave temporária a cada inicialização. Para o deploy, configure uma
chave permanente no provedor.
