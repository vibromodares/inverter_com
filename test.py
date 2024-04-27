# print(type(asd))


# asd = chr('ENQ')
ENQ = chr(5)
EOT = chr(4)

asd = bytes(ENQ + '01R000073' + EOT, 'utf-8')
print(asd)
