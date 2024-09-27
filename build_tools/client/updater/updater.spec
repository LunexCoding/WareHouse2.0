block_cipher = None


ROOT_DIR = "../../.."


a = Analysis(
    [f'{ROOT_DIR}/builds/updater/updater.py'],
    pathex=[f'{ROOT_DIR}/builds/updater'],
    binaries=[],
    datas=[
        (f'{ROOT_DIR}/builds/updater/network', 'network'),
        (f'{ROOT_DIR}/builds/updater/shared', 'shared'),
        (f'{ROOT_DIR}/builds/updater/common', 'common'),
        (f'{ROOT_DIR}/builds/updater/Logger', 'Logger'),
        (f'{ROOT_DIR}/builds/updater/consts.py', '.'),
        (f'{ROOT_DIR}/builds/updater/preinit.py', '.'),
        (f'{ROOT_DIR}/builds/updater/.env', '.')
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='updater',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,  # Запрет на создание временной директории
    console=True
)
