echo "Build Artemis executable.."

rm -rf output

mkdir output
mkdir output/artemis

pyinstaller Artemis.spec

mv -v ./dist/Artemis ./output/Artemis
rm -rfv dist build

echo "Build _ArtemisUpdater.."

pyinstaller updater.spec

mv -v ./dist/_ArtemisUpdater ./output/_ArtemisUpdater
rm -rfv dist build

echo "Create single archives"
cd output

cp -r ../../../src/themes artemis/themes
rm -f artemis/themes/__current_theme
cp Artemis artemis/Artemis
cp _ArtemisUpdater artemis/_ArtemisUpdater

tar -czvf Artemis_linux.tar.gz Artemis -C artemis themes
tar -czvf _ArtemisUpdater_linux.tar.gz ./_ArtemisUpdater

echo "Create full archive for website"

cp ../artemis3.svg artemis
cp ../create_shortcut.sh artemis

tar -czvf ArtemisWebDownlaod_linux.tar.gz artemis

echo "Get size and sha256"
python ../../__get_hash_code.py Artemis_linux.tar.gz _ArtemisUpdater_linux.tar.gz ArtemisWebDownlaod_linux.tar.gz

cd ..
echo "Done."
