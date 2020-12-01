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
import sys
from colorama import Fore, init

def main():
    init() #colorama
    parser = argparse.ArgumentParser()
    parser.add_argument('-pipe' ,'--pipeline', type=int, default=7, help='Pipeline no. Defaults to 8.')
    parser.add_argument('-pipe2' ,'--pipeline2', type=int, default=8, help='Pipeline no. Defaults to 7.')
    parser.add_argument('-ip', '--ip_address', type=str, default='192.168.0.12', help='IP address of 1st receiver. Defaults to 192.168.0.10')
    parser.add_argument('-ip2', '--ip_address2', type=str, default='192.168.0.11', help='IP address of 2nd receiver. Defaults to 192.168.0.11')
    parser.add_argument('-s', '--station', type=int, default=0, help='Station no. Defaults to 0')
    parser.add_argument('-s2', '--station2', type=int, default=1, help='Station no. Defaults to 1')
    parser.add_argument('-c', '--com_port', type=str, help='COM port of 1st scanner. Defaults to COM8')
    parser.add_argument('-c2', '--com_port2', type=str, help='COM port of 2nd scanner. Defaults to COM9')
    parser.add_argument('-p', '--period', type=float, default=0.05, help='Time period to send data over EGD protocol. Defaults to 0.05')
    parser.add_argument('-f', '--filename', type=str, default='barcodes.txt', help='Name of file to search in. Defaults to barcodes.txt')
    args = parser.parse_args()

    barcode_queue = Queue()
    checkFile(args.filename)
    com_ports = serialPorts()
    print('Active COM ports: ', com_ports)
    if len(com_ports) == 0:
        print(Fore.LIGHTRED_EX+ "No devices connected! Check USB connection of the scanner.", Fore.RESET)
        sys.exit()

    if args.com_port is None:
        com_port = com_ports[0]
    else:
        print('Forced COM port 1:', args.com_port)
        com_port = args.com_port

    if args.com_port2 is None:

        com_port2 = com_ports[1]
    else:
        print('Forced COM port 2:', args.com_port2)
        com_port2 = args.com_port2

    threads = []
    threads.append(Thread(name="scanning_loop",
                        target=scanning_loop, 
                        kwargs={'queue_output': barcode_queue,
                                'com_port': com_port,
                                'baud':9600, 
                                'timeout':10},
                        daemon=True))

    threads.append(Thread(name="scanning_loop",
                        target=scanning_loop, 
                        kwargs={'queue_output': barcode_queue,
                                'com_port': com_port2,
                                'baud':9600, 
                                'timeout':10},
                        daemon=True))

    threads.append(Thread(name="parse_and_send_loop",
                        target=parse_and_send_loop,
                        kwargs={'queue_input': barcode_queue,
                                'ip_address_dest': [args.ip_address, args.ip_address2],
                                'station_nos': [args.station, args.station2],
                                'pipelines': [args.pipeline, args.pipeline2],                                
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

if __name__ == "__main__":
    main()    
    