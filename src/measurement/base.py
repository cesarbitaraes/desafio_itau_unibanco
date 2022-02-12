from pydantic import BaseModel


class MeasurementResult(BaseModel):
    """
        Classe responsável por definir o modelo
        de uma resposta de cálculo de taxa.
    """
    status: int
    value: float
