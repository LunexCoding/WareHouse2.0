@echo off
chcp 65001
setlocal enabledelayedexpansion

set "ROOT_DIR=..\.."
set "SRC_PATH=%ROOT_DIR%\src"
set "OUT_PATH=%ROOT_DIR%\out"
set "BUILD_PATH=%ROOT_DIR%\builds"
set "ENV=%ROOT_DIR%\venvs\server_env"
set "SERVER_PATH=%BUILD_PATH%\server"
set "ENV_ARCHIVE_ZIP=server_env.zip"
set "VERSION_FILE=version.txt"

REM Получаем полный путь к ROOT_DIR, SERVER_PATH и BUILD_PATH
pushd "%ROOT_DIR%"
set "FULL_ROOT_PATH=%cd%"
popd

set "FULL_SRC_PATH=%FULL_ROOT_PATH%\src"
set "FULL_OUT_PATH=%FULL_ROOT_PATH%\out"
set "FULL_BUILD_PATH=%FULL_ROOT_PATH%\builds"
set "FULL_SERVER_PATH=%FULL_BUILD_PATH%\server"
set "FULL_ENV_ARCHIVE_ZIP=%FULL_BUILD_PATH%\%ENV_ARCHIVE_ZIP%"
set "FTP_SCRIPT=%FULL_SRC_PATH%\common\ftp.py"

REM Создайте директорию сборки и архивной директории, если они не существуют
if not exist "%FULL_BUILD_PATH%" (
    mkdir "%FULL_BUILD_PATH%"
    echo Директория сборки создана: %FULL_BUILD_PATH%
)

if exist "%FULL_SERVER_PATH%" (
    rmdir /s /q "%FULL_SERVER_PATH%"
    echo Удалена старая директория сборки: %FULL_SERVER_PATH%
)
mkdir "%FULL_SERVER_PATH%"
echo Директория сервера создана: %FULL_SERVER_PATH%

REM Ввод версии
echo Запуск version.bat...
if exist "..\version.bat" (
    call "..\version.bat" "version.txt" "%FULL_SERVER_PATH%"
) else (
    echo version.bat не найден.
)

REM Копируйте содержимое директории src в server
if exist "%FULL_SRC_PATH%\server" (
    xcopy "%FULL_SRC_PATH%\server" "%FULL_SERVER_PATH%" /s /e /i /y /exclude:%FULL_ROOT_PATH%\build_tools\exclude_list.txt
    echo Содержимое из %FULL_SRC_PATH%\server скопировано в %FULL_SERVER_PATH%
) else (
    echo Исходная директория %FULL_SRC_PATH%\server не найдена.
)

if exist "%FULL_SRC_PATH%\common" (
    xcopy "%FULL_SRC_PATH%\common" "%FULL_SERVER_PATH%\common" /s /e /i /y
    echo Содержимое из %FULL_SRC_PATH%\common скопировано в %FULL_SERVER_PATH%\common
) else (
    echo Исходная директория %FULL_SRC_PATH%\common не найдена.
)

if exist "%FULL_SRC_PATH%\network" (
    xcopy "%FULL_SRC_PATH%\network" "%FULL_SERVER_PATH%\network" /s /e /i /y
    echo Содержимое из %FULL_SRC_PATH%\network скопировано в %FULL_SERVER_PATH%\network
) else (
    echo Исходная директория %FULL_SRC_PATH%\network не найдена.
)

if exist "%FULL_SRC_PATH%\Logger" (
    xcopy "%FULL_SRC_PATH%\Logger" "%FULL_SERVER_PATH%\Logger" /s /e /i /y
    echo Содержимое из %FULL_SRC_PATH%\Logger скопировано в %FULL_SERVER_PATH%\Logger
) else (
    echo Папка Logger не найдена в %FULL_SRC_PATH%.
)

if exist "run.bat" (
    copy "run.bat" "%FULL_SERVER_PATH%\run.bat" /y
    echo Файл run.bat скопирован в %FULL_SERVER_PATH%\run.bat
) else (
    echo run.bat не найден.
)

REM Удаление файлов и папок, указанных в exclude_list.txt
for /f "delims=" %%i in (%FULL_ROOT_PATH%\build_tools\exclude_list.txt) do (
    echo Удаление: %%i
    for /d /r "%FULL_SERVER_PATH%" %%j in (%%i) do (
        if /i not "%%~dpj"=="%FULL_SERVER_PATH%\server_env\" (
            if exist "%%j" (
                echo Удаление директории: %%j
                rmdir /s /q "%%j"
            )
        )
    )
    for /r "%FULL_SERVER_PATH%" %%j in (%%i) do (
        if /i not "%%~dpj"=="%FULL_SERVER_PATH%\server_env\" (
            if exist "%%j" (
                echo Удаление файла: %%j
                del /f /q "%%j"
            )
        )
    )
)

if exist "%FULL_ENV_ARCHIVE_ZIP%" (
    del "%FULL_ENV_ARCHIVE_ZIP%"
)

echo Запуск create_env_archive.bat...
call "create_env_archive.bat"

REM Проверьте, создан ли архив
echo Проверка существования архива: %FULL_ENV_ARCHIVE_ZIP%
if not exist "%FULL_ENV_ARCHIVE_ZIP%" (
    echo Архив не создан: %FULL_ENV_ARCHIVE_ZIP%
    pause
    exit /b 1
)

REM Распакуйте архив в директорию сборки
echo Распаковка архива...
powershell -Command "Expand-Archive -Path '%FULL_ENV_ARCHIVE_ZIP%' -DestinationPath '%FULL_SERVER_PATH%' -Force"

REM Проверьте успешность выполнения PowerShell команды
if errorlevel 1 (
    echo Ошибка при распаковке архива.
    pause
    exit /b 1
)

echo Удаление архива env...
del "%FULL_ENV_ARCHIVE_ZIP%"

echo Запуск acreate_server_archive.bat...
call "create_server_archive.bat"

REM Чтение версии из файла
set /p VERSION=<"%VERSION_FILE%"
REM Удаление лишних пробелов перед проверкой формата
set "CLEAN_VERSION="
for %%A in (%VERSION%) do (
    set "CLEAN_VERSION=!CLEAN_VERSION! %%A"
)
set "VERSION=!CLEAN_VERSION:~1!"

echo Активируем виртуальное окружение...
call "%ENV%\Scripts\activate.bat"

REM Загрузка в облако
echo Загрузка server на FTP...
set PYTHONPATH=%FULL_SRC_PATH%
python "%FTP_SCRIPT%" --file "%FULL_OUT_PATH%\server_!VERSION!.zip"
if errorlevel 1 (
    echo Ошибка при загрузке на FTP.
    pause
)

del "%FULL_OUT_PATH%\server_!VERSION!.zip"

@REM rmdir /S /Q "logs"

REM Убедитесь, что все файлы скопированы
echo Статус выполнения: %errorlevel%.

REM Завершение
echo Сборка завершена.
endlocal
pause
