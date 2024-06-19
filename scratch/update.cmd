python c:\Users\Oliver\Downloads\GladiusBot\scratch\update.py

cd C:\Users\Oliver\Downloads\GladiusBot\scratch\ddstronk\src\DDStronk
dotnet run Program.cs C:\Users\Oliver\Downloads\GladiusBot\Zephon\Icons
dotnet run Program.cs C:\Users\Oliver\Downloads\GladiusBot\Gladius\Icons
cd C:\Users\Oliver\Downloads\GladiusBot\Zephon\Icons
del /S *.dds
cd C:\Users\Oliver\Downloads\GladiusBot\Gladius\Icons
del /S *.dds

python C:\Users\Oliver\Downloads\GladiusBot\scratch\fixXMLfiles.py C:\Users\Oliver\Downloads\GladiusBot\Zephon\English
python C:\Users\Oliver\Downloads\GladiusBot\scratch\fixXMLfiles.py C:\Users\Oliver\Downloads\GladiusBot\Gladius\English