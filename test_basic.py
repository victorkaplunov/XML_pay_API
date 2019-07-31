"""Tests for payment gate sandbox."""
import pytest


@pytest.mark.parametrize("amount", ['10', '10', '10', '10', '10', '10', '10', '10', '10', '10'])
@pytest.mark.parametrize("rebill", '0')
def test_success_payment_(simple_payment):
    """Test for success simple payment
        with mandatory parameters only."""
    
    assert simple_payment.find('status').text == "NEW", \
        'Field "status" do not contain string "NEW".'


@pytest.mark.parametrize("amount",
                         ['-5', '-5', '0', '4.98', '4.99', '500.01',
                          '5000000000000000000000000000000000000000000000000'])
@pytest.mark.parametrize("rebill", '0')
def test_unsuccess_payment(simple_payment):
    """Negative test for boundary amount values."""
    
    assert simple_payment.find('status').text != "NEW", \
        'Field "status" contain string "NEW", but should not.'


@pytest.mark.parametrize("amount, rebill", [('100', '1'), ('100', '1'), ('100', '1')])
def test_rebill_payment_(rebill_payment):
    """Test for success rebill."""
    
    assert rebill_payment.find('status').text == "REBILL_OK", \
        'Field "status" do not contain string "REBILL_OK".'
