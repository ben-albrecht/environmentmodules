from __future__ import print_function

import os, re, subprocess, shlex
from subprocess import Popen, PIPE

# Environment Variables
_home = os.getenv('HOME')
moduleshome = os.getenv('MODULESHOME')
modulespath = os.getenv('MODULESPATH')
loadedmodules = os.getenv('LOADEDMODULES')
lmfiles_ = os.getenv('_LMFILES_')
modulesbeginenv = os.getenv('MODULESBEGINENV')
modulesbeginenv_ = os.getenv('_MODULESBEGINENV_')


# File paths
filepath = {
    #'moduleshome'         : TODO /usr/local/Cellar/modules/3.2.10/Modules
    'rc'                  : os.path.join(moduleshome, 'etc/rc'),
    'modulerc'            : os.path.join(_home, '.modulerc'),
    'modulefiles'         : os.path.join(moduleshome, 'modulefiles'),
    'modulecmd'           : os.path.join(moduleshome, 'bin/modulecmd'),
    #'shell'               : TODO os.path.join(moduleshome, '.init/shell'),
    'moduleavailcache'    : os.path.join(moduleshome, '.moduleavailcache'),
    'moduleavailcachedir' : os.path.join(moduleshome, '.moduleavailcachedir'),
    'modulesbeginenv'     : os.path.join(_home, '.modulesbeginenv'),
    }


# Modified Environment Module python module
def _setup():
    """Setup and confirmation that Environment Modules is installed"""
    # Make sure MODULEPATH is defined
    if 'MODULEPATH' not in os.environ.keys():
        f = open(os.environ['MODULESHOME'] + "/init/.modulespath", "r")
        path = []
        for line in f.readlines():
            line = re.sub("#.*$", '', line)
            if line is not '':
                path.append(line)
        os.environ['MODULEPATH'] = ':'.join(path)

    # Make sure LOADEDMODULES is defined
    if 'LOADEDMODULES' not in os.environ.keys():
        os.environ['LOADEDMODULES'] = ''

    # Make sure MODULESHOME is defined
    if not os.environ.get('MODULESHOME'):
        sys.stderr.write("Error: MODULESHOME must be set\n")
        sys.exit(1)


def _get_modulecmd():
    """Get path to modulecmd."""
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

    output, moduleoutput = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE).communicate()

    exec(output)

    return moduleoutput.decode()


# A partial set of wrapper scripts for module

#
# Command line API
#

def help(modulefile='', flags=''):
    """
     Print  the  usage  of  each  sub-command.   If an
     argument is given, print the Module-specific help
     information for the modulefile(s).
    """
    return module('help {0} {1}'.format(modulefile, flags))


def version():
    """Version of modules"""
    return module('--v')


def load(modulefile, flags=''):
    """Load modulefile(s) into the shell environment."""
    return module('load {0} {1}'.format(modulefile, flags))


def add(modulefile, flags=''):
    """Load modulefile(s) into the shell environment."""
    return module('load {0} {1}'.format(modulefile, flags))


def unload(modulefile, flags=''):
    """Remove  modulefile(s) from the shell environment."""
    return module('unload {0} {1}'.format(modulefile, flags))


def rm(modulefile, flags=''):
    """Remove  modulefile(s) from the shell environment."""
    return module('unload {0} {1}'.format(modulefile, flags))


def swap(modulefile1, modulefile2):
    """
     Switch loaded modulefile1 with  modulefile2.   If modulefile1
     is not specified, then it is assumed to be the currently
     loaded module with  the  same root name as modulefile2.
     return module('swap {0} {1}'.format(modulefile1, modulefile2))
    """
    return module('swap {0} {1}'.format(modulefile1, modulefile2))


def switch(modulefile1, modulefile2):
    """
     Switch loaded modulefile1 with  modulefile2.   If modulefile1
     is not specified, then it is assumed to be the currently
     loaded module with  the  same root name as modulefile2.
     return module('swap {0} {1}'.format(modulefile1, modulefile2))
    """
    return module('swap {0} {1}'.format(modulefile1, modulefile2))


def show(modulefile, flags=''):
    """
     Display    information    about   one   or   more modulefiles.  The
     display sub-command  will  list the  full  path  of the modulefile(s) and
     all (or most)   of   the    environment    changes    the modulefile(s)
     will make if loaded.  (It will not display  any  environment  changes
     found  within conditional statements.)
    """
    return module('show {0} {1}'.format(modulefile, flags))


def display(modulefile, flags=''):
    """
     Display    information    about   one   or   more modulefiles.  The
     display sub-command  will  list the  full  path  of the modulefile(s) and
     all (or most)   of   the    environment    changes    the modulefile(s)
     will make if loaded.  (It will not display  any  environment  changes
     found  within conditional statements.)
    """
    return module('show {0} {1}'.format(modulefile, flags))


def ls(flags='-t'):
    """List loaded modules."""
    return module('list {0}'.format(flags))


def avail(path, flags=''):
    """
     List  all  available  modulefiles  in the current
     MODULEPATH, where the sorting order is  given  by
     the LC_COLLATE locale environment variable.

     All directories in the MODULEPATH are recursively
     searched  for  files  containing  the  modulefile
     magic cookie.

     If  an  argument is given, then each directory in
     the MODULEPATH is searched for modulefiles  whose
     pathname match the argument.

     Multiple   versions  of  an  application  can  be
     supported by  creating  a  subdirectory  for  the
     application   containing   modulefiles  for  each
     version.
    """
    return module('avail {0} {1}'.format(path, flags))


def use(directory, flags=''):
    """
     Prepend one or more directories to the MODULEPATH
     environment  variable.   The  --append  flag will
     append the directory to MODULEPATH.
    """
    return module('use {0} {1}'.format(directory, flags))


def unuse(directory):
    """
     Remove  one  or   more   directories   from   the
     MODULEPATH environment variable.
    """
    return module('unuse {0} {1}'.format(directory))


def update():
    """
     Attempt  to  reload  all loaded modulefiles.  The
     environment will be  reconfigured  to  match  the
     environment saved in ${HOME}/.modulesbeginenv (if
     BEGINENV=1)   or   the   file   pointed   at   by
     $MODULESBEGINEV    (if   BEGINENV=99)   and   the
     modulefiles will be reloaded.  This is only valid
     if  modules was configured with --enable-beginenv
     (which defines  BEGINENV),  otherwise  this  will
     cause  a  warning.   update  will only change the
     environment variables that the modulefiles set.
    """
    return module('update {0} {1}'.format(directory))


def clear():
    """
     Force the Modules  package  to  believe  that  no
     modules are currently loaded.
    """
    return module('clear')


def purge():
    """Unload all loaded modulefiles."""
    return module('purge')


def refresh():
    """
     Force  a refresh of all non-persistent components
     of currently loaded modules.  This should be used
     on  derived  shells  where  aliases  need  to  be
     reinitialized but the environment variables  have
     already been set by the currently loaded modules.
    """
    return module('refresh')


def whatis(modulefile):
    """
     Display the information set  up  by  the  module-
     whatis     commands    inside    the    specified
     modulefile(s). If no modulefile is specified, all
     'whatis' lines will be shown.
    """
    return module('whatis {0}'.format(modulefile))


# Module file API
def isloaded(modulefile):
    return bool([m for m in ls() if modulefile in m])
