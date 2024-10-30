# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['/Users/shungiku/Library/Mobile Documents/com~apple~CloudDocs/研究/Mediapipe image/MediapipeCSV/script/'],
    binaries=[],
    datas=[
        ('/Users/shungiku/Library/Mobile Documents/com~apple~CloudDocs/研究/Mediapipe image/MediapipeCSV/script/hand_landmarker.task', '.'),
        ('/Users/shungiku/Library/Mobile Documents/com~apple~CloudDocs/研究/Mediapipe image/MediapipeCSV/script/pose_landmarker_heavy.task', '.'),
        ('/Users/shungiku/Library/Mobile Documents/com~apple~CloudDocs/研究/Mediapipe image/MediapipeCSV/script/pose_landmarker_lite.task', '.'),
        ('/Users/shungiku/Library/Mobile Documents/com~apple~CloudDocs/研究/Mediapipe image/MediapipeCSV/script/face_landmarker.task', '.'),
        ("/Users/shungiku/Library/Mobile Documents/com~apple~CloudDocs/研究/Mediapipe image/MediapipeCSV/image/icon.png", "image")
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

exe = EXE(
    pyz,
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
    icon='/Users/shungiku/Library/Mobile Documents/com~apple~CloudDocs/研究/Mediapipe image/MediapipeCSV/image/icon.png'
)

app = BUNDLE(
    exe,
    name='MediapipeCSVWriter.app',
    icon='/Users/shungiku/Library/Mobile Documents/com~apple~CloudDocs/研究/Mediapipe image/MediapipeCSV/image/icon.png',
    bundle_identifier='com.example.MediapipeCSVWriter',
    info_plist={
        'CFBundleDisplayName': 'MediapipeCSVWriter',
        'CFBundleName': 'MediapipeCSVWriter',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
        'NSHighResolutionCapable': 'True',
    }
)