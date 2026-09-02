# Guia-mãe operacional - FACAMP TAI

Projeto: aplicação e banco de dados de e-commerce com PostgreSQL e Python/Flask.

Este guia consolida os 3 HTMLs da conversa como fonte principal de trabalho. A ordem e as exigências seguem o HTML inicial de etapas do projeto. O material de e-commerce entra como manual prático/projeto-base. O material SQL e NoSQL entra como fundamentação conceitual, sem ampliar silenciosamente o escopo obrigatório.

## Fontes usadas

1. [HTML inicial - Etapas do projeto de e-commerce](fontes_html/facamp_tai_etapas_projeto_ecommerce_animacao_interativa.html)  
   Papel: fonte principal para ordem, blocos, entregáveis, critérios, checklist e atividade prática.

2. [HTML prático - E-commerce com Python e PostgreSQL](fontes_html/facamp_tai_ecommerce_postgresql_animacao_interativa_v3.html)  
   Papel: manual de execução, projeto-base, RF/RNF, modelo sugerido, DDL, Flask, SQLAlchemy, checkout, testes, deploy e perguntas técnicas.

3. [HTML conceitual - SQL e NoSQL](fontes_html/facamp_tai_sql_nosql_animacao_interativa_v3.html)  
   Papel: fundamentação para justificar PostgreSQL, modelagem relacional, normalização, ACID, transações, índices, segurança, cloud e possíveis extensões NoSQL.

## Regra de interpretação

O HTML inicial manda na ordem:

1. Problema e requisitos
2. Modelagem conceitual e lógica
3. PostgreSQL e estrutura física
4. Aplicação Python/Flask
5. Transações, testes e segurança
6. Deploy cloud e atividade prática

O MVP deve ser pequeno e rastreável. Não adicionar pagamento real, autenticação completa, integração logística, MongoDB, Redis, analytics avançado ou dashboard se isso não for cobrado explicitamente. Esses itens aparecem como contexto, extensão ou possibilidade futura.

## Escopo mínimo do MVP

Com base nos materiais, o sistema deve permitir:

- listar produtos disponíveis;
- adicionar produto ao carrinho;
- visualizar carrinho e total;
- finalizar pedido;
- registrar pedido e itens no banco;
- atualizar estoque;
- registrar cliente e histórico de pedidos;
- proteger a consistência com transação, commit e rollback;
- publicar app e banco em cloud;
- demonstrar o funcionamento com evidências.

Fora do escopo didático mínimo:

- pagamento real;
- autenticação completa;
- logística/frete;
- painel administrativo completo;
- NoSQL implementado;
- GitHub Actions;
- Docker obrigatório;
- interface sofisticada.

---

# 1. Problema e Requisitos

Fontes principais: HTML inicial, slides 6 a 11; HTML e-commerce, slides 4 a 6; HTML SQL/NoSQL, slides 4, 7 e 10.

## Objetivo

Definir exatamente qual problema o e-commerce resolve, quem usa o sistema, quais funcionalidades entram no MVP e quais regras precisam ser respeitadas pelo banco e pela aplicação.

Pergunta central do bloco: como estruturar um e-commerce simples que permita listar produtos, montar carrinho e concluir pedidos com integridade?

## Conceitos mínimos

- Problema de negócio: dor que o sistema resolve.
- Ator: pessoa ou papel que interage com o processo.
- Requisito funcional: o que o sistema faz.
- Requisito não funcional: restrição de qualidade, segurança, desempenho, disponibilidade ou manutenção.
- MVP: versão mínima funcional.
- Backlog: lista priorizada do que será feito.
- Critério de aceite: condição objetiva para dizer que um requisito está concluído.
- Fluxo principal: caminho catálogo -> carrinho -> checkout -> pedido -> estoque.

## Tarefas a executar

1. Escrever o problema central em uma frase: controlar catálogo, carrinho, pedidos e estoque em um e-commerce simples sem inconsistência.
2. Listar os atores do material: cliente, operação, gestão e TI/desenvolvimento.
3. Registrar as dores: perda de controle de estoque, duplicidade de dados e pedidos inconsistentes.
4. Fixar os requisitos funcionais do material:
   - RF01 listar produtos disponíveis;
   - RF02 adicionar produto ao carrinho;
   - RF03 visualizar carrinho e total;
   - RF04 finalizar pedido;
   - RF05 atualizar estoque;
   - RF06 registrar cliente e histórico de pedidos.
5. Registrar requisitos não funcionais:
   - integridade: não permitir preço negativo, estoque negativo ou item sem pedido/produto;
   - segurança: senha como hash e credenciais por variável de ambiente;
   - disponibilidade: banco gerenciado com backup e aplicação pronta para reinício;
   - desempenho: índices para produtos, pedidos por cliente e itens por pedido;
   - manutenibilidade: separar modelos, rotas, templates e configuração quando o projeto crescer;
   - portabilidade: rodar localmente e em cloud com PostgreSQL.
6. Separar MVP e evolução futura.
7. Criar um fluxo simples do processo de compra.
8. Escrever critérios de aceite para cada requisito.

## Artefatos/entregáveis

- Documento de escopo.
- Lista de atores, dores e objetivos.
- Requisitos funcionais e não funcionais.
- Backlog inicial.
- Fluxo do processo.
- Critérios de aceite.
- Lista explícita do que não entra no MVP.

