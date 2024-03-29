from django.shortcuts import render, redirect
import requests
from django.contrib import messages
from web3 import Web3, exceptions
from decimal import Decimal
from .utils.contracts import link_eth_usd, strategy_manager, eigen_pod_manager, cb_eth, st_eth, r_eth, ethx, ankr_eth, oeth, os_eth, sw_eth, w_beth, sfrx_eth, ls_eth, m_eth
from .utils.convertors import convert_to_readable_format, convert_to_adj_total_shares
from .forms import UserEmailForm, WalletAddressForm
from web3.exceptions import Web3Exception



def get_api_data():
    url = 'https://api.llama.fi/tvl/eigenlayer'
    
    response = requests.get(url)
    if response.status_code == 200:

        return float(response.text)
    else:
        print("Failed to retrieve data from the API")
        return None

def get_api_data_historical():
    url = 'https://api.llama.fi/protocol/eigenlayer'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json() 

        ethereum_tvl_data = data.get("chainTvls", {}).get("Ethereum", {}).get("tvl", [])

        tvl_data = [{"date": item["date"], "totalLiquidityUSD": Decimal(item["totalLiquidityUSD"])} for item in ethereum_tvl_data]

        return tvl_data
    else:
        print("Failed to retrieve data from the API")
        return None

def get_num_pods():
    num_pods = eigen_pod_manager.functions.numPods().call()
    return num_pods

def get_min_withdrawal_delay():
    min_withdrawal_delay = strategy_manager.functions.withdrawalDelayBlocks().call()
    return min_withdrawal_delay

def get_wallet_shares_lsd(wallet_address):
    contracts = [cb_eth, st_eth, r_eth, ethx, ankr_eth, oeth, os_eth, sw_eth, w_beth, sfrx_eth, ls_eth, m_eth]
    shares_list = []
    
    for contract in contracts:
        try:
            shares_in_wei = contract.functions.shares(wallet_address).call()
            shares_in_ether = Web3.from_wei(shares_in_wei, 'ether')
            shares_list.append(shares_in_ether)
        except Exception as e:
                return []

    return shares_list

def index(request):
    email_form = UserEmailForm(request.POST or None)
    wallet_form = WalletAddressForm(request.POST or None)
    wallet_shares = request.session.get('wallet_shares', [])
    error_message = None
    pod_address = request.session.get('pod_address', None)

    if request.method == 'POST':
        if 'email_submit' in request.POST and email_form.is_valid():
            email_form.save()
            messages.success(request, "Email saved successfully.")

        elif 'check_wallet' in request.POST and wallet_form.is_valid():
            wallet_address = wallet_form.cleaned_data['wallet_address']

            try:
                # Attempt to get wallet shares directly with the provided address
                wallet_shares = get_wallet_shares_lsd(wallet_address)
                request.session['wallet_shares'] = wallet_shares

                # Attempt to get pod address directly with the provided address
                pod_address = eigen_pod_manager.functions.getPod(wallet_address).call()
                request.session['pod_address'] = pod_address

            except exceptions.InvalidAddress as e:
                try:
                    # If the provided address is not valid, try converting it to a checksum address
                    checksum_address = Web3.to_checksum_address(wallet_address)
                    wallet_shares = get_wallet_shares_lsd(checksum_address)
                    request.session['wallet_shares'] = wallet_shares

                    # Attempt to get pod address with the converted checksum address
                    pod_address = eigen_pod_manager.functions.getPod(checksum_address).call()
                    request.session['pod_address'] = pod_address

                except exceptions.InvalidAddress as e:
                    error_message = "Invalid wallet address format: " + str(e)
                    messages.error(request, error_message)

            except Web3Exception as e:
                error_message = "Error fetching wallet shares: " + str(e)
                messages.error(request, error_message)

    # Fetch the USD conversion rate and convert to Decimal
    usd_conversion_rate_raw = link_eth_usd.functions.latestRoundData().call()[1]
    usd_conversion_rate = float(convert_to_readable_format(usd_conversion_rate_raw, decimal_places=8))

    #Fetch Minimum Withdrwal Delay from Strategy Manager
    min_withdrawal_delay = get_min_withdrawal_delay()

    #Fetch numPods from EigenPod Manager
    num_pods = get_num_pods()

    # Define the list of contracts and their names
    lsds = [cb_eth, st_eth, r_eth, ethx, ankr_eth, oeth, os_eth, sw_eth, w_beth, sfrx_eth, ls_eth, m_eth]
    lsd_names = ['cbEth', 'stEth', 'rEth', 'Ethx', 'ankrEth', 'OEth', 'osEth', 'swEth', 'wBEth', 'sfrxEth', 'lsEth', 'mEth']

    # Calculate total shares in ETH and USD using Decimal for precision
    lsd_total_shares_eth = [round(convert_to_adj_total_shares(lsd), 2) for lsd in lsds]
    lsd_total_shares_usd = [round((lsd * usd_conversion_rate), 2) for lsd in lsd_total_shares_eth]

    # Fetch and calculate total value locked in USD and ETH
    total_value_locked_usd = round(get_api_data(), 2)
    total_value_locked_eth = round((total_value_locked_usd / usd_conversion_rate), 2)

    tvl_data = get_api_data_historical()  

    # Calculate beacon ETH TVL in ETH and USD
    beacon_eth_tvl_eth = round((total_value_locked_eth - sum(lsd_total_shares_eth)), 2)
    beacon_eth_tvl_usd = round((beacon_eth_tvl_eth * usd_conversion_rate),2)

    lsd_data = [{'name': name, 'eth_value': eth, 'usd_value': usd} for name, eth, usd in zip(lsd_names, lsd_total_shares_eth, lsd_total_shares_usd)]
    wallet_shares_data = {name: shares for name, shares in zip(lsd_names, wallet_shares)}

    pod_address = request.session.pop('pod_address', None)
    error_message = request.session.pop('error_message', None)

    context = {
        'total_value_locked_usd': total_value_locked_usd,
        'total_value_locked_eth': total_value_locked_eth,
        'beacon_eth_tvl_eth': beacon_eth_tvl_eth,
        'beacon_eth_tvl_usd': beacon_eth_tvl_usd,
        'lsd_data': lsd_data,
        'tvl_data': tvl_data,
        'num_pods': num_pods,
        'min_withdrawal_delay': min_withdrawal_delay,
        'email_form': email_form, 
        'wallet_form': wallet_form,
        'pod_address': pod_address, 
        'error_message': error_message,
        'wallet_shares_data': wallet_shares_data 
    }

    return render(request, 'index.html', context)

