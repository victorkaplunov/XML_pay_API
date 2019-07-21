import pytest
import requests
import xml.etree.ElementTree as ETr


@pytest.mark.parametrize("amount", [5, 500])
def test_success_payment(config, body, amount):
    """Boundary value test for success simple payment with mandatory parameters only."""
    response = requests.post(config['base_url'], data=body, verify=False)
    root = ETr.fromstring(response.content)
    assert root.find('description').text != "opcode is absent!"


@pytest.mark.parametrize("amount", [-5, 0, 4.99, 500.01, 50000000000000000000000])
def test_unsuccess_payment(config, body, amount):
    """Boundary value test for unsuccessful payment with mandatory parameters only."""
    response = requests.post(config['base_url'], data=body, verify=False)
    root = ETr.fromstring(response.content)
    assert root.find('status').text == "KO"


