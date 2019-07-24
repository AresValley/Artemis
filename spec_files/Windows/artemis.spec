# -*- mode: python -*-

block_cipher = None

import glob,os

data_file = [(f, '.') for f in glob.glob('*.[pu][yi]') if f != "artemis.py"]
data_file.append(('cacert.pem', '.'))

a = Analysis(['artemis.py'],
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
          console=False , icon='Artemis3.ico')
