@echo off
setlocal enabledelayedexpansion

REM Получаем пути к файлам из параметров
set "VERSION_FILE=%~1"
set "COPY_PATH=%~2"

REM Проверяем, переданы ли оба параметра
if "%VERSION_FILE%"=="" (
    echo Ошибка: Необходимо указать путь к файлу версии.
    exit /b 1
)

if "%COPY_PATH%"=="" (
    echo Ошибка: Необходимо указать путь для копирования файла.
    exit /b 1
)

:input_version
echo Введите версию (формат 0.0.0):
set /p VERSION=

REM Проверка формата версии
for /f "tokens=1,2,3 delims=." %%a in ("%VERSION%") do (
    set "MAJOR=%%a"
    set "MINOR=%%b"
    set "PATCH=%%c"
)

REM Проверка, что все части версии являются числами
if "!MAJOR!" == "" goto invalid_format
if "!MINOR!" == "" goto invalid_format
if "!PATCH!" == "" goto invalid_format

REM Проверка, что все части версии - числа
for %%i in (!MAJOR! !MINOR! !PATCH!) do (
    set /a "temp=%%i+0" >nul 2>&1
    if errorlevel 1 goto invalid_format
)

REM Чтение предыдущей версии из файла
if exist "%VERSION_FILE%" (
    set /p PREVIOUS_VERSION=<"%VERSION_FILE%"
) else (
    set "PREVIOUS_VERSION=0.0.0"
)

REM Функция для сравнения версий
call :compare_versions "!VERSION!" "!PREVIOUS_VERSION!" result

if "!result!" == "greater" (
    echo Версия %VERSION% больше предыдущей версии %PREVIOUS_VERSION%.
    echo !VERSION! > "%VERSION_FILE%"
    echo Версия записана в файл "%VERSION_FILE%"
    copy "%VERSION_FILE%" "%COPY_PATH%\version.txt" /Y
) else (
    echo Версия %VERSION% не больше предыдущей версии %PREVIOUS_VERSION%. Пожалуйста, попробуйте еще раз.
    goto input_version
)

goto :eof

:invalid_format
echo Неверный формат версии. Убедитесь, что вы вводите версию в формате 0.0.0.
goto input_version

:compare_versions
setlocal
set "v1=%~1"
set "v2=%~2"

for /f "tokens=1,2,3 delims=." %%a in ("!v1!") do (
    set "MAJOR1=%%a"
    set "MINOR1=%%b"
    set "PATCH1=%%c"
)

for /f "tokens=1,2,3 delims=." %%a in ("!v2!") do (
    set "MAJOR2=%%a"
    set "MINOR2=%%b"
    set "PATCH2=%%c"
)

REM Сравнение версий
if !MAJOR1! gtr !MAJOR2! (
    endlocal & set "%~3=greater" & exit /b
) else if !MAJOR1! lss !MAJOR2! (
    endlocal & set "%~3=less" & exit /b
)

if !MINOR1! gtr !MINOR2! (
    endlocal & set "%~3=greater" & exit /b
) else if !MINOR1! lss !MINOR2! (
    endlocal & set "%~3=less" & exit /b
)

if !PATCH1! gtr !PATCH2! (
    endlocal & set "%~3=greater" & exit /b
) else (
    endlocal & set "%~3=less" & exit /b
)
endlocal & set "%~3=same" & exit /b
