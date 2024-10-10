import os
from PyInstaller.utils.hooks import collect_data_files

# Укажите директорию, содержащую ваши исходные файлы
appPath = os.path.abspath('../../builds/client')

# Путь к .env файлу
envFile = os.path.join(appPath, '.env')
updater = os.path.join(appPath, 'updater.exe')
version = os.path.join(appPath, 'version.txt')
updaterVersion = os.path.join(appPath, 'updaterVersion.txt')

# Список дополнительных данных и бинарных файлов, которые нужно включить
datas = [
    (envFile, '.'),             # Добавить .env в корень
    (updater, '.'),            # Добавить updater.exe в корень
    (version, '.'),            # Добавить version.txt в корень
    (updaterVersion, '.'),     # Добавить updaterVersion.txt в корень
]

hiddenimports = ['strenum']

a = Analysis(
    [os.path.join(appPath, 'main.py')],
    pathex=[appPath],
    binaries=[],  # Включите дополнительные бинарные файлы, если они нужны
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name='client',
    debug=False,
    bootloader_ignore_signals=True,
    strip=False,
    upx=True,
    console=False,
    cipher=None,
    noarchive=False,
    runtime_tmpdir=None,  # Запретить временную директорию
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='client',
)
