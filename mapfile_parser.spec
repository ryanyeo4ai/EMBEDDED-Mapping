# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

added_files = [ ('login.ui','.'),
                ('register.ui','.'),
                ('process.ui','.'),
                ('icon_group_lg.png','.'),
                ('icon_group_sm.png','.'),
                ('icon_T.png','.'),
                ('logo_lg.png','.'),
                ('logo_sm.png','.')
 ]

a = Analysis(['mapfile_parser.py'],
             pathex=[],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          name='mapfile_parser',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
