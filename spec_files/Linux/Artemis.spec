# -*- mode: python -*-

import glob
import os


block_cipher = None


SRC_PATH = "../../src/"

data_file = [
    (f, '.') for f in glob.glob(SRC_PATH + '*.[pu][yi]')
    if f.split('/')[-1] != "artemis.py" and f.split('/')[-1] != "updater.py"
]
data_file.append((SRC_PATH + 'cacert.pem', '.'))

a = Analysis([SRC_PATH + 'artemis.py'],  # noqa: 821
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
          name='Artemis',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False)
