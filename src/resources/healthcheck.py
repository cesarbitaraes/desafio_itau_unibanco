"""
    Implementação da rota de healthcheck

"""
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.services.database import get_conn, Session
from src.schemas import ErrorMessage, Message

router = APIRouter()


@router.get("/healthcheck", responses={
    200: {"model": Message},
    500: {"model": ErrorMessage}
})
async def run_healthcheck(conn: Session = Depends(get_conn)):
    """
    Make sure that all the internal and dependent systems are up and healthy.

    :param conn: Conexão com o banco de dados.
    :return: Status da API.
    """
    try:
        conn.query().from_statement(text("SELECT 1"))
        return JSONResponse(status_code=200, content=dict(message="Everything is fine!"))
    except SQLAlchemyError as error:
        return JSONResponse(
            status_code=500,
            content=dict(
                message="SQLAlchemy returned an error.",
                details=" ".join(error.args)
            ))
