import requests
import time
import os
from datetime import datetime

st=.1

def gp(crypto):
    try:
        res = requests.get(f"https://api.coinbase.com/v2/prices/{crypto}-USD/spot")
        price = float(res.json()["data"]["amount"])
    except KeyError:
        price = 0.000000001
    return price

def rp(fn):
    with open(fn, 'r') as f:
        lines = f.readlines()
    pf = []
    for line in lines:
        data = line.strip().split(',')
        if len(data) == 2: 
            crypto, amount_str = data
            if '+' in amount_str:
                amounts = amount_str.split('+')
                amount = sum(float(a) for a in amounts)
            else:
                amount = float(amount_str)
            pf.append((crypto, amount))
    return pf

def last_value(fn):
    with open(fn, 'r') as f:
        lines = f.readlines()
    if lines:
        last_line = lines[-1]
        last_value = float(last_line.split(": ")[1].strip().replace('$', ''))  # replace() added here
        return last_value
    else:
        return None

cr = ['BTC', 'ETH', 'SOL','EUR', 'DOT', 'ORCA', 'MATIC', 'SHIB', 'ONDO', 'ATOM', 'XTZ', 'API3', 'SUPER', 'SWFTC', 'NCT', 'MPL', 'AUCTION', 'DIA', 'CGLD', 'SUKU', 'BONK', 'RAI', 'ALEPH', 'VARA', 'LDO', 'CHZ', 'ARPA', 'RBN', 'AURORA', 'WBTC', 'GAL', 'QI', 'SHPING', 'XYO', 'IOTX', 'SYN', 'HOPR', 'GST', 'FOX', 'RARE', 'MEDIA', 'SPELL', 'SAND', 'ALGO', 'CLV', 'BIGTIME', 'EUROC', 'HNT', 'RNDR', 'ADA', 'ICP', 'ARB']
if not os.path.exists('moneylogs'):
    os.makedirs('moneylogs')

fn = f"moneylogs/moneylog.txt"  # Define the filename outside the loop

while True:
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    v0 = 0
    pf = rp("mycryptos.txt")
    lv = last_value(fn)  # Move this line up here
    for crypto, amount in pf:
        try:
            amount = float(amount)
            cp = gp(crypto)
            v = cp * amount
            v0 += v
        except Exception as e:
            print(f"Could not fetch price for {crypto}. Error: {e}")
            exit()
    with open(fn, 'a') as f:  # Use 'a' for append mode
        f.write(f"Time{ts}: ${v0}\n")  # Add a newline character at the end
    if lv is None or v0 == lv:
        print('\033[0;36m' + f"${v0}")
    elif v0 > lv:
        print('\033[0;32m' + f"${v0}")
    else:
        print('\033[0;31m' + f"${v0}")
    time.sleep(st*60)