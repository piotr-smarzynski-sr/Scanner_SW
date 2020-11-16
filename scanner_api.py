from colorama import Fore, init
from thread_print import s_print

init()

def scanBCR(com_port='COM3', baud=9600, timeout=10):
    """Use serial scanner to scan barcode

    Args:
        com_port (str): name of COM port. Defaults to COM3
        baud (int): baud rate. Defaults to 9600
        timeout (int): Timeout for scanning in seconds. Defaults to 10

    Returns:
        [type]: [description]
    """
    import serial
    with serial.Serial(com_port, baud, timeout=timeout) as ser:
        serial_data = ser.read(15)        # read up to ten bytes (timeout)
        s_print(Fore.RED, 'scanned: ', serial_data.decode(), Fore.RESET)
        # s_print(Fore.RED, 'type(serial_data): ', type(serial_data), Fore.RESET)
        # assert isinstance(serial_data, str), 'Not string'
        
    return serial_data.decode()