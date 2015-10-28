from __future__ import print_function

import os, re, subprocess, shlex
from subprocess import Popen, PIPE

# Modified Environment Module python module
def _setup():
    """Setup and confirmation that Environment Modules is installed"""
    # Make sure MODULEPATH is defined
    if not os.environ.has_key('MODULEPATH'):
        f = open(os.environ['MODULESHOME'] + "/init/.modulespath", "r")
        path = []
        for line in f.readlines():
            line = re.sub("#.*$", '', line)
            if line is not '':
                path.append(line)
        os.environ['MODULEPATH'] = ':'.join(path)

    # Make sure LOADEDMODULES is defined
    if not os.environ.has_key('LOADEDMODULES'):
        os.environ['LOADEDMODULES'] = ''

    # Make sure MODULESHOME is defined
    if not os.environ.get('MODULESHOME'):
        sys.stderr.write("Error: MODULESHOME must be set\n")
        sys.exit(1)


def _get_modulecmd():
    # Get path to modulecmd
    modulekeys = [m for m in os.environ.keys() if 'BASH_FUNC_module' in m]
    if not modulekeys:
        sys.stderr.write("Error: BASH_FUNC_module must be set\n")
        sys.exit(1)
    else:
        modulekey = modulekeys[0]

    modcmd = os.getenv(modulekey).split()
    modulecmd = [c for c in modcmd if 'modulecmd' in c][0].strip('`')

    return modulecmd


def module(*args):
    """Call modulecmd with 'python' argument to get python commands for exec"""

    _setup()

    modulecmd = _get_modulecmd()

    args = ' '.join(args)
    cmd = shlex.split('{0} python {1}'.format(modulecmd, args))

    output, moduleoutput = Popen(cmd, stdout=PIPE, stderr=PIPE).communicate()

    exec(output)

    return moduleoutput


# A partial set of wrapper scripts for module

# Command line API
def ls(flags='-t'):
    return module('list {0}'.format(flags))


def show(modulefile):
    return module('show {0}'.format(modulefile))


def load(modulefile):
    return module('load {0}'.format(modulefile))


def unload(modulefile):
    return module('unload {0}'.format(modulefile))


def swap(modulefile1, modulefile2):
    return module('swap {0} {1}'.format(modulefile1, modulefile2))


def help(modulefile):
    return module('help {0}'.format(modulefile))


# Module file API
def isloaded(modulefile):
    return bool([m for m in ls() if modulefile in m])

