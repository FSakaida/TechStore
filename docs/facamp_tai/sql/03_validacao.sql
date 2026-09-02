-- Bloco 3 - Consultas de validação
-- Use estas consultas como evidência de que o banco foi criado corretamente.

-- 1. Produtos com categoria para validar catálogo.
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

-- 2. Estoque inválido deve retornar zero linhas.
SELECT *
FROM produtos
WHERE estoque < 0;

-- 3. Pedidos por cliente.
SELECT
  c.id AS cliente_id,
  c.nome,
  c.telefone,
  COUNT(p.id) AS total_pedidos,
  COALESCE(SUM(p.total), 0) AS valor_total
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.id
GROUP BY c.id, c.nome, c.telefone
ORDER BY c.nome;

-- 3b. Estrutura de dados básicos do checkout em pedidos.
SELECT
  id,
  cliente_id,
  status,
  total,
  cep,
  cidade,
  estado,
  endereco,
  numero,
  criado_em
FROM pedidos
ORDER BY id DESC
LIMIT 5;

-- 4. Itens de pedidos registrados.
SELECT
  ip.pedido_id,
  pr.nome AS produto,
  ip.quantidade,
  ip.preco_unitario
FROM itens_pedido ip
JOIN produtos pr ON pr.id = ip.produto_id
ORDER BY ip.pedido_id, pr.nome;

-- 5. Plano de consulta do catálogo.
EXPLAIN
SELECT *
FROM produtos
ORDER BY nome;

-- 6. Constraints criadas no schema público.
SELECT
  tc.table_name,
  tc.constraint_name,
  tc.constraint_type
FROM information_schema.table_constraints tc
WHERE tc.table_schema = 'public'
  AND tc.table_name IN ('clientes', 'categorias', 'produtos', 'pedidos', 'itens_pedido')
ORDER BY tc.table_name, tc.constraint_type, tc.constraint_name;

-- 7. Índices criados no schema público.
SELECT
  tablename,
  indexname,
  indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename IN ('clientes', 'categorias', 'produtos', 'pedidos', 'itens_pedido')
ORDER BY tablename, indexname;
