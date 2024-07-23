from lxml import etree as ET
import time

tree = ET.parse('Zephon/Buildings/AcrinInfantry.xml')
root = tree.getroot()
start = time.time()

asdf = tree.find('modifiers').xpath('modifier[@visible]/effects/*')
#asdf = tree.xpath('/building/modifiers/modifier[not(@visible)]/effects')

print(time.time() - start)
print(ET.tostring(asdf[0]))
print(asdf)
for x in asdf:
    print(x)