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
    parsed = barcode.split('-')
    if len(parsed) == 4:
        for index, part in enumerate(parsed):
            if part.isnumeric() is False:
                print('Part', index + 1, 'of barcode is not numeric:', part)

        print('parsed: ', parsed)
        #jezeli indeks 2 jest poza zakresem 0-105 to etykieta jest bledna
        # sprawdzic ilosc czesci i poprawnosc znakow
        label_correct = int(parsed[LABEL_CORRECT])
        if label_correct >= 0 and label_correct <= 105:
            line_no_search = int(parsed[LINE_NO_SEARCH])

        return line_no_search
    
    else:
        print('Wrong barcode scanned!')
        return -1
    
