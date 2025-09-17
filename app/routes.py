from app.helpers import convert_gold_price_to_grams, convert_USD_to_BHD

from fastapi import APIRouter, HTTPException, Query
from config.environment import GOLD_API_KEY

import httpx

router = APIRouter()

GOLD_API_URL = "https://www.goldapi.io/api"
headers = {"x-access-token": GOLD_API_KEY, "Content-Type": "application/json"}

@router.get("/")
def read_root():
    return {"message": "Welcome to the Gold Price API!"}

@router.get("/current")
async def get_current_gold_price():
    '''
    Gets the current gold price in BHD per gram.
    '''
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{GOLD_API_URL}/XAU/USD", headers=headers) # API doesn't support BHD, so we get USD first
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Failed to fetch gold price")
        data = resp.json()
        price = data.get("price")

        # Covert price from USD/ounce to BHD/gram
        price = convert_gold_price_to_grams(price)
        price = convert_USD_to_BHD(price)

        return {
            "price_usd_per_ounce": price,
            "currency": "BHD",
            "unit": "gram",
            "carat": 24
        }


@router.get("/history")
async def get_historical_gold_price(date: str = Query(..., regex="^\d{8}$")):
    """
    Get historical gold price for a specific date.
    Date format: YYYYMMDD (e.g., 20250909)
    """
    url = f"{GOLD_API_URL}/XAU/USD/{date}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Failed to fetch historical gold price")
        data = resp.json()
        price = convert_gold_price_to_grams(data.get("price"))
        return {
            "date": date,
            "price_usd_per_ounce": price,
            "currency": "USD",
            "unit": "ounce"
        }


@router.get("/convert")
async def convert_gold_to_currency(amount_ounces: float, currency: str = "USD"):
    '''
    Convert a specified amount of gold (in ounces) to a given currency.
    Default currency is USD.
    Example: /convert?amount_ounces=2.5&currency=EUR
    '''
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{GOLD_API_URL}/XAU/{currency.upper()}", headers=headers)
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail="Failed to fetch conversion rate")
        data = resp.json()
        price_per_ounce = data.get("price")
        if price_per_ounce is None:
            raise HTTPException(status_code=500, detail="Price not available")
        total = amount_ounces * price_per_ounce
        return {
            "amount_ounces": amount_ounces,
            "currency": currency.upper(),
            "total_value": total
        }