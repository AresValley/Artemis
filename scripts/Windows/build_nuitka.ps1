$VERSION = "4.1.1"

Write-Output "Building Windows target"

Write-Output "Install building dependencies ..."
uv add 'nuitka==4.1.2'

Write-Output "Compiling resources ..."
uv run pyside6-rcc ./artemis.qrc -o artemis/resources.py

Write-Output "Building with Nuitka ..."
uv run --python 3.13 nuitka `
  --python-flag=-m artemis `
  --standalone `
  --show-modules `
  --assume-yes-for-downloads `
  --windows-console-mode=disable `
  --enable-plugin=pyside6 `
  --noinclude-dlls="Qt6Charts*" `
  --noinclude-dlls="Qt6Quick3D*" `
  --noinclude-dlls="Qt6Sensors*" `
  --noinclude-dlls="Qt6Test*" `
  --noinclude-dlls="Qt6WebEngine*" `
  --include-qt-plugins=styles `
  --include-qt-plugins=qml `
  --include-qt-plugins=multimedia `
  --include-data-files=.\config\qtquickcontrols2.conf=.\config\qtquickcontrols2.conf `
  --force-stderr-spec="{TEMP}\artemis.err.log" `
  --force-stdout-spec="{TEMP}\artemis.out.log" `
  --windows-company-name=Aresvalley.com `
  --windows-product-name=Artemis `
  --windows-file-version=$VERSION `
  --windows-product-version=$VERSION `
  --windows-file-description=Artemis `
  --windows-icon-from-ico=data\images\artemis_icon.ico

Write-Output "Building Windows target finished."
