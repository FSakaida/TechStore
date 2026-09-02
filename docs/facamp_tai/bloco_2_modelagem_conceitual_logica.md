# Bloco 2 - Modelagem Conceitual e Lógica

Projeto: aplicação e banco de dados de e-commerce com PostgreSQL e Python/Flask.

## Fontes

- HTML inicial - Etapas do projeto de e-commerce: Bloco 2, slides 12 a 18.
- HTML prático - E-commerce com Python e PostgreSQL: slides 10 a 17.
- HTML conceitual - SQL e NoSQL: slides 11 a 13.

## 1. Escopo da Etapa

Esta etapa transforma os requisitos aprovados no Bloco 1 em modelo de dados. O resultado esperado é: DER, modelo lógico, cardinalidades, dicionário de dados e regras de integridade planejadas.

O modelo deve sustentar o fluxo definido no Bloco 1:

```text
catálogo -> carrinho -> checkout -> pedido -> atualização de estoque
```

O carrinho será mantido em sessão no MVP; portanto, não será modelado como tabela obrigatória. Os dados básicos de contato e entrega coletados no checkout serão armazenados em Cliente e Pedido, sem criar módulo logístico.

Ferramentas recomendadas pelo material: dbdiagram.io, Draw.io/diagrams.net, pgModeler ou DBeaver.

## 2. Objetivo

Representar o domínio do e-commerce por meio de entidades, atributos, relacionamentos, cardinalidades, chaves e regras, preparando a criação do banco PostgreSQL no Bloco 3.

## 3. Entidades do Modelo Conceitual

| Entidade | Descrição | Origem no Bloco 1 |
|---|---|---|
| Cliente | Pessoa associada aos pedidos realizados, com dados básicos de contato. | RF06 |
| Categoria | Agrupamento dos produtos do catálogo. | RF01 |
| Produto | Item vendido, com preço, estoque e categoria. | RF01, RF02, RF05 |
| Pedido | Registro da compra finalizada por um cliente, incluindo dados básicos de entrega informados no checkout. | RF04, RF06 |
| ItemPedido | Associação entre pedido e produto, com quantidade e preço unitário. | RF04, RF05 |

## 4. Relacionamentos e Cardinalidades

| Relacionamento | Cardinalidade | Interpretação |
|---|---:|---|
| Cliente -> Pedido | 1:N | Um cliente pode realizar vários pedidos; cada pedido pertence a um cliente. |
| Categoria -> Produto | 1:N | Uma categoria pode conter vários produtos; cada produto pertence a uma categoria. |
| Pedido -> ItemPedido | 1:N | Um pedido pode possuir vários itens; cada item pertence a um pedido. |
| Produto -> ItemPedido | 1:N | Um produto pode aparecer em vários itens de pedido; cada item referencia um produto. |

## 5. Representação Conceitual do DER

```text
Cliente 1:N Pedido
Pedido 1:N ItemPedido
Produto 1:N ItemPedido
Categoria 1:N Produto
```

Leitura do modelo:

- Cliente realiza Pedido.
- Pedido possui ItemPedido.
- ItemPedido referencia Produto.
- Produto pertence a Categoria.

## 6. Modelo Lógico

| Tabela | Campos principais |
|---|---|
| clientes | id PK, nome, email UNIQUE, telefone, senha_hash |
| categorias | id PK, nome UNIQUE |
| produtos | id PK, nome, descricao, preco, estoque, categoria_id FK |
| pedidos | id PK, cliente_id FK, status, total, cep, cidade, estado, endereco, numero, criado_em |
| itens_pedido | id PK, pedido_id FK, produto_id FK, quantidade, preco_unitario |

Observação: `senha_hash` é mantido por coerência com o projeto-base e com o requisito de segurança. Isso não implica autenticação completa no MVP.

## 7. Dicionário de Dados

