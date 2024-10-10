[Setup]
AppName=WareHouse2.0
AppVersion=0.0.1
DefaultDirName={pf}\WareHouse2.0
DefaultGroupName=WareHouse2.0
OutputDir=..\..\out
OutputBaseFilename=WareHouse2.0_Installer
Compression=lzma
SolidCompression=yes
DisableDirPage=no
PrivilegesRequired=admin
UsePreviousAppDir=no

[Files]
Source: "dist\client\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\WareHouse2.0"; Filename: "{app}\client.exe"
Name: "{userdesktop}\WareHouse2.0"; Filename: "{app}\client.exe"

[Registry]
Root: HKCU; Subkey: "Software\MyClientApp"; ValueType: string; ValueName: "Install_Dir"; ValueData: "{app}"; Flags: uninsdeletevalue

[Run]
Filename: "{app}\client.exe"; Description: "Launch WareHouse2.0"; Flags: nowait postinstall skipifsilent
