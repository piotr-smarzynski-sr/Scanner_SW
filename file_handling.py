NO_INDEX = 0
TEXT_INDEX = 1

NUMBER_SAVED_INDEX = 0
ACTUAL_LINE_NUMBER_INDEX = 1

def searchLineFromBCR(line_no_search, filename):
    """Search and return line from given file

    Args:
        line (int): line number to be searched
        filename (file): text file to be searched
    """
    line_found = False
    line_text = ''
    with open(filename) as file_opened:
        for line in file_opened:
            if line[0].isnumeric() and '$' in line:
                line_parsed = line.split('$')
                if int(line_parsed[NO_INDEX]) == line_no_search: #one line offset
                    line_text = line_parsed[TEXT_INDEX]
                    line_found = True

    if line_found is False:
        line_text = 'NOT_FOUND'

    return line_text

def checkFile(filename):
    """Check file for correct syntax and line numbering

    Args:
        filename (str): name of checked file
    """
    print('File check:', filename, 'start.')
    line_numbers = []
    with open(filename) as file_opened:
        for line_no, line in enumerate(file_opened):
            if line[0].isnumeric() and '$' in line: # check if lines are incrementally numbered
                line_parsed = line.split('$')
                line_numbers.append((int(line_parsed[NO_INDEX]), line_no + 1))

            else:
                print('Incorrect syntax in line', line_no + 1)

        last_number = 0
        for number_saved, line_number in line_numbers:
            if last_number != number_saved - 1:
                print('Incorrect numbering in line', line_number, ':', number_saved, 'after', last_number)
            last_number = number_saved

    print('File', filename, 'checked\n')



            