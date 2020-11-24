from thread_print import s_print

LINE_NO_SEARCH = 3
LABEL_CORRECT = 2
TEXT_SEARCH = 3
LINE_TEXT_BARCODE = 1
BARCODE_EXPECTED_PARTS = 4

def parseBCR(barcode):
    """Parse scanned barcode

    Args:
        barcode (strong): input barcode

    Returns:
        int: number of line extracted from barcode
    """
    line_no_search = 0
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

        return line_no_search
    
    else:
        # s_print('Wrong barcode scanned!')
        return 0
    
