# Bloco 3 - PostgreSQL e Estrutura Física em Cloud

Projeto: aplicação e banco de dados de e-commerce com PostgreSQL e Python/Flask.

## 0. Conferência de Coerência

Este documento está alinhado ao Guia-Mãe, ao HTML inicial e aos Blocos 1 e 2.

No Bloco 1, o MVP foi definido como:

```text
catálogo -> carrinho -> checkout -> pedido -> atualização de estoque
```

No Bloco 2, esse fluxo virou o modelo:

```text
Cliente -> Pedido -> ItemPedido -> Produto -> Categoria
```

No Bloco 3, o modelo passa a existir fisicamente no PostgreSQL cloud:

```text
entidades -> tabelas
atributos -> colunas
cardinalidades -> chaves estrangeiras
regras -> constraints
consultas esperadas -> índices
```

O escopo permanece o mesmo: não criar tabela de carrinho, pagamento real, logística/frete/rastreamento, autenticação completa, MongoDB ou Redis nesta etapa. O telefone em `clientes` e o endereço básico em `pedidos` existem apenas para persistir os dados já coletados no checkout.

## 1. Fontes

- HTML inicial - Etapas do projeto de e-commerce: Bloco 3, slides 19 a 25.
- HTML prático - E-commerce com Python e PostgreSQL: slides 18 a 22.
- HTML conceitual - SQL e NoSQL: slides 14 a 22.
- Guia-Mãe operacional: Bloco 3.
- Documentação oficial do PostgreSQL, Neon e SQLAlchemy.

## 2. Objetivo da Etapa

Criar o banco PostgreSQL em cloud com:

- tabelas;
- chaves primárias;
- chaves estrangeiras;
- constraints;
- índices mínimos;
- dados iniciais;
- consultas de validação;
- evidências para apresentação.

Em linguagem simples: neste bloco, montamos o "estoque organizado" do sistema. Cada prateleira é uma tabela, cada etiqueta é uma coluna, cada regra de entrada é uma constraint, e cada mapa de busca é um índice.

## 3. Ferramentas Definidas Para Este Projeto

O provedor escolhido para este projeto é a Neon. A alternativa Supabase aparece no material da disciplina, mas não será usada neste roteiro.

| Item | Configuração atual |
|---|---|
| Projeto Neon | `techstore-facamp-tai` |
| Project ID | `cool-darkness-01827021` |
| Região | São Paulo, `aws-sa-east-1` |
| Branch | `production` |
| PostgreSQL | versão 18 |
| Serviços usados | Postgres |
| Serviços fora do MVP | Neon Auth, Object Storage, Functions, AI Gateway |

Ferramentas usadas no Bloco 3:

| Ferramenta | Uso prático |
|---|---|
| Neon Console | Acessar o projeto, abrir SQL Editor, visualizar tabelas e copiar conexão. |
| Neon SQL Editor | Executar `01_schema.sql`, `02_seed.sql`, `03_validacao.sql` e `04_testes_constraints.sql`. |
| Neon CLI | Manter a pasta local vinculada ao projeto Neon. |
| Arquivos SQL do projeto | Criar e validar a estrutura física do banco. |

## 4. Atenção Antes de Começar

Não rode comandos de criação local como `CREATE DATABASE` ou `CREATE USER` neste roteiro. A Neon já criou:

- projeto;
- banco;
- usuário;
- senha;
- host;
- porta;
- string de conexão.

Também já foram executados no projeto:

- instalação da Neon CLI;
- login na Neon;
- `neon skills -y`;
- `neon mcp -y`;
- `neon link --project-id cool-darkness-01827021 --branch production -y`;
- `neon config init`;
- configuração mínima em `neon.ts`;
- `neon deploy`.

Portanto, o trabalho do grupo no Bloco 3 é criar a estrutura do e-commerce dentro do banco Neon já vinculado.

## 5. Arquivos Pré-Prontos

Os arquivos estão na subpasta:

[sql](sql)

| Ordem | Arquivo | Função |
|---:|---|---|
| 0 | `00_leia_primeiro_cloud.md` | Instruções rápidas para execução em cloud. |
| 1 | `01_schema.sql` | Cria tabelas, chaves, constraints e índices mínimos. |
| 2 | `02_seed.sql` | Insere dados fictícios para demonstração. |
| 3 | `03_validacao.sql` | Valida catálogo, JOINs, estoque, constraints, índices e plano de consulta. |
| 4 | `04_testes_constraints.sql` | Confirma que o banco bloqueia dados inválidos. |

## 6. Passo a Passo Intuitivo

### Passo 1 - Conferir o projeto Neon

Este passo já foi preparado. Antes de rodar os SQLs, confirme no painel da Neon:

