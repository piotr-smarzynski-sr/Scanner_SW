def pack_data(ip, line_no, machine_no, data):
    """pack data in communication frame

    Args:
        line_no (int): line number
        machine_no (int): machine number
        data (str): data to be sent

    Returns:
        bytes: packed data
    """ 
    from struct import pack
    #todo machine_no bedzie nazwane pipeline_no
    packed = pack('>BBBBQb10s', ip[0], ip[1], ip[2], ip[3], line_no, machine_no, data)
    return packed

