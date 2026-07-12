"""
Lambda: ValidarPedido
Valida a estrutura e as regras de negocio de um pedido de delivery.
Retorna um dicionario com 'valido', 'motivo' e o 'pedido' normalizado.
"""
import json

VALOR_MINIMO = 15.0  # valor minimo do pedido em R$


def lambda_handler(event, context):
    print("Evento recebido:", json.dumps(event, ensure_ascii=False))

    motivos = []

    itens = event.get("itens") or []
    endereco = (event.get("endereco") or "").strip()
    valor_total = float(event.get("valorTotal") or 0)

    if not itens:
        motivos.append("Pedido sem itens.")
    if not endereco:
        motivos.append("Endereco de entrega ausente.")
    if valor_total < VALOR_MINIMO:
        motivos.append(f"Valor total (R$ {valor_total:.2f}) abaixo do minimo de R$ {VALOR_MINIMO:.2f}.")

    valido = len(motivos) == 0

    resultado = {
        "valido": valido,
        "motivo": "OK" if valido else " ".join(motivos),
        "pedido": {
            "pedidoId": event.get("pedidoId"),
            "cliente": event.get("cliente", {}),
            "itens": itens,
            "endereco": endereco,
            "valorTotal": valor_total,
        },
    }

    print("Resultado da validacao:", json.dumps(resultado, ensure_ascii=False))
    return resultado
