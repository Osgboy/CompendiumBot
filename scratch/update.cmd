python C:\Projects\GladiusBot\scratch\update.py

cd C:\Projects\GladiusBot\scratch\ddstronk\src\DDStronk
dotnet run Program.cs C:\Projects\GladiusBot\Zephon\Icons
dotnet run Program.cs C:\Projects\GladiusBot\Gladius\Icons
cd C:\Projects\GladiusBot\Zephon\Icons
del /S *.dds
cd C:\Projects\GladiusBot\Gladius\Icons
del /S *.dds

python C:\Projects\GladiusBot\scratch\fixXMLfiles.py C:\Projects\GladiusBot\Zephon\English
python C:\Projects\GladiusBot\scratch\fixXMLfiles.py C:\Projects\GladiusBot\Gladius\English