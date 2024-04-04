# Development Guide

This document describes the process for developing this application.

## Getting Started

The software is developed using _Python 3.10.9_.
To run run the application, simply run `run.py`. This will open the GUI.

### Requirement

- Python >3.8

### Installation

1. It is recommended to start with creating and entering virtual environment:

```bash
python -m venv env
./env/Scripts/activate
```

2. Install Python dependencies

```bash
pip install -r requirements-dev.txt
```

### Running the app

The app is developed using _Flask_ + _Pywebview_.
Flask handles all the routing and communication between back-end and the front-end.
Pywebview creates GUI window to display the front-end.

1. Make sure CWD is in `.\src\`
2. Run file:

```bash
python run.py
```

**Debugging**

If needed we can skip using _Pywebview_ by altering the code in `run.py`:

```python
...
if __name__ == "__main__":
    application.run(debug=True)
```

### Running individual script

Make sure CWD is in `.\src\`

1. Run scrape.py:

```bash
python -m app.services.scrape
```

2. Run qeury_handler.py:

```bash
python -m app.qeury_handler
```

3. Run scrape_and_store.py:

```bash
python -m app.scrape_and_store
```

## Build

Packaging is done by creating standalone Python executable generated using _PyInstaller_.

1. Run the `build.bat`

```bash
./build-tools/build.bat
```

> Note: Currently all the API keys are exposed. Ideally this should be kept out of the source control and stored privately
