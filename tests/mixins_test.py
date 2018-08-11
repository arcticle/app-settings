import pytest
import tests.testsetup
from app_settings.mixins import FileMixin, Serializable


''' mock has been included in the built-in unittest library since Python 3.3
    This block intends to support Python 2.7 builds in which mock resides
    as a standalone package.'''
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

@mock.patch("tests.mixins_test.SerializableMock", spec=SerializableMock)
def test_deserialize_called_onload(serializable):
    with mock.patch("builtins.open", create=True) as open_mock:
        FileMixin(__filename__, serializable.return_value).load()
        assert serializable.return_value._deserialize.called_with(open_mock)

@mock.patch("tests.mixins_test.SerializableMock", spec=SerializableMock)
def test_serialize_called_onflush(serializable):
    _dummy_str = "dummy"
    with mock.patch("builtins.open", create=True) as open_mock:
        FileMixin(__filename__, serializable.return_value).flush(_dummy_str)
        assert serializable.return_value._deserialize.called_with(_dummy_str, open_mock)
