"""
    Modelos para validação de payloads com dados de endereço
"""
from datetime import datetime

from pydantic import BaseModel, Field, confloat
from typing import List

from src.models.clients import ClientOptions, TaxType


class FeeInput(BaseModel):
    """
        Responsável por validar o payload de registro de taxa.
    """
    tax_en_cliente: ClientOptions = Field(..., alias='segmento')
    tax_en_tipo: TaxType = Field(..., alias='tipo_taxa')
    tax_vl_valor: confloat(gt=0.0) = Field(..., alias='valor_taxa')

    class Config:
        """
            Classe de configuração do esquema.
        """
        allow_population_by_field_name = True


class FeeUpdate(BaseModel):
    """
        Responsável por validar o payload de atualização de taxa.
    """
    tax_en_tipo: TaxType = Field(..., alias='tipo_taxa')
    tax_vl_valor: confloat(gt=0.0) = Field(..., alias='valor_taxa')


class FeeOutput(BaseModel):
    """
        Responsável por validar o payload de retorno de taxa.
    """
    tax_pk_taxa: int = Field(..., alias='id')
    tax_en_cliente: ClientOptions = Field(..., alias='segmento')
    tax_en_tipo: TaxType = Field(..., alias='tipo_taxa')
    tax_vl_valor: confloat(gt=0.0) = Field(..., alias='valor_taxa')
    tax_dt_criacao: datetime = Field(..., alias='data_criacao')
    tax_dt_atualizacao: datetime = Field(None, alias='data_atualizacao')

    class Config:
        """
            Classe de configuração.
        """
        orm_mode = True
        allow_population_by_field_name = True


class FeeList(BaseModel):
    """
        Esquema utilizado para formatar e retornar
        todas taxas configurados no sistema.
    """
    fees: List[FeeOutput]

    class Config:
        """
            Classe de configuração.
        """
        orm_mode = True
        allow_population_by_field_name = True
