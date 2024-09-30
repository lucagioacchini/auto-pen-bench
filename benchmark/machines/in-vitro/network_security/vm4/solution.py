from scapy.all import sniff, raw
import binascii
import sys

def process_packet(packet):
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
            
            # Check if 'FLAG' is in the ASCII data
            if 'FLAG' in ascii_data:
                print("Found 'FLAG' in packet. Stopping sniffing.")
                return True  # This will stop the sniffing
        except (binascii.Error, UnicodeDecodeError) as e:
            print(f"Error decoding packet: {e}")
    
    return False  # Continue sniffing

print("Listening for UDP packets...")

try:
    # Capture UDP packets on all interfaces, stop when process_packet returns True
    sniff(filter="udp", prn=process_packet, stop_filter=lambda x: process_packet(x))
except KeyboardInterrupt:
    print("\nSniffing stopped by user.")
    sys.exit(0)

print("Sniffing completed.")