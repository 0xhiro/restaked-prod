import json 
from ....services.llama_api_fetchers import get_api_data, get_api_data_historical
from ..generators.line_chart_generator import generate_line_chart_data


def get_tvl_hist():
    historical_data = get_api_data_historical()
    
    dates = [item['date'].strftime('%Y-%m-%d') for item in historical_data]
    total_liquidity_usd = [round(float(item['total_liquidity_usd']), 2) for item in historical_data]

    generate_line_chart_data(dates, total_liquidity_usd)

    tvl_hist = json.dumps(generate_line_chart_data(dates, total_liquidity_usd), ensure_ascii=False)

    return tvl_hist