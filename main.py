from parse_and_search import parseBCR
from scanner_api import scanBCR
import socket
from udp_communication import get_ip, parse_ip, send_data
from data_packing import pack_data, pack_data_egd
from file_handling import searchLineFromBCR, checkFile
from threads import parse_and_send_loop, scanning_loop

from threading import Thread
from queue import Queue
from time import sleep


#TODO argparse
'''
pipeline no
IP address of receiver
station_no
'''

barcode_queue = Queue()
checkFile('barcodes.txt')


threads = []
threads.append(Thread(name="scanning_loop",
                      target=scanning_loop, 
                      kwargs={'queue_output': barcode_queue,
                              'com_port':'COM3',
                              'baud':9600, 
                              'timeout':10},
                      daemon=True))

threads.append(Thread(name="parse_and_send_loop",
                      target=parse_and_send_loop,
                      args=(barcode_queue,),
                      daemon=True))


for thread in threads:
    thread.start()
    print('thread', thread.name, 'started!')



while True:
    sleep(1)
    