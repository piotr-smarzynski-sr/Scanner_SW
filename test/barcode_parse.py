barcode = "*1-2-0003-0027*"

barcode = barcode.replace("*", "") # remove asterisks
print('barcode: ', barcode)
barcode = barcode.replace(" ", "") # remove spaces
barcode = barcode.replace("_R2", "") # remove spaces
print('barcode: ', barcode)
parsed = barcode.split('-')
print('parsed: ', parsed)