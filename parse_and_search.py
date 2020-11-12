LINE_NO_SEARCH = 3
TEXT_SEARCH = 3
LINE_TEXT_BARCODE = 1

def parseBCR(barcode):
    """Parse scanned barcode

    Args:
        barcode (strong): input barcode

    Returns:
        int: number of line extracted from barcode
    """
    barcode = barcode.replace("*", "") # remove asterisks
    parsed = barcode.split('-')
    print('parsed: ', parsed)
    #jezeli indeks 2 jest poza zakresem 0-105 to etykieta jest bledna
    # sprawdzic ilosc czesci i poprawnosc znakow
    line_no_search = int(parsed[LINE_NO_SEARCH])

    return line_no_search
    

def searchLineFromBCR(line_no_search, filename):
    """Search and return line from given file

    Args:
        line (int): line number to be searched
        filename (file): text file to be searched
    """
    line_found = False
    line_text = ''
    with open(filename) as file_opened:
        for i, line in enumerate(file_opened):
            if i == line_no_search - 1: #one line offset
                line_text = line
                line_found = True

    if line_found is False:
        line_text = 'NOT_FOUND'

    return line_text
