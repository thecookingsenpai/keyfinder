from random import randrange, randint
import pyetherbalance
import requests
import tabulate
from os.path import exists
from os import remove, getpid, system
import threading
import psutil
import time
import datetime
from web3 import Web3
import time, json
import secrets
from eth_keys import keys as keyhelper
import struct
import sys, select, tty, termios


firstPassage = False

rpclist = []
with open("bscrpc", 'r') as rpc:
    for line in rpc.readlines():
        rpclist.append(line.strip("\n"))

bsc = "https://bsc-dataseed3.binance.org/"
web3bsc = Web3(Web3.HTTPProvider(bsc))
print(web3bsc.isConnected())
#infura_url = "https://mainnet.infura.io/v3/f5dcd7cc27a54ac4ac75458fe2033d2b"
infura_url = "http://localhost:8550"
ethbalance = pyetherbalance.PyEtherBalance(infura_url)
bscscan_token = "Y2UC9V8C3UWK1RTS8Z8H4EI6FE9P8AJTFN"


completed_pages = {
                "page number" : "milliseconds"
                }
balanced_list = {
            "address" : "balance"
        }
registry = {
                "started at" : datetime.datetime.now(),
                "checking balance on" : "BSC, ETH",
                "medium speed per address" : 0,
                "medium speed per page" : 0,
                "total pages to check" : 0,
                "checked pages" : 0,
                "balanced accounts found" : 0,
                "accounts checked" : 0
                                                                                                                            }
logging = {
        "process name" : "log"
        }

class NonBlockingConsole(object):
    def __enter__(self):
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        return self

    def __exit__(self, type, value, traceback):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def get_data(self):
        try:
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                return sys.stdin.read(1)
        except:
            return '[CTRL-C]'
        return False

class scrapeThread(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global bsc
        global infuraUrl
        global ethbalance
        global web3
        global bscscan_token
        global registry
        global logging
        global balanced_list
        global completed_pages
        global rpclist
        stepper = 1
        pid = self.name
        while True:
            start = stepper
            combo = []
            time_debug = True
            stime = datetime.datetime.now()
            total_execution_time = 0.00000000
            addresses = []
            keys = []
            is_balanced = False
            iterations = 128
            
            pkey = "{:064x}".format(secrets.randbits(256))
            pkey_bytes = bytes.fromhex(pkey)
            public = keyhelper.PrivateKey(pkey_bytes).public_key
            public_bytes = bytes.fromhex(str(public)[2:])
            address = str(keyhelper.PublicKey(public_bytes).to_address())
            address = Web3.toChecksumAddress(address.lower())

            balance = ethbalance.get_eth_balance(address)
            try:
                headers = {
                    'Content-Type': 'application/json',
                }
                data = ' { "jsonrpc": "2.0", "method": "eth_getBalance", "params": ["' + str(address) + '", "latest"], "id": 1 } '
                chosenRPC = rpclist[randrange(0,len(rpclist)-1)]
                response = requests.post(chosenRPC, headers=headers, data=data)
                bsc_balance = json.loads(response.text).get('result')
                bsc_balance = float.fromhex(bsc_balance)
            except:
                print("!! Cannot connect to BSC for checking address! !!")
                bsc_balance = 0.000000000
            try:
                if balance.get("balance") > 0.000 or bsc_balance > 0.00:
                    print(str(address) + " has on ETH " + str(balance.get("balance")))
                    print("And has " + str(bsc_balance) + " balance on BSC")
                    balanced_list[address] = str(balance.get("balance")) + "ETH," + str(bsc_balance) + "BNB"
                    if not exists("balanced_addresses"):
                        with open("balanced_addresses", "w+") as balancedfile:
                            balancedfile.write("BEGIN\n")
                            balancedfile.flush()
                    with open("balanced_addresses", "a") as balancedfile:
                        balancedfile.write(str(address) + " has " + str(balance.get("balance")) + " on ETH and has " + str(bsc_balance) + " on BSC \n")
                        balancedfile.flush()
                        is_balanced = True
            except:
                pass
            if is_balanced:
                registry["balanced accounts found"]+=1
                combo.append({
                    "address": addresses[-1],
                    "key": keys[-1]
                })
                with open(addresses[-1], "w+") as addressfile:
                    addressfile.write(keys[-1])
                    is_balanced = False
                if time_debug:
                    etime = datetime.datetime.now()
                    dtime = (etime - stime)
                    total_execution_time = dtime.total_seconds()*1000
                    completed_pages[step] = str(total_execution_time)
                    registry["checked pages"]+=1
                    registry["accounts checked"] += iterations
                    registry["medium speed per address"] = (registry["medium speed per address"] * (registry["accounts checked"]-iterations) + (total_execution_time/iterations)) / registry["accounts checked"]
                    registry["medium speed per pages"] = (registry["medium speed per page"] * (registry["checked pages"]-1) + (total_execution_time)) / registry["checked pages"]
                firstPassage = True
if __name__ == '__main__':
    animation = "\\"
    threads = []
    for i in range(0,200):
        time.sleep((randrange(10)/100))
        p = scrapeThread(str(i))
        threads.append(p)
        p.start()
        print("[" + str(i)  + "/200 >] Thread " + str(i) + " started", end="\r", flush=True)
    print("Spawned.")
    print("\n------------------ Processes spawned. Initializing registry and logging...")
    checkpoint = 0



additionalMsg = ""
additionalMsgLifespan = 10
with NonBlockingConsole() as nbc:
    while True:
        c = nbc.get_data()
        if c:
            if c == '\x1b':  # x1b is ESC
                for balanced in balanced_list:
                    additionalMsg = "Here is the complete list of the funded account we found:"
                    additionalMsg = additionalMsg + balanced + " : " + balanced_list[balanced] + "\n"
            elif c == '[CTRL-C]':
                print("Aborted!")
                exit(1)
        try:
            time.sleep(1)
            checkpoint = checkpoint + 1
            if checkpoint <= 15:
                pass
            else:
                checkpoint = 0
                counterThread = 0
                for process in threads:
                    counterThread += 1
                    if process.is_alive():
                        pass
                    else:
                        print("Process " + str(counterThread) + " died. Replacing!")
                        threads.remove(process)
                        p = scrapeThread(str(counterThread))
                        threads.append(p)
                        print("EXECUTED:")
                        print("Process: " + str(counterThread))
            realtimeTracking = True
            if realtimeTracking:
                system("clear")
                print("\n\t\t========= Registry:")
                print("current time: " + str(datetime.datetime.now()))
                for element in registry:
                    print(str(element)  + " : " + str(registry[element]))
                print("\n\t\t==== Logging:")
                for log in logging:
                    print(str(log) + " : " + str(logging[log]))
                if not firstPassage:
                    if animation == "\\":
                        animation = "/"
                    else:
                        animation = "\\"
                    print("\t\t\nINITIALIZING, PLEASE WAIT..." + animation)

                print("\n\t\t\t[Menu]")
                print("\t\tPress ESC to view the funded account we already found")
                print("\t\tPress CTRL+C to stop the program\n\n")
                
                if not additionalMsg == "":
                    additionalMsgLifespan -= 1
                    if additionalMsgLifespan == 0:
                        additionalMsg = ""
                        additionalMsgLifespan = 10
                    else:
                        print("\n" + additionalMsg)
        except KeyboardInterrupt:
            print("Aborted.")
            exit(0)
