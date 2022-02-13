import pytest

from fastapi.testclient import TestClient

from src.app import app
from src.utils.database import MigrationType, run_migration
from src.services.database import Session


@pytest.fixture
def web_client():
    client = TestClient(app)
    yield client


@pytest.fixture
def db_client():
    """
    Aplica as migrações para todos os testes.
    Primeiro volta a versão para a inicial e depois
    aplica todas existentes.
    Isto garante que não haverá resquícios de outros
    testes para comprometer os resultados.
    """
    run_migration(MigrationType.downgrade, 'base')
    run_migration(MigrationType.upgrade, 'head')
    session = Session()
    yield session
    session.close()


@pytest.fixture
def valid_fee_post_payload():
    return {
        "segmento": "PRIVATE",
        "tipo_taxa": "MOEDA_ESTRANGEIRA",
        "valor_taxa": 0.10
    }


@pytest.fixture
def another_valid_fee_post_payload():
    return {
        "segmento": "VAREJO",
        "tipo_taxa": "MOEDA_ESTRANGEIRA",
        "valor_taxa": 0.15
    }


@pytest.fixture
def invalid_fee_post_payload():
    return {
        "segmento": "SEGMENTO",
        "tipo_taxa": "MOEDA_ESTRANGEIRA",
        "valor_taxa": 0
    }


@pytest.fixture
def valid_fee_patch_payload():
    return {
        "tipo_taxa": "MOEDA_ESTRANGEIRA",
        "valor_taxa": 0.2
    }


@pytest.fixture
def invalid_fee_patch_payload():
    return {
        "tipo_taxa": "SEGMENTO",
        "valor_taxa": 0
    }


@pytest.fixture
def valid_calculate_foreign_currency_post_payload():
    return {
        "segmento": "PRIVATE",
        "quantidade_moeda_estrangeira": 1000,
        "taxa_conversao": 5.46
    }


@pytest.fixture
def invalid_calculate_foreign_currency_post_payload():
    return {
        "segmento": "PRIVATE",
        "quantidade_moeda_estrangeira": 0,
        "taxa_conversao": 0
    }


@pytest.fixture
def unregistered_fee_calculate_foreign_currency_post_payload():
    return {
        "segmento": "VAREJO",
        "quantidade_moeda_estrangeira": 1500,
        "taxa_conversao": 5.46
    }
