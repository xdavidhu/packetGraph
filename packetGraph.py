import random, time
import os

scr_height = 15
scr_widht = 80
packets = []

def get_multiplicator():
    largestInt = 0
    multiplicator = 1
    for num in packets:
        if num > largestInt:
            largestInt = num
    if largestInt > scr_height:
        multiplicator = scr_height / largestInt
    return multiplicator

def addNumber(number):
    if len(packets) >= scr_widht:
        packets.pop(0)
    packets.append(number)
    return packets

def visualize():
    multiplicator = get_multiplicator()
    os.system("clear||cls")
    print(80 * "-")
    for index in reversed(range(1, scr_height + 1)):
        line = ""
        for num in packets:
            num *= multiplicator
            if num >= index:
                line = line + "#"
            else:
                line = line + " "
        print(line)
    print(80 * "-")

def showESP():
    pass

def showIface():
    pass

def showDemo():
    while True:
        number = random.randint(1, 500)
        allPackets = addNumber(number)
        visualize()
        time.sleep(0.1)

def header():
    header = """
                      __        __  ______                 __
    ____  ____ ______/ /_____  / /_/ ____/________ _____  / /_
   / __ \/ __ `/ ___/ //_/ _ \/ __/ / __/ ___/ __ `/ __ \/ __ \\
  / /_/ / /_/ / /__/ ,< /  __/ /_/ /_/ / /  / /_/ / /_/ / / / /
 / .___/\__,_/\___/_/|_|\___/\__/\____/_/   \__,_/ .___/_/ /_/
/_/                                             /_/
"""
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
        print("[+] Starting WiFi Interface traffic visualizer...")
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
