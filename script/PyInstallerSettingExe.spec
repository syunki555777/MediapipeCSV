# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['main.py'],
             pathex=['C:\\Users\\syunk\\PycharmProjects\\MediapipeCSV\\script\\main.py'],
             binaries=[],
             datas=[('/Users/shungiku/Library/Mobile Documents/com~apple~CloudDocs/研究/Mediapipe image/MediapipeCSV/script/hand_landmarker.task', '.'),
                    ('/Users/shungiku/Library/Mobile Documents/com~apple~CloudDocs/研究/Mediapipe image/MediapipeCSV/script/pose_landmarker_heavy.task', '.'),
                    ('/Users/shungiku/Library/Mobile Documents/com~apple~CloudDocs/研究/Mediapipe image/MediapipeCSV/script/pose_landmarker_lite.task', '.'),
                    ('/Users/shungiku/Library/Mobile Documents/com~apple~CloudDocs/研究/Mediapipe image/MediapipeCSV/script/face_landmarker.task', '.'),
                    ("/Users/shungiku/Library/Mobile Documents/com~apple~CloudDocs/研究/Mediapipe image/MediapipeCSV/image/icon.png", "image")],
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
          console=False,  # ウィンドウモード
          icon='/Users/shungiku/Library/Mobile Documents/com~apple~CloudDocs/研究/Mediapipe image/MediapipeCSV/image/icon.png'  # アイコンのパス
          )