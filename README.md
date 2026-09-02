# TechStore — frontend do e-commerce

Protótipo simples das páginas de catálogo, carrinho, checkout e confirmação. O carrinho usa `localStorage` enquanto o projeto ainda não está conectado ao PostgreSQL.

## Como abrir no macOS

No terminal do VS Code, dentro desta pasta, execute:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Abra `http://127.0.0.1:5000` no navegador.

## Estrutura

- `app.py`: rotas temporárias para visualizar as páginas.
- `templates/`: páginas HTML.
- `static/css/style.css`: aparência de todas as páginas.
- `static/js/script.js`: catálogo, carrinho e checkout temporários.

Na próxima etapa, os produtos poderão vir do PostgreSQL e o checkout poderá gravar pedidos por meio do Flask.
