import os
import sys
import re
import html

def replaceChrs(matchobj: re.Match):
   name = matchobj.group(1)
   value = matchobj.group(2)
   value = html.escape(value, quote=False) # replace all prohibited characters with character entity references
   return f'<entry name="{name}" value="{value}"/>'

for dirpath, dirnames, filenames in os.walk(sys.argv[1]): # .\Zephon\English, .\scratch
   for filename in filenames:
      if filename.endswith(".xml"):
        filepath = os.path.join(dirpath, filename)
        print(filepath)
        with open(filepath, 'r', encoding='utf8') as file:
            filedata = file.readlines()

        with open(filepath, 'w', encoding='utf8') as file:
            for line in range(len(filedata)):
                filedata[line] = re.sub(r'^\s*<entry\sname=\"(.*?)\"\svalue=\"(.*)\"\/>$', replaceChrs, filedata[line])

        # Write the file out again
        with open(filepath, 'w', encoding='utf8') as file:
            file.writelines(filedata)