import pytest
import requests
import xml.etree.ElementTree as ETr


@pytest.mark.parametrize("amount", [5, 500])
def test_success_payment(config, body, amount):
    """Test of success simple payment with mandatory parameters only."""
    print(body)
    response = requests.post(config['base_url'], data=str(body), verify=False)
    root = ETr.fromstring(response.content)
    print(response.content)
    assert root.find('description').text != "opcode is absent!"


@pytest.mark.parametrize("amount", [-1, 0, 4.99, 500.01])
def test_unsuccess_payment(config, body, amount):
    """Test of success simple payment with mandatory parameters only."""
    print(body)
    response = requests.post(config['base_url'], data=str(body), verify=False)
    root = ETr.fromstring(response.content)
    print(response.content)
    assert root.find('status').text == "KO"


