# Desafio de Extensão: Login e Histórico do Cliente

## 1. Fonte do desafio

O desafio foi extraído do HTML complementar `facamp_tai_ecommerce_postgresql_animacao_interativa_v3.html`, seção "Desafios de extensão".

| Item | Exigência |
|---|---|
| Tema | Autenticação e histórico do cliente |
| Funcionalidades | Login, logout e área "Meus pedidos" |
| Banco | Usar `senha_hash` e garantir e-mail único |
| Código | Criar sessão autenticada, proteger rotas e consultar pedidos do usuário logado |
| Teste | Login válido/inválido e histórico filtrado pelo cliente correto |

## 2. Decisão de implementação

A extensão foi implementada sem alteração no schema do banco. O modelo existente já possui `clientes.email UNIQUE`, `clientes.senha_hash`, `pedidos.cliente_id` e os relacionamentos com `itens_pedido`.

Clientes criados anteriormente pelo checkout podem usar a tela de cadastro para definir senha no mesmo e-mail.

## 3. Funcionalidades entregues

| Rota | Função |
|---|---|
| `/cadastro` | Cria cliente ou define senha para e-mail já existente |
| `/login` | Autentica cliente por e-mail e senha |
| `/logout` | Encerra sessão autenticada |
| `/meus-pedidos` | Mostra apenas pedidos do cliente logado |
| `/alterar-senha` | Altera senha após validar a senha atual |

## 4. Validação realizada

| Critério | Resultado |
|---|---|
| Login inválido recusado | OK |
| Login válido aceito | OK |
| Rota protegida sem login redireciona para `/login` | OK |
| Histórico mostra pedido do cliente correto | OK |
| Alteração de senha valida senha atual | OK |
| Nova senha permite login posterior | OK |
| Testes preservam o banco com rollback | OK |

## 5. Observação de escopo

Esta extensão atende ao desafio escolhido, mas não transforma o MVP em autenticação completa de produção. Permanecem fora do escopo: recuperação de senha por e-mail, confirmação de e-mail, autenticação multifator, rate limit e painel administrativo.
