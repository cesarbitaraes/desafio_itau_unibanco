from unittest.mock import patch

from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError


def test_get_healthcheck_successfully(db_client, web_client):

    result = web_client.get("/api/healthcheck")
    body = result.json()

    assert result.status_code == 200
    assert body.get("message") == "Everything is fine!"


def test_get_healthcheck_with_database_error(web_client):
    with patch.object(Session, 'query', side_effect=SQLAlchemyError):
        result = web_client.get("/api/healthcheck")
        body = result.json()

        assert result.status_code == 500
        assert "message" in body
        assert "details" in body
        assert body.get("message") == "SQLAlchemy retornou um erro."
