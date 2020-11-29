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
        serial_data = ser.read(18)        # read up to ten bytes (timeout)
        if serial_data != b'':
            s_print(Fore.RED, 'scanned: ', serial_data.decode(), Fore.RESET)
        
    return serial_data.decode()

def serialPorts():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    import sys
    import glob
    import serial
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result