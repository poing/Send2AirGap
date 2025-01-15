# Send 2 Air-Gap

![Static Badge](https://img.shields.io/badge/Status%3A-Pre--Alpha-%23FF0000)
[![CI](https://github.com/poing/Send2AirGap/actions/workflows/main.yml/badge.svg)](https://github.com/poing/Send2AirGap/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/poing/Send2AirGap/branch/0.0.4/graph/badge.svg?token=LTQYLRKJ6M)](https://codecov.io/gh/poing/Send2AirGap)
[![PyPI version](https://badge.fury.io/py/send2airgap.svg)](https://badge.fury.io/py/send2airgap)
[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)
[![JS2PySecrets Documentation](https://img.shields.io/badge/Documentation-white?logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz48c3ZnIGlkPSJhIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA4MDEgNjE3LjU2Ij48cGF0aCBkPSJNODAwLjUsMjg3LjNoLTkxLjU5QzY5Ny44NSwxMjcuMyw1NjQuMTYuNSw0MDEuMzkuNVMxMDQuOTQsMTI3LjMsOTMuODcsMjg3LjNILjV2NDIuOTVoOTMuMzdjMTEuMDcsMTYwLDE0NC43NSwyODYuOCwzMDcuNTIsMjg2LjhzMjk2LjQ1LTEyNi44LDMwNy41Mi0yODYuOGg5MS41OXYtNDIuOTVaTTQwMS4zOSw1NzQuMTFjLTEzOS4wNywwLTI1My40OC0xMDcuNTUtMjY0LjQ1LTI0My44NWgxMzIuMDJ2MTU3LjY3bDIyMC4xMy0xMzkuNDF2MTM3LjQ0aDQyLjk1di0xNTUuN2gxMzMuOGMtMTAuOTcsMTM2LjMtMTI1LjM4LDI0My44NS0yNjQuNDUsMjQzLjg1Wk0zMTEuOTEsMjA3LjE4bDE2MC4wNCwxMDEuMzUtMTYwLjA0LDEwMS4zNXYtMjAyLjcxWk01MzIuMDQsMjg3LjN2LTE1NS43aC00Mi45NXYxMzYuOTVsLTIyMC4xMy0xMzkuNDF2MTU4LjE3aC0xMzIuMDJjMTAuOTctMTM2LjMsMTI1LjM4LTI0My44NSwyNjQuNDUtMjQzLjg1czI1My40OCwxMDcuNTUsMjY0LjQ1LDI0My44NWgtMTMzLjhaIiBmaWxsPSIjZmZmIiBzdHJva2U9IiMwMDAiIHN0cm9rZS1taXRlcmxpbWl0PSIxMCIvPjwvc3ZnPg==&labelColor=526CFE)](https://poing.github.io/Send2AirGap/)




This is a project to provide data to an air-gapped system.

The air-gapped system uses a camera to receive unidirectional communication.  Creating a "data diode" that can be used to provide data **to** systems in a high security environment.

The *unsecure* system will display the `data` using qr-codes, that are decoded on the secure air-gapped system.

There's even a method to *acknowledge* receipt of the `data`.  The method *involves* inputing an associated timestamp on the *unsecure* system.  This would *typically* be a manual operation, but **does** provide *possible* ways to automate the acknowledgement.  





## Install it from PyPI

```bash
pip install send2airgap
```

## Usage

```py
from send2airgap import BaseClass
from send2airgap import base_function

BaseClass().base_method()
base_function()
```

```bash
$ python -m send2airgap
#or
$ send2airgap
```

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.
