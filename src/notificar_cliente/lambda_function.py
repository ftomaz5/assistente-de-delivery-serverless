"""
Lambda: NotificarCliente
Monta a confirmacao final e publica no topico SNS.
Recebe o estado completo do fluxo (pedido, rota e resposta do Bedrock).
"""
import json
import os

import boto3

sns = boto3.client("sns")
TOPIC_ARN = os.environ.get("TOPIC_ARN", "")


def _extrair_resposta_bedrock(event):
    """Extrai o texto gerado pelo Bedrock de forma tolerante a falhas."""
    try:
        return event["bedrock"]["Body"]["content"][0]["text"]
    except (KeyError, IndexError, TypeError):
        return "Seu pedido foi confirmado e ja esta sendo preparado!"


def lambda_handler(event, context):
    print("Evento recebido:", json.dumps(event, ensure_ascii=False))

    pedido = event.get("validacao", {}).get("pedido", {})
    rota = event.get("rota", {})
    resposta_cliente = _extrair_resposta_bedrock(event)

    mensagem = {
        "status": "ROTEADO",
        "pedidoId": pedido.get("pedidoId"),
        "prioridade": rota.get("prioridade"),
        "sla": rota.get("sla"),
        "respostaCliente": resposta_cliente,
        "canalNotificacao": "SNS",
    }

    if TOPIC_ARN:
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject=f"Pedido {pedido.get('pedidoId')} confirmado",
            Message=json.dumps(mensagem, ensure_ascii=False),
        )
        print("Notificacao publicada no SNS.")
    else:
        print("TOPIC_ARN nao configurado - notificacao apenas em log.")

    return mensagem
