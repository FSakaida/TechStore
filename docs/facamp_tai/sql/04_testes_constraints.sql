-- Bloco 3 - Testes de constraints
-- Execute depois de 01_schema.sql e 02_seed.sql.
-- O resultado esperado são mensagens NOTICE iniciadas por "OK".

DO $$
DECLARE
  v_categoria_id INTEGER;
  v_cliente_id INTEGER;
  v_produto_id INTEGER;
  v_pedido_id INTEGER;
BEGIN
  SELECT id INTO v_categoria_id FROM categorias ORDER BY id LIMIT 1;
  SELECT id INTO v_cliente_id FROM clientes ORDER BY id LIMIT 1;
  SELECT id INTO v_produto_id FROM produtos ORDER BY id LIMIT 1;

  IF v_categoria_id IS NULL OR v_cliente_id IS NULL OR v_produto_id IS NULL THEN
    RAISE NOTICE 'Execute 02_seed.sql antes deste arquivo.';
    RETURN;
  END IF;

  INSERT INTO pedidos (
    cliente_id,
    status,
    total,
    cep,
    cidade,
    estado,
    endereco,
    numero
  )
  VALUES (
    v_cliente_id,
    'CRIADO',
    0,
    '13000-000',
    'Campinas',
    'SP',
    'Rua Demonstração',
    '100'
  )
  RETURNING id INTO v_pedido_id;

  BEGIN
    INSERT INTO produtos (nome, descricao, preco, estoque, categoria_id)
    VALUES ('Produto Preço Inválido', 'Teste', -1.00, 10, v_categoria_id);
    RAISE NOTICE 'FALHA: preço negativo foi aceito.';
  EXCEPTION WHEN check_violation THEN
    RAISE NOTICE 'OK: preço negativo foi bloqueado.';
  END;

  BEGIN
    INSERT INTO produtos (nome, descricao, preco, estoque, categoria_id)
    VALUES ('Produto Estoque Inválido', 'Teste', 10.00, -5, v_categoria_id);
    RAISE NOTICE 'FALHA: estoque negativo foi aceito.';
  EXCEPTION WHEN check_violation THEN
    RAISE NOTICE 'OK: estoque negativo foi bloqueado.';
  END;

  BEGIN
    INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario)
    VALUES (999999, v_produto_id, 1, 10.00);
    RAISE NOTICE 'FALHA: item sem pedido válido foi aceito.';
  EXCEPTION WHEN foreign_key_violation THEN
    RAISE NOTICE 'OK: item sem pedido válido foi bloqueado.';
  END;

  BEGIN
    INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario)
    VALUES (v_pedido_id, v_produto_id, 0, 10.00);
    RAISE NOTICE 'FALHA: quantidade inválida foi aceita.';
  EXCEPTION WHEN check_violation THEN
    RAISE NOTICE 'OK: quantidade inválida foi bloqueada.';
  END;

  BEGIN
    INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario)
    VALUES (v_pedido_id, v_produto_id, 1, -10.00);
    RAISE NOTICE 'FALHA: preço unitário negativo foi aceito.';
  EXCEPTION WHEN check_violation THEN
    RAISE NOTICE 'OK: preço unitário negativo foi bloqueado.';
  END;

  BEGIN
    INSERT INTO pedidos (cliente_id, status, total)
    VALUES (v_cliente_id, 'CRIADO', 0);
    RAISE NOTICE 'FALHA: pedido sem dados básicos do checkout foi aceito.';
  EXCEPTION WHEN not_null_violation THEN
    RAISE NOTICE 'OK: pedido sem dados básicos do checkout foi bloqueado.';
  END;

  BEGIN
    INSERT INTO clientes (nome, email, telefone, senha_hash)
    VALUES ('Cliente Duplicado', 'cliente.demo@facamp.local', '(11) 98888-8888', 'hash_teste');
    RAISE NOTICE 'FALHA: e-mail duplicado foi aceito.';
  EXCEPTION WHEN unique_violation THEN
    RAISE NOTICE 'OK: e-mail duplicado foi bloqueado.';
  END;

  DELETE FROM pedidos WHERE id = v_pedido_id;
END $$;
