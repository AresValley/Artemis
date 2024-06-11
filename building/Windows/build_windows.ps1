Write-Output "Building Windows target"

Write-Output "Installing requirements ..."
pip install -r requirements.txt
pip install nuitka==2.3

Write-Output "Building with Nuitka ..."
python -m nuitka app.py `
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
  --include-data-files=.\artemis\resources.py=.\artemis\resources.py `
  --include-data-files=.\config\qtquickcontrols2.conf=.\config\qtquickcontrols2.conf `
  --force-stderr-spec="{TEMP}\artemis.err.log" `
  --force-stdout-spec="{TEMP}\artemis.out.log" `
  --windows-company-name=Aresvalley.com `
  --windows-product-name=Artemis `
  --windows-file-version=4.0.3 `
  --windows-product-version=4.0.3 `
  --windows-file-description=Artemis `
  --windows-icon-from-ico=images\artemis_icon.ico

Rename-Item -Path app.dist\app.exe -NewName artemis.exe

Write-Output "Building Windows target finished."
