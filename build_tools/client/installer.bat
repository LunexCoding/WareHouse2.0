@echo off
chcp 65001
setlocal

echo Запуск build_tools\client\installer.bat...

REM Установите путь к скрипту Inno Setup
set "iss_script=installer.iss"

REM Установите путь к Inno Setup Compiler
set "inno_setup_path=C:\Program Files (x86)\Inno Setup 6"

REM Запустите сборку с помощью Inno Setup
echo Запуск сборки Inno Setup...
"%inno_setup_path%\ISCC.exe" "%iss_script%"

REM Проверьте успешность выполнения
if errorlevel 1 (
    echo Ошибка при сборке установщика.
    exit /b 1
)

echo Установочный файл создан успешно.
