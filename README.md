# environmentmodules
Python API for the [Environment Modules Project](http://modules.sourceforge.net/)

I was unhappy with the Python module provided by Environment Modules (poorly named `python`), so I created my own Python module.

Here's a little taste:

```python
import environmentmodules as mod

# module load gcc/3.1.1
mod.load('gcc/3.1.1')

mod.switch('gcc', 'gcc/3.2.0')

mod.unload('gcc')

if mod.isloaded('gcc-5'):
    print('gcc-5 loaded successfully!')
```

#### Advantages over the python module provided by Environment Modules:
* Pythonic API
* A proper setup.py (rather than manually appending to `sys.path` or `$PYTHONPATH`)
* Extended functionality to modulefile-specific calls, i.e. `mod.isloaded('foo')`
* The package is not named `python`