## Critérios de validação

- Cada requisito funcional tem critério de aceite.
- O fluxo principal está validado antes da modelagem.
- Nenhum requisito importante ficou implícito.
- Cada regra de negócio já aponta para uma futura entidade, campo, constraint ou teste.
- O grupo consegue explicar por que pagamento, autenticação completa e logística ficaram fora.

## Exemplos do material

História de usuário:

> Como cliente, quero adicionar produtos ao carrinho para revisar meus itens antes de finalizar a compra.

Critérios de aceite do exemplo:

- o produto deve existir;
- a quantidade deve ser positiva;
- o sistema deve recalcular o total.

Exemplos de atores:

- Cliente: busca produtos, consulta preço e finaliza compra.
- Operação: controla estoque, pedidos e clientes.
- Gestão: deseja relatórios básicos de vendas e produtos.
- TI/desenvolvimento: precisa de escopo claro para modelar, programar e testar.

## Dependências da próxima etapa

Os requisitos aprovados viram entidades, atributos, relacionamentos e regras de integridade. Se RF04 é finalizar pedido, o modelo precisa representar pedido e itens. Se RF05 é atualizar estoque, produto precisa ter estoque e o checkout precisa ser transacional.

## Necessário vs opcional

Necessário:

- problema e escopo;
- RF/RNF;
- backlog;
- fluxo catálogo -> carrinho -> checkout;
- critérios de aceite.

Opcional:

- usar Miro, Trello, Jira ou ferramenta específica;
- detalhar relatórios avançados;
- criar autenticação completa;
- criar pagamento real;
- criar logística/frete.

---

# 2. Modelagem Conceitual e Lógica

Fontes principais: HTML inicial, slides 12 a 18; HTML e-commerce, slides 10 a 17; HTML SQL/NoSQL, slides 11 a 13.

## Objetivo

Transformar o domínio do e-commerce em um modelo de dados coerente: DER, modelo lógico, cardinalidades, chaves, tipos, regras e dicionário de dados.

Pergunta central do bloco: quais objetos do negócio precisam virar entidades e como eles se relacionam?

## Conceitos mínimos

- Entidade: objeto do negócio, como Cliente, Produto ou Pedido.
- Atributo: característica da entidade, como nome, email, preço ou estoque.
- Relacionamento: associação entre entidades.
- Cardinalidade: quantidade de ocorrências entre entidades.
- Chave primária: identificador único.
- Chave estrangeira: ligação entre tabelas.
- Modelo conceitual: visão de negócio, normalmente DER.
- Modelo lógico: tabelas, campos, chaves e relacionamentos.
- Normalização: redução de redundância e anomalias.
- Dicionário de dados: documentação de cada campo.

## Tarefas a executar

1. Criar o modelo conceitual com as entidades do material:
   - Cliente;
   - Categoria;
   - Produto;
   - Pedido;
   - ItemPedido.
2. Registrar que Carrinho é temporário em sessão no MVP, não tabela obrigatória.
3. Definir relacionamentos:
   - Cliente 1:N Pedido;
   - Categoria 1:N Produto;
   - Pedido 1:N ItemPedido;
   - Produto 1:N ItemPedido.
4. Definir atributos principais:
   - clientes: id, nome, email, telefone, senha_hash;
   - categorias: id, nome;
   - produtos: id, nome, descricao, preco, estoque, categoria_id;
   - pedidos: id, cliente_id, status, total, cep, cidade, estado, endereco, numero, criado_em;
   - itens_pedido: id, pedido_id, produto_id, quantidade, preco_unitario.
5. Definir regras:
   - email único;
   - categoria única;
   - preço >= 0;
   - estoque >= 0;
   - quantidade > 0;
   - item sempre ligado a pedido e produto.
6. Escolher tipos adequados:
   - NUMERIC/DECIMAL para preço;
   - INTEGER para quantidades e identificadores;
   - VARCHAR/TEXT para textos;
   - TIMESTAMPTZ para data/hora.
7. Validar normalização:
   - 1FN: campos atômicos; itens em tabela própria;
   - 2FN: ItemPedido separa a associação pedido/produto;
   - 3FN: Categoria separada de Produto; dados do cliente não repetidos em Pedido.
8. Montar dicionário de dados com nome do campo, tipo, obrigatoriedade, regra e exemplo.

## Artefatos/entregáveis

- DER/modelo entidade-relacionamento.
- Modelo lógico.
- Cardinalidades documentadas.
- Dicionário de dados.
- Lista de constraints planejadas.
- Hipóteses de modelagem, como carrinho em sessão e preço histórico em ItemPedido.

## Critérios de validação

- Toda tabela tem chave primária.
- Todo relacionamento necessário tem chave estrangeira.
- Nenhum pedido existe sem cliente.
- Nenhum item existe sem pedido e produto.
- Produto tem categoria, preço e estoque válidos.
- Preço do item fica registrado no pedido para preservar histórico caso o preço do produto mude depois.
- Itens do pedido não ficam armazenados diretamente na tabela Pedido.
- As cardinalidades são explicáveis em linguagem de negócio.

## Exemplos do material

Modelo lógico sugerido:

