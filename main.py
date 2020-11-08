import serial
with serial.Serial('COM14', 9600, timeout=10) as ser:
    s = ser.read(13)        # read up to ten bytes (timeout)
    print('s: ', s)
