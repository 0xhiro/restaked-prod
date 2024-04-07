import json
import os 
from web3 import Web3
from datetime import datetime, timezone
from ..utils.contracts import eigen_pod_manager
from ..utils.charts.generators.line_chart_generator import generate_line_chart_data

API_KEY = os.environ.get('MAINNET_API')

w3 = Web3(Web3.HTTPProvider(API_KEY))

def get_num_pods():
    start_block = 17445564  
    step = 50000 
    try:
        current_block = w3.eth.block_number
    except Exception as e:
        print(f"Failed to fetch current block number: {e}")
        return json.dumps({})

    block_timestamp_list = []
    num_pods_list = []

    for block_number in range(start_block, current_block, step):
        try:
            num_pods = eigen_pod_manager.functions.numPods().call(block_identifier=block_number)
            block = w3.eth.get_block(block_number)
        except Exception as e:
            print(f"Error fetching data for block {block_number}: {e}")
            continue  # Skip this block if there was an error
        
        num_pods_list.append(num_pods)
        block_timestamp = datetime.fromtimestamp(block.timestamp, tz=timezone.utc).strftime('%Y-%m-%d')
        block_timestamp_list.append(block_timestamp)

    try:
        num_pods_hist = json.dumps(generate_line_chart_data(block_timestamp_list, num_pods_list))
    except Exception as e:
        print(f"Error generating chart data: {e}")
        return json.dumps({})
    
    return num_pods_hist