1. O projeto aberto é `techstore-facamp-tai`.
2. A branch selecionada é `production`.
3. O serviço ativo é Postgres.
4. Neon Auth está desativado.
5. A região é São Paulo.

O comando de conferência local é:

```bash
neon status
```

Se `neon` não for reconhecido no terminal, abra um novo terminal. A configuração já foi feita; não é necessário repetir o login.

### Passo 2 - Abrir o SQL Editor da Neon

No painel da Neon:

1. Abrir o projeto `techstore-facamp-tai`.
2. Entrar em `SQL Editor`.
3. Conferir se a branch é `production`.
4. Apagar qualquer SQL de exemplo que aparecer.
5. Executar os scripts do projeto, um por vez.

Para este Bloco 3, use o SQL Editor da Neon. DBeaver e pgAdmin ficam opcionais.

### Passo 3 - Criar a estrutura física

Abra o arquivo:

[01_schema.sql](sql/01_schema.sql)

Copie e execute no SQL Editor da Neon.

Use um banco vazio. Se alguém já tiver executado uma versão antiga do schema, revise antes de repetir o script, porque `CREATE TABLE IF NOT EXISTS` não adiciona campos novos em tabelas já criadas.

Esse script cria:

- `categorias`;
- `clientes`;
- `produtos`;
- `pedidos`;
- `itens_pedido`;
- índices mínimos.
 
O schema também inclui `telefone` em `clientes` e dados básicos de entrega em `pedidos`, em coerência com a tela de checkout já existente.

Trecho central:

```sql
CREATE TABLE IF NOT EXISTS produtos (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(140) NOT NULL,
  descricao TEXT,
  preco NUMERIC(10,2) NOT NULL CHECK (preco >= 0),
  estoque INTEGER NOT NULL DEFAULT 0 CHECK (estoque >= 0),
  categoria_id INTEGER NOT NULL REFERENCES categorias(id)
);
```

Validação esperada: o painel deve informar execução concluída sem erro.

### Passo 4 - Entender as regras do banco

O script usa constraints para proteger o MVP:

| Regra | Como aparece no banco |
|---|---|
| Registro único | `PRIMARY KEY` |
| Relacionamento obrigatório | `FOREIGN KEY` |
| Campo obrigatório | `NOT NULL` |
| Sem duplicidade de e-mail/categoria | `UNIQUE` |
| Sem preço, estoque ou quantidade inválida | `CHECK` |
| Dados obrigatórios do checkout | `NOT NULL` |

Apenas uma interpretação mais didática: a aplicação pode errar, mas o banco continua sendo o porteiro. Se alguém tentar inserir preço negativo, estoque negativo ou item sem pedido, o PostgreSQL deve bloquear.

### Passo 5 - Carregar dados fictícios

Abra o arquivo:

[02_seed.sql](sql/02_seed.sql)

Execute no mesmo banco cloud.

Ele cria:

- categorias: Tecnologia e Acessórios;
- cliente fictício;
- produtos fictícios para demonstração.
 
O cliente fictício inclui telefone para respeitar o modelo atualizado.

Os dados são suficientes para mostrar catálogo, carrinho e checkout nas próximas etapas.

### Passo 6 - Validar a estrutura

Abra o arquivo:

[03_validacao.sql](sql/03_validacao.sql)

Execute no banco cloud.

O que observar:

- a consulta de produtos deve retornar produtos com categoria;
- a consulta de estoque inválido deve retornar zero linhas;
- a consulta de pedidos por cliente deve retornar o cliente de demonstração;
- a listagem de constraints deve mostrar PK, FK, UNIQUE e CHECK;
- a listagem de índices deve mostrar os índices mínimos;
- `EXPLAIN` deve mostrar o plano da consulta do catálogo.

Consulta principal:

```sql
SELECT
  p.id,
  p.nome,
  p.preco,
  p.estoque,
  c.nome AS categoria
FROM produtos p
JOIN categorias c ON c.id = p.categoria_id
WHERE p.estoque > 0
ORDER BY p.nome;
```

Esta consulta comprova que Produto e Categoria estão ligados corretamente.

### Passo 7 - Testar as travas de segurança dos dados

Abra o arquivo:

[04_testes_constraints.sql](sql/04_testes_constraints.sql)

Execute no banco cloud.

Resultado esperado: mensagens `NOTICE` começando com `OK`.

Esses testes verificam se o banco bloqueia:

- preço negativo;
- estoque negativo;
- item sem pedido válido;
- quantidade inválida;
- preço unitário negativo;
- pedido sem dados básicos do checkout;
- e-mail duplicado.

Se aparecer alguma mensagem começando com `FALHA`, pare e revise o `01_schema.sql`.

