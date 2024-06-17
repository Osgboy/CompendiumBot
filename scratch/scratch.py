from lxml import etree as ET

# def val2val(value: str) -> str:
#     if '<string name=' in value:
#         path = value[14:-3]
#         file, name = path.split('/', 1)
#         tree = ET.parse(ENGLISH_PATH + file + '.xml', parser=ET.XMLParser(recover=True, remove_comments=True))
#         xmlTree = tree.getroot()
#         for entry in xmlTree.iterdescendants('entry'):
#             if entry.get('name') == name:
#                 return entry.get('value')
#     else:
#         return value

#tree = ET.parse('testXML.xml', parser=ET.XMLParser(recover=True, remove_comments=True))
tree = ET.parse('./scratch/fixedXML.xml', parser=ET.XMLParser(recover=True, remove_comments=True))
root = tree.getroot()
modifiers = root.find('modifiers')
for entry in ET.tostringlist(modifiers, encoding='unicode'):
    print(entry)
    print('asfd')