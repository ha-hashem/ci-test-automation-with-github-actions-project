def convert_gold_price_to_grams(price_per_ounce):
    """
    Convert gold price from per ounce to per gram.
    1 ounce = 31.1035 grams
    """
    if price_per_ounce <= 0:
        raise ValueError("Price per ounce must be greater than zero.")
    price_per_gram = price_per_ounce / 31.1035
    return round(price_per_gram, 2)

def convert_USD_to_BHD(usd_amount):
    """
    Convert USD amount to BHD (Bahraini Dinar).
    Example conversion rate: 1 USD = 0.376 BHD
    """
    if usd_amount < 0:
        raise ValueError("USD amount cannot be negative.")
    conversion_rate = 0.376
    return round(usd_amount * conversion_rate, 3)