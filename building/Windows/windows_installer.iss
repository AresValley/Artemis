#define MyAppName "Artemis"
#define MyAppVersion "4.1.0"
#define MyAppPublisher "AresValley"
#define MyAppURL "https://www.aresvalley.com/"
#define MyAppExeName "artemis.exe"

[Setup]
AppName={#MyAppName}
AppId={{2A04F9B8-0EF1-4D46-A335-E484DA6CE8A7}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=..\..\LICENSE
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=..\
OutputBaseFilename=Artemis
SetupIconFile=..\..\images\installer_icon.ico
Compression=lzma2/ultra64
SolidCompression=yes
VersionInfoVersion={#MyAppVersion}
ArchitecturesAllowed=x64
UninstallDisplayIcon={app}\{#MyAppExeName}
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\..\app.dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\app.dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{localappdata}\{#MyAppPublisher}\{#MyAppName}\cache"
Type: filesandordirs; Name: "{localappdata}\{#MyAppPublisher}\{#MyAppName}\config"
