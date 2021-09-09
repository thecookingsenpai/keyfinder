import os
import time
from random import randrange
from requests_html import HTMLSession
from multiprocessing import Process
import psutil
from sys import argv

threads = []
session = HTMLSession()
defaultAggressiveness = 20

def checkAll():
    while True:
        try:
            time.sleep(0.2)
            with open("checked", "r+") as checked:
                stream = checked.read()
            url = "https://privatekeys.pw/keys/ethereum/"
            foundRandom = False
            randomPage = 0
            while not foundRandom:
                #print("Trying a new random...")
                randomPage = str(randrange(2573157538607026564968244111304175730063056983979442319613448069811514699875))
                if randomPage in stream:
                    #print("Checked.")
                    pass
                else:
                    #print("To check.")
                    foundRandom = True
                    #print(randomPage)

            #print("Checking the page...")
            url = url + randomPage
            r = session.get(url)
            if not "200" in str(r):
                print(str(os.getpid()) + " || " + "[X] Bad http response code: " + str(r))
                return -2
            r.html.render()
            balance = r.html.text
            for line in str(balance).splitlines():
                if "Total balance" in line:
                    with open("checked", "a") as checked:
                        checked.write(randomPage + "\n")
                        checked.flush()
                    #print(line)
                    try:
                        totalBalance = line.split(": ")[1]
                        print(str(os.getpid()) + " || " + "[" + randomPage + "] - " + totalBalance)
                        if float(totalBalance)  > 0:
                            print(str(os.getpid()) + " || " + "[!!!] Balance found!")
                            print(str(os.getpid()) + " || " + url)
                            with open("balanced", "w+") as balanced:
                                balanced.write(url + " - " + str(totalBalance) + "\n")
                            for pids in threads:
                                pid = pids.pid
                                if not pid == Process.pid:
                                    handler = psutil.Process(pid)
                                    handler.suspend()
                            input(str(os.getpid()) + " || " + "Press enter to continue...\n")
                            for pids in threads:
                                pid = pids.pid
                                if not pid == Process.pid:
                                    handler = psutil.Process(pid)
                                    handler.resume()
                    except:
                        pass
        except KeyboardInterrupt:
            print("ABORTED")
            return -1
        except:
            print(str(os.getpid()) + " || " + "[x] Unhandled exception. Retrying.")

if __name__ == '__main__':
    if len(argv) < 2:
        pass
    else:
        if isinstance(int(argv[1]), int) and int(argv[1]) < 31 and int(argv[1]) > 0:
            defaultAggressiveness = int(argv[1])
        else:
            print("[x] Wrong aggressiveness. Must be an int between 1 and 30")
            exit(0)
    print("[i] Aggressiveness is now " + str(defaultAggressiveness))
    time.sleep(1)
    for i in range(0,defaultAggressiveness):
        time.sleep((randrange(10)/10))
        p = Process(target=checkAll)
        threads.append(p)
        p.daemon = True
        p.start()
        print("[>] Thread " + str(p.pid) + " started")
    for thread in threads:
        print("EXECUTED:")
        print("Process: " + str(thread.pid))
    checkpoint = 0
    while True:
        time.sleep(3)
        checkpoint = checkpoint + 1
        if checkpoint == 30:
            pass
        for process in threads:
            process.join(timeout=0)
            if process.is_alive():
                pass
            else:
                print("Process " + str(process.pid) + " died. Replacing!")
                threads.remove(process)
                p = Process(target=checkAll)
                threads.append(p)
                p.start()
                print("EXECUTED:")
                print("Process: " + str(p.pid))

