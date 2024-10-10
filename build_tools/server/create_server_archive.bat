@echo off
chcp 65001
setlocal enabledelayedexpansion

echo Запуск build_tools\server\create_server_archive.bat...

set "ROOT_DIR=..\.."
set "SERVER_PATH=%ROOT_DIR%\builds\server"
set "BUILD_PATH=%ROOT_DIR%\builds"
set "OUT_PATH=%ROOT_DIR%\out"
set "VERSION_FILE=version.txt"

REM Получаем полный путь к ROOT_DIR, SERVER_PATH и BUILD_PATH
pushd "%ROOT_DIR%"
set "FULL_ROOT_PATH=%cd%"
popd

pushd "%SERVER_PATH%"
set "FULL_SERVER_PATH=%cd%"
popd

pushd "%BUILD_PATH%"
set "FULL_BUILD_PATH=%cd%"
popd

pushd "%OUT_PATH%"
set "FULL_OUT_PATH=%cd%"
popd

set /p VERSION=<"%VERSION_FILE%"
REM Удаление лишних пробелов перед проверкой формата
set "CLEAN_VERSION="
for %%A in (%VERSION%) do (
    set "CLEAN_VERSION=!CLEAN_VERSION! %%A"
)
set "VERSION=!CLEAN_VERSION:~1!"
set "FULL_ARCHIVE_FILE=%FULL_OUT_PATH%\server_!VERSION!.zip"

echo Создание архива сервера...
pushd "%FULL_SERVER_PATH%"
powershell -Command "Compress-Archive -Path * -DestinationPath '%FULL_ARCHIVE_FILE%' -Force"
popd

REM Проверка успешного создания архива
if exist "%FULL_ARCHIVE_FILE%" (
    echo Архив успешно создан: %FULL_ARCHIVE_FILE%
) else (
    echo Ошибка при создании архива.
    exit /b 1
)

endlocal
