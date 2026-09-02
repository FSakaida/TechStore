# Evidência do checkout publicado — 2026-09-02

## Ambiente validado

- Aplicação: `https://techstore-facamp-tai.onrender.com`
- Commit publicado: `e9717ac` — **Adiciona DER e evidências de demonstração**
- Banco: PostgreSQL no Neon, branch `production`
- Dados do checkout: exclusivamente fictícios

## Fluxo executado

1. `POST /api/carrinho/itens/1` retornou **201** e incluiu uma unidade do
   Teclado Mecânico no carrinho de teste.
2. `POST /api/checkout` retornou **201** e informou o pedido **#11**.
3. A consulta posterior confirmou o pedido com status `CRIADO`, total
   `R$ 299,90` e um item de Teclado Mecânico com quantidade `1`.
4. O catálogo publicado passou a mostrar estoque atual de `18` unidades para
   esse produto.
5. `GET /api/carrinho` na mesma sessão retornou carrinho vazio após a
   confirmação.

## Contagens do banco

| Tabela | Antes | Depois |
|---|---:|---:|
| categorias | 2 | 2 |
| clientes | 2 | 3 |
| produtos | 3 | 3 |
| pedidos | 1 | 2 |
| itens_pedido | 2 | 3 |

O aumento de um cliente, pedido e item confirma a persistência do fluxo. A
consulta de detalhe confirmou que o novo pedido recebeu o preço unitário e a
quantidade corretos, enquanto o estoque foi atualizado pela transação.

## Repetição para apresentação

Use as consultas 3b e 4 de `../sql/03_validacao.sql` após um checkout de
demonstração. Não exponha e-mail, endereço, `DATABASE_URL`, cookies ou tokens
em capturas de tela.
