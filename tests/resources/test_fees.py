import unittest.mock

from src.models.fees import Taxas


def test_get_all_fees_with_success(web_client,
                                   db_client,
                                   valid_fee_post_payload,
                                   another_valid_fee_post_payload):
    web_client.post("/fees/", json=valid_fee_post_payload)
    web_client.post("/fees/", json=another_valid_fee_post_payload)
    result = web_client.get("/fees/")
    body = result.json()
    print(body)

    assert result.status_code == 200
    assert len(body.get('fees')) == 2


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


def test_patch_fee_with_success(web_client,
                                db_client,
                                valid_fee_post_payload,
                                valid_fee_patch_payload):
    web_client.post("/fees/", json=valid_fee_post_payload)
    result = web_client.patch("/fees/1", json=valid_fee_patch_payload)
    body = result.json()

    assert result.status_code == 200
    assert body == 'Nova taxa para o segmento PRIVATE atualizada com sucesso: 0.2.'


def test_patch_fee_with_invalid_payload(web_client,
                                        db_client,
                                        valid_fee_post_payload,
                                        invalid_fee_patch_payload):
    web_client.post("/fees/", json=valid_fee_post_payload)
    result = web_client.patch("/fees/1", json=invalid_fee_patch_payload)

    assert result.status_code == 422


def test_patch_nonexistent_fee(web_client,
                               db_client,
                               valid_fee_post_payload,
                               valid_fee_patch_payload):
    web_client.post("/fees/", json=valid_fee_post_payload)
    result = web_client.patch("/fees/2", json=valid_fee_patch_payload)
    body = result.json()

    assert result.status_code == 404
    assert body == 'Taxa não encontrada.'


def test_patch_fee_with_database_error(web_client,
                                       db_client,
                                       valid_fee_post_payload,
                                       valid_fee_patch_payload):
    with unittest.mock.patch.object(Taxas, 'update', return_value=(False, [])):
        web_client.post("/fees/", json=valid_fee_post_payload)
        result = web_client.patch("/fees/1", json=valid_fee_patch_payload)
        body = result.json()

        assert result.status_code == 500
        assert body == 'Ocorreu um erro ao salvar a taxa.'
