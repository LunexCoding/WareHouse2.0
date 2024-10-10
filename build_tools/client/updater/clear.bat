@echo off
chcp 65001
setlocal

set "NEW_VERSION=%1"

echo Запуск build_tools\client\updater\clear.bat...
set "ROOT_PATH=..\..\..\"
set "OUT_PATH=%ROOT_PATH%\out"
set "DIST_PATH=dist"
set "BUILD_PATH=build"

REM Получаем полный путь к директориям
pushd "%ROOT_PATH%"
set "FULL_ROOT_PATH=%cd%"
popd

pushd "%ROOT_PATH%"
set "FULL_OUT_PATH=%cd%\out"
popd

if exist "%DIST_PATH%" (
    echo Удаление папки dist...
    rmdir /s /q "%DIST_PATH%"
) else (
    echo Папка dist не найдена.
)

if exist "%BUILD_PATH%" (
    echo Удаление папки build...
    rmdir /s /q "%BUILD_PATH%"
) else (
    echo Папка build не найдена.
)

if exist "logs" (
    echo Удаление папки logs...
    rmdir /s /q "logs"
) else (
    echo Папка logs не найдена.
)


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
if exist "%FULL_OUT_PATH%\updater_%NEW_VERSION%.exe" (
    del /F /Q "%FULL_OUT_PATH%\updater_%NEW_VERSION%.exe"
)

echo Очистка завершена.
