# DustBusters/tests/ambientes/test_duas_salas.py

from src.ambientes.ambiente_duas_salas import AmbienteDuasSalas

# Teste para verificar se a inicialização do ambiente está correta
def test_inicializacao():
    amb = AmbienteDuasSalas(sujeira_inicial={"A": True, "B": False})

    assert amb.estado_sujeira["A"] is True
    assert amb.estado_sujeira["B"] is False
    assert amb.estado_objetivo() is False

# Teste para verificar se a percepção de espaço e sujeira está correta
def test_obter_percepcao():
    amb = AmbienteDuasSalas()

    loc, sujo = amb.obter_percepcao("A")
    assert loc == "A"
    assert sujo is True

    loc, sujo = amb.obter_percepcao("B")
    assert loc == "B"
    assert sujo is True

# Verificação da realização da limpeza das salas e se info está correto
def test_limpar_sala():
    amb = AmbienteDuasSalas()

    agente_fake = type("FakeAgente", (), {"posicao": "A"})()

    sucesso, info = amb.executar_acao(agente_fake, "Suck")

    assert sucesso is True
    assert amb.estado_sujeira["A"] is False
    assert info["nova_posicao"] == "A"


# Testes para verificar se as movimentações de A para B e de B para A estão funcionando corretamente
def test_movimento_right():
    amb = AmbienteDuasSalas()
    agente_fake = type("FakeAgente", (), {"posicao": "A"})()

    sucesso, info = amb.executar_acao(agente_fake, "Right")

    assert sucesso is True
    assert info["nova_posicao"] == "B"

def test_movimento_left():
    amb = AmbienteDuasSalas()
    agente_fake = type("FakeAgente", (), {"posicao": "B"})()

    sucesso, info = amb.executar_acao(agente_fake, "Left")

    assert sucesso is True
    assert info["nova_posicao"] == "A"


# Teste para verificar se a identificação do estado objetivo (tudo limpo) está correta
def test_estado_objetivo():
    amb = AmbienteDuasSalas(sujeira_inicial={"A": False, "B": False})
    assert amb.estado_objetivo() is True