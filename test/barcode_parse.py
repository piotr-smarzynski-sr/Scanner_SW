barcode = "*1-2-0003-0027*"

barcode = barcode.replace("*", "") # remove asterisks
print('barcode: ', barcode)
barcode = barcode.replace(" ", "") # remove spaces
print('barcode: ', barcode)
parsed = barcode.split('-')
print('parsed: ', parsed)