```text
clientes(id, nome, email, telefone, senha_hash)
categorias(id, nome)
produtos(id, nome, descricao, preco, estoque, categoria_id)
pedidos(id, cliente_id, status, total, cep, cidade, estado, endereco, numero, criado_em)
itens_pedido(id, pedido_id, produto_id, quantidade, preco_unitario)
```

Exemplo de dicionário:

```text
produtos.preco: preço unitário do produto; NUMERIC(10,2); deve ser >= 0.
pedidos.status: situação do pedido; VARCHAR; exemplo: CRIADO.
itens_pedido.quantidade: quantidade comprada; INTEGER; deve ser > 0.
```

## Dependências da próxima etapa

O modelo lógico vira o script SQL. Cada campo precisa de tipo. Cada regra importante precisa virar constraint. Cada consulta esperada ajuda a definir índices.

## Necessário vs opcional

Necessário:

- DER;
- modelo lógico;
- cardinalidades;
- dicionário de dados;
- regras e constraints planejadas;
- normalização básica.

Opcional:

- pgModeler ou dbdiagram.io específico;
- tabela de histórico de status do pedido;
- entidade de pagamento;
- entidade de entrega;
- tabela de carrinho;
- desnormalização para performance.

---

# 3. PostgreSQL e Estrutura Física

Fontes principais: HTML inicial, slides 19 a 25; HTML e-commerce, slides 18 a 22; HTML SQL/NoSQL, slides 14 a 21, 22, 39, 43 a 45.

## Objetivo

Transformar o modelo lógico em banco real: database, usuário, tabelas, constraints, índices, dados iniciais e consultas de validação.

Pergunta central do bloco: o PostgreSQL está estruturado para impedir dados inválidos e sustentar as consultas do MVP?

## Conceitos mínimos

- Database: banco lógico do projeto.
- Schema: agrupamento lógico de objetos.
- Tabela: estrutura física para entidade.
- DDL: comandos de criação e alteração de estrutura.
- DML: comandos para inserir, atualizar e consultar dados.
- Constraint: regra aplicada pelo banco.
- Índice: estrutura que acelera leitura, com custo em escrita e espaço.
- Role/usuário: conta de acesso ao banco.
- Seed/carga inicial: dados de exemplo.
- EXPLAIN: análise de plano de consulta.

## Tarefas a executar

1. Criar ou acessar PostgreSQL local/cloud.
2. Criar database, por exemplo `ecommerce`.
3. Criar usuário próprio da aplicação, sem usar superusuário em produção.
4. Criar `SQL/schema.sql`.
5. Criar tabelas:
   - categorias;
   - clientes;
   - produtos;
   - pedidos;
   - itens_pedido.
6. Aplicar constraints:
   - PRIMARY KEY;
   - FOREIGN KEY;
   - UNIQUE;
   - NOT NULL;
   - CHECK;
   - ON DELETE CASCADE em itens do pedido, se seguir o material.
7. Criar índices mínimos:
   - `idx_produtos_nome`;
   - `idx_pedidos_cliente`;
   - `idx_itens_pedido`;
   - UNIQUE em `clientes.email`;
   - UNIQUE em `categorias.nome`.
8. Criar `seed.sql` ou comando de inicialização para inserir categorias e produtos.
9. Rodar consultas de validação:
   - produtos com categoria;
   - produtos com estoque positivo;
   - pedidos por cliente;
   - itens por pedido;
   - tentativa de detectar estoque inválido.
10. Guardar evidências das consultas.

## Artefatos/entregáveis

- Banco PostgreSQL criado.
- Usuário/permissões da aplicação.
- `SQL/schema.sql`.
- Dados iniciais.
- Índices mínimos.
- Consultas SQL de validação.
- Evidências de que constraints rejeitam dados inválidos.

## Critérios de validação

- Não é possível inserir preço negativo.
- Não é possível inserir estoque negativo.
- Não é possível inserir quantidade menor ou igual a zero.
- Não é possível duplicar email de cliente.
- Não é possível criar produto sem categoria.
- Não é possível criar pedido sem cliente.
- Não é possível criar item sem pedido ou sem produto.
- Consultas com JOIN retornam dados coerentes.
- O schema físico bate com o modelo lógico.

## Exemplos do material

DDL de produto:

```sql
CREATE TABLE produtos (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(140) NOT NULL,
  descricao TEXT,
  preco NUMERIC(10,2) NOT NULL CHECK (preco >= 0),
  estoque INTEGER NOT NULL DEFAULT 0 CHECK (estoque >= 0),
  categoria_id INTEGER NOT NULL REFERENCES categorias(id)
);
```

Índices sugeridos:

```sql
CREATE INDEX idx_produtos_nome ON produtos(nome);
CREATE INDEX idx_pedidos_cliente ON pedidos(cliente_id);
```

Consulta inicial:

```sql
SELECT p.id, p.nome, p.preco, p.estoque, c.nome AS categoria
FROM produtos p
JOIN categorias c ON c.id = p.categoria_id
WHERE p.estoque > 0
ORDER BY p.nome;
```

## Dependências da próxima etapa

A aplicação Flask/SQLAlchemy precisa apontar para esse banco via `DATABASE_URL`. Os modelos ORM devem refletir as tabelas e constraints. Se o banco estiver errado, a aplicação só vai esconder inconsistências.

## Necessário vs opcional

