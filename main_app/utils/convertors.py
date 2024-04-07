from decimal import Decimal

def convert_to_readable_format(number, decimal_places=18):
    converted_number = number / 10**decimal_places
    return format(converted_number, '.2f')


def get_total_shares(contract):
    try:
        total_shares_raw = contract.functions.totalShares().call()
        total_shares = Decimal(convert_to_readable_format(total_shares_raw))
        return float(total_shares)
    except Exception as e:
        print(e)
        return None

def get_underlying_to_shares(contract):
    try:
        underlying_to_shares_raw = contract.functions.underlyingToShares(1000000).call()
        underlying_to_shares = underlying_to_shares_raw / 1000000
        return float(underlying_to_shares)
    except Exception as e:
        print(e)
        return None
    
def convert_to_adj_total_shares(contract):
    try:
        total_shares = get_total_shares(contract)
        underlying_to_shares = get_underlying_to_shares(contract)
        return total_shares * underlying_to_shares
    except Exception as e:
        print(e)
        return None