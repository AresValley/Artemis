#!/usr/bin/env bash

echo "Building Linux target ..."

echo "Installing requirements ..."
pip install -r requirements.txt
pip install nuitka==2.3

echo "Building with Nuitka ..."
python -m nuitka app.py \
  --standalone \
  --follow-imports \
  --show-modules \
  --assume-yes-for-downloads \
  --enable-plugin=pyside6 \
  --noinclude-dlls=Qt6Charts* \
  --noinclude-dlls=Qt6Quick3D* \
  --noinclude-dlls=Qt6Sensors* \
  --noinclude-dlls=Qt6Test* \
  --noinclude-dlls=Qt6WebEngine* \
  --include-qt-plugins=sensible \
  --include-qt-plugins=styles \
  --include-qt-plugins=qml \
  --include-qt-plugins=multimedia \
  --include-data-files=./artemis/resources.py=./artemis/resources.py \
  --include-data-files=./config/qtquickcontrols2.conf=./config/qtquickcontrols2.conf \
  --include-data-files=./building/Linux/create_shortcut.sh=./create_shortcut.sh \
  --include-data-files=./images/artemis_icon.svg=./images/artemis_icon.svg \
  --force-stderr-spec="{TEMP}/artemis.err.log" \
  --force-stdout-spec="{TEMP}/artemis.out.log"

chmod 755 ./app.dist/app.bin

echo "Building Linux target finished."
