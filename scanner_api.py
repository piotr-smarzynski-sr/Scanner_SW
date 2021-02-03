from colorama import Fore, init
from thread_print import s_print

init()

def scanBCR(com_port='/dev/ttyUSB0', baud=9600, timeout=10):
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
        serial_data = ser.read(18)        # read up to 18 bytes (timeout)
        if serial_data != b'':
            # s_print(Fore.RED, 'scanned: ', serial_data.decode(), Fore.RESET)
            pass
    try:   
        return serial_data.decode()        
    except UnicodeDecodeError:
        print('Scanner exception! Serial_data: ', serial_data)
        return ''

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
        
        #import subprocess
      #  for port in ports:
      #      bashCommand = "sudo chmod 777 " + str(port)            
      #      process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
       #     output, error = process.communicate()
        
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port, 9600)
            s.bytesize = serial.EIGHTBITS
            s.parity = serial.PARITY_NONE
            s.stopbits = serial.STOPBITS_TWO
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result