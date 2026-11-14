#!/usr/bin/env bash
set -e

# Directory setup
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"

echo "=== Artemis macOS Native Build (Xcode & Briefcase) ==="

# Check Python environment
if [ -d ".venv" ]; then
    PYTHON=".venv/bin/python"
    BRIEFCASE=".venv/bin/briefcase"
    PYSIDE_RCC=".venv/bin/pyside6-rcc"
else
    PYTHON="python3"
    BRIEFCASE="briefcase"
    PYSIDE_RCC="pyside6-rcc"
fi

echo "1. Compiling Qt resources with pyside6-rcc..."
$PYSIDE_RCC ./artemis.qrc -o artemis/resources.py

echo "2. Generating/Updating macOS Xcode Project..."
$BRIEFCASE create macOS Xcode --no-input --log

echo "3. Building Native macOS App with Xcode..."
$BRIEFCASE build macOS Xcode --no-input --log

echo ""
echo "=== Build Completed Successfully! ==="
echo "Xcode Project : $PROJECT_ROOT/build/artemis/macos/xcode/Artemis.xcodeproj"
echo "Native App    : $PROJECT_ROOT/build/artemis/macos/xcode/build/Release/Artemis.app"
echo ""
echo "To open the project in Xcode GUI, run:"
echo "  open build/artemis/macos/xcode/Artemis.xcodeproj"
echo ""
echo "To package into a distributable .dmg, run:"
echo "  $BRIEFCASE package macOS Xcode --adhoc-sign"
