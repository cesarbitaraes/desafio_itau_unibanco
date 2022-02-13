

def test_calculate_foreign_currency_with_success(db_client,
                                                 web_client,
                                                 valid_fee_post_payload,
                                                 valid_calculate_foreign_currency_post_payload):
    web_client.post("/fees/", json=valid_fee_post_payload)
    result = web_client.post("/calculate_foreign_currency/", json=valid_calculate_foreign_currency_post_payload)
    body = result.json()
    print(body)

    assert result.status_code == 200
    assert body == 'Valor da conversão em reais: R$ 6006.0.'


def test_calculate_foreign_currency_with_invalid_payload(db_client,
                                                         web_client,
                                                         valid_fee_post_payload,
                                                         invalid_calculate_foreign_currency_post_payload):
    web_client.post("/fees/", json=valid_fee_post_payload)
    result = web_client.post("/calculate_foreign_currency/", json=invalid_calculate_foreign_currency_post_payload)

    assert result.status_code == 422


def test_calculate_foreign_currency_with_not_registered_fee(db_client,
                                                            web_client,
                                                            valid_fee_post_payload,
                                                            unregistered_fee_calculate_foreign_currency_post_payload):
    web_client.post("/fees/", json=valid_fee_post_payload)
    result = web_client.post("/calculate_foreign_currency/",
                             json=unregistered_fee_calculate_foreign_currency_post_payload)
    body = result.json()
    print(body)

    assert result.status_code == 404
    assert body == 'Não existe taxa cadastrada para esse segmento.'
