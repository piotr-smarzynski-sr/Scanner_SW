from time import sleep

from udp_communication import get_ip, parse_ip, send_data
from data_packing import pack_data_egd
from file_handling import searchLineFromBCR, checkFile
from barcode_parsing import parseBCR
from scanner_api import scanBCR
from thread_print import s_print

from queue import Queue

from serial import SerialException

PROTOCOL_NO = 13
PROTOCOL_VERSION = 1
TIMESTAMP = 0
STATUS = 0
CONF_SIGNATURE = 0
RESERVED = 0

gui_queue = Queue()

def scanning_loop(queue_output, com_port='COM8', baud=9600, timeout=10):
    """Thread definition - barcode scanning

    Args:
        queue_output (Queue): Queue for communicating with sending thread
        com_port (str, optional): COM port address of scanner. Defaults to 'COM3'.
        baud (int, optional): COM port baud. Defaults to 9600.
        timeout (int, optional): Scanner timeout. Defaults to 10.
    """
    serial_data = ''
    while True:
        try:
            serial_data = scanBCR(com_port, baud, timeout)
        except SerialException:
            s_print('Could not open port', com_port)
            sleep(10)            

        if serial_data != '':
            queue_output.put((serial_data, com_port))

        sleep(1)


def parse_and_send_loop(queue_input, ip_address_dest, station_nos, pipeline, filename, period):
    """Thread definition - sending data

    Args:
        queue_input (Queue): Queue with barcodes to send
        ip_address_dest (str): IP address of receiver
        station_no (int): No of station
        pipeline (int): No of pipeline
        period (float): Period of time to send data in seconds
    """
    packet_counters = [0, 0]
    barcode_counters = [0, 0]
    barcode = ''
    lines = [0, 0]
    newlines = [0, 0]
    texts = ['', '']
    ip_address_local = get_ip()
    ip_parsed_local = parse_ip(ip_address_local)
    msgs = [None, None]
    while True:        
        if queue_input.empty() is False:
            barcode, com_port = queue_input.get()
            newline, station = parseBCR(barcode)

            newlines[station] = newline
            station_no = station
            texts[station] = searchLineFromBCR(newlines[station], filename)
            if newlines[station] != 0:
                barcode_counters[station] += 1
                if barcode_counters[station] > 255:
                    barcode_counters[station] = 0
                lines[station] = newlines[station]

            gui_queue.put([barcode,
                        texts[station],
                        packet_counters[station], 
                        ip_parsed_local, 
                        pipeline,
                        lines[station], 
                        barcode_counters[station], 
                        station_no
                        ]) 

        msgs[0] = pack_data_egd(PROTOCOL_NO, 
                            PROTOCOL_VERSION, 
                            packet_counters[0], 
                            ip_parsed_local, 
                            pipeline, 
                            TIMESTAMP, 
                            STATUS, 
                            CONF_SIGNATURE, 
                            RESERVED, 
                            lines[0], 
                            barcode_counters[0], 
                            station_nos[0])   

        msgs[1] = pack_data_egd(PROTOCOL_NO, 
                            PROTOCOL_VERSION, 
                            packet_counters[1], 
                            ip_parsed_local, 
                            pipeline, 
                            TIMESTAMP, 
                            STATUS, 
                            CONF_SIGNATURE, 
                            RESERVED, 
                            lines[1], 
                            barcode_counters[1], 
                            station_nos[1])

        send_data(ip_address_dest[0], 18246, msgs[0]) #dane muszą być wysyłane często, nawet 10/s, bo robot zerwie komunikację
        send_data(ip_address_dest[1], 18246, msgs[1]) #dane muszą być wysyłane często, nawet 10/s, bo robot zerwie komunikację

        packet_counters[0] += 1
        if packet_counters[0] > 65535:
            packet_counters[0] = 0
        
        packet_counters[1] += 1
        if packet_counters[1] > 65535:
            packet_counters[1] = 0
        sleep(period)
