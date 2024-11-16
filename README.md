# babyyoda

[![PyPI - Version](https://img.shields.io/pypi/v/babyyoda.svg)](https://pypi.org/project/babyyoda)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/babyyoda.svg)](https://pypi.org/project/babyyoda)
[![CI/CD](https://github.com/APN-Pucky/babyyoda/actions/workflows/ci.yml/badge.svg)](https://github.com/APN-Pucky/babyyoda/actions/workflows/ci.yml)
[![Code Coverage](https://codecov.io/gh/APN-Pucky/babyyoda/graph/badge.svg?branch=master)](https://codecov.io/gh/APN-Pucky/babyyoda?branch=master)

______________________________________________________________________

## Differences to yoda

`babyyoda` has the advantages

- works with just Python 3 and can be installed with pip.
- makes it easy to manipulate the bin contents (compared to YODA-1).
- tries to adhere to the UHI standard.
- is easy to plot in a Jupyter notebook.
- keeps data representation close to the yoda file format.

and the disadvantages to `yoda` are that it

- is slower.
- is not as feature complete.
- is not as well tested.
- only has histogram support.

## Installation

```console
pip install babyyoda
```

## Design

`babyyoda` is designed to be a drop-in replacement for `yoda` with a few key differences:

```python
import babyyoda as yoda
```

with UHI support.
It can use either `yoda` (C++) or `babyyoda.grogu` (Python) as backend.
At some point the UHI support might be adapted by the original `yoda` package.

For a less feature complete version, `babyyoda.grogu` is a simpler python drop-in replacement for `yoda` without UHI:

```python
import babyyoda.grogu as yoda
```

or force yoda use with

```python
import babyyoda.yoda as yoda
```

## Interfaces

| Interface                                                        | Status | Examples                                                                                                             |
| ---------------------------------------------------------------- | ------ | -------------------------------------------------------------------------------------------------------------------- |
| [histoprint](https://github.com/scikit-hep/histoprint)           | ✅     | [histoprint histo1d](examples/interface/histoprint/histo1d.ipynb)                                                    |
| [mplhep](https://github.com/scikit-hep/mplhep)                   | ✅     | [mplhep histo1d](examples/interface/mplhep/histo1d.ipynb), [mplhep histo2d](examples/interface/mplhep/histo2d.ipynb) |
| [plothist](https://github.com/scikit-hep/plothist)               | ❌     | Does not support UHI/PlottableProtocol, only boost-histogram                                                         |
| [uproot](https://github.com/scikit-hep/uproot)                   | ❌     | WIP: [uproot histo1d](examples/interface/uproot/histo1d.ipynb)                                                       |
| [hist](https://github.com/scikit-hep/hist)                       | ❌     | WIP: Unidirectional conversion planned                                                                               |
| [boost-histogram](https://github.com/scikit-hep/boost-histogram) | ❌     | WIP: Unidirectional conversion planned                                                                               |
| [cuda-histogram](https://github.com/scikit-hep/cuda-histogram)   | ❔     |                                                                                                                      |
| [ROOT](https://github.com/root-project/root)                     | ❔     |                                                                                                                      |

## License

`babyyoda` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
