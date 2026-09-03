import re

from werkzeug.security import check_password_hash, generate_password_hash

from models import Cliente


class AuthError(ValueError):
    pass


def normalizar_email(email):
    if not isinstance(email, str) or not email.strip():
        raise AuthError("Informe o e-mail.")

    email = email.strip().lower()
    if len(email) > 160 or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        raise AuthError("Informe um e-mail válido.")
    return email


def validar_senha(senha, campo="senha"):
    if not isinstance(senha, str) or not senha:
        raise AuthError(f"Informe a {campo}.")
    if len(senha) < 6:
        raise AuthError("A senha deve ter pelo menos 6 caracteres.")
    if len(senha) > 72:
        raise AuthError("A senha deve ter no máximo 72 caracteres.")
    return senha


def texto_obrigatorio(valor, campo, limite):
    if not isinstance(valor, str) or not valor.strip():
        raise AuthError(f"Informe {campo}.")

    valor = " ".join(valor.split())
    if len(valor) > limite:
        raise AuthError(f"{campo.capitalize()} deve ter no máximo {limite} caracteres.")
    return valor


def autenticar_cliente(email, senha, sessao):
    email = normalizar_email(email)
    if not isinstance(senha, str) or not senha:
        raise AuthError("Informe a senha.")

    cliente = sessao.query(Cliente).filter(Cliente.email == email).one_or_none()
    if cliente is None or not check_password_hash(cliente.senha_hash, senha):
        raise AuthError("E-mail ou senha inválidos.")
    return cliente


def cadastrar_ou_atualizar_cliente(dados, sessao):
    nome = texto_obrigatorio(dados.get("nome"), "nome", 120)
    email = normalizar_email(dados.get("email"))
    telefone = texto_obrigatorio(dados.get("telefone"), "telefone", 20)
    senha = validar_senha(dados.get("senha"))
    confirmar_senha = dados.get("confirmar_senha")

    if senha != confirmar_senha:
        raise AuthError("As senhas não conferem.")

    cliente = sessao.query(Cliente).filter(Cliente.email == email).one_or_none()
    if cliente is None:
        cliente = Cliente(nome=nome, email=email, telefone=telefone)
        sessao.add(cliente)
    else:
        cliente.nome = nome
        cliente.telefone = telefone

    cliente.senha_hash = generate_password_hash(senha)
    sessao.flush()
    return cliente


def alterar_senha_cliente(cliente, senha_atual, nova_senha, confirmar_senha):
    if not check_password_hash(cliente.senha_hash, senha_atual or ""):
        raise AuthError("Senha atual inválida.")

    nova_senha = validar_senha(nova_senha, "nova senha")
    if nova_senha != confirmar_senha:
        raise AuthError("As senhas não conferem.")

    cliente.senha_hash = generate_password_hash(nova_senha)
