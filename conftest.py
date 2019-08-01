"""Fixtures for payment gate sandbox."""
import hashlib
import xml.etree.ElementTree as ETr
import xml.dom.minidom
import pytest
import requests
import yaml


@pytest.fixture(scope="session")
def config():
    """Get data from configuration file config.yaml."""
    
    with open("config.yaml", "r") as file:
        return yaml.load(file, Loader=yaml.SafeLoader)


@pytest.fixture()
def request_string(config, amount, rebill):
    """
        This fuction make signed request string for simple payment.
    """

    # Create the sign.
    string_for_signature = ''.join([
        str(config['test_merchant1']['merchant_id']),
        str(config['test_merchant1']['product_id']),
        str(amount),
        str(config['test_merchant1']['cf']),
        config['test_merchant1']['secret_word']
    ]).lower().encode('utf-8')
    md5_hash = hashlib.md5()
    md5_hash.update(string_for_signature)
    sign = md5_hash.hexdigest()

    request_string = ''.join([
        '?',
        'opcode=0',
        '&product_id=', config['test_merchant1']['product_id'],
        '&amount=', amount,
        '&pan=', config['test_card1']['pan'],
        '&ip_address=', config['ip_address'],
        '&cf=', config['test_merchant1']['cf'],
        '&cardholder=', config['test_card1']['cardholder'],
        '&exp_month=', config['test_card1']['exp_month'],
        '&exp_year=', config['test_card1']['exp_year'],
        '&cvv=', config['test_card1']['cvv'],
        '&token=', sign,
        '&user_rebill_approved=', rebill
    ])
    return request_string


@pytest.fixture()
def simple_payment(config, request_string):
    """
        This function sends POST request for simple payment
        creation and prints some useful information for debugging.
    """
    url = config['base_url'] + request_string
    response = requests.post(url, verify=False)
    root = ETr.fromstring(response.content)
    print('POST request to {0}'.format(url))
    print('Status code: {0}'.format(response.status_code))
    print('RESPONSE: {0}'.format(xml.dom.minidom.parseString(response.text).toprettyxml()))
    return root


@pytest.fixture()
def request_string_for_rebill(config, amount, simple_payment):
    """
        This function make signed request string for rebill payment.
    """

    # Get payment_id
    try:
        payment_id = simple_payment.find('extended_id').text
    except AttributeError:
        print("Response do not contain 'extended_id' tag.")

    # Create the sign.
    string_for_signature = ''.join([
        str(config['test_merchant1']['merchant_id']),
        payment_id,
        str(amount),
        config['test_merchant1']['secret_word']
    ]).lower().encode('utf-8')
    md5_hash = hashlib.md5()
    md5_hash.update(string_for_signature)
    sign = md5_hash.hexdigest()

    request_string = ''.join([
        '?',
        'opcode=6',
        '&payment_id=', payment_id,
        '&amount=', amount,
        '&token=', sign,
    ])
    return request_string


@pytest.fixture()
def rebill_payment(config, request_string_for_rebill):
    """
        This function sends POST request for rebill payment
        creation and prints some useful information for debugging.
    """
    url = config['base_url'] + request_string_for_rebill
    response = requests.post(url, verify=False)
    root = ETr.fromstring(response.content)
    print('POST request to {0}'.format(url))
    print('Status code: {0}'.format(response.status_code))
    print('RESPONSE: {0}'.format(xml.dom.minidom.parseString(response.text).toprettyxml()))
    return root
