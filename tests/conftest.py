"""Configuração compartilhada dos testes.

As duas funções Lambda vivem em ``src/<funcao>/lambda_function.py`` e têm o mesmo
nome de módulo. Para conseguir importá-las lado a lado (sem colisão de nome no
``sys.modules``) carregamos cada arquivo explicitamente via ``importlib`` e o
expomos como uma fixture.
"""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
from types import ModuleType

import pytest

# Região fictícia para que ``boto3.client(...)`` criado no import não exploda.
os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")

SRC = Path(__file__).resolve().parent.parent / "src"


def _carregar_modulo(nome: str, caminho: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(nome, caminho)
    assert spec and spec.loader, f"Não foi possível carregar {caminho}"
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


@pytest.fixture()
def validar_pedido() -> ModuleType:
    """Módulo da Lambda ValidarPedido, recarregado a cada teste."""
    return _carregar_modulo("validar_pedido_fn", SRC / "validar_pedido" / "lambda_function.py")


@pytest.fixture()
def notificar_cliente() -> ModuleType:
    """Módulo da Lambda NotificarCliente, recarregado a cada teste."""
    return _carregar_modulo(
        "notificar_cliente_fn", SRC / "notificar_cliente" / "lambda_function.py"
    )
