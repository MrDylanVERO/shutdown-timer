[Setup]
AppId={{8B3F963A-9A35-44F2-A6E4-72E8B941225F}
AppName=Shutdown Timer
AppVersion=2.0.1
DefaultDirName={localappdata}\Programs\Shutdown Timer
DefaultGroupName=Shutdown Timer
PrivilegesRequired=lowest
OutputDir=installer
OutputBaseFilename=Shutdown-Timer-Setup
SetupIconFile=logo.ico
UninstallDisplayIcon={app}\Shutdown-Timer.exe
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\Shutdown-Timer.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Shutdown Timer"; Filename: "{app}\Shutdown-Timer.exe"
Name: "{autodesktop}\Shutdown Timer"; Filename: "{app}\Shutdown-Timer.exe"; Tasks: desktopicon

[Registry]
Root: HKA; Subkey: "Software\ShutdownTimer"; ValueType: string; ValueName: "Language"; ValueData: "{language}"; Flags: uninsdeletekey

[Run]
Filename: "{app}\Shutdown-Timer.exe"; Description: "{cm:LaunchProgram,Shutdown Timer}"; Flags: nowait postinstall skipifsilent
