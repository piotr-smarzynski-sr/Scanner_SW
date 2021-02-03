from thread_print import s_print

LINE_NO_SEARCH = 3
LABEL_CORRECT = 2
TEXT_SEARCH = 3
LINE_TEXT_BARCODE = 1
BARCODE_EXPECTED_PARTS = 4

def parseBCR(barcode_raw):
    """Parse scanned barcode

    Args:
        barcode (strong): input barcode

    Returns:
        int: number of line extracted from barcode
    """

    barcode_station = barcode_raw.split('_')
    print('barcode_station: ', barcode_station)

    if len(barcode_station) == 2:
        # print('barcode_station: ', barcode_station)
        if barcode_station[1][0] == 'S':
            try:
                station = int(barcode_station[1][1:])
                # if barcode_station[1] == 'S0':
                #     station = 0
                # if barcode_station[1] == 'S1':
                #     station = 1
                
                line_no_search = 0
                barcode = barcode_station[0]
                barcode = barcode.replace("*", "") # remove asterisks
                barcode = barcode.replace(" ", "") # remove spaces
                barcode = barcode.replace("_R2", "") # remove suffix
                parsed = barcode.split('-')
                if len(parsed) == BARCODE_EXPECTED_PARTS:
                    for index, part in enumerate(parsed):
                        if part.isnumeric() is False and part != '':
                            s_print('Part', index + 1, 'of barcode is not numeric:', part)

                    # s_print('parsed: ', parsed)
                    label_correct = int(parsed[LABEL_CORRECT])
                    if label_correct == 105:
                        line_no_search = int(parsed[LINE_NO_SEARCH][:4])

                    return line_no_search, station
                
                else:
                    # s_print('Wrong barcode scanned!')
                    return 0, 0
            except:
                return 0, 0

    elif len(barcode_station) != 2:
        return 0,0
    
