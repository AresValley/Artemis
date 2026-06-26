#!/usr/bin/env bash

echo "Building macOS target ..."

echo "Install building dependencies ..."
uv add 'nuitka==4.1.2'
uv add 'imageio'

echo "Compiling resources ..."
uv run pyside6-rcc ./artemis.qrc -o artemis/resources.py

echo "Building with Nuitka ..."
uv run --python 3.13 nuitka \
  --python-flag=-m artemis \
  --standalone \
  --follow-imports \
  --show-modules \
  --assume-yes-for-downloads \
  --enable-plugin=pyside6 \
  --include-qt-plugins=sensible,styles,qml,multimedia \
  --include-data-files=./config/qtquickcontrols2.conf=./config/qtquickcontrols2.conf \
  --include-data-files=./scripts/Linux/create_shortcut.sh=./create_shortcut.sh \
  --macos-create-app-bundle \
  --macos-app-icon=data/images/artemis_icon.ico \
  --macos-signed-app-name=com.AresValley.Artemis \
  --macos-app-name=Artemis \
  --macos-app-mode=gui \
  --macos-sign-identity=auto \
  --macos-app-version=4.1.0

echo "Building macOS target finished."
