set base=C:\Users\olive\Documents\GitHub\CompendiumBot

python %base%\scratch\update.py %base%

cd %base%\scratch\ddstronk\src\DDStronk
dotnet run Program.cs %base%\Zephon\Icons
dotnet run Program.cs %base%\Gladius\Icons
cd %base%\Zephon\Icons
del /S *.dds
cd %base%\Gladius\Icons
del /S *.dds

python %base%\scratch\fixXMLfiles.py %base%\Zephon\English
python %base%\scratch\fixXMLfiles.py %base%\Gladius\English