@echo off
chcp 65001
setlocal

set "ROOT_PATH=..\..\..\"
set "SRC_PATH=%ROOT_PATH%\src"
set "OUT_PATH=%ROOT_PATH%\out"
set "BUILDS_PATH=%ROOT_PATH%\builds"
set "UPDATER_PATH=%BUILDS_PATH%\updater"
set "EXCLUDE_LIST=..\..\exclude_list.txt"
set "VENV_DIR=%ROOT_PATH%\venvs\updater_env"
set "SPEC_FILE=updater.spec"
set "VERSION_FILE=version.txt"
set "FTP_SCRIPT=%SRC_PATH%\common\ftp.py"

REM Получаем полный путь к директориям
pushd "%ROOT_PATH%"
set "FULL_ROOT_PATH=%cd%"
popd

pushd "%ROOT_PATH%"
set "FULL_SRC_PATH=%cd%\src"
set "FULL_BUILD_PATH=%cd%\builds"
set "FULL_OUT_PATH=%cd%\out"
set "FULL_UPDATER_PATH=%FULL_BUILD_PATH%\updater"
set "FULL_SPEC_FILE=%cd%\build_tools\updater.spec"
set "FULL_VENV_DIR=%cd%\venvs\updater_env"
popd

REM Чтение текущей версии из version.txt
if not exist "%VERSION_FILE%" (
    echo 0.0.0 > "%VERSION_FILE%"
)

set /p CURRENT_VERSION=<"%VERSION_FILE%"

REM Разделение версии на мажорную, минорную и патч-части
for /f "tokens=1,2,3 delims=." %%a in ("%CURRENT_VERSION%") do (
    set MAJOR_VERSION=%%a
    set MINOR_VERSION=%%b
    set PATCH_VERSION=%%c
)

REM Увеличение патч-версии на 1
set /a PATCH_VERSION+=1

REM Формирование новой версии
set NEW_VERSION=%MAJOR_VERSION%.%MINOR_VERSION%.%PATCH_VERSION%

REM Запись новой версии в файл
echo %NEW_VERSION% > "%VERSION_FILE%"

echo Текущая версия: %CURRENT_VERSION%
echo Обновлённая версия: %NEW_VERSION%

if not exist "%FULL_BUILD_PATH%" (
    echo Создание каталога сборки...
    mkdir "%FULL_BUILD_PATH%"
)

if exist "%FULL_UPDATER_PATH%" (
    echo Удаление существующего каталога updater...
    rmdir /s /q "%FULL_UPDATER_PATH%"
)

if not exist "%FULL_OUT_PATH%" (
    echo Создание каталога out...
    mkdir "%FULL_OUT_PATH%"
)

if not exist "%FULL_UPDATER_PATH%" (
    echo Создание каталога updater...
    mkdir "%FULL_UPDATER_PATH%"
)

xcopy "%FULL_SRC_PATH%\client\.env" "%FULL_UPDATER_PATH%" /y 

echo Копирование файлов updater...
xcopy "%FULL_SRC_PATH%\updater" "%FULL_UPDATER_PATH%" /s /e /i /y /exclude:%FULL_SRC_PATH%\..\build_tools\exclude_list.txt

echo Копирование shared...
xcopy "%FULL_SRC_PATH%\shared" "%FULL_UPDATER_PATH%\shared" /s /e /i /y

echo Копирование network...
xcopy "%FULL_SRC_PATH%\network" "%FULL_UPDATER_PATH%\network" /s /e /i /y

echo Копирование common...
xcopy "%FULL_SRC_PATH%\common" "%FULL_UPDATER_PATH%\common" /s /e /i /y

echo Копирование Logger...
mkdir "%FULL_UPDATER_PATH%\Logger"
xcopy /e /i "%FULL_SRC_PATH%\Logger\*" "%FULL_UPDATER_PATH%\Logger" /EXCLUDE:%EXCLUDE_LIST%

REM Удаление файлов и папок, указанных в exclude_list.txt
for /f "delims=" %%i in (%EXCLUDE_LIST%) do (
    echo Удаление: %%i
    REM Ищем все папки, которые соответствуют шаблонам в exclude_list.txt
    for /d /r "%FULL_UPDATER_PATH%" %%j in (%%i) do (
        if exist "%%j" (
            echo Удаление директории: %%j
            rmdir /s /q "%%j"
        )
    )
    REM Ищем все файлы, которые соответствуют шаблонам в exclude_list.txt
    for /r "%FULL_UPDATER_PATH%" %%j in (%%i) do (
        if exist "%%j" (
            echo Удаление файла: %%j
            del /f /q "%%j"
        )
    )
)

echo Активируем виртуальное окружение...
call "%FULL_VENV_DIR%\Scripts\activate.bat"

echo Запуск PyInstaller...
start /wait pyinstaller "%SPEC_FILE%"

REM Убедитесь, что сборка завершена
if errorlevel 1 (
    echo Ошибка при сборке с помощью PyInstaller.
    echo Сборка завершена с ошибкой.
    pause
    exit /b 1
)

IF EXIST "dist\updater.exe" (
    echo Копирование updater.exe...
    copy /Y "dist\updater.exe" "%FULL_OUT_PATH%\updater.exe"
    copy /Y "dist\updater.exe" "%FULL_OUT_PATH%\updater_%NEW_VERSION%.exe"
) ELSE (
    echo Файл updater.exe не найден.
)

REM Загрузка на FTP
echo Загрузка updater на FTP...
set PYTHONPATH=D:\GitHub\test_wx\src
python "%FTP_SCRIPT%" --file "%FULL_OUT_PATH%\updater_%NEW_VERSION%.exe"
if errorlevel 1 (
    echo Ошибка при загрузке на FTP.
    pause
)

REM Запуск clear.bat
echo Запуск clear_build.bat...
if exist "clear.bat" (
    call "clear.bat" %NEW_VERSION%
) else (
    echo clear.bat не найден.
)

REM Убедитесь, что все файлы скопированы
echo Статус выполнения: %errorlevel%.
echo Сборка завершена!
