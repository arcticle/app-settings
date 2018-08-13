import sys, os

_dir = os.path.dirname(__file__)
source_dir = os.path.join(_dir,os.pardir,"app_settings")
sys.path.append(os.path.abspath(source_dir))

''' mock has been included in the built-in unittest library since Python 3.3
    This block intends to support Python 2.7 builds in which mock resides
    as a standalone package.'''
if sys.version_info.major == 3:
    from unittest import mock
    mock = mock
    builtins = "builtins"
else:
    import mock
    mock = mock
    builtins = "__builtin__"
