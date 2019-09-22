echo "Build Artemis executable.."

rm -rf output

mkdir output

pyinstaller Artemis.spec

mv -v ./dist/Artemis ./output/Artemis
rm -rfv dist build

echo "Build _ArtemisUpdater.."

pyinstaller updater.spec

mv -v ./dist/_ArtemisUpdater ./output/_ArtemisUpdater
rm -rfv dist build

echo "Create single archives"
cd output

tar -czvf Artemis_linux.tar.gz Artemis -C ../../../src themes
tar -czvf _ArtemisUpdater_linux.tar.gz ./_ArtemisUpdater

echo "Create full archive for website"

tar -czvf ArtemisWebDownlaod_linux.tar.gz Artemis _ArtemisUpdater -C ../../../src themes

echo "Get size and sha256"
python ../../__get_hash_code.py Artemis_linux.tar.gz _ArtemisUpdater_linux.tar.gz ArtemisWebDownlaod_linux.tar.gz

cd ..
echo "Done."
