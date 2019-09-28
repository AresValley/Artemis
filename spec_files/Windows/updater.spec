# -*- mode: python ; coding: utf-8 -*-

import os


BASE_FOLDER = "../../src/"
block_cipher = None

data_file = [
    (os.path.join(BASE_FOLDER, "download_db_window.ui"), "."),
    (os.path.join(BASE_FOLDER, "download_window.py"), "."),
    (os.path.join(BASE_FOLDER, "utilities.py"), "."),
    (os.path.join(BASE_FOLDER, "versioncontroller.py"), "."),
    (os.path.join(BASE_FOLDER, "downloadtargetfactory.py"), "."),
    (os.path.join(BASE_FOLDER, "executable_utilities.py"), "."),
    (os.path.join(BASE_FOLDER, "os_utilities.py"), "."),
    (os.path.join(BASE_FOLDER, "web_utilities.py"), "."),
    (os.path.join(BASE_FOLDER, "constants.py"), "."),
    (os.path.join(BASE_FOLDER, "threads.py"), "."),
    (os.path.join(BASE_FOLDER, "default_imgs_rc.py"), "."),
    (os.path.join(BASE_FOLDER, "cacert.pem"), "."),
]
a = Analysis([os.path.join(BASE_FOLDER, 'updater.py')],  # noqa: 821
             pathex=[os.getcwd()],
             binaries=[],
             datas=data_file,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure,  # noqa: 821
          a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,  # noqa: 821
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='_ArtemisUpdater',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,
          icon='Artemis3.ico')
