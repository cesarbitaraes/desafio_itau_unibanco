import datetime

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.models.fees import Taxas
from src.services.database import get_conn, Session
from src.schemas.fee import FeeInput, FeeUpdate, FeeList

router = APIRouter()


@router.get("/", status_code=200, response_model=FeeList)
async def get_all_fees(conn: Session = Depends(get_conn)):
    """
    Retorna todas as taxas cadastradas no sistema.
    :param conn: Conexão com o banco de dados.
    :return: Objeto FeeList que contém todas as taxas.
    """

    all_fees = Taxas.obtem_todas_taxas(conn)
    return FeeList(fees=all_fees)


@router.post("/", status_code=200)
async def create_fees(fee_payload: FeeInput, conn: Session = Depends(get_conn)):
    """
    Cria e armazena uma noxa taxa.
    :param fee_payload: Payload de entrada.
    :param conn: Conexão com o banco de dados.
    :return: JSON indicando sucesso ou falha operação.
    """
    segmento = fee_payload.tax_en_cliente.name
    tipo_taxa = fee_payload.tax_en_tipo.name
    taxa_cadastrada = Taxas.obtem_taxa_por_cliente_e_tipo(db_session=conn,
                                                          cliente=segmento,
                                                          tipo=tipo_taxa)
    if taxa_cadastrada:
        return JSONResponse(
            status_code=404,
            content=f'Já existe uma taxa cadastrada para o segmento {segmento}.'
        )
    nova_taxa = Taxas(tax_en_cliente=segmento,
                      tax_en_tipo=tipo_taxa,
                      tax_vl_valor=fee_payload.tax_vl_valor)

    saved, nova_taxa = nova_taxa.save(conn)
    if not saved:
        return JSONResponse(
            status_code=500,
            content="Ocorreu um erro ao salvar a taxa."
        )

    return JSONResponse(
            status_code=200,
            content=f'Taxa para o segmento {segmento} foi criada com sucesso.'
        )


@router.patch("/{fee_id}", status_code=200)
async def update_fees(fee_id: int, fee_payload: FeeUpdate, conn: Session = Depends(get_conn)):
    """
    Função responsável por atualizar uma taxa previamente registrada
    no sistema.
    :param fee_id: Identificação única da taxa.
    :param fee_payload: Payload de entrada.
    :param conn: Conexão com o banco de dados.
    :return: JSON indicando sucesso ou falha operação.
    """
    taxa_cadastrada = Taxas.obtem_taxa_por_id(db_session=conn,
                                              id=fee_id)
    if not taxa_cadastrada:
        return JSONResponse(
            status_code=404,
            content="Taxa não encontrada."
        )
    taxa_cadastrada.tax_dt_atualizacao = datetime.datetime.now()

    updated, nova_taxa = taxa_cadastrada.update(conn, **fee_payload.dict())

    if not updated:
        print(nova_taxa)
        return JSONResponse(
            status_code=500,
            content="Ocorreu um erro ao salvar a taxa."
        )

    return JSONResponse(
            status_code=200,
            content=f'Nova taxa para o segmento {taxa_cadastrada.tax_en_cliente.name} atualizada com sucesso: '
                    f'{fee_payload.tax_vl_valor}.'
        )
