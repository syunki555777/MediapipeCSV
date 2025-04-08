# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['main.py'],
             pathex=['.'],
             binaries=[],
             datas=[
                 ('./hand_landmarker.task', '.'),
                 ('./pose_landmarker_heavy.task', '.'),
                 ('./pose_landmarker_lite.task', '.'),
                 ('./face_landmarker.task', '.'),
                 ("../image/icon.icon", "image")
             ],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='MediapipeCSVWriter',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='../image/icon.icon'
          )

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='MediapipeCSVWriter.app'
)
