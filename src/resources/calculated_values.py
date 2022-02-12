from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.measurement.measurement import Measurement
from src.services.database import get_conn, Session
from src.schemas.measurement import CalculateTaxForeignCurrencyInput

router = APIRouter()


@router.post("/", status_code=200)
async def calculate_tax_foreign_currency(calc_payload: CalculateTaxForeignCurrencyInput,
                                         conn: Session = Depends(get_conn)):
    """
    Função responsável por fazer a conversão de uma moeda estrangeira
    para reais.
    :param calc_payload: Payload de entrada.
    :param conn: Conexão com o banco de dados.
    :return: JSON indicando o status e o valor da conversão, em caso
    de sucesso, ou uma mensagem de erro.
    """
    valor_reais = Measurement().foreign_currency(calc_payload, conn)
    if valor_reais.status == 200:
        return JSONResponse(
            status_code=valor_reais.status,
            content=f'Valor da conversão em reais: R$ {valor_reais.value}.'
        )
    return JSONResponse(
        status_code=404,
        content='Não existe taxa cadastrada para esse segmento.'
    )
