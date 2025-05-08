@echo off
setlocal enabledelayedexpansion

echo Checking and installing missing dependencies...

for /f "tokens=*" %%i in (data\requirements.txt) do (
    set "line=%%i"
    rem Ignore empty lines or comments
    if not "!line!"=="" if "!line:~0,1!" NEQ "#" (
        for /f "tokens=1,2 delims==" %%a in ("!line!") do (
            set "pkg=%%a"
            set "ver=%%b"
            
            pip show !pkg! >nul 2>&1
            if errorlevel 1 (
                echo !pkg! not installed. Installing...
                pip install "!line!"
            ) else (
                if defined ver (
                    for /f "tokens=2 delims= " %%v in ('pip show !pkg! ^| findstr /b "Version"') do (
                        if not "%%v"=="!ver!" (
                            echo !pkg! version %%v found, but !ver! required. Installing correct version...
                            pip install "!line!"
                        )
                    )
                )
            )
        )
    )
)

echo.
echo Running tests...
pytest --maxfail=5 --rootdir=.

echo.
echo Done.
pause