from time import sleep

from udp_communication import get_ip, parse_ip, send_data
from data_packing import pack_data_egd
from file_handling import searchLineFromBCR, checkFile
from parse_and_search import parseBCR
from scanner_api import scanBCR
from thread_print import s_print

def scanning_loop(queue_output, com_port='COM3', baud=9600, timeout=10):
    serial_data = ''
    serial_data_last = ''
    while True:
        serial_data = scanBCR(com_port, baud, timeout)

        if serial_data != serial_data_last:
            queue_output.put(serial_data)

        serial_data_last = serial_data
        sleep(1)


def parse_and_send_loop(queue_input):
    packet_counter = 0
    barcode_counter = 0
    while True:
        barcode = ''
        if queue_input.empty() is False:
            barcode = queue_input.get()
            barcode_counter += 1
            if barcode_counter > 255:
                barcode_counter = 0
            s_print('barcode_counter: ', barcode_counter)

        line = parseBCR(barcode)
        s_print('line: ', line)

        text = searchLineFromBCR(line, 'barcodes.txt')
        s_print('text: ', text)

        ip_address = get_ip()
        ip_parsed = parse_ip(ip_address)
        # s_print('ip_parsed: ', ip_parsed)

        msg = pack_data_egd(13, 1, packet_counter, ip_parsed, 12, 0, 0, 0, 0, line, barcode_counter, 2)
        
        # s_print('msg: ', msg)

        send_data('192.168.254.92', 18246, msg) #dane muszą być wysyłane często, nawet 10/s, bo robot zerwie komunikację
        s_print('data sent')
        #todo zamknac w petle
        packet_counter += 1
        if packet_counter > 65535:
            packet_counter = 0
        sleep(1)


