@echo off
chcp 65001
setlocal

REM Путь к виртуальному окружению
set "venv_dir=server_env"

REM Активируйте виртуальное окружение
if exist "%venv_dir%\Scripts\activate" (
    call "%venv_dir%\Scripts\activate"
) else (
    echo Виртуальное окружение не найдено в %venv_dir%.
    pause
    exit /b 1
)

REM Установите зависимости
if exist "requirements.txt" (
    echo Установка зависимостей...
    pip install -r requirements.txt
) else (
    echo Файл requirements.txt не найден.
    pause
    exit /b 1
)

REM Запустите main.py
echo Запуск main.py...
python main.py

REM Завершение
echo Запуск завершен.
pause
