LINE_NO_SEARCH = 2
TEXT_SEARCH = 3
LINE_TEXT_BARCODE = 1

# barcode = "1-2-0105-0819"
barcode = "1-2-0003-1234"

parsed = barcode.split('-')
print('parsed: ', parsed)

line_no_search = int(parsed[LINE_NO_SEARCH])
text_search = parsed[TEXT_SEARCH]
print('line_no_search: ', line_no_search)
print('text_search: ', text_search)

# f = open("barcodes.txt", "r")
# print(f.read(5))

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
    line_text_parsed = line_text.split(' ')

    print('line_text_parsed[LINE_TEXT_BARCODE]:', line_text_parsed[LINE_TEXT_BARCODE])
    print('parsed[TEXT_SEARCH]:', parsed[TEXT_SEARCH])

    if int(line_text_parsed[LINE_TEXT_BARCODE]) == int(parsed[TEXT_SEARCH]):
        print("Barcode found in database!")
    else:
        print("Barcode NOT found in database!")