| Tabela | Campo | Significado | Tipo previsto | Obrigatoriedade/regra | Exemplo |
|---|---|---|---|---|---|
| clientes | id | Identificador do cliente. | INTEGER/SERIAL | PK | 1 |
| clientes | nome | Nome do cliente. | VARCHAR(120) | NOT NULL | Maria Silva |
| clientes | email | E-mail do cliente. | VARCHAR(160) | NOT NULL, UNIQUE | maria@email.com |
| clientes | telefone | Telefone informado no checkout. | VARCHAR(20) | NOT NULL | (11) 99999-9999 |
| clientes | senha_hash | Senha protegida por hash, quando houver senha. | VARCHAR(255) | NOT NULL no projeto-base | hash gerado pela aplicação |
| categorias | id | Identificador da categoria. | INTEGER/SERIAL | PK | 1 |
| categorias | nome | Nome da categoria. | VARCHAR(80) | NOT NULL, UNIQUE | Tecnologia |
| produtos | id | Identificador do produto. | INTEGER/SERIAL | PK | 1 |
| produtos | nome | Nome comercial do produto. | VARCHAR(140) | NOT NULL | Teclado Mecânico |
| produtos | descricao | Descrição do produto. | TEXT | Opcional | Switches táteis |
| produtos | preco | Preço unitário atual do produto. | NUMERIC(10,2) | NOT NULL, CHECK preco >= 0 | 299.90 |
| produtos | estoque | Quantidade disponível. | INTEGER | NOT NULL, CHECK estoque >= 0 | 20 |
| produtos | categoria_id | Categoria do produto. | INTEGER | FK, NOT NULL | 1 |
| pedidos | id | Identificador do pedido. | INTEGER/SERIAL | PK | 1 |
| pedidos | cliente_id | Cliente responsável pelo pedido. | INTEGER | FK, NOT NULL | 1 |
| pedidos | status | Situação do pedido. | VARCHAR(30) | NOT NULL, padrão CRIADO | CRIADO |
| pedidos | total | Valor total do pedido. | NUMERIC(10,2) | NOT NULL, padrão 0 | 449.80 |
| pedidos | cep | CEP informado no checkout. | VARCHAR(12) | NOT NULL | 13000-000 |
| pedidos | cidade | Cidade informada no checkout. | VARCHAR(100) | NOT NULL | Campinas |
| pedidos | estado | Estado informado no checkout. | CHAR(2) | NOT NULL | SP |
| pedidos | endereco | Endereço informado no checkout. | VARCHAR(180) | NOT NULL | Rua Exemplo |
| pedidos | numero | Número informado no checkout. | VARCHAR(20) | NOT NULL | 100 |
| pedidos | criado_em | Data e hora de criação. | TIMESTAMPTZ | NOT NULL, padrão data/hora atual | 2026-09-02 10:30:00-03 |
| itens_pedido | id | Identificador do item. | INTEGER/SERIAL | PK | 1 |
| itens_pedido | pedido_id | Pedido ao qual o item pertence. | INTEGER | FK, NOT NULL | 1 |
| itens_pedido | produto_id | Produto comprado. | INTEGER | FK, NOT NULL | 1 |
| itens_pedido | quantidade | Quantidade comprada. | INTEGER | NOT NULL, CHECK quantidade > 0 | 2 |
| itens_pedido | preco_unitario | Preço registrado no momento da compra. | NUMERIC(10,2) | NOT NULL, CHECK preco_unitario >= 0 | 299.90 |

## 8. Regras de Integridade Planejadas

| Regra | Implementação prevista |
|---|---|
| Cada cliente deve ter identificador único. | PRIMARY KEY em `clientes.id`. |
| E-mails não devem ser duplicados. | UNIQUE em `clientes.email`. |
| Categorias não devem ser duplicadas. | UNIQUE em `categorias.nome`. |
| Produto deve pertencer a uma categoria. | FK `produtos.categoria_id`. |
| Preço não pode ser negativo. | CHECK em `produtos.preco` e `itens_pedido.preco_unitario`. |
| Estoque não pode ser negativo. | CHECK em `produtos.estoque`. |
| Pedido deve pertencer a um cliente. | FK `pedidos.cliente_id`. |
| Pedido deve registrar os dados básicos do checkout. | NOT NULL em `pedidos.cep`, `cidade`, `estado`, `endereco` e `numero`. |
| Item deve pertencer a um pedido. | FK `itens_pedido.pedido_id`. |
| Item deve referenciar um produto. | FK `itens_pedido.produto_id`. |
| Quantidade comprada deve ser positiva. | CHECK em `itens_pedido.quantidade`. |

## 9. Índices Planejados

| Índice | Finalidade |
|---|---|
| idx_produtos_nome | Busca e ordenação no catálogo. |
| idx_pedidos_cliente | Consulta de histórico de pedidos por cliente. |
| idx_itens_pedido | Consulta dos itens de um pedido. |

A criação física dos índices será detalhada no Bloco 3.

## 10. Validação e Normalização

| Forma | Aplicação no modelo |
|---|---|
| 1FN | Campos atômicos; produtos de um pedido ficam em `itens_pedido`, não em colunas repetidas. |
| 2FN | `ItemPedido` representa a associação entre pedido e produto, evitando dependências parciais. |
| 3FN | `Categoria` fica separada de `Produto`; dados do cliente não são repetidos em `Pedido`. |

Validações conceituais:

- Um pedido sem cliente não é válido.
- Um item de pedido sem produto não é válido.
- Um produto sem categoria não é válido no modelo adotado.
- O preço unitário deve ficar em `ItemPedido` para preservar o histórico da compra.
- O carrinho é processo temporário do MVP, não entidade persistente obrigatória.
- Os dados de entrega ficam em `Pedido`, pois podem variar entre compras do mesmo cliente.

## 11. Artefatos da Etapa

- DER/modelo entidade-relacionamento.
- Modelo lógico.
- Cardinalidades documentadas.
- Dicionário de dados.
- Regras de integridade planejadas.
- Índices planejados.

## 12. Validação da Etapa

Esta etapa estará concluída quando:

- as entidades Cliente, Categoria, Produto, Pedido e ItemPedido estiverem definidas;
- os relacionamentos e cardinalidades estiverem documentados;
- o modelo lógico estiver coerente com RF01 a RF06;
- o dicionário de dados contiver campos, tipos e regras principais;
- as constraints planejadas cobrirem integridade, unicidade e obrigatoriedade;
- a normalização básica estiver justificada;
- o grupo conseguir explicar por que Carrinho não é tabela no MVP.
- o grupo conseguir explicar que os campos de entrega não representam logística, apenas dados básicos do checkout.

## 13. Encaminhamento Para o Bloco 3

O modelo lógico servirá de base para criar o PostgreSQL, suas tabelas, constraints, índices e carga inicial.

| Saída do Bloco 2 | Uso no Bloco 3 |
|---|---|
| Entidades | Criação das tabelas. |
| Atributos | Definição das colunas. |
| Cardinalidades | Definição das chaves estrangeiras. |
| Regras de integridade | Criação de NOT NULL, UNIQUE, CHECK e FK. |
| Índices planejados | Criação dos índices físicos no PostgreSQL. |
