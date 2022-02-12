from pydantic import BaseModel, Field, confloat

from src.models.clients import ClientOptions


class CalculateTaxForeignCurrencyInput(BaseModel):
    """
        Responsável por validar o payload de cálculo de moeda estrangeira.
    """
    cal_en_cliente: ClientOptions = Field(..., alias='segmento')
    cal_vl_moeda_estrangeira: confloat(gt=0.0) = Field(..., alias='quantidade_moeda_estrangeira')
    cal_vl_taxa_conversao: confloat(gt=0.0) = Field(..., alias='taxa_conversao')

    class Config:
        """
            Classe de configuração do esquema.
        """
        allow_population_by_field_name = True
