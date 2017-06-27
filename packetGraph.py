import random, time
import os

# VISUALIZER VARIABLES
scr_height = 15
scr_widht = 80
allPackets = []
# IFACE SNIFFER VARIABLES
ifacePackets = 0
channel = ""
monitor_iface = ""
stoppingIface = False
sniffStarted = False
sniffError = False

def get_multiplicator():
    largestInt = 0
    multiplicator = 1
    for num in allPackets:
        if num > largestInt:
            largestInt = num
    if largestInt > scr_height:
        multiplicator = scr_height / largestInt
    return multiplicator

def addNumber(number):
    global allPackets
    if len(allPackets) >= scr_widht:
        allPackets.pop(0)
    allPackets.append(number)
    return allPackets

def visualize():
    global allPackets
    global monitor_iface
    multiplicator = get_multiplicator()
    print(chr(27) + "[2J")
    graph = header(True) + "\n" + 80 * "-" + "\n"
    for index in reversed(range(1, scr_height + 1)):
        line = ""
        for num in allPackets:
            num *= multiplicator
            if num >= index:
                line = line + "#"
            else:
                line = line + " "
        graph = graph + line + "\n"
    graph += 80 * "-" + "\n"
    if sniffStarted:
        graph += str(allPackets[-1]) + " packets/sec - interface: " + \
        str(monitor_iface) + " - channel: " + str(channel) + "\n"
    print(graph)

def showESP():
    pass

def ifaceCounter(pckt):
    global ifacePackets
    ifacePackets += 1

def ifaceSniffer():
    import sys, logging
    logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
    from scapy.all import sniff
    global stoppingIface
    global monitor_iface
    global sniffStarted
    global sniffError
    while True:
        if not stoppingIface:
            try:
                sniffStarted = True
                sniff(iface=monitor_iface, prn=ifaceCounter)
            except:
                sniffError = True
                sys.exit()
        else:
            sys.exit()

def showIface():
    import time, threading
    global allPackets
    global stoppingIface
    global ifacePackets
    global sniffStarted
    global sniffError
    snifferthread = threading.Thread(target=ifaceSniffer)
    snifferthread.daemon = True
    snifferthread.start()
    curTs = int(round(time.time() * 1000))
    prevTs = int(round(time.time() * 1000))
    printedLoading = False
    while True:
        try:
            if sniffStarted:
                if sniffError:
                    print("[!] Something went wrong with the wireless interface. Exiting...")
                    stoppingIface = True
                    exit()
                curTs = int(round(time.time() * 1000))
                if curTs - prevTs > 1000:
                    prevTs = curTs
                    allPackets = addNumber(ifacePackets)
                    ifacePackets = 0
                    visualize()
            else:
                if not printedLoading:
                    print("\n[+] Starting WiFi Interface traffic visualizer...")
                    printedLoading = True
        except KeyboardInterrupt:
            print("\n[+] Exiting...")
            stoppingIface = True
            exit()


def showDemo():
    while True:
        number = random.randint(1, 500)
        allPackets = addNumber(number)
        visualize()
        time.sleep(0.1)

def header(toReturn=False):
    header = """
                      __        __  ______                 __
    ____  ____ ______/ /_____  / /_/ ____/________ _____  / /_
   / __ \/ __ `/ ___/ //_/ _ \/ __/ / __/ ___/ __ `/ __ \/ __ \\
  / /_/ / /_/ / /__/ ,< /  __/ /_/ /_/ / /  / /_/ / /_/ / / / /
 / .___/\__,_/\___/_/|_|\___/\__/\____/_/   \__,_/ .___/_/ /_/
/_/                                             /_/
"""
    if toReturn:
        return header
    print(header)

def menu():
    print("\n\t[1] - Show traffic from ESP")
    print("\t[2] - Show traffic from wireless interface")
    print("\t[3] - Show traffic from random numbers\n")
    option = input("menu> ")
    if option == "1":
        print("[+] Starting ESP traffic visualizer...")
        time.sleep(0.5)
        showESP()
    elif option == "2":
        global monitor_iface
        global channel
        print("\n[?] Please enter the name of your WiFi interface (in monitor mode):\n")
        monitor_iface = input("interface> ")
        print("\n[?] Please select which channel to use:\n")
        channel = input("channel> ")
        print("\n[+] Setting channel to " + str(channel) + "...")
        os.system("iwconfig " + monitor_iface + " channel " + str(channel))
        time.sleep(0.5)
        showIface()
    elif option == "3":
        print("[+] Starting Demo visualizer...")
        time.sleep(0.5)
        showDemo()
    else:
        print("[!] Please choose a number from the list.")
        menu()

header()
menu()
