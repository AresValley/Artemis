#!/usr/bin/env bash

echo "Building Linux target ..."

echo "Install building dependencies ..."
uv add 'nuitka==4.1.2'

echo "Compiling resources ..."
uv run pyside6-rcc ./artemis.qrc -o artemis/resources.py

echo "Building with Nuitka ..."
uv run --python 3.13 nuitka \
  --python-flag=-m artemis \
  --standalone \
  --show-modules \
  --assume-yes-for-downloads \
  --enable-plugin=pyside6 \
  --noinclude-dlls=libQt6Charts* \
  --noinclude-dlls=libQt6Quick3D* \
  --noinclude-dlls=libQt6Sensors* \
  --noinclude-dlls=libQt6Test* \
  --noinclude-dlls=libQt6WebEngine* \
  --noinclude-dlls="*/objects-RelWithDebInfo/*" \
  --include-qt-plugins=qml \
  --include-qt-plugins=multimedia \
  --include-data-files=./config/qtquickcontrols2.conf=./config/qtquickcontrols2.conf \
  --include-data-files=./building/Linux/create_shortcut.sh=./create_shortcut.sh \
  --include-data-files=./images/artemis_icon.svg=./images/artemis_icon.svg \
  --force-stderr-spec="{TEMP}/artemis.err.log" \
  --force-stdout-spec="{TEMP}/artemis.out.log"

echo "Building Linux target finished."
