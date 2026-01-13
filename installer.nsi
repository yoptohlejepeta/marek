!include "MUI2.nsh"

Name "MAReK Image Annotator"
OutFile "deployment\MAReK-Installer.exe"
InstallDir "$PROGRAMFILES\MAReK"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"

Section "Install"
    SetOutPath "$INSTDIR"
    File /r "deployment\MAReK\*.*" 
    
    CreateShortCut "$DESKTOP\MAReK.lnk" "$INSTDIR\MAReK.exe"
    WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$DESKTOP\MAReK.lnk"
    RMDir /r "$INSTDIR"
SectionEnd
