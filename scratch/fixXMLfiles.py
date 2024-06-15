import os

# abspath = os.path.abspath(__file__)
# dname = os.path.dirname(abspath)
# os.chdir(dname)

for dirpath, dirnames, filenames in os.walk(".\Zephon\English"): # .\Gladius\English
   for filename in filenames:
      if filename.endswith(".xml"):
        filepath = os.path.join(dirpath, filename)
        print(filepath)
        with open(filepath, 'r', encoding='utf8') as file:
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace('"<', '"&lt;')
        filedata = filedata.replace("'/>", "'/&gt;")

        # Write the file out again
        with open(filepath, 'w', encoding='utf8') as file:
            file.write(filedata)