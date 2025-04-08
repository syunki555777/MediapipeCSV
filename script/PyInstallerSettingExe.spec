# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['main.py'],
             pathex=['.'],
             binaries=[],
             datas=[('./hand_landmarker.task', '.'),
                    ('./pose_landmarker_heavy.task', '.'),
                    ('./pose_landmarker_lite.task', '.'),
                    ('./face_landmarker.task', '.'),
                    ("../image/icon.png", "image")],
             # favicon.icoを含める場合
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
          name='MediapipeCSVWriter',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='../image/icon.png',
          target_arch='arm64'
          )
