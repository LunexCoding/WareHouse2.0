@echo off
chcp 65001
setlocal

echo Запуск build_tools\server\create_env_archive.bat...

REM Установите путь к виртуальному окружению и имя архива
set "ROOT_DIR=..\.."
set "VENV=%ROOT_DIR%\venvs\server_env"

REM Получаем полный путь к ROOT_DIR
pushd "%ROOT_DIR%"
set "FULL_ROOT_PATH=%cd%"
popd

set "ARCHIVE_FILE=%FULL_ROOT_PATH%\builds\server_env.zip"

REM Убедитесь, что архив не существует
if exist "%ARCHIVE_FILE%" (
    del "%ARCHIVE_FILE%"
    echo Удален существующий архив: %ARCHIVE_FILE%
)

REM Создайте архив виртуального окружения
echo Создание архива виртуального окружения...
powershell -command "Compress-Archive -Path '%VENV%' -DestinationPath '%ARCHIVE_FILE%' -Force"

REM Проверьте, был ли создан архив
if exist "%ARCHIVE_FILE%" (
    echo Архив создан: %ARCHIVE_FILE%
) else (
    echo Ошибка при создании архива.
    exit /b 1
)
