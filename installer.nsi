!define APPNAME "MAReK"
!define COMPANYNAME "YourName"
!define DESCRIPTION "PySide6 Scientific App"

!define SOURCE_DIR "dist\MAReK"

Name "${APPNAME}"
OutFile "${APPNAME}-Windows-Setup.exe"
InstallDir "$PROGRAMFILES64\${APPNAME}"
RequestExecutionLevel admin

Page directory
Page instfiles

Section "Install"
    SetOutPath "$INSTDIR"
    File /r "${SOURCE_DIR}\*"
    
    CreateShortcut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\MAReK.exe" "" "$INSTDIR\MAReK.exe" 0
    
    WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$DESKTOP\${APPNAME}.lnk"
    RMDir /r "$INSTDIR"
SectionEnd
