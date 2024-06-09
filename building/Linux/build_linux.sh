#!/usr/bin/env bash

echo "Building Linux target ..."

echo "Installing requirements ..."
pip install -r requirements.txt
pip install nuitka==2.3.1

echo "Building with Nuitka ..."
python -m nuitka app.py \
  --standalone \
  --follow-imports \
  --show-modules \
  --assume-yes-for-downloads \
  --enable-plugin=pyside6 \
  --force-stderr-spec="{TEMP}/artemis.err.log" \
  --force-stdout-spec="{TEMP}/artemis.out.log" \
  --include-qt-plugins=sensible,styles,qml,multimedia \
  --include-data-files=./artemis/resources.py=./artemis/resources.py \
  --include-data-files=./config/qtquickcontrols2.conf=./config/qtquickcontrols2.conf \
  --include-data-files=./building/Linux/create_shortcut.sh=./create_shortcut.sh \
  --include-data-files=./images/artemis_icon.svg=./images/artemis_icon.svg

chmod 755 ./app.dist/app.bin

echo "Building Linux target finished."
