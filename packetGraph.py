import random, time, pyshark
import os

# VISUALIZER VARIABLES
scr_height = 15
scr_widht = 80
allPackets = []
# IFACE SNIFFER VARIABLES
ifacePackets = 0
ifaceChannel = ""
monitor_iface = ""
stoppingIface = False
sniffStarted = False
sniffError = False
# ESP VARTIABLES
serialport = ""
boardRate = 0
ser = ""
espChannel = 1
espStarted = False
stoppingEsp = False

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
            if num == 0:
                num = 1
            if num >= index:
                line = line + "#"
            else:
                line = line + " "
        graph = graph + line + "\n"
    graph += 80 * "-" + "\n"
    if sniffStarted:
        graph += str(allPackets[-1]) + " packets/sec - interface: " + \
        str(monitor_iface) + " - channel: " + str(ifaceChannel) + "\n"
    elif espStarted:
        global ser
        graph += str(allPackets[-1]) + " packets/sec - connection: " + \
        str(ser.name) + " - channel: " + str(espChannel) + "\n"
    print(graph)

def showESP():
    try:
        import serial
    except ImportError:
        print("\n[!] Package 'Pyserial' not found... Make sure to install the requirements with 'pip3 install -r requirements.txt'.")
        exit()
    canBreak = False
    global serialport
    global boardRate
    global ser
    global allPackets
    global espStarted
    global espChannel
    print("\n[+] Connecting to device...")
    while not canBreak:
        try:
            ser = serial.Serial(serialport, boardRate)
            canBreak = True
        except KeyboardInterrupt:
            print("\n[+] Exiting...")
            exit()
        except:
            print("[!] Serial connection failed... Retrying...")
            time.sleep(2)
            continue
    print("[+] Serial connected. Name: " + ser.name)
    espStarted = True
    ser.write(espChannel.encode())
    try:
        while True:
            packet = ser.readline().decode("utf-8")
            packet = packet.replace("\r\n", "")
            try:
                packet = int(packet)
            except:
                print("[!] Recived corrupted serial input... Exiting...")
                exit()
            allPackets = addNumber(packet)
            visualize()
    except KeyboardInterrupt:
        print("\n[+] Exiting...")
        exit()
    except:
        print("\n[!] Serial disconnected... Exiting...")
        exit()

def ifaceCounter(pkt):
    global ifacePackets
    ifacePackets += 1

def ifaceSniffer():
    global sniffError
    global stoppingIface
    global monitor_iface
    global sniffStarted
    if not stoppingIface:
        try:
            capture = pyshark.LiveCapture(interface=monitor_iface)
            sniffStarted = True
            capture.apply_on_packets(ifaceCounter)
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
                if sniffError:
                    stoppingIface = True
                    exit()
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
                              v1.0 by David Schütz (@xdavidhu)
"""
    if toReturn:
        return header
    print(header)

def menu():
    print("\n\t[1] - Show traffic from ESP")
    print("\t[2] - Show traffic from wireless interface")
    print("\t[3] - Show traffic from random numbers\n")
    try:
        option = input("menu> ")
    except KeyboardInterrupt:
        print("\n[+] Exiting...")
        exit()
    if option == "1":
        global serialport
        print("\n[!] Make sure that you flashed your ESP with @Spacehuhn's code!\n\thttps://github.com/spacehuhn")
        try:
            print("\n[?] Please select a serial port (default '/dev/ttyUSB0')\n")
            serialportInput = input("serial-port> ")
            if serialportInput == "":
                serialport = "/dev/ttyUSB0"
            else:
                serialport = serialportInput
            print("[+] Serial port => '" + str(serialport) + "'")
        except KeyboardInterrupt:
            print("\n[+] Exiting...")
            exit()
        try:
            global boardRate
            canBreak = False
            while not canBreak:
                print("\n[?] Please select a baudrate (default '115200')\n")
                boardRateInput = input("baudrate> ")
                if boardRateInput == "":
                    boardRate = 115200
                    canBreak = True
                else:
                    try:
                        boardRate = int(boardRateInput)
                    except KeyboardInterrupt:
                        print("\n[+] Exiting...")
                        exit()
                    except Exception as e:
                        print("\n[!] Please enter a number!")
                        continue
                    canBreak = True
                print("[+] Baudrate => '" + str(boardRate) + "'")
        except KeyboardInterrupt:
            print("\n[+] Exiting...")
            exit()
        try:
            global espChannel
            canBreak = False
            while not canBreak:
                print("\n[?] Please select which channel to use:\n")
                espChannelInput = input("channel> ")
                if espChannelInput == "":
                    print("\n[!] Please enter a number!")
                    continue
                else:
                    try:
                        espChannel = int(espChannelInput)
                        espChannel = str(espChannelInput)
                    except KeyboardInterrupt:
                        print("\n[+] Exiting...")
                        exit()
                    except Exception as e:
                        print("\n[!] Please enter a number!")
                        continue
                    canBreak = True
                print("[+] Channel => '" + str(espChannel) + "'")
        except KeyboardInterrupt:
            print("\n[+] Exiting...")
            exit()
        time.sleep(0.5)
        showESP()
    elif option == "2":
        global monitor_iface
        global ifaceChannel
        try:
            print("\n[?] Please enter the name of your WiFi interface (in monitor mode):\n")
            monitor_iface = input("interface> ")
            print("[+] Monitor interface => '" + str(monitor_iface) + "'")
        except KeyboardInterrupt:
            print("\n[+] Exiting...")
            exit()
        try:
            print("\n[?] Please select which channel to use:\n")
            ifaceChannel = input("channel> ")
            print("[+] Channel => '" + str(ifaceChannel) + "'")
        except KeyboardInterrupt:
            print("\n[+] Exiting...")
            exit()
        print("\n[+] Setting channel to " + str(ifaceChannel) + "...")
        os.system("iwconfig " + monitor_iface + " channel " + str(ifaceChannel))
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
