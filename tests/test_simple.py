import send2airgap.transmit as transmit
import send2airgap.receive as receive
import pytest


def test_tx():
    assert True == True
    assert transmit.foo() == "bar"


def test_rx():
    assert True == True
    assert receive.foo() == "bar"
