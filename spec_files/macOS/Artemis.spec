# -*- mode: python -*-

block_cipher = None
import glob, os

data_file = [(f, '.') for f in glob.glob('*.[pu][yi]') if f != "artemis.py"]
data_file.append(('themes','./themes'))

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
          [],
          exclude_binaries=True,
          name='Artemis',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Artemis')
app = BUNDLE(coll,
             name='Artemis.app',
             icon='Artemis3.icns',
             bundle_identifier=None)
