def pack_data(ip, line_no, pipeline_no, data):
    """pack data in communication frame

    Args:
        line_no (int): line number
        pipeline_no (int): pipeline number
        data (str): data to be sent

    Returns:
        bytes: packed data
    """ 
    from struct import pack
    packed = pack('<BBBBQB10s', ip[0], ip[1], ip[2], ip[3], line_no, pipeline_no, data)
    return packed

def pack_data_egd(protocol_no,
                  protocol_version,
                  request_id,
                  ip_address,
                  exchange_id,
                  timestamp,
                  status,
                  conf_sign,
                  reserved,
                  panel_no,
                  barcode_no,
                  station_no):

    from struct import pack
    packed = pack('<BBHBBBBIQIIIIBB',                  
                  protocol_no,
                  protocol_version,
                  request_id,
                  ip_address[0], ip_address[1], ip_address[2], ip_address[3],
                  exchange_id,
                  timestamp,
                  status,
                  conf_sign,
                  reserved,
                  panel_no,
                  barcode_no,
                  station_no)
    
    return packed  

