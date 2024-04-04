pyinstaller --noconfirm ^
    --onefile --windowed ^
    --icon "%~dp0/subway-locator.ico" ^
    --name "Subway Locator" ^
    --clean ^
    --add-data "%~dp0../src/app/static;static/" ^
    --add-data "%~dp0../src/app/templates;templates/" ^
    --distpath "%~dp0../dist/" ^
    "%~dp0../src/run.py"