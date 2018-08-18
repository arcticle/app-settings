import pytest
from tests import mock, builtins
from app_settings import Config

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

def test_getfiles_single_file():
    cfg = Config("foo.json", auto_create=False)
    assert cfg.files[0] == "foo"

def test_getfiles_single_file_in_list():
    cfg = Config(["foo.json"], auto_create=False)
    assert cfg.files[0] == "foo"

def test_getfiles_some_files():
    cfg = Config(["foo.json", "baz.yaml"], auto_create=False)
    assert sorted(cfg.files) == ["baz","foo"]

def test_getfiles_duplicate_names():
    cfg = Config(["foo.json", "foo.yaml"], auto_create=False)
    assert cfg.files == ["foo"]

def test_getfiles_invalid_chars_in_filename():
    invalid_filename = "File()`~!@#$%^&*-+=|{}[]:;\"'<>,.?name.json"
    cfg = Config([invalid_filename], auto_create=False)
    assert cfg.files == ["File_____________________________name"]

def test_check_file_attribute_single_file():
    cfg = Config(["foo.json"], auto_create=False)
    assert not cfg.foo

def test_check_file_attribute_some_files():
    cfg = Config(["foo.json", "baz.yaml"], auto_create=False)
    assert not cfg.foo
    assert not cfg.baz

def test_check_file_attribute_duplicate_names():
    cfg = Config(["foo.json", "foo.yaml"], auto_create=False)
    assert not cfg.foo

def test_check_file_attribute_invalid_chars_in_filename():
    invalid_filename = "File()`~!@#$%^&*-+=|{}[]:;\"'<>,.?name.json"
    cfg = Config([invalid_filename], auto_create=False)
    assert not cfg.File_____________________________name

def test_set_attribute_simple_type():
    cfg = Config(["foo.json", "baz.yaml"], auto_create=False)
    cfg.foo.bar = "bar"
    cfg.baz.ham = "ham"
    assert cfg.foo.bar == "bar"
    assert cfg.baz.ham == "ham"

def test_set_attribute_complex_type():
    cfg = Config(["foo.json"], auto_create=False)
    cfg.foo.bar = {"baz":"ham"}
    assert cfg.foo.bar.baz == "ham"

def test_set_attribute_more_complex_type():
    cfg = Config(["foo.json"], auto_create=False)
    cfg.foo.bar = {"baz":{"eggs":{"price":7, "currency":"pounds"}}}
    assert "{} {}".format(cfg.foo.bar.baz.eggs.price, cfg.foo.bar.baz.eggs.currency) == "7 pounds"