Necessário:

- banco PostgreSQL;
- tabelas;
- PK/FK;
- NOT NULL, UNIQUE e CHECK;
- índices mínimos;
- dados iniciais;
- consultas de validação.

Opcional:

- Docker local;
- views;
- triggers;
- particionamento;
- índices avançados;
- backup/restauração completos já nesta etapa;
- ferramenta específica como DBeaver ou pgAdmin.

---

# 4. Aplicação Python/Flask

Fontes principais: HTML inicial, slides 26 a 32; HTML e-commerce, slides 23 a 40 e 56; HTML SQL/NoSQL, slides 6, 7 e 39.

## Objetivo

Implementar a aplicação web navegável, conectada ao PostgreSQL, com catálogo, carrinho e checkout.

Pergunta central do bloco: a aplicação consegue transformar ações do usuário em consultas e gravações corretas no banco?

## Conceitos mínimos

- Flask: framework web para rotas, sessão, mensagens e templates.
- Jinja: templates HTML.
- SQLAlchemy: ORM para mapear objetos Python em tabelas.
- psycopg: driver de conexão com PostgreSQL.
- `DATABASE_URL`: string de conexão configurada por ambiente.
- Sessão: estado temporário do carrinho no MVP.
- Rota: endpoint que responde a uma ação do usuário.
- Template: página renderizada para o usuário.

## Tarefas a executar

1. Baixar ou clonar o projeto-base incorporado ao HTML de e-commerce.
2. Abrir a estrutura sugerida:
   - `app.py`;
   - `requirements.txt`;
   - `.env.example`;
   - `Procfile`;
   - `render.yaml`;
   - `SQL/schema.sql`;
   - `templates/base.html`;
   - `templates/catalogo.html`;
   - `templates/carrinho.html`.
3. Criar ambiente virtual.
4. Instalar dependências:
   - Flask;
   - Flask-SQLAlchemy;
   - psycopg;
   - gunicorn.
5. Configurar `DATABASE_URL`.
6. Definir modelos ORM coerentes com o schema.
7. Implementar ou conferir rotas:
   - catálogo;
   - adicionar ao carrinho;
   - visualizar carrinho;
   - checkout.
8. Usar sessão para o carrinho no MVP.
9. Executar `flask --app app init-db`.
10. Executar localmente com `flask --app app run --debug`.
11. Testar cada rota antes do checkout final.

## Artefatos/entregáveis

- Aplicação Flask funcionando localmente.
- Catálogo exibindo produtos vindos do PostgreSQL.
- Carrinho funcional em sessão.
- Checkout gerando pedido e itens.
- Modelos ORM.
- Templates básicos.
- `requirements.txt`.
- `.env.example` sem segredos reais.
- README com comandos de execução.

## Critérios de validação

- A página inicial lista produtos do banco.
- Adicionar produto altera o carrinho.
- O carrinho mostra quantidades e total.
- O checkout persiste pedido e itens.
- A aplicação usa `DATABASE_URL`, não credencial fixa.
- A estrutura do projeto é simples e reproduzível.
- O app roda localmente antes do deploy.

## Exemplos do material

Fluxo da rota de catálogo:

```text
navegador solicita /
Flask executa a rota
SQLAlchemy gera SELECT
PostgreSQL devolve linhas
template monta o HTML
```

Exemplo de configuração:

```python
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/ecommerce"
)
db = SQLAlchemy(app)
```

Carrinho em sessão:

```python
carrinho = session.get("carrinho", {})
carrinho[str(produto_id)] = carrinho.get(str(produto_id), 0) + 1
session["carrinho"] = carrinho
```

## Dependências da próxima etapa

O checkout precisa ser protegido por transação. As rotas devem estar funcionais para que os testes validem fluxo feliz e falhas controladas.

## Necessário vs opcional

Necessário:

- Flask conectado ao PostgreSQL;
- catálogo;
- carrinho;
- checkout;
- modelos ORM;
- templates mínimos;
- comandos locais documentados.

Opcional:

- Postman/Insomnia;
- refatorar `app.py` em múltiplos arquivos;
- painel administrativo;
- design visual avançado;
- persistir carrinho no banco;
- usar Redis para sessão;
- autenticação completa.

---

# 5. Transações, Testes e Segurança

Fontes principais: HTML inicial, slides 33 a 38; HTML e-commerce, slides 34 a 42; HTML SQL/NoSQL, slides 8, 21, 43 a 45.

## Objetivo

Garantir que o checkout seja consistente, testável e minimamente seguro. O pedido, os itens e a baixa de estoque devem ocorrer como uma unidade.

Pergunta central do bloco: o sistema impede pedidos parciais, estoque inválido e exposição de dados sensíveis?

## Conceitos mínimos

- Transação: unidade de trabalho confirmada com commit ou desfeita com rollback.
- Atomicidade: tudo ocorre ou nada ocorre.
- Consistência: regras do banco permanecem válidas.
- Isolamento: compras concorrentes não devem corromper estoque.
- Durabilidade: após commit, o pedido permanece.
- Teste funcional: valida uma ação observável do usuário.
- Teste de erro: força uma falha esperada.
- Hash de senha: senha não armazenada em texto puro.
- Segredo: credencial fora do código.
- Privilégio mínimo: usuário de banco restrito à aplicação.
- Log seguro: registra erro sem expor credenciais.

