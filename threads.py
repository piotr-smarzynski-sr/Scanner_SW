from time import sleep

from udp_communication import get_ip, parse_ip, send_data
from data_packing import pack_data_egd
from file_handling import searchLineFromBCR, checkFile
from barcode_parsing import parseBCR
from scanner_api import scanBCR
from thread_print import s_print

PROTOCOL_NO = 13
PROTOCOL_VERSION = 1
TIMESTAMP = 0
STATUS = 0
CONF_SIGNATURE = 0
RESERVED = 0

def scanning_loop(queue_output, com_port='COM3', baud=9600, timeout=10):
    """Thread definition - barcode scanning

    Args:
        queue_output (Queue): Queue for communicating with sending thread
        com_port (str, optional): COM port address of scanner. Defaults to 'COM3'.
        baud (int, optional): COM port baud. Defaults to 9600.
        timeout (int, optional): Scanner timeout. Defaults to 10.
    """
    serial_data = ''
    serial_data_last = ''
    while True:
        serial_data = scanBCR(com_port, baud, timeout)

        if serial_data != serial_data_last and serial_data != '':
            queue_output.put(serial_data)

        serial_data_last = serial_data
        sleep(1)


def parse_and_send_loop(queue_input, ip_address_dest, station_no, pipeline, period):
    """Thread definition - sending data

    Args:
        queue_input (Queue): Queue with barcodes to send
        ip_address_dest (str): IP address of receiver
        station_no (int): No of station
        pipeline (int): No of pipeline
        period (float): Period of time to send data is seconds
    """
    packet_counter = 0
    barcode_counter = 0
    barcode = ''
    line = 0
    while True:        
        if queue_input.empty() is False:
            barcode = queue_input.get()
            barcode_counter += 1
            if barcode_counter > 255:
                barcode_counter = 0
            s_print('barcode_counter: ', barcode_counter)
            line = parseBCR(barcode)
            s_print('line: ', line)

        text = searchLineFromBCR(line, 'barcodes.txt')
        if text != 'NOT_FOUND':
            s_print('text: ', text)

        ip_address = get_ip()
        ip_parsed = parse_ip(ip_address)

        msg = pack_data_egd(PROTOCOL_NO, 
                            PROTOCOL_VERSION, 
                            packet_counter, 
                            ip_parsed, 
                            pipeline, 
                            TIMESTAMP, 
                            STATUS, 
                            CONF_SIGNATURE, 
                            RESERVED, 
                            line, 
                            barcode_counter, 
                            station_no)
        
        s_print('msg: ',PROTOCOL_NO, 
                        PROTOCOL_VERSION, 
                        packet_counter, 
                        ip_parsed, 
                        pipeline, 
                        TIMESTAMP, 
                        STATUS, 
                        CONF_SIGNATURE, 
                        RESERVED, 
                        line, 
                        barcode_counter, 
                        station_no)

        send_data(ip_address_dest, 18246, msg) #dane muszą być wysyłane często, nawet 10/s, bo robot zerwie komunikację

        packet_counter += 1
        if packet_counter > 65535:
            packet_counter = 0
        sleep(period)


