#set text(size: 14pt)
= #text(font: "VictorMono NF", size: 34pt)[ MAReK ]

== Instalace pro Windows

Je pravděpodobné, že Windows bude protestovat ve formě varování před cizím software oknem typu: #quote()[Chcete aplikaci od neznámého vydavatele povolit, aby prováděla změny? ].
Stačí kliknout na tlačítko `Ano`.


1. Extrahovat `MAReK-Windows-Installer.zip`.
2. Spustit `MAReK-Windows-Setup.exe`.
3. V instalačním okně kliknout na tlačítko `Install`.
#image("screens/install-screen.png", width: 80%)
4. Poté co okno vypíše `Completed`, se na ploše objeví následující ikona s názvem `MAReK`.

#align(center)[
  #image("pyinstaller-icon.png", width: 50pt)
]

Během instalace se v `Destination Folder` (na ukázce je to `C:\Program Files\MAReK`) vytvoří i `uninstall.exe`, kterým je aplikaci možnost odinstalovat.

== Popis aplikace

#h(10pt)

#align(center)[
  #image("screens/app-annotated.png", width: 120%)
]

#h(10pt)

1. *Import a navigace* (Dolní lišta)
  - ⬅️,➡️-- přepínání mezi snímky
  - 📁-- otevírání nových snímků (lze vybrat více snímků najednou)
    - ve výběrníku jsou viditelné pouze `.png` a `.jpg` snímky
    - pro načtení anotací (`.npy` soubory), musí být ve stejném adresáři jako otevírané obrázky.
  - #text(font: "Adwaita Sans", size: 14pt)[ Image X of Y ] -- ukazuje celkový postup v sadě
2. *Nástroje* (Pravá lišta) - přepínání kliknutím na liště
  - ✋-- _Interakce_: posouvání snímku
  - ✏️-- _Anotace_: kreslení hranic
  - 🧹-- _Mazání_: odstraňování anotací
  - 💾-- _Uložení_: uložení anotací ve formátu `.npy` do adresáře ke snímku
3. *Pracovní plocha* (Střed)
  - zobrazení aktuálního snímku s anotacemi
  - lze přiblížit kolečkem myši

// == Workflow
// Import snímků (📁) #sym.arrow.r Pohyb po ploše (✋)/přiblížení (kolečko myši) \
// #sym.arrow.r Anotace (✏️)/mazání (🧹) #sym.arrow.r Uložení úprav (💾)
