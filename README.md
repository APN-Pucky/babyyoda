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

| Interface                                                        | Status | Examples and Notes                                                                                                       |
| ---------------------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------ |
| [histoprint](https://github.com/scikit-hep/histoprint)           | ✅     | [histo1d](examples/interface/histoprint/histo1d.ipynb)                                                                   |
| [mplhep](https://github.com/scikit-hep/mplhep)                   | ✅     | [histo1d](examples/interface/mplhep/histo1d.ipynb), [histo2d](examples/interface/mplhep/histo2d.ipynb)                   |
| [plothist](https://github.com/scikit-hep/plothist)               | ❌     | WIP: https://github.com/cyrraz/plothist/issues/98 Does not support UHI/PlottableProtocol, only boost-histogram()         |
| [uproot](https://github.com/scikit-hep/uproot)                   | ❌     | WIP: https://github.com/scikit-hep/uproot5/issues/1339 [histo1d](examples/interface/uproot/histo1d.ipynb)                |
| [hist](https://github.com/scikit-hep/hist)                       | ✅     | [histo1d](examples/interface/hist/histo1d.ipynb), [histo2d](examples/interface/hist/histo2d.ipynb)                       |
| [boost-histogram](https://github.com/scikit-hep/boost-histogram) | ✅     | [histo1d](examples/interface/boost-histogram/histo1d.ipynb), [histo2d](examples/interface/boost-histogram/histo2d.ipynb) |
| [cuda-histogram](https://github.com/scikit-hep/cuda-histogram)   | ❔     |                                                                                                                          |
| [ROOT](https://github.com/root-project/root)                     | ❔     |                                                                                                                          |

## License

`babyyoda` is distributed under the terms of the [BSD-3-Clause](https://spdx.org/licenses/BSD-3-Clause.html) license.
