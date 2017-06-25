from scapy import *
import time, threading

curTs = int(round(time.time() * 1000))
prevTs = int(round(time.time() * 1000))
packets = 0
stopping = False
sniffStarted = False
monitor_iface = input("Interface name: ")

def counter(pckt):
    global packets
    packets += 1

def sniffer():
    from scapy.all import sniff
    global stopping
    global monitor_iface
    global sniffStarted
    while True:
        if not stopping:
            try:
                sniffStarted = True
                sniff(iface=monitor_iface, prn=counter)
            except:
                print("[!] An error occurred. Debug:")
                time.sleep(5)
        else:
            sys.exit()

snifferthread = threading.Thread(target=sniffer)
snifferthread.daemon = True
snifferthread.start()

def main():
    packets = 0
    while True:
        if sniffStarted:
            curTs = int(round(time.time() * 1000))
            if curTs - prevTs > 1000:
                prevTs = curTs
                return(packets)
