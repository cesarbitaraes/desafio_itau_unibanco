"""
    Modulo responsavel pela incialização do sistema.
"""

from fastapi import FastAPI

from src.utils.database import MigrationType, run_migration

from src.resources.healthcheck import router as healthcheck_router


app = FastAPI(title="desafio-itau", version="0.0.1", openapi_url='/swagger.json')
app.include_router(healthcheck_router, prefix="/api", tags=["healthcheck"])


@app.on_event('startup')
async def setup_application():
    """
    Rotinas executadas quando a aplicação é iniciada.

    :return: None
    """
    try:
        # Executa as migrações.
        run_migration(MigrationType.upgrade, 'head')

    except Exception as error:
        print(f'Exceção ao iniciar: {error}')
