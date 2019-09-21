echo "Build Artemis executable.."

rm -rf output

mkdir output

pyinstaller artemis.spec

mv -v dist/Artemis ./output/Artemis
rm -rfv dist build

echo "Build _ArtemisUpdater.."

pyinstaller _ArtemisUpdater.spec

mv -v dist/_ArtemisUpdater ./output/_ArtemisUpdater
rm -rfv dist build

echo "Create single archives"
cd output
tar -czvf Artemis_linux.tar.gz Artemis ../../../src/themes
tar -czvf _ArtemisUpdater_linux.tar.gz _ArtemisUpdater

echo "Create full archive for website"
mkdir Artemis/
cp -rv !(__current_theme) Artemis ../../../src/themes _ArtemisUpdater Artemis/
# rm Artemis/themes/__current_theme
tar -czvf ArtemisWebDownlaod_linux.tar.gz Artemis/

echo "Get size and sha256"
python ../../__get_hash_code.py Artemis_linux.tar.gz _ArtemisUpdater_linux.tar.gz ArtemisWebDownlaod_linux.tar.gz

cd ..
echo "Done."