## Tarefas a executar

1. Conferir se o checkout está dentro de `try/except`.
2. Criar pedido.
3. Para cada item do carrinho:
   - buscar produto;
   - validar se existe;
   - validar estoque;
   - reduzir estoque;
   - criar ItemPedido com `preco_unitario`;
   - acumular total.
4. Fazer `commit` somente se tudo der certo.
5. Fazer `rollback` se qualquer etapa falhar.
6. Testar casos mínimos:
   - compra normal;
   - estoque insuficiente;
   - produto inexistente;
   - catálogo carregando produtos;
   - carrinho calculando total;
   - banco refletindo pedido e itens.
7. Registrar evidências:
   - prints da aplicação;
   - consultas SQL;
   - logs relevantes;
   - antes/depois do estoque.
8. Aplicar segurança mínima:
   - `DATABASE_URL` fora do código;
   - `SECRET_KEY` fora do código;
   - senha como hash, se houver cadastro/autenticação;
   - usuário próprio no PostgreSQL;
   - `.env` no `.gitignore`;
   - nenhum dado pessoal real;
   - logs sem senha ou string completa de conexão.
9. Registrar estratégia básica de backup/restore ou pelo menos confirmar backup do provedor cloud.

## Artefatos/entregáveis

- Checkout transacional.
- Evidências de commit no fluxo feliz.
- Evidências de rollback em erro.
- Testes funcionais documentados.
- Consultas SQL de validação.
- Checklist de segurança.
- Logs sem credenciais.

## Critérios de validação

- Compra normal cria pedido, cria itens e reduz estoque.
- Estoque insuficiente não cria pedido válido nem reduz estoque parcialmente.
- Produto inexistente não finaliza pedido.
- Quantidade inválida não passa.
- Pedido sem itens não deve ser aceito como compra concluída.
- Credenciais não aparecem no GitHub.
- `SECRET_KEY` e `DATABASE_URL` são variáveis de ambiente.
- O grupo consegue explicar ACID com o exemplo do checkout.

## Exemplos do material

Fluxo transacional:

```text
BEGIN
cria pedido
insere itens
atualiza estoque
COMMIT
```

Se falhar:

```text
ROLLBACK
```

Exemplo de checkout:

```python
try:
    pedido = Pedido(cliente=cliente, status="CRIADO")
    db.session.add(pedido)

    for produto_id, quantidade in carrinho.items():
        produto = db.session.get(Produto, int(produto_id))
        if produto.estoque < quantidade:
            raise ValueError("Estoque insuficiente")
        produto.estoque -= quantidade
        db.session.add(ItemPedido(
            pedido=pedido,
            produto=produto,
            quantidade=quantidade,
            preco_unitario=produto.preco
        ))

    db.session.commit()
except Exception:
    db.session.rollback()
```

Consultas de validação:

```sql
SELECT * FROM pedidos ORDER BY id DESC;

SELECT p.id, c.nome, p.status, p.total
FROM pedidos p
JOIN clientes c ON c.id = p.cliente_id;

SELECT ip.pedido_id, pr.nome, ip.quantidade, ip.preco_unitario
FROM itens_pedido ip
JOIN produtos pr ON pr.id = ip.produto_id;
```

## Dependências da próxima etapa

Só vale publicar depois que o fluxo local estiver validado. O deploy expõe a aplicação; se a transação falha localmente, ela também falhará em cloud.

## Necessário vs opcional

Necessário:

- commit/rollback no checkout;
- testes do fluxo feliz e dos erros mínimos;
- evidências;
- segurança básica de segredos;
- validação no formulário e no banco;
- logs sem credenciais.

Opcional ou avançado:

- suíte completa com pytest;
- Postman/Insomnia;
- teste de concorrência;
- `SELECT ... FOR UPDATE`;
- monitoramento com ferramentas externas;
- backup/restore completo com automação;
- GitHub Actions.

---

# 6. Deploy Cloud e Atividade Prática

Fontes principais: HTML inicial, slides 39 a 44; HTML e-commerce, slides 43 a 52; HTML SQL/NoSQL, slides 35, 38, 43 a 45 e 50 a 53.

## Objetivo

Publicar banco e aplicação em ambiente acessível pela web, validar a URL pública e preparar a demonstração final com evidências.

Pergunta central do bloco: a solução está publicada, utilizável e demonstrável?

## Conceitos mínimos

- GitHub: versionamento e entrega do código.
- Banco cloud: PostgreSQL hospedado, por exemplo Neon ou Supabase.
- App cloud: hospedagem Flask, por exemplo Render, Railway ou serviço equivalente.
- Build command: instala dependências.
- Start command: inicia a aplicação.
- Variáveis de ambiente: segredos configurados fora do código.
- SSL: conexão segura conforme exigência do provedor.
- Logs: evidência de execução e diagnóstico.
- URL pública: endereço final para demonstração.

## Tarefas a executar

1. Publicar o código no GitHub.
2. Conferir que `.env` não foi enviado.
3. Criar banco PostgreSQL cloud.
4. Copiar string de conexão.
5. Configurar `DATABASE_URL` como segredo.
6. Configurar `SECRET_KEY` como segredo.
7. Executar `schema.sql` ou `flask --app app init-db` no ambiente adequado.
8. Conectar serviço de app ao repositório.
9. Configurar build:
   - `pip install -r requirements.txt`.
