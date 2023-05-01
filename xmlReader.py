# import xml.etree.ElementTree as ET
# mytree = ET.parse('exported_01-05-2023.xml')
# myroot = mytree.getroot()
#

#print(myroot)
# print(myroot.tag)
# print(myroot[0].tag)
# for el in myroot[0][0]:
#     print(el)
# for x in myroot[0]:
#      print(x.tag, x.attrib,x.text)
def str_to_int(token):
    res = 0
    secret = 67
    for c in token:
        res *= secret
        res += ord(c)
    return str(res)[-6:]

s ="63d17ef7f15eb77270eb7cd003e1020c2d5ebb61"
code = str_to_int(s)
print(code)
#783063
# 646433