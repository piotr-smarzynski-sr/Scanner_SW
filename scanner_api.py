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
        serial_data = ser.read(13)        # read up to ten bytes (timeout)
        print('s: ', serial_data.decode())
    return serial_data