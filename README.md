# Send 2 Air-Gap

[![codecov](https://codecov.io/gh/poing/Send2AirGap/branch/0.0.3/graph/badge.svg?token=LTQYLRKJ6M)](https://codecov.io/gh/poing/Send2AirGap)

[![CI](https://github.com/poing/Send2AirGap/actions/workflows/main.yml/badge.svg)](https://github.com/poing/Send2AirGap/actions/workflows/main.yml)

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
