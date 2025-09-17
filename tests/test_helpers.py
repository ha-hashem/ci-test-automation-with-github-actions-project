import pytest
from app.helpers import convert_gold_price_to_grams, convert_USD_to_BHD

def test_convert_gold_price_to_grams():
    test_price = 1800  # Example price per ounce in USD
    converted_price = convert_gold_price_to_grams(test_price)
    assert converted_price == 57.87  # Expected price per gram
    assert isinstance(converted_price, float)
    assert converted_price > 0

def test_convert_gold_price_to_grams_invalid():
    with pytest.raises(ValueError):
        convert_gold_price_to_grams(0)
    with pytest.raises(ValueError):
        convert_gold_price_to_grams(-100)

def test_convert_USD_to_BHD():
    test_amount = 100  # Example amount in USD
    converted_amount = convert_USD_to_BHD(test_amount)
    assert converted_amount == 37.6  # Expected amount in BHD
    assert isinstance(converted_amount, float)
    assert converted_amount > 0

def test_convert_USD_to_BHD_invalid():
    with pytest.raises(ValueError):
        convert_USD_to_BHD(-50)

