# Evidências da demonstração

Esta pasta reúne o roteiro e os registros sem credenciais da validação final do
MVP. Use apenas dados fictícios durante o checkout de demonstração.

## Roteiro mínimo

1. Execute `flask --app app check-db` e registre as contagens iniciais.
2. Abra a URL publicada e mostre o catálogo com preço e estoque.
3. Adicione um produto, altere sua quantidade e mostre o total do carrinho.
4. Finalize um único pedido com nome e e-mail fictícios.
5. Registre a tela de sucesso, o número do pedido e as contagens posteriores.
6. Execute as consultas 3b e 4 de `../sql/03_validacao.sql` para mostrar o
   pedido, seus itens e o estoque atualizado.

## Cuidados com as capturas

- Não mostre `DATABASE_URL`, cookies, tokens, senhas ou dados pessoais reais.
- Registre o nome do produto, a quantidade e o número do pedido, mas não a
  string de conexão do Neon.
- Guarde a consulta SQL utilizada ao lado da captura para que a evidência seja
  reproduzível.

O registro do teste final publicado ficará neste diretório após sua execução.
