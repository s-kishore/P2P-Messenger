# -*- mode: python -*-

block_cipher = None


a = Analysis(['Messenger.py'],
             pathex=['E:\\Grizder\\OneDrive\\Desktop\\Code Tmp\\Instant Messenger'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.datas += [('app.ico', 'E:\\Grizder\\OneDrive\\Desktop\\Code Tmp\\Instant Messenger\\app.ico', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Messenger',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='app.ico')
