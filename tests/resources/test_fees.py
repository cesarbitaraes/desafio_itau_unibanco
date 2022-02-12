import unittest.mock

from src.models.fees import Taxas


def test_post_fee_with_success(web_client,
                               db_client,
                               valid_fee_post_payload):
    result = web_client.post("/fees/", json=valid_fee_post_payload)
    body = result.json()

    assert result.status_code == 200
    assert body == 'Taxa para o segmento PRIVATE foi criada com sucesso.'


def test_post_fee_with_invalid_payload(web_client,
                                       db_client,
                                       invalid_fee_post_payload):
    result = web_client.post("/fees/", json=invalid_fee_post_payload)
    body = result.json()

    assert result.status_code == 422


def test_post_fee_already_registered(web_client,
                                     db_client,
                                     valid_fee_post_payload):
    web_client.post("/fees/", json=valid_fee_post_payload)
    result = web_client.post("/fees/", json=valid_fee_post_payload)
    body = result.json()

    assert result.status_code == 404
    assert body == 'Já existe uma taxa cadastrada para o segmento PRIVATE.'


def test_post_fee_with_database_error(web_client,
                                      db_client,
                                      valid_fee_post_payload):
    with unittest.mock.patch.object(Taxas, 'save', return_value=(False, [])):
        result = web_client.post("/fees/", json=valid_fee_post_payload)
        body = result.json()

        assert result.status_code == 500
        assert body == 'Ocorreu um erro ao salvar a taxa.'
