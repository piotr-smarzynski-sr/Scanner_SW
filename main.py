from parse_and_search import parseBCR
from scanner_api import scanBCR
import socket
from udp_communication import get_ip, parse_ip, send_data
from data_packing import pack_data, pack_data_egd
from file_handling import searchLineFromBCR, checkFile
from threading import Thread
from queue import Queue

#TODO argparse
'''
pipeline no
IP address of receiver
station_no

'''
checkFile('barcodes.txt')

packet_counter = 0
barcode_counter = 0
barcode = "*1-2-0003-0027*"
barcode = "*1-2-0003-0002*"
# barcode = scanBCR()
print('Scanning complete')

line = parseBCR(barcode)
print('line: ', line)

text = searchLineFromBCR(line, 'barcodes.txt')
print('text: ', text)

if text != 'NOT_FOUND':
    ip_address = get_ip()
    ip_parsed = parse_ip(ip_address)
    print('ip_parsed: ', ip_parsed)

    # msg = pack_data(ip_parsed, line, 2, text.encode())
    msg = pack_data_egd(13, 1, packet_counter, ip_parsed, 12, 0, 0, 0, 0, line, barcode_counter, 2)
    
    print('msg: ', msg)

    send_data('localhost', 50000, msg) #dane muszą być wysyłane często, nawet 10/s, bo robot zerwie komunikację
    print('data sent')
    #todo zamknac w petle