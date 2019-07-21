import pytest
import yaml
import hashlib
import xml.etree.ElementTree as ETr


@pytest.fixture(scope="session")
def config():
    """Get data from config.yaml."""
    with open("config.yaml", "r") as file:
        return yaml.load(file, Loader=yaml.SafeLoader)


@pytest.fixture()
def body(config, amount):
    """Make signed request body from XML template and data from config file."""

    # Open template
    with open("simple_payment_tmplt.xml", "r", encoding='utf8') as file:
        tree = ETr.parse(file)
        root = tree.getroot()

        # Create the sign.
        string_for_signature = ''.join([
            str(config['test_merchant1']['merchant_id']),
            root.find('product_id').text,
            str(root.find('amount').text),
            root.find('cf').text,
            config['test_merchant1']['secret_word']
        ]).lower().encode('utf-8')
        m = hashlib.md5()
        m.update(string_for_signature)
        sign = m.hexdigest()

        # Paste sign and other value into template.
        amount_field = root.find('amount')
        amount_field.text = str(amount)
        token = root.find('token')
        token.text = sign
        product_id = root.find('product_id')
        product_id.text = str(config['test_merchant1']['product_id'])

        pan = root.find('pan')
        pan.text = str(config['test_card1']['pan'])
        cardholder = root.find('cardholder')
        cardholder.text = str(config['test_card1']['cardholder'])
        exp_month = root.find('exp_month')
        exp_month.text = str(config['test_card1']['exp_month'])
        exp_year = root.find('exp_year')
        exp_year.text = str(config['test_card1']['exp_year'])
        cvv = root.find('cvv')
        cvv.text = str(config['test_card1']['cvv'])

        xml_string = ETr.tostring(root, encoding='utf8', method='xml')
        return xml_string
