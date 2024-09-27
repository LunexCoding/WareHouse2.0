@echo off
chcp 65001
setlocal enabledelayedexpansion

set "ROOT_DIR=..\.."
set "SRC_PATH=%ROOT_DIR%\src"
set "BUILD_PATH=%ROOT_DIR%\builds"
set "OUT_PATH=%ROOT_DIR%\out"
set "CLIENT_BUILD_PATH=%BUILD_PATH%\client"
set "SPEC_FILE=%ROOT_DIR%\build_tools\client\client.spec"  REM Путь к файлу spec
set "VENV=%ROOT_DIR%\venvs\client_env"  REM Путь к виртуальному окружению
set "BUILD_UPDATER_VERSION_FILE=updaterVersion.txt"
set "FTP_SCRIPT=%SRC_PATH%\shared\tools\ftp.py"
set "VERSION_FILE=version.txt"

REM Получаем полный путь к директориям
pushd "%ROOT_DIR%"
set "FULL_ROOT_PATH=%cd%"
popd

pushd "%ROOT_DIR%"
set "FULL_SRC_PATH=%cd%\src"
set "FULL_BUILD_PATH=%cd%\builds"
set "FULL_OUT_PATH=%cd%\out"
set "FULL_CLIENT_BUILD_PATH=%FULL_BUILD_PATH%\client"
set "FULL_SPEC_FILE=%cd%\build_tools\client\client.spec"
set "FULL_VENV=%cd%\venvs\client_env"
popd

if not exist "%FULL_OUT_PATH%" (
    echo Создание директории out...
    mkdir "%FULL_OUT_PATH%"
)
if not exist "%FULL_BUILD_PATH%" (
    echo Создание общей директории сборки...
    mkdir "%FULL_BUILD_PATH%"
)
if exist "%FULL_CLIENT_BUILD_PATH%" (
    rmdir /s /q "%FULL_CLIENT_BUILD_PATH%"
    echo Удалена старая директория сборки
)
echo Создание директории сборки...
mkdir "%FULL_CLIENT_BUILD_PATH%"

REM Ввод версии
echo Запуск version.bat...
if exist "..\version.bat" (
    call "..\version.bat" "version.txt" "%FULL_CLIENT_BUILD_PATH%"
) else (
    echo version.bat не найден.
)

REM Сборка Updater
echo Проверка сборки Updater...
if not exist "%FULL_OUT_PATH%\updater.exe" (
    echo Запуск updater/build.bat...
    cd updater
    call "build.bat"
    cd ../
) else (
    echo Использование готовой сборки Updater UPDATER_VERSION
)

xcopy "%FULL_OUT_PATH%\updater.exe" "%FULL_CLIENT_BUILD_PATH%" /i /y 
rename "%FULL_CLIENT_BUILD_PATH%\version.txt" "last.txt"
xcopy "updater\version.txt" "%FULL_CLIENT_BUILD_PATH%" /y /i
rename "%FULL_CLIENT_BUILD_PATH%\version.txt" "updaterVersion.txt"
rename "%FULL_CLIENT_BUILD_PATH%\last.txt" "version.txt"

REM Копируйте содержимое директории src в клиентскую сборку
echo Копирование содержимого из %FULL_SRC_PATH%\client в %FULL_CLIENT_BUILD_PATH%...
xcopy "%FULL_SRC_PATH%\client" "%FULL_CLIENT_BUILD_PATH%" /s /e /i /y /exclude:%FULL_SRC_PATH%\..\build_tools\exclude_list.txt
xcopy "%FULL_SRC_PATH%\shared" "%FULL_CLIENT_BUILD_PATH%\shared" /s /e /i /y
xcopy "%FULL_SRC_PATH%\network" "%FULL_CLIENT_BUILD_PATH%\network" /s /e /i /y
xcopy "%FULL_SRC_PATH%\common" "%FULL_CLIENT_BUILD_PATH%\common" /s /e /i /y


REM Копируйте Logger
if exist "%FULL_SRC_PATH%\Logger" (
    echo Копирование Logger в %FULL_CLIENT_BUILD_PATH%...
    xcopy "%FULL_SRC_PATH%\Logger" "%FULL_CLIENT_BUILD_PATH%\Logger" /s /e /i /y
) else (
    echo Папка Logger не найдена в %FULL_SRC_PATH%.
)

REM Удаление файлов и папок, указанных в exclude_list.txt
for /f "delims=" %%i in (%FULL_ROOT_PATH%\build_tools\exclude_list.txt) do (
    echo Удаление: %%i
    REM Ищем все папки, которые соответствуют шаблонам в exclude_list.txt
    for /d /r "%FULL_CLIENT_BUILD_PATH%" %%j in (%%i) do (
        if exist "%%j" (
            echo Удаление директории: %%j
            rmdir /s /q "%%j"
        )
    )
    REM Ищем все файлы, которые соответствуют шаблонам в exclude_list.txt
    for /r "%FULL_CLIENT_BUILD_PATH%" %%j in (%%i) do (
        if exist "%%j" (
            echo Удаление файла: %%j
            del /f /q "%%j"
        )
    )
)

REM Активируйте виртуальное окружение
echo Активируем виртуальное окружение из %FULL_VENV%...
call "%FULL_VENV%\Scripts\activate.bat"

REM Запустите PyInstaller для сборки с использованием client.spec
echo Запуск PyInstaller с файлом спецификации: %FULL_SPEC_FILE%...
start /wait pyinstaller "%FULL_SPEC_FILE%"

REM Убедитесь, что сборка завершена
if errorlevel 1 (
    echo Ошибка при сборке с помощью PyInstaller.
    echo Сборка завершена с ошибкой.
    pause
    exit /b 1
)

REM Запуск installer.bat
echo Запуск installer.bat...
if exist "installer.bat" (
    call "installer.bat"
) else (
    echo installer.bat не найден.
)

REM Чтение версии из файла
set /p VERSION=<"%VERSION_FILE%"
REM Удаление лишних пробелов перед проверкой формата
set "CLEAN_VERSION="
for %%A in (%VERSION%) do (
    set "CLEAN_VERSION=!CLEAN_VERSION! %%A"
)
set "VERSION=!CLEAN_VERSION:~1!"
echo Запуск archive.bat...
if exist "archive.bat" (
    call "archive.bat" !VERSION!
) else (
    echo archive.bat не найден.
)

REM Загрузка на FTP
echo Загрузка client на FTP...
set PYTHONPATH=D:\GitHub\test_wx\src
python "%FTP_SCRIPT%" --file "%FULL_OUT_PATH%\client_!VERSION!.zip"
if errorlevel 1 (
    echo Ошибка при загрузке на FTP.
    pause
)
del "%FULL_OUT_PATH%\client_!VERSION!.zip"

echo Запуск clear_build.bat...
if exist "clear.bat" (
    call "clear.bat"
) else (
    echo clear.bat не найден.
)

REM Убедитесь, что все файлы скопированы
echo Статус выполнения: %errorlevel%.

REM Завершение
echo Сборка завершена.
endlocal
pause
