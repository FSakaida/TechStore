# Bloco 4 - Aplicação Python/Flask

## 1. Objetivo

Conectar a aplicação Flask ao PostgreSQL da Neon e implementar o fluxo:

```text
catálogo -> carrinho em sessão -> checkout -> pedido e itens -> baixa de estoque
```

Esta etapa segue o Guia-Mãe e os três HTMLs. O schema criado no Bloco 3 não foi alterado.

## 2. Componentes Implementados

| Componente | Implementação |
|---|---|
| Conexão | `DATABASE_URL` carregada de `.env.local` e adaptada para o driver `psycopg`. |
| ORM | Modelos SQLAlchemy para `categorias`, `clientes`, `produtos`, `pedidos` e `itens_pedido`. |
| Catálogo | Produtos, categorias, preços e estoques consultados no Neon. |
| Carrinho | IDs e quantidades mantidos na sessão Flask; produtos não são persistidos em tabela de carrinho. |
| Checkout | Dados do cliente validados no servidor e pedido persistido no PostgreSQL. |
| Estoque | Produtos bloqueados durante o checkout e quantidades reduzidas na mesma transação. |
| Segurança básica | Credenciais fora do código, sessão assinada, consultas parametrizadas pelo ORM e mensagens de erro sem dados internos. |

O layout, os templates visuais e o CSS existentes foram preservados. Somente o conteúdo do catálogo passou a refletir os dados reais do banco.

## 3. Arquivos Principais

| Arquivo | Responsabilidade |
|---|---|
| `app.py` | Configuração Flask, páginas, API do carrinho, checkout e comando de verificação. |
| `extensions.py` | Instância compartilhada do SQLAlchemy. |
| `models.py` | Mapeamento ORM fiel ao schema do Bloco 3. |
| `checkout_service.py` | Validação do checkout e criação transacional do pedido. |
| `static/js/script.js` | Interação das telas com as rotas Flask, sem alterar o desenho visual. |
| `.env.example` | Exemplo de variáveis sem credenciais reais. |
| `requirements.txt` | Flask, Flask-SQLAlchemy, psycopg, python-dotenv e gunicorn. |
| `tests/test_smoke.py` | Testes mínimos do catálogo, carrinho, checkout, schema e rollback. |

## 4. Atendimento aos Requisitos

| Requisito | Evidência na aplicação |
|---|---|
| RF01 | A rota `/` consulta `produtos` e `categorias` no Neon. |
| RF02 | `POST /api/carrinho/itens/<id>` valida produto, quantidade e estoque. |
| RF03 | `/carrinho` exibe itens, quantidades, preços e total. |
| RF04 | `POST /api/checkout` cria cliente, pedido e itens do pedido. |
| RF05 | O checkout reduz `produtos.estoque` e impede quantidade superior à disponível. |
| RF06 | O pedido fica ligado ao cliente pelo campo `pedidos.cliente_id`. |

## 5. Fluxo do Checkout

1. O navegador envia apenas dados do formulário.
2. O servidor lê o carrinho da sessão.
3. A aplicação valida campos, produtos e quantidades.
4. O PostgreSQL bloqueia temporariamente os produtos selecionados com `FOR UPDATE`.
5. A aplicação localiza ou cria o cliente.
6. Pedido, itens e baixa de estoque são preparados na mesma transação.
7. O commit confirma todas as alterações; qualquer falha provoca rollback.
8. O carrinho é limpo somente depois da confirmação do banco.

O preço e o total são calculados no servidor a partir do banco. Valores enviados pelo navegador não são aceitos como fonte de verdade.

## 6. Decisão Sobre `senha_hash`

O schema exige `clientes.senha_hash`, mas autenticação completa está fora do MVP. Para novos clientes, a aplicação gera o hash de um segredo aleatório e descarta o valor original. Isso atende ao `NOT NULL` sem armazenar senha em texto puro nem criar uma credencial conhecida.

## 7. Execução Local

Na raiz do projeto, execute:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app app check-db
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m flask --app app run --debug
```

Acesse `http://127.0.0.1:5000`.

O arquivo `.env.local` já contém a conexão criada pelo `neon link` e está ignorado pelo Git. Não execute `init-db`, pois o Bloco 3 já criou o schema e os dados iniciais.

## 8. Validação Mínima

O Bloco 4 estará concluído quando:

- `check-db` confirmar as cinco tabelas;
- o catálogo mostrar os produtos do Neon;
- adicionar, alterar e remover itens atualizar o carrinho;
- o checkout retornar o número real do pedido;
- `pedidos` e `itens_pedido` receberem os registros;
- o estoque diminuir pela quantidade comprada;
- uma compra acima do estoque for recusada;
- nenhuma credencial aparecer no repositório ou nos logs.

Resultado da verificação local: seis testes aprovados, mapeamento das cinco tabelas confirmado e banco preservado com zero pedidos e zero itens de teste.

Foram incluídos testes mínimos para proteger a integração feita nesta etapa. A ampliação da suíte, as evidências formais de rollback e a revisão aprofundada de segurança pertencem ao Bloco 5.

## 9. Fontes

- HTML inicial: Bloco 4, slides 26 a 32.
- HTML prático: configuração, ORM, catálogo, sessão e checkout, slides 23 a 40.
- HTML SQL e NoSQL: fundamentos de integração entre aplicação e banco relacional.
- Guia-Mãe operacional: seção 4, Aplicação Python/Flask.
- [Flask-SQLAlchemy - Quick Start](https://flask-sqlalchemy.palletsprojects.com/en/stable/quickstart/)
- [SQLAlchemy - SELECT FOR UPDATE](https://docs.sqlalchemy.org/en/20/core/selectable.html)
- [Neon - Conectar aplicação Python](https://neon.com/docs/guides/python)
- [Psycopg 3 - Instalação](https://www.psycopg.org/psycopg3/docs/basic/install.html)
