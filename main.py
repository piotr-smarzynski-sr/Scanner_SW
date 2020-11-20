"""Swiss Rotors Barcode scanner interface
Program scans barcodes, looks for data in file and send it via EGD protocol to Fanuc industrial robot.

Author: Piotr Smarzyński
"""
from barcode_parsing import parseBCR
from scanner_api import scanBCR, serialPorts
import socket
from udp_communication import get_ip, parse_ip, send_data
from data_packing import pack_data, pack_data_egd
from file_handling import searchLineFromBCR, checkFile
from threads import parse_and_send_loop, scanning_loop, gui_queue
from thread_print import s_print
from gui import gui

import argparse
from threading import Thread
from queue import Queue
from time import sleep

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-pipe' ,'--pipeline', type=int, default=7, help='Pipeline no. Defaults to 7.')
    parser.add_argument('-ip', '--ip_address', type=str, default='192.168.0.11', help='IP address of receiver. Defaults to 192.168.0.11')
    parser.add_argument('-s', '--station', type=int, default=1, help='Station no. Defaults to 1')
    parser.add_argument('-c', '--com_port', type=str, default='', help='COM port of scanner')
    parser.add_argument('-p', '--period', type=float, default=0.05, help='Time period to send data. Defaults to 0.05')
    parser.add_argument('-f', '--filename', type=str, default='barcodes.txt', help='Name of file to search in. Defaults to barcodes.txt')
    args = parser.parse_args()

    barcode_queue = Queue()
    checkFile(args.filename)
    com_ports = serialPorts()
    print('Active COM ports: ', com_ports)
    if args.com_port == '':
        com_port = com_ports[0]
    else:
        print('Forced COM port:', args.com_port)
        com_port = args.com_port

    threads = []
    threads.append(Thread(name="scanning_loop",
                        target=scanning_loop, 
                        kwargs={'queue_output': barcode_queue,
                                'com_port': com_port,
                                'baud':9600, 
                                'timeout':10},
                        daemon=True))

    threads.append(Thread(name="parse_and_send_loop",
                        target=parse_and_send_loop,
                        kwargs={'queue_input': barcode_queue,
                                'ip_address_dest': args.ip_address,
                                'station_no': args.station,
                                'pipeline': args.pipeline,
                                'filename': args.filename,
                                'period': args.period},
                        daemon=True))

    threads.append(Thread(name="gui",
                        target=gui,
                        kwargs={},
                        daemon=True))

    for thread in threads:
        thread.start()
        s_print('Thread', thread.name, 'started!')

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        s_print("Exiting program")


    #TODO close nicely
    