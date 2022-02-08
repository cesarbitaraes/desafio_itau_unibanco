"""
    Modelos gerais de resposta.
"""
from typing import Optional, List, Union

from pydantic import BaseModel


class Message(BaseModel):
    """
    Classe utilizada para retornos simples
    """
    message: str


class ErrorMessage(BaseModel):
    """
    Classe utilizada para formatar as respostas de erro.
    """
    message: str
    details: Optional[Union[str, List]]


# Respostas básicas retornadas pelos endpoints
basic_error_responses = {
    400: {
        "model": ErrorMessage,
        "description": "Invalid request.",
    },
    401: {
        "model": ErrorMessage,
        "description": "Unauthorized request."
    },
    404: {
        "model": ErrorMessage,
        "description": "Resource not found."
    },
    500: {
        "model": ErrorMessage,
        "description": "Unexpected system error."
    },
    502: {
        "model": ErrorMessage,
        "description": "The provider returned an error."
    }
}