10. Configurar start:
   - `gunicorn app:app`.
11. Abrir URL pública.
12. Testar catálogo, carrinho e checkout em produção.
13. Conferir logs.
14. Coletar evidências:
   - link do repositório;
   - URL pública;
   - prints;
   - consultas SQL;
   - README;
   - modelo ER;
   - dicionário de dados.
15. Preparar apresentação.

## Artefatos/entregáveis

Pelo HTML inicial, a atividade prática orientada consolida:

- Entrega 1: repositório com código e README atualizado.
- Entrega 2: banco PostgreSQL cloud configurado.
- Entrega 3: aplicação publicada com URL acessível.
- Entrega 4: modelo ER, dicionário de dados e evidências de teste.

Pelo manual de e-commerce, também é útil ter:

- script SQL;
- aplicação publicada;
- banco cloud;
- justificativa do banco;
- constraints e índices;
- explicação da transação;
- limitações do MVP e melhorias futuras.

## Critérios de validação

- URL pública abre.
- Produtos aparecem no catálogo.
- Carrinho funciona.
- Checkout cria pedido e itens.
- Estoque reduz após commit.
- Erro de estoque insuficiente não deixa gravação parcial.
- Banco cloud contém o schema e dados esperados.
- README explica instalação, variáveis e execução.
- GitHub não expõe credenciais.
- O grupo consegue demonstrar com prints, SQL e navegação real.

## Exemplos do material

Arquitetura cloud:

```text
GitHub -> serviço web Flask -> PostgreSQL cloud -> usuário acessa URL pública
```

Variáveis:

```text
DATABASE_URL=postgresql+psycopg://usuario:senha@host:5432/ecommerce
SECRET_KEY=valor_aleatorio_forte
```

Roteiro da atividade prática:

```text
formar grupos
adaptar o projeto-base
subir banco
publicar app
rodar testes
apresentar o resultado
```

## Dependências posteriores

A apresentação depende de evidências objetivas. Sem URL, prints, consultas SQL, DER, dicionário e README, o grupo pode até ter código funcionando, mas fica fraco para demonstrar aprendizado.

## Necessário vs opcional

Necessário:

- GitHub atualizado;
- banco PostgreSQL cloud;
- app publicado;
- URL acessível;
- variáveis de ambiente configuradas;
- testes em produção;
- evidências;
- README;
- modelo ER;
- dicionário de dados.

Opcional:

- provedor específico, desde que publique app e PostgreSQL;
- GitHub Actions;
- Docker;
- domínio próprio;
- monitoramento avançado;
- analytics;
- Redis/MongoDB;
- extensão do MVP.

---

# Como os Materiais Se Complementam

## Papel do HTML inicial

É o roteiro oficial de execução. Ele define o ciclo:

```text
requisito -> entidade -> tabela -> ORM -> rota -> transação/teste -> deploy
```

Ele também define o checklist final:

- problema e escopo do MVP;
- RF/RNF;
- DER e modelo lógico;
- PostgreSQL com tabelas, constraints e índices mínimos;
- Flask conectado;
- checkout com commit/rollback;
- testes e evidências;
- segredos fora do código;
- GitHub atualizado;
- aplicação publicada em cloud.

## Papel do HTML E-commerce com Python e PostgreSQL

É o manual prático. Use para executar:

- RF01 a RF06;
- RNFs;
- entidades Cliente, Categoria, Produto, Pedido e ItemPedido;
- DDL;
- carga inicial;
- estrutura do projeto;
- dependências;
- configuração `DATABASE_URL`;
- modelos ORM;
- rotas;
- carrinho em sessão;
- checkout transacional;
- testes SQL;
- deploy;
- projeto-base incorporado.

Não usar esse material para inflar o escopo sem necessidade. Os desafios de extensão são úteis se houver tempo ou se o professor cobrar explicitamente.

## Papel do HTML SQL e NoSQL

É a fundamentação. Use para responder "por que" em apresentação:

- por que PostgreSQL serve para o núcleo transacional;
- por que SQL é adequado a dados estruturados, integridade forte e consultas relacionais;
- como ACID justifica o checkout;
- por que normalizar;
- por que índices ajudam e também custam;
- quando NoSQL faria sentido como extensão;
- quais cuidados de segurança, LGPD, backup, observabilidade e cloud importam.

Não implementar NoSQL no MVP só porque o material conceitual apresenta várias tecnologias.

---

# Checklist Final Consolidado

## Escopo e requisitos

- [ ] Problema do e-commerce descrito.
- [ ] Atores listados.
- [ ] Dores e metas registradas.
- [ ] RF01 a RF06 documentados.
- [ ] RNFs documentados.
- [ ] Backlog priorizado.
- [ ] Fluxo catálogo -> carrinho -> checkout desenhado.
- [ ] Critérios de aceite definidos.
- [ ] Fora de escopo declarado.

## Modelagem

- [ ] DER pronto.
- [ ] Modelo lógico pronto.
- [ ] Entidades Cliente, Categoria, Produto, Pedido e ItemPedido representadas.
- [ ] Carrinho tratado como sessão no MVP.
- [ ] Cardinalidades documentadas.
- [ ] Dicionário de dados pronto.
- [ ] Regras de integridade planejadas.
- [ ] Normalização básica explicada.

