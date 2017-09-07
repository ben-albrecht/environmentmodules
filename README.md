# environmentmodules
Python interface for the [Environment Modules Project](https://github.com/cea-hpc/modules)


## Why?

I needed to test some modulefiles, and found the builtin `python` module insufficient, so I created this as a cleaner interface with a more reasonable build process.

## Example

```python
import environmentmodules as mod

# module load gcc/3.1.1
mod.load('gcc/3.1.1')

mod.switch('gcc', 'gcc/3.2.0')

mod.unload('gcc')

if mod.isloaded('gcc-5'):
    print('gcc-5 loaded successfully!')
```
