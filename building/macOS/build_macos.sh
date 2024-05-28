#!/usr/bin/env bash

echo "Building maacOS target ..."

echo "Installing requirements ..."
pip install -r requirements.txt
pip install nuitka imageio

echo "Building with Nuitka ..."
python -m nuitka app.py \
  --standalone \
  --follow-imports \
  --show-modules \
  --assume-yes-for-downloads \
  --disable-console \
  --enable-plugin=pyside6 \
  --include-qt-plugins=sensible,styles,qml,multimedia \
  --include-data-files=./artemis/resources.py=./artemis/resources.py \
  --include-data-files=./config/qtquickcontrols2.conf=./config/qtquickcontrols2.conf \
  --include-data-files=./building/Linux/create_shortcut.sh=./create_shortcut.sh \
  --macos-create-app-bundle \
  --macos-app-icon=images/artemis_icon.ico \
  --macos-signed-app-name=com.AresValley.Artemis \
  --macos-app-name=Artemis \
  --macos-app-mode=gui \
  --macos-sign-identity=ad-hoc \
  --macos-app-version=4.0.0

echo "Building Linux target finished."
