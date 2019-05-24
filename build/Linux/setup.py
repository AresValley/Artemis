import os
from os import listdir
from os.path import isfile, join

mypath='../..'
excluded=['.gitignore','requirements_win.txt','artemis.py']
data_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for i in excluded:
    data_files.remove(i)

datas=["('../../" + i + "', '.')" for i in data_files]

pyinst_head='''
# -*- mode: python -*-

block_cipher = None

a = Analysis(['../../artemis.py'],
             pathex=['../../'],
             binaries=[],
             datas=[
'''

pyinst_tail='''
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Artemis',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True)
'''

setup_file = open('./setup.spec','w')
setup_file.write(pyinst_head + ','.join(datas) + "]," + pyinst_tail)
setup_file.close() 

os.system("pyinstaller --onefile setup.spec")
os.system("cp -r ../../themes dist")
os.system("rm -rf build")

desktop = open('./artemis.desktop','w')
desktop.write("""#!/usr/bin/env xdg-open
[Desktop Entry]
Name=Artemis
StartupWMClass=artemis3
Exec=. /SETUP_PATH/Artemis
Terminal=False
Icon=artemis3
Type=Application""")
desktop.close()

print("""To finalize the installation (add Artemis in the main menu):\n
1)\tEdit artemis.desktop file properly and move it to '/.local/share/applications'
2)\tMove the icon file artemis3.svg to '/usr/share/icons/'
""")