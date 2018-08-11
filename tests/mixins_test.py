import pytest
import tests.testsetup
from app_settings.mixins import FileMixin, Serializable

try:
    from unittest import mock
except:
    import mock

__filename__ = "usr/test/filename.json"

class SerializableMock(Serializable):
    def __init__(self, filename):
        pass

@mock.patch("tests.mixins_test.SerializableMock", spec=SerializableMock)
def test_init_valid_serializable(serializable):
    FileMixin(__filename__, serializable)

@mock.patch("tests.mixins_test.SerializableMock")
def test_init_invalid_serializable(serializable):
    with pytest.raises(AssertionError):
        FileMixin(__filename__, serializable)

@mock.patch("tests.mixins_test.SerializableMock", spec=SerializableMock)
def test_init_filename(serializable):
    _file = FileMixin(__filename__, serializable)
    assert _file.filename == __filename__

@mock.patch("app_settings.mixins.FileMixin._ensure_file")
@mock.patch("tests.mixins_test.SerializableMock", spec=SerializableMock)
def test_ensurefile_notcalled_noautocreate(serializable, ensurefile):
    _file = FileMixin(__filename__, serializable, auto_create=False)
    assert not ensurefile.called

@mock.patch("app_settings.mixins.FileMixin._ensure_file")
@mock.patch("tests.mixins_test.SerializableMock", spec=SerializableMock)
def test_ensurefile_called_autocreate(serializable, ensurefile):
    _file = FileMixin(__filename__, serializable, auto_create=True)
    assert ensurefile.called

@mock.patch("app_settings.mixins.__create_file__")
@mock.patch("tests.mixins_test.SerializableMock", spec=SerializableMock)
def test_createfile_called_ifnotexists(serializable, createfile):
    with mock.patch("app_settings.mixins.__file_exists__", return_value=False):
        _file = FileMixin(__filename__, serializable, auto_create=True)
        assert createfile.called

@mock.patch("app_settings.mixins.__create_file__")
@mock.patch("tests.mixins_test.SerializableMock", spec=SerializableMock)
def test_createfile_notcalled_ifexists(serializable, createfile):
    with mock.patch("app_settings.mixins.__file_exists__", return_value=True):
        _file = FileMixin(__filename__, serializable, auto_create=True)
        assert not createfile.called
