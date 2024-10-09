# babyyoda

[![PyPI - Version](https://img.shields.io/pypi/v/babyyoda.svg)](https://pypi.org/project/babyyoda)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/babyyoda.svg)](https://pypi.org/project/babyyoda)

-----

## Differences to yoda

`babyyoda` has the advantages

- works with just Python 3 and can be installed with pip.
- makes it easy to manipulate the bin contents.
- tries to adhere to the UHI standard.
- is easy to plot in a Jupyter notebook.
- keeps representation close to the yoda file format.

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

For a less feature complete version, `babyyoda.grogu` is a simpler python drop-in replacement for `yoda`:

```python
import babyyoda.grogu as yoda
```

## License

`babyyoda` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
