Write-Output "Building Windows target"

Write-Output "Installing requirements ..."
pip install -r requirements.txt
pip install nuitka

Write-Output "Building with Nuitka ..."
python -m nuitka app.py `
  --standalone `
  --follow-imports `
  --show-modules `
  --assume-yes-for-downloads `
  --disable-console `
  --enable-plugin=pyside6 `
  --include-qt-plugins=sensible,styles,qml,multimedia `
  --include-data-files=.\artemis\resources.py=.\artemis\resources.py `
  --include-data-files=.\config\qtquickcontrols2.conf=.\config\qtquickcontrols2.conf `
  --windows-company-name=Aresvalley.com `
  --windows-product-name=Artemis `
  --windows-file-version=4.0.0 `
  --windows-product-version=4.0.0 `
  --windows-file-description=Artemis `
  --windows-icon-from-ico=images\artemis_icon.ico

Rename-Item -Path app.dist\app.exe -NewName artemis.exe

Write-Output "Building Windows target finished."
