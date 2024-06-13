from lxml import etree as ET

internalID = "Items/AdamantiumWeaveVestFlavor"

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
tree = ET.parse('fixedXML.xml')
root = tree.getroot()
for entry in root.iterdescendants('entry'):
    targetStr = entry.get('name')
    if targetStr == internalID:
        objName = entry.get('value')
        print(objName)
        break