### Passo 8 - Guardar a conexão para o Flask

No Bloco 4, a aplicação usará a variável:

```text
DATABASE_URL=postgresql+psycopg://usuario:senha@host:porta/banco
```

A Neon já salvou variáveis em `.env.local`, incluindo `DATABASE_URL`, `DATABASE_URL_UNPOOLED` e `NEON_BRANCH`. Esse arquivo está no `.gitignore` e não deve ser enviado ao GitHub.

Se a string vier como `postgresql://`, ela poderá precisar ser ajustada para `postgresql+psycopg://` no projeto Flask, porque o material usa SQLAlchemy com `psycopg`.

Exemplo didático:

```text
postgresql+psycopg://usuario:senha@host/banco?sslmode=require&channel_binding=require
```

Não publicar a string completa.

## 7. Observações Específicas da Neon

### O que já está configurado

O arquivo [neon.ts](../../neon.ts) está com a configuração mínima:

```ts
import { defineConfig } from "@neon/config/v1";

export default defineConfig({});
```

Isso significa que não estamos ativando serviços extras da Neon. O projeto usa apenas Postgres, coerente com o MVP.

### O que os comandos da Neon fizeram

| Comando | Resultado |
|---|---|
| `neon skills -y` | Instalou instruções locais da Neon para agentes. |
| `neon mcp -y` | Configurou integração local com a Neon. |
| `neon link ...` | Vinculou a pasta `TechStore` ao projeto Neon e à branch `production`. |
| `neon config init` | Criou `neon.ts`. |
| `neon deploy` | Aplicou a configuração; a Neon informou que não havia mudanças pendentes. |

Esses comandos configuram o ambiente. Eles não criam as tabelas do e-commerce. As tabelas serão criadas pelos arquivos SQL deste Bloco 3.

### Conexão

A documentação da Neon mostra conexão Python com variável `.env` e string parecida com:

```text
postgresql://usuario:senha@host/banco?sslmode=require&channel_binding=require
```

Para o projeto com SQLAlchemy/psycopg, use a forma compatível com o material:

```text
postgresql+psycopg://usuario:senha@host/banco?sslmode=require&channel_binding=require
```

## 8. Evidências Para Apresentação

Salvar:

- print das tabelas criadas;
- print dos índices;
- print da consulta de produtos com categoria;
- print da consulta de estoque inválido retornando zero linhas;
- print da listagem de constraints;
- print da listagem de índices;
- print das mensagens `OK` dos testes de constraints;
- print do projeto Neon mostrando nome, região e branch;
- print da área de conexão sem mostrar senha;
- arquivo `01_schema.sql`;
- arquivo `02_seed.sql`;
- arquivo `03_validacao.sql`;
- arquivo `04_testes_constraints.sql`.

## 9. Critérios de Validação do Bloco 3

O Bloco 3 estará concluído quando:

- o banco cloud estiver criado;
- o projeto Neon `techstore-facamp-tai` estiver vinculado à branch `production`;
- as cinco tabelas existirem;
- os campos básicos do checkout existirem em `clientes` e `pedidos`;
- as chaves primárias e estrangeiras estiverem implementadas;
- `NOT NULL`, `UNIQUE` e `CHECK` estiverem aplicados;
- os índices mínimos existirem;
- os dados fictícios estiverem carregados;
- as consultas de validação funcionarem;
- os testes de constraints retornarem `OK`;
- a equipe souber explicar como o banco protege a integridade do MVP.

## 10. Funcionalidade Esperada

Se você executar este bloco corretamente:

- o catálogo do Bloco 4 conseguirá buscar produtos no PostgreSQL;
- o checkout terá tabelas para criar pedido e itens;
- os dados básicos do checkout poderão ser persistidos junto ao cliente e ao pedido;
- a baixa de estoque terá uma regra impedindo valor negativo;
- o histórico de pedidos por cliente poderá ser consultado;
- o banco impedirá dados inválidos mesmo se a aplicação tiver erro;
- haverá evidências objetivas para apresentação.

## 11. Links Oficiais Conferidos

- [PostgreSQL - CREATE TABLE](https://www.postgresql.org/docs/18/sql-createtable.html)
- [PostgreSQL - Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [PostgreSQL - CREATE INDEX](https://www.postgresql.org/docs/current/sql-createindex.html)
- [PostgreSQL - EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html)
- [Neon - Learn the basics](https://neon.com/docs/get-started/signing-up)
- [Neon - Manage projects](https://neon.com/docs/manage/projects)
- [Neon - Connect a Python application to Neon Postgres](https://neon.com/docs/guides/python)
- [SQLAlchemy - PostgreSQL dialect](https://docs.sqlalchemy.org/en/21/dialects/postgresql.html)
