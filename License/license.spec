# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['D:/Heat Exchanger/Project/SGHEDA_v1.0/License/license.py'],
    pathex=[],
    binaries=[],
    datas=[('D:/Heat Exchanger/Project/SGHEDA_v1.0/License/Images', 'Images/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='license',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['D:\\Heat Exchanger\\Project\\SGHEDA_v1.0\\License\\logo.ico'],
)
