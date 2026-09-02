# Leia Primeiro - Bloco 3 no Neon

Este bloco deve ser executado diretamente no projeto Neon `techstore-facamp-tai`, vinculado à branch `production`.

A configuração Neon local já foi feita. O próximo passo é criar e validar as tabelas do e-commerce no SQL Editor da Neon.

## Ordem de execução

1. Abra o projeto `techstore-facamp-tai` na Neon.
2. Confirme que a branch selecionada é `production`.
3. Abra o `SQL Editor`.
4. Execute `01_schema.sql`.
5. Execute `02_seed.sql`.
6. Execute `03_validacao.sql`.
7. Execute `04_testes_constraints.sql`.
8. Guarde a `DATABASE_URL` para o Bloco 4.

## Importante

- Não é necessário rodar `CREATE DATABASE` nem `CREATE USER` nos scripts do projeto.
- A Neon já entrega database, usuário, host, porta e senha.
- Execute em um banco vazio. Se uma versão antiga do schema já tiver sido executada, revise antes de repetir o script, porque `CREATE TABLE IF NOT EXISTS` não altera tabelas existentes.
- Use somente dados fictícios.
- Não exponha senha, string completa de conexão nem chaves nos prints.
- `.env.local` contém a conexão do banco e já está no `.gitignore`.
