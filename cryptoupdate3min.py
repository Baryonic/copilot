import requests
import time
import os
from datetime import datetime

st=3

def gp(crypto):
    try:
        res = requests.get(f"https://api.coinbase.com/v2/prices/{crypto}-USD/spot")
        price = float(res.json()["data"]["amount"])
    except KeyError:
        price = 0.000000001
    return price

def mtd(cp, pp):
    pc = (cp - pp) / pp * 100
    if pc >= .1:
        return '\033[0;31m' + f"sell{pc:.4f}%"+'\033[1;37m' + f"price diff"+'\033[0;31m' + f"{(cp - pp):.4f}"
    elif pc <= -.1:
        return '\033[0;32m' + f"buy{pc:.4f}%"+'\033[1;37m' + f"price diff"+'\033[0;32m' + f"{(cp - pp):.4f}"
    else:
        return '\033[0;33m' + f"HOLD{pc:.4f}%"+'\033[1;37m' + f"price diff"+'\033[0;33m' + f"{(cp - pp):.4f}"

def stf(fn, crypto, price):
    with open(fn, 'a') as f:
        f.write(f"{crypto},{price}\n")

def rff(crypto, pf):
    files = os.listdir("datalogs")
    files.sort()
    for file in reversed(files): 
        with open(f"datalogs/{file}", 'r') as f:
            for line in f.readlines():
                if line.startswith(crypto):
                    data = line.strip().split(',')
                    if file != pf:
                        timestamp_str = file[:-4] 
                        ts = datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")
                        print(f"The previous file was created at: {ts}")
                    return float(data[1]), file
    return None, None

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
cr = ['BTC', 'ETH', 'SOL','EUR', 'DOT', 'ORCA', 'MATIC', 'SHIB', 'ONDO', 'ATOM', 'XTZ', 'API3', 'SUPER', 'SWFTC', 'NCT', 'MPL', 'AUCTION', 'DIA', 'CGLD', 'SUKU', 'BONK', 'RAI', 'ALEPH', 'VARA', 'LDO', 'CHZ', 'ARPA', 'RBN', 'AURORA', 'WBTC', 'GAL', 'QI', 'SHPING', 'XYO', 'IOTX', 'SYN', 'HOPR', 'GST', 'FOX', 'RARE', 'MEDIA', 'SPELL', 'SAND', 'ALGO', 'CLV', 'BIGTIME', 'EUROC', 'HNT', 'RNDR', 'ADA', 'ICP', 'ARB']
if not os.path.exists('datalogs'):
    os.makedirs('datalogs')

while True:
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    fn = f"datalogs/{ts}.txt"
    pf = None
    v0 = 0
    pf = rp("mycryptos.txt")
    for crypto, amount in pf:
        try:
            amount = float(amount)
            cp = gp(crypto)
            pp, pf = rff(crypto, pf)
            if pp is None:
                print('\033[0;36m'+f"No data{crypto}.")
                pp = cp
                stf(fn, crypto, cp)
            d = mtd(cp, pp)
            v = cp * amount
            v0 += v
            cryptoamount=f"{amount} {crypto}="+'\033[0;32m'+f" ${v:.2f}"
            if pp-cp>0:
                print('\033[1;37m'+f"{crypto}"+'\033[0;35m'+f"now:"+'\033[0;31m'+ f"${cp}" '\033[0;35m' + f" before: " + '\033[0;96m'+ f"${pp}" + '\033[0;35m' + f" Decision: {d}" + '\033[1;37m' + f"{crypto}" + cryptoamount)
            elif pp-cp<0:
                print('\033[1;37m'+f"{crypto}"+'\033[0;35m'+f"now:"+'\033[0;32m'+ f"${cp}" '\033[0;35m' + f" before: " + '\033[0;96m'+ f"${pp}" + '\033[0;35m' + f" Decision: {d}" + '\033[1;37m' + f"{crypto}" + cryptoamount)
            elif pp-cp==0:
                print('\033[1;37m'+f"{crypto}"+'\033[0;35m'+f"now:"+'\033[0;37m'+ f"${cp}" '\033[0;35m' + f" before: " + '\033[0;96m'+ f"${pp}" + '\033[0;35m' + f" Decision: {d}" + '\033[1;37m' + f"{crypto}" + cryptoamount)
            stf(fn, crypto, cp)
            time.sleep(.2) 
        except Exception as e:
            print(f"Could not fetch price for {crypto}. Error: {e}")
            exit()
    print(f""+'\033[4;36m'+'\033[40m'+'\033[4;36m'+'\033[1;30m')
    print('\033[0;37m' + f"end loop, datalog file with name {ts}.txt created, sleeping for {st}min")
    print(f"$= "+'\033[4;32m'+ f"${v0:.2f}")
    print(f""+'\033[0;33m'+f"file: {__file__}  mother file: {os.path.basename(__file__)}")
    time.sleep(st*60)
