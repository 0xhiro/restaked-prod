from datetime import datetime
import requests
from decimal import Decimal

def get_api_data():
    url = 'https://api.llama.fi/tvl/eigenlayer'
    
    response = requests.get(url)
    if response.status_code == 200:
        current_data = float(response.text)
        return current_data
    else:
        print("Failed to retrieve data from the API")
        return None

def get_api_data_historical():
    url = 'https://api.llama.fi/protocol/eigenlayer'
    response = requests.get(url)
    historical_data = []

    if response.status_code == 200:
        data = response.json() 
        ethereum_tvl_data = data.get("chainTvls", {}).get("Ethereum", {}).get("tvl", [])
        
        for item in ethereum_tvl_data:
            date = datetime.fromtimestamp(item["date"]).date()
            total_liquidity_usd = Decimal(item["totalLiquidityUSD"])
            historical_data.append({
                'date': date,
                'total_liquidity_usd': total_liquidity_usd
            })
    else:
        print("Failed to retrieve data from the API")

    return historical_data
