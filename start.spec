# -*- mode: python -*-

block_cipher = None



# define a list with all added_files
added_files = [
				( 'Nitori/*.*', 'Nitori' ),
				( 'Stat/*.*', 'Stat' ),
				( 'template/*.*', 'template' ),
				( 'setting/*.*', 'setting' )
]



# modify "datas" to "added_files"
a = Analysis(['D:\\TosoProgram\\TosoFrame\\TosoFrame\\start.py'],
             pathex=['D:\\PyInstaller-3.2\\start'],
             binaries=None,
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='start',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='start')