## PostgreSQL

- [ ] Banco criado.
- [ ] Usuário próprio da aplicação criado.
- [ ] `schema.sql` pronto.
- [ ] Tabelas criadas.
- [ ] PK/FK aplicadas.
- [ ] NOT NULL, UNIQUE e CHECK aplicados.
- [ ] Índices mínimos criados.
- [ ] Dados iniciais carregados.
- [ ] Consultas de validação salvas.

## Aplicação

- [ ] Projeto-base baixado/adaptado.
- [ ] Dependências instaladas.
- [ ] `DATABASE_URL` configurada.
- [ ] Modelos ORM conferidos.
- [ ] Catálogo funcionando.
- [ ] Carrinho funcionando.
- [ ] Checkout funcionando.
- [ ] README com comandos locais.
- [ ] `.env.example` sem credenciais reais.

## Transações, testes e segurança

- [ ] Checkout usa commit/rollback.
- [ ] Compra normal testada.
- [ ] Estoque insuficiente testado.
- [ ] Produto inexistente testado.
- [ ] SQL confirma pedido, itens e estoque.
- [ ] Prints/evidências coletados.
- [ ] `SECRET_KEY` fora do código.
- [ ] `DATABASE_URL` fora do código.
- [ ] `.env` no `.gitignore`.
- [ ] Nenhuma credencial no GitHub.
- [ ] Logs sem string de conexão completa.
- [ ] Dados pessoais reais evitados.

## Deploy e apresentação

- [ ] GitHub atualizado.
- [ ] PostgreSQL cloud configurado.
- [ ] App cloud configurado.
- [ ] Variáveis de ambiente cadastradas.
- [ ] Schema/seed aplicado em cloud.
- [ ] URL pública funcionando.
- [ ] Fluxo completo testado na URL pública.
- [ ] Modelo ER separado para apresentação.
- [ ] Dicionário de dados separado para apresentação.
- [ ] Evidências organizadas.
- [ ] Limitações do MVP documentadas.
- [ ] Próximos passos documentados.

---

# Modo Emergência: Poucas Horas

Objetivo: maximizar chance de entrega com o menor escopo fiel ao material.

## Regra de corte

Não construir nada que não esteja no fluxo mínimo:

```text
catálogo -> carrinho -> checkout -> pedido/itens -> baixa de estoque -> evidências -> deploy
```

## Prioridade P0: não negociar

1. Usar projeto-base.
2. Definir RF01 a RF06.
3. Fazer DER com 5 entidades.
4. Criar schema PostgreSQL com constraints.
5. Rodar catálogo/carrinho/checkout.
6. Garantir commit/rollback.
7. Registrar 3 testes: compra normal, estoque insuficiente, produto inexistente.
8. Subir GitHub.
9. Publicar app e banco.
10. Preparar apresentação com URL, DER, SQL e evidências.

## Prioridade P1: fazer se couber

- README bem explicado.
- Dicionário de dados completo.
- Prints antes/depois do estoque.
- Consulta SQL com JOIN para pedido e itens.
- Pequena explicação SQL x NoSQL.
- Justificativa dos índices.
- Segurança básica bem documentada.

## Prioridade P2: cortar se o tempo apertar

- layout bonito;
- CRUD administrativo;
- autenticação completa;
- pagamento;
- frete;
- Redis;
- MongoDB;
- analytics dashboard;
- migrations;
- Docker;
- GitHub Actions;
- teste automatizado extenso;
- monitoramento avançado.

## Roteiro de execução em 4 horas

| Tempo | Foco | Saída mínima |
|---:|---|---|
| 0:00-0:20 | Escopo | RF/RNF, fluxo e fora de escopo |
| 0:20-0:50 | Modelagem | DER, modelo lógico e regras |
| 0:50-1:30 | PostgreSQL | schema, seed e consultas |
| 1:30-2:30 | Flask | projeto-base rodando com catálogo/carrinho |
| 2:30-3:00 | Checkout | pedido, itens, estoque, commit/rollback |
| 3:00-3:25 | Testes | evidências dos 3 casos mínimos |
| 3:25-4:00 | Deploy/apresentação | GitHub, cloud, URL, roteiro final |

Se o deploy atrasar, ainda assim organizar todas as evidências locais e deixar claro o erro específico. Mas, pelo HTML inicial, deploy publicado deve ser tratado como obrigatório.

---

# Perguntas que o Grupo Deve Saber Responder

## Sobre requisitos e domínio

1. Qual problema de negócio o MVP resolve?
2. Quais atores aparecem no processo e o que cada um precisa?
3. Quais são RF01 a RF06?
4. O que ficou fora do MVP e por quê?
5. Como o fluxo catálogo -> carrinho -> checkout vira dados persistidos?
6. Qual critério de aceite prova que "adicionar ao carrinho" funciona?
7. Qual critério de aceite prova que "finalizar pedido" funciona?

## Sobre modelagem

