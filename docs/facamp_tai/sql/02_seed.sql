-- Bloco 3 - Carga inicial de dados
-- Dados fictícios para demonstrar catálogo, carrinho, pedido e estoque.
-- Já executado na base Neon!
INSERT INTO categorias (nome)
VALUES
  ('Tecnologia'),
  ('Acessórios')
ON CONFLICT (nome) DO NOTHING;

INSERT INTO clientes (nome, email, telefone, senha_hash)
VALUES
  ('Cliente Demonstração', 'cliente.demo@facamp.local', '(11) 99999-9999', 'hash_demonstrativo_nao_usar_em_producao')
ON CONFLICT (email) DO NOTHING;

INSERT INTO produtos (nome, descricao, preco, estoque, categoria_id)
SELECT 'Teclado Mecânico', 'Switches táteis', 299.90, 20, c.id
FROM categorias c
WHERE c.nome = 'Tecnologia'
  AND NOT EXISTS (
    SELECT 1 FROM produtos p WHERE p.nome = 'Teclado Mecânico'
  );

INSERT INTO produtos (nome, descricao, preco, estoque, categoria_id)
SELECT 'Mouse Sem Fio', 'Sensor óptico', 149.90, 35, c.id
FROM categorias c
WHERE c.nome = 'Tecnologia'
  AND NOT EXISTS (
    SELECT 1 FROM produtos p WHERE p.nome = 'Mouse Sem Fio'
  );

INSERT INTO produtos (nome, descricao, preco, estoque, categoria_id)
SELECT 'Suporte para Notebook', 'Base ajustável', 89.90, 15, c.id
FROM categorias c
WHERE c.nome = 'Acessórios'
  AND NOT EXISTS (
    SELECT 1 FROM produtos p WHERE p.nome = 'Suporte para Notebook'
  );
