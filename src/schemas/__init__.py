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
