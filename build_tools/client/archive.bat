@echo off
chcp 65001
setlocal

set "VERSION=%1"

set "ROOT_DIR=..\.."
set "OUT_PATH=%ROOT_DIR%\out"
set "SRC_DIR=%OUT_PATH%\client_%VERSION%"
set "CLIENT_BUILD=%ROOT_DIR%\builds\client"
set "ARCHIVE_FILE=%SRC_DIR%.zip"

REM Получаем полный путь к директориям
pushd "%ROOT_DIR%"
set "FULL_ROOT_PATH=%cd%"
popd

pushd "%ROOT_DIR%"
set "FULL_OUT_PATH=%cd%\out"
set "FULL_SRC_DIR=%FULL_OUT_PATH%\client_%VERSION%"
set "FULL_CLIENT_BUILD=%ROOT_DIR%\builds\client"
set "FULL_ARCHIVE_FILE=%FULL_SRC_DIR%.zip"
popd

if not exist "%FULL_SRC_DIR%" (
    echo Создание директории архивации...
    mkdir "%FULL_SRC_DIR%"
)

xcopy "%FULL_CLIENT_BUILD%\version.txt" "%FULL_SRC_DIR%" /y
xcopy "dist\client\client.exe" "%FULL_SRC_DIR%" /y
xcopy "%FULL_CLIENT_BUILD%\.env" "%FULL_SRC_DIR%" /y

echo Создание архива "client_%VERSION%.zip"...
powershell -command "Compress-Archive -Path '%FULL_SRC_DIR%\*' -DestinationPath '%FULL_ARCHIVE_FILE%'"

echo Проверка существования архива: %FULL_ARCHIVE_FILE%
if not exist "%FULL_ARCHIVE_FILE%" (
    echo Архив не создан: %FULL_ARCHIVE_FILE%
    pause
    exit /b 1
)

echo Удаление директории %FULL_SRC_DIR%...
rmdir /s /q "%FULL_SRC_DIR%"

endlocal
