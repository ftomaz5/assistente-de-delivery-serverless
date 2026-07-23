"""Testes da Lambda ValidarPedido (regras de negócio da validação de pedidos)."""

from __future__ import annotations


def _evento_valido() -> dict:
    return {
        "pedidoId": "PED-1",
        "cliente": {"nome": "Ana"},
        "itens": [{"nome": "Pizza", "quantidade": 1, "preco": 50.0}],
        "endereco": "Rua A, 100",
        "valorTotal": 50.0,
    }


def test_pedido_valido_retorna_ok(validar_pedido):
    resultado = validar_pedido.lambda_handler(_evento_valido(), None)
    assert resultado["valido"] is True
    assert resultado["motivo"] == "OK"
    assert resultado["pedido"]["pedidoId"] == "PED-1"
    assert resultado["pedido"]["valorTotal"] == 50.0


def test_pedido_sem_itens_e_invalido(validar_pedido):
    evento = _evento_valido()
    evento["itens"] = []
    resultado = validar_pedido.lambda_handler(evento, None)
    assert resultado["valido"] is False
    assert "sem itens" in resultado["motivo"].lower()


def test_pedido_sem_endereco_e_invalido(validar_pedido):
    evento = _evento_valido()
    evento["endereco"] = "   "
    resultado = validar_pedido.lambda_handler(evento, None)
    assert resultado["valido"] is False
    assert "endereco" in resultado["motivo"].lower()


def test_valor_abaixo_do_minimo_e_invalido(validar_pedido):
    evento = _evento_valido()
    evento["valorTotal"] = 10.0
    resultado = validar_pedido.lambda_handler(evento, None)
    assert resultado["valido"] is False
    assert "minimo" in resultado["motivo"].lower()


def test_valor_exatamente_no_minimo_e_valido(validar_pedido):
    evento = _evento_valido()
    evento["valorTotal"] = validar_pedido.VALOR_MINIMO
    resultado = validar_pedido.lambda_handler(evento, None)
    assert resultado["valido"] is True


def test_multiplos_motivos_sao_concatenados(validar_pedido):
    resultado = validar_pedido.lambda_handler({}, None)
    assert resultado["valido"] is False
    # Deve reportar itens ausentes, endereço ausente e valor abaixo do mínimo.
    assert resultado["motivo"].count(".") >= 3


def test_valor_total_ausente_vira_zero(validar_pedido):
    evento = _evento_valido()
    del evento["valorTotal"]
    resultado = validar_pedido.lambda_handler(evento, None)
    assert resultado["pedido"]["valorTotal"] == 0.0
    assert resultado["valido"] is False