1. Por que Cliente, Categoria, Produto, Pedido e ItemPedido viraram entidades?
2. Por que Carrinho não precisa virar tabela no MVP?
3. Qual é a cardinalidade Cliente 1:N Pedido?
4. Qual é a cardinalidade Pedido 1:N ItemPedido?
5. Qual é a cardinalidade Produto 1:N ItemPedido?
6. O que aconteceria se os itens fossem gravados diretamente em Pedido?
7. Por que `preco_unitario` deve ficar em ItemPedido?
8. Onde aparecem 1FN, 2FN e 3FN no modelo?

## Sobre PostgreSQL

1. Por que PostgreSQL foi escolhido para o núcleo transacional?
2. Por que preço usa NUMERIC/DECIMAL e não FLOAT?
3. Para que servem PRIMARY KEY e FOREIGN KEY neste projeto?
4. Que erro de negócio é evitado por CHECK em preço, estoque e quantidade?
5. Por que email e categoria podem ter UNIQUE?
6. Quais índices mínimos foram criados e que consultas eles ajudam?
7. Por que índice demais pode ser ruim?

## Sobre aplicação Flask

1. Qual é o caminho de uma requisição desde o navegador até o PostgreSQL?
2. O que Flask faz?
3. O que SQLAlchemy faz?
4. O que psycopg faz?
5. Para que serve `DATABASE_URL`?
6. Como o catálogo busca produtos no banco?
7. Como o carrinho fica salvo temporariamente?
8. Como o checkout transforma sessão em pedido persistido?

## Sobre transações, testes e segurança

1. Por que o checkout precisa ser atômico?
2. O que pode acontecer se o pedido for gravado, mas o estoque não for reduzido?
3. Quando o sistema deve fazer commit?
4. Quando deve fazer rollback?
5. Como o teste de estoque insuficiente prova que o rollback funciona?
6. Como as consultas SQL comprovam que pedido e itens foram persistidos?
7. Por que senha não deve ser armazenada em texto puro?
8. Por que `DATABASE_URL` e `SECRET_KEY` não podem ir para o GitHub?
9. O que significa privilégio mínimo no usuário do PostgreSQL?
10. Que cuidados básicos de LGPD e dados pessoais foram adotados?

## Sobre deploy e arquitetura

1. Quais são as entregas finais?
2. Como o GitHub entra no deploy?
3. Como o PostgreSQL cloud foi configurado?
4. Quais variáveis de ambiente foram cadastradas?
5. Qual comando inicia a aplicação no deploy?
6. Que evidências demonstram que a URL está funcional?
7. Quais limitações do MVP devem ser assumidas na apresentação?
8. Se fosse evoluir, qual extensão faria mais sentido primeiro?

## Sobre SQL x NoSQL

1. Por que SQL é adequado para pedidos, estoque e cliente?
2. Em que cenário NoSQL de documentos faria sentido?
3. Em que cenário Redis faria sentido?
4. Por que não implementar NoSQL agora apenas para parecer mais avançado?
5. O que significa arquitetura híbrida ou polyglot persistence?
6. Como ACID se relaciona com o checkout?
7. Como a matriz SQL x NoSQL ajuda a justificar a escolha do banco?

---

# Extensões: Como Tratar Sem Perder o Escopo

O HTML de e-commerce apresenta desafios de extensão. Pelo HTML inicial, eles não devem substituir o MVP. Trate como aprofundamento se houver tempo ou se o professor exigir.

Extensões possíveis do material:

- cadastro administrativo de produtos e categorias;
- autenticação e área "meus pedidos";
- ciclo de vida do pedido;
- migrations e testes automatizados;
- imagens em object storage;
- analytics de vendas.

Regra didática para qualquer extensão:

1. Qual problema resolve?
2. O que muda no modelo?
3. O que muda no código?
4. Como será testada?

Extensão mais segura academicamente, se sobrar tempo: analytics de vendas simples com SQL, porque reforça GROUP BY, views, índices e evidências, sem mexer no núcleo transacional.

---

# Roteiro Curto da Apresentação

1. Problema: controlar catálogo, carrinho, pedido e estoque em um e-commerce simples.
2. Requisitos: RF01 a RF06 e RNFs principais.
3. Modelo: DER com Cliente, Categoria, Produto, Pedido e ItemPedido.
4. Banco: mostrar tabelas, constraints e índices.
5. Aplicação: demonstrar catálogo e carrinho.
6. Checkout: finalizar pedido e explicar commit/rollback.
7. Evidência SQL: mostrar pedido, itens e estoque atualizado.
8. Segurança: segredos fora do código, hash, usuário próprio e logs sem credenciais.
9. Deploy: abrir URL pública.
10. Limitações e próximos passos: sem pagamento real, sem logística e sem autenticação completa no MVP.

---

# Como Aprofundar Depois

Use este guia como índice operacional. Para continuar subseção por subseção, peça uma destas frentes:

- "Aprofunde o Bloco 1 e transforme em documento de escopo com RF/RNF e critérios de aceite."
- "Aprofunde o Bloco 2 e monte o DER, modelo lógico e dicionário de dados."
- "Aprofunde o Bloco 3 e gere o schema.sql e seed.sql."
- "Aprofunde o Bloco 4 e adapte o projeto-base Flask."
- "Aprofunde o Bloco 5 e monte os testes e evidências."
- "Aprofunde o Bloco 6 e prepare o deploy e roteiro de apresentação."

O caminho mais seguro é avançar na ordem. Cada etapa produz insumos para a próxima.
