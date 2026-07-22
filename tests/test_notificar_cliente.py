"""Testes da Lambda NotificarCliente (montagem da mensagem e publicação no SNS)."""

from __future__ import annotations

import json
from unittest.mock import MagicMock


def _evento_completo() -> dict:
    return {
        "validacao": {
            "pedido": {"pedidoId": "PED-1042", "cliente": {"nome": "Flávio"}},
        },
        "rota": {"prioridade": "EXPRESS", "sla": "30 min", "taxaEntrega": 12.9},
        "bedrock": {
            "Body": {"content": [{"text": "Seu pedido EXPRESS está a caminho!"}]}
        },
    }


def test_monta_mensagem_com_resposta_do_bedrock(notificar_cliente, monkeypatch):
    monkeypatch.setattr(notificar_cliente, "TOPIC_ARN", "")  # sem SNS, só log
    resultado = notificar_cliente.lambda_handler(_evento_completo(), None)
    assert resultado["status"] == "ROTEADO"
    assert resultado["pedidoId"] == "PED-1042"
    assert resultado["prioridade"] == "EXPRESS"
    assert resultado["sla"] == "30 min"
    assert resultado["respostaCliente"] == "Seu pedido EXPRESS está a caminho!"


def test_usa_fallback_quando_bedrock_ausente(notificar_cliente, monkeypatch):
    monkeypatch.setattr(notificar_cliente, "TOPIC_ARN", "")
    evento = _evento_completo()
    del evento["bedrock"]
    resultado = notificar_cliente.lambda_handler(evento, None)
    assert "confirmado" in resultado["respostaCliente"].lower()


def test_publica_no_sns_quando_topic_arn_definido(notificar_cliente, monkeypatch):
    fake_sns = MagicMock()
    monkeypatch.setattr(notificar_cliente, "sns", fake_sns)
    monkeypatch.setattr(
        notificar_cliente, "TOPIC_ARN", "arn:aws:sns:us-east-1:123456789012:delivery"
    )

    resultado = notificar_cliente.lambda_handler(_evento_completo(), None)

    fake_sns.publish.assert_called_once()
    kwargs = fake_sns.publish.call_args.kwargs
    assert kwargs["TopicArn"] == "arn:aws:sns:us-east-1:123456789012:delivery"
    assert "PED-1042" in kwargs["Subject"]
    corpo = json.loads(kwargs["Message"])
    assert corpo["pedidoId"] == "PED-1042"
    assert resultado["canalNotificacao"] == "SNS"


def test_nao_publica_sem_topic_arn(notificar_cliente, monkeypatch):
    fake_sns = MagicMock()
    monkeypatch.setattr(notificar_cliente, "sns", fake_sns)
    monkeypatch.setattr(notificar_cliente, "TOPIC_ARN", "")

    notificar_cliente.lambda_handler(_evento_completo(), None)

    fake_sns.publish.assert_not_called()
