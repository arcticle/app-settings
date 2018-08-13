import pytest
from tests.testsetup import mock, builtins
import sys
print(sys.path)
from app_settings.config import Config

def test_init_no_args():
    with pytest.raises(ValueError):
        Config()

def test_init_invalid_args_file_Case1():
    with pytest.raises(AssertionError):
        Config([None])

def test_init_invalid_args_file_Case2():
    with pytest.raises(AssertionError):
        Config(["usr/test", None])

def test_init_invalid_args_file_Case3():
    with pytest.raises(ValueError):
        Config(None)

def test_init_invalid_args_file_Case4():
    with pytest.raises(AssertionError):
        Config(4)

def test_init_invalid_args_dir_Case1():
    with pytest.raises(ValueError):
        Config(dir=None)

def test_init_invalid_args_dir_Case2():
    with pytest.raises(AssertionError):
        Config(dir=4)

def test_init_invalid_args_dir_Case3():
    with pytest.raises(AssertionError):
        Config(dir="invalid_dir")

def test_getfilespecs_singlefile():
    cfg = Config(["foo.json"], auto_create=False)
    assert cfg.files[0] == "foo"

def test_getfilespecs_somefiles():
    cfg = Config(["foo.json", "baz.yaml"], auto_create=False)
    assert cfg.files == ["foo","baz"]

