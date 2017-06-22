#for index in range(len(list))
# print (80 * "-")
# for i in range(15):
#     print()
# print (80 * "-")
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

while True:
    number = random.randint(1, 500)
    allPackets = addNumber(number)
    visualize()
    time.sleep(0.1)
