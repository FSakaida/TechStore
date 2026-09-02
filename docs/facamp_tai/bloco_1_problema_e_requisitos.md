# Bloco 1 - Problema e Requisitos

Projeto: aplicação e banco de dados de e-commerce com PostgreSQL e Python/Flask.

## Fontes

- HTML inicial - Etapas do projeto de e-commerce: Bloco 1, slides 6 a 11.
- HTML prático - E-commerce com Python e PostgreSQL: slides 4 a 6.
- HTML conceitual - SQL e NoSQL: apoio para justificar integridade, persistência e escolha tecnológica.

## 1. Escopo da Etapa

Esta etapa define o problema de negócio, os atores, os requisitos funcionais e não funcionais, o backlog inicial, o fluxo do processo e os critérios de aceite do MVP.

O fluxo principal do projeto é:

```text
catálogo -> carrinho -> checkout -> pedido -> atualização de estoque
```

Ficam fora do MVP: pagamento real, autenticação completa, integração logística/frete/rastreamento, uso obrigatório de NoSQL e interface visual sofisticada.

O MVP poderá registrar telefone do cliente e endereço básico do pedido, apenas como dados informados no checkout, sem implementar logística.

## 2. Problema

Como estruturar uma aplicação de e-commerce simples que permita listar produtos, montar carrinho e concluir pedidos, garantindo integridade entre cliente, produtos, pedidos, itens do pedido e estoque?

## 3. Objetivo do MVP

Construir e publicar uma aplicação web em Python/Flask conectada ao PostgreSQL, capaz de exibir produtos, registrar carrinho, finalizar pedido, persistir os dados da compra e atualizar o estoque de forma consistente.

## 4. Atores

| Ator | Necessidade |
|---|---|
| Cliente | Consultar produtos, montar carrinho, informar dados básicos do checkout e finalizar pedido. |
| Administrador/Operação | Controlar estoque, pedidos e clientes. |
| Gestão | Obter visão básica de vendas, pedidos e produtos. |
| TI/Desenvolvimento | Implementar, testar e publicar a solução com escopo controlado. |

## 5. Requisitos Funcionais

| ID | Requisito | Critério de aceite |
|---|---|---|
| RF01 | Listar produtos disponíveis. | O catálogo exibe produtos cadastrados no PostgreSQL com nome, preço, categoria e estoque. |
| RF02 | Adicionar produto ao carrinho. | Apenas produtos existentes podem ser adicionados; a quantidade deve ser positiva. |
| RF03 | Visualizar carrinho e total. | O carrinho apresenta itens, quantidades, preços e total calculado corretamente. |
| RF04 | Finalizar pedido. | O sistema cria pedido e itens do pedido a partir do carrinho e dos dados básicos informados no checkout. |
| RF05 | Atualizar estoque. | A quantidade comprada é abatida do estoque; o estoque não pode ficar negativo. |
| RF06 | Registrar cliente e histórico de pedidos. | Cada pedido fica associado a um cliente e pode ser consultado posteriormente. |

## 6. Requisitos Não Funcionais

| Categoria | Requisito |
|---|---|
| Integridade | O banco deve impedir preço negativo, estoque negativo, quantidade inválida e registros sem relacionamento obrigatório. |
| Segurança | Credenciais devem ficar fora do código; senhas, quando usadas, devem ser armazenadas como hash. |
| Disponibilidade | A aplicação e o banco devem estar disponíveis em ambiente cloud para demonstração. |
| Desempenho | Devem existir índices mínimos para catálogo, pedidos por cliente e itens por pedido. |
| Manutenibilidade | A estrutura do projeto deve ser simples, documentada e coerente com o projeto-base. |
| Portabilidade | O mesmo código deve funcionar localmente e em cloud por meio de variáveis de ambiente. |

## 7. Backlog Inicial

| Prioridade | Item |
|---|---|
| P0 | Definir escopo, atores, RFs, RNFs e fluxo principal. |
| P0 | Validar escopo e fluxo principal com professor/equipe. |
| P0 | Modelar Cliente, Categoria, Produto, Pedido e ItemPedido. |
| P0 | Criar PostgreSQL com tabelas, constraints, índices mínimos e dados iniciais. |
| P0 | Implementar catálogo, carrinho e checkout no Flask. |
| P0 | Garantir atualização de estoque com commit/rollback. |
| P0 | Registrar testes e evidências. |
| P0 | Publicar repositório, banco e aplicação em cloud. |
| P1 | Refinar README, dicionário de dados e justificativa técnica. |
| P2 | Avaliar extensões somente após o MVP estar completo. |

## 8. Fluxo do Processo

```text
1. Cliente acessa o catálogo.
2. Sistema lista produtos disponíveis.
3. Cliente adiciona produto ao carrinho.
4. Sistema atualiza carrinho e total.
5. Cliente finaliza pedido.
6. Sistema valida dados do checkout, produtos, quantidades e estoque.
7. Sistema cria pedido e itens do pedido.
8. Sistema atualiza estoque.
9. Sistema confirma a compra ou desfaz a operação em caso de erro.
```

## 9. Artefatos da Etapa

- Documento de escopo.
- Requisitos funcionais e não funcionais.
- Backlog inicial priorizado.
- Fluxo principal do processo.
- Critérios de aceite.
- Lista de itens fora do MVP.

## 10. Validação da Etapa

Esta etapa estará concluída quando:

- o problema e o objetivo do MVP estiverem definidos;
- os atores estiverem identificados;
- RF01 a RF06 estiverem documentados;
- os requisitos não funcionais estiverem registrados;
- o fluxo de compra estiver descrito;
- o backlog inicial estiver priorizado;
- os critérios de aceite estiverem claros;
- o grupo souber explicar o que ficou fora do MVP.
- o escopo estiver validado com professor/equipe antes da modelagem.

## 11. Encaminhamento Para o Bloco 2

Os requisitos aprovados serão convertidos em entidades, atributos, relacionamentos, cardinalidades e regras de integridade.

| Requisito | Consequência na modelagem |
|---|---|
| Cliente finaliza pedido. | Criar Cliente e Pedido. |
| Pedido possui produtos. | Criar ItemPedido. |
| Produto pertence a categoria. | Criar Categoria e relacioná-la a Produto. |
| Estoque deve ser atualizado. | Produto precisa de campo `estoque` e regra de não negativo. |
| Histórico deve ser consultável. | Pedido precisa estar associado a Cliente. |
| Checkout coleta telefone e endereço básico. | Cliente recebe `telefone`; Pedido recebe dados básicos de entrega. |
