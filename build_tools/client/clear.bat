@echo off
chcp 65001
setlocal

echo Запуск build_tools\client\clear.bat...

REM Получаем полный путь к текущему каталогу
pushd .
set "FULL_PATH=%cd%"
popd

set "DIST_PATH=%FULL_PATH%\dist"
set "BUILD_PATH=%FULL_PATH%\build"
set "LOGS_PATH=%FULL_PATH%\logs"

if exist "%DIST_PATH%" (
    echo Удаление папки dist: %DIST_PATH%...
    rmdir /s /q "%DIST_PATH%"
) else (
    echo Папка dist не найдена: %DIST_PATH%.
)

if exist "%BUILD_PATH%" (
    echo Удаление папки build: %BUILD_PATH%...
    rmdir /s /q "%BUILD_PATH%"
) else (
    echo Папка build не найдена: %BUILD_PATH%.
)

if exist "%LOGS_PATH%" (
    echo Удаление папки logs: %LOGS_PATH%...
    rmdir /s /q "%LOGS_PATH%"
) else (
    echo Папка logs не найдена: %LOGS_PATH%.
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

echo Очистка завершена.
