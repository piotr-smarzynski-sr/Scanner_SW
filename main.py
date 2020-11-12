from parse_and_search import parseBCR, searchLineFromBCR
from scanner_api import scanBCR
import socket
from udp_communication import get_ip, parse_ip, send_data
from data_packing import pack_data

#TODO argparse
'''
pipeline no
IP address of receiver
station_no

'''

barcode = "*1-2-0003-0027*"
# barcode = scanBCR()
print('Scanning complete')

line = parseBCR(barcode)
print('line: ', line)

#todo dodac znaczniki linii zakonczone znakiem specjalnym do pliku barcodes
text = searchLineFromBCR(line, 'barcodes.txt')
print('text: ', text)

if text != 'NOT_FOUND':
    ip_address = get_ip()
    ip_parsed = parse_ip(ip_address)
    print('ip_parsed: ', ip_parsed)

    msg = pack_data(ip_parsed, line, 2, text.encode())
    print('msg: ', msg)

    send_data('localhost', 50000, msg) #dane muszą być wysyłane często, nawet 10/s, bo robot zerwie komunikację
    print('data sent')
    #todo zamknac w petle