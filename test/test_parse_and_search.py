LINE_NO_SEARCH = 3
TEXT_SEARCH = 3
LINE_TEXT_BARCODE = 1

# barcode = "1-2-0105-0819"
# barcode = "1-2-0003-1234"

barcode = "1-2-0003-0025"

parsed = barcode.split('-')
print('parsed: ', parsed)

line_no_search = int(parsed[LINE_NO_SEARCH])
# text_search = parsed[TEXT_SEARCH]
print('line_no_search: ', line_no_search)
# print('text_search: ', text_search)

line_found = False
line_text = ''
with open("barcodes.txt") as fp:
    for i, line in enumerate(fp):
        if i == line_no_search - 1: #one line offset
            line_text = line
            line_found = True

if line_found is True:
    print('line_found: ', line_found)
    print('line_text: ', line_text)



