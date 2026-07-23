"""Testes de sanidade dos artefatos de infraestrutura (ASL e evento de exemplo).

Estes testes protegem contra regressões como JSON corrompido no arquivo da
máquina de estados, garantindo que o pipeline serverless permaneça implantável.
"""

from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def test_asl_e_json_valido_e_bem_formado():
    asl = json.loads((RAIZ / "statemachine" / "delivery-assistant.asl.json").read_text("utf-8"))
    assert asl["StartAt"] == "ValidarPedido"
    assert "ValidarPedido" in asl["States"]
    # Todo estado com "Next" deve apontar para um estado existente.
    estados = asl["States"]
    for nome, estado in estados.items():
        if "Next" in estado:
            assert estado["Next"] in estados, f"{nome} aponta para estado inexistente"


def test_evento_exemplo_e_json_valido():
    evento = json.loads((RAIZ / "events" / "pedido-exemplo.json").read_text("utf-8"))
    assert evento["pedidoId"]
    assert evento["valorTotal"] > 0
