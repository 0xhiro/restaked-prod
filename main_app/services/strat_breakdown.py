import json
import os
from web3 import Web3
from ..utils.contracts import link_eth_usd, strategy_manager, cb_eth, st_eth, r_eth, ethx, ankr_eth, oeth, os_eth, sw_eth, w_beth, sfrx_eth, ls_eth, m_eth
from ..utils.charts.generators.pie_chart_generator import generate_pie_chart_data
from .llama_api_fetchers import get_api_data

API_KEY = os.environ.get('MAINNET_API')

w3 = Web3(Web3.HTTPProvider('MAINNET_API'))

def get_strat_breakdown():
    contracts = [cb_eth, st_eth, r_eth, ethx, ankr_eth, oeth, os_eth, sw_eth, w_beth, sfrx_eth, ls_eth, m_eth]
    labels = ['cbEth', 'stEth', 'rEth', 'ethx', 'ankrEth', 'oEth', 'osEth', 'swEth', 'wBEth', 'sfrxEth', 'lsEth', 'mEth']
    strat_shares = []
    current_data = get_api_data()
    usd_conversion_rate = (link_eth_usd.functions.latestRoundData().call()[1]) / 10 ** 8
    
    for contract in contracts:
        try:
            shares_in_wei = contract.functions.totalShares().call()
            underlying_in_wei = contract.functions.sharesToUnderlying(shares_in_wei).call()
            underlying_in_ether = Web3.from_wei(underlying_in_wei, 'ether')
            strat_shares.append(round(float(underlying_in_ether), 2))
            
        except Exception as e:
                return []
    
    labels.append('beacon_eth')
    beacon_shares = (current_data - sum(strat_shares)) / usd_conversion_rate
    print(beacon_shares)
    print(usd_conversion_rate)
    strat_shares.append(beacon_shares)

    strat_breakdown = json.dumps(generate_pie_chart_data(labels, strat_shares))

    return strat_breakdown
