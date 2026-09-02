-- Bloco 3 - Estrutura física do banco
-- Baseado no Bloco 2: Cliente, Categoria, Produto, Pedido e ItemPedido.
-- Já executado na base de dados do Neon!
CREATE TABLE IF NOT EXISTS categorias (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS clientes (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(120) NOT NULL,
  email VARCHAR(160) NOT NULL UNIQUE,
  telefone VARCHAR(20) NOT NULL,
  senha_hash VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS produtos (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(140) NOT NULL,
  descricao TEXT,
  preco NUMERIC(10,2) NOT NULL CHECK (preco >= 0),
  estoque INTEGER NOT NULL DEFAULT 0 CHECK (estoque >= 0),
  categoria_id INTEGER NOT NULL REFERENCES categorias(id)
);

CREATE TABLE IF NOT EXISTS pedidos (
  id SERIAL PRIMARY KEY,
  cliente_id INTEGER NOT NULL REFERENCES clientes(id),
  status VARCHAR(30) NOT NULL DEFAULT 'CRIADO',
  total NUMERIC(10,2) NOT NULL DEFAULT 0 CHECK (total >= 0),
  cep VARCHAR(12) NOT NULL,
  cidade VARCHAR(100) NOT NULL,
  estado CHAR(2) NOT NULL,
  endereco VARCHAR(180) NOT NULL,
  numero VARCHAR(20) NOT NULL,
  criado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS itens_pedido (
  id SERIAL PRIMARY KEY,
  pedido_id INTEGER NOT NULL REFERENCES pedidos(id) ON DELETE CASCADE,
  produto_id INTEGER NOT NULL REFERENCES produtos(id),
  quantidade INTEGER NOT NULL CHECK (quantidade > 0),
  preco_unitario NUMERIC(10,2) NOT NULL CHECK (preco_unitario >= 0)
);

CREATE INDEX IF NOT EXISTS idx_produtos_nome
  ON produtos(nome);

CREATE INDEX IF NOT EXISTS idx_pedidos_cliente
  ON pedidos(cliente_id);

CREATE INDEX IF NOT EXISTS idx_itens_pedido
  ON itens_pedido(pedido_id);
