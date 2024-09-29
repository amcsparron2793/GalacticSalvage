# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['..\\..\\GalacticSalvage\\GalacticSalvage.py'],
             pathex=['C:\\Users\\amcsparron\\Desktop\\Python_Projects\\GalacticSalvage\\Misc_Project_Files\\pyinstaller_build_dir',
             'C:\\Users\\amcsparron\\Desktop\\Python_Projects\\GalacticSalvage\\GalacticSalvage'],
             binaries=[],
             datas=['C:\\Users\\amcsparron\\Desktop\\Python_Projects\\GalacticSalvage\\Misc_Project_Files\\images\\*',
             'C:\\Users\\amcsparron\\Desktop\\Python_Projects\\GalacticSalvage\\Misc_Project_Files\\sounds\\*',
              'C:\\Users\\amcsparron\\Desktop\\Python_Projects\\GalacticSalvage\\Misc_Project_Files\\CreateTables.sql'],
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
          [],
          exclude_binaries=True,
          # this needs to be changed to successfully change the name of the output dirs and exes
          name='GalacticSalvage',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               # this needs to be changed to successfully change the name of the output dirs and exes
               name='GalacticSalvage')
