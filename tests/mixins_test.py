import pytest
from tests.testsetup import mock, builtins
from app_settings.mixins import FileMixin, Serializable, FileInfo

__filename__ = "usr/test/filename.json"
__fileinfo__ = FileInfo.create(__filename__)

class SerializableMock(Serializable):
    def __init__(self, filename):
        pass

@mock.patch("tests.mixins_test.SerializableMock", spec=SerializableMock)
def test_init_valid_serializable(serializable):
    FileMixin(__fileinfo__, serializable)

@mock.patch("tests.mixins_test.SerializableMock")
def test_init_invalid_serializable(serializable):
    with pytest.raises(AssertionError):
        FileMixin(__fileinfo__, serializable)

@mock.patch("tests.mixins_test.SerializableMock", spec=SerializableMock)
def test_init_filename(serializable):
    _file = FileMixin(__fileinfo__, serializable)
    assert _file.name == __fileinfo__.name

@mock.patch("app_settings.mixins.FileMixin._ensure_file")
@mock.patch("tests.mixins_test.SerializableMock", spec=SerializableMock)
def test_ensurefile_notcalled_noautocreate(serializable, ensurefile):
    _file = FileMixin(__fileinfo__, serializable, auto_create=False)
    assert not ensurefile.called

@mock.patch("app_settings.mixins.FileMixin._ensure_file")
@mock.patch("tests.mixins_test.SerializableMock", spec=SerializableMock)
def test_ensurefile_called_autocreate(serializable, ensurefile):
    _file = FileMixin(__fileinfo__, serializable, auto_create=True)
    assert ensurefile.called

@mock.patch("app_settings.mixins.__create_file__")
@mock.patch("tests.mixins_test.SerializableMock", spec=SerializableMock)
def test_createfile_called_ifnotexists(serializable, createfile):
    with mock.patch("app_settings.mixins.__file_exists__", return_value=False):
        _file = FileMixin(__fileinfo__, serializable, auto_create=True)
        assert createfile.called

@mock.patch("app_settings.mixins.__create_file__")
@mock.patch("tests.mixins_test.SerializableMock", spec=SerializableMock)
def test_createfile_notcalled_ifexists(serializable, createfile):
    with mock.patch("app_settings.mixins.__file_exists__", return_value=True):
        _file = FileMixin(__fileinfo__, serializable, auto_create=True)
        assert not createfile.called

@mock.patch("tests.mixins_test.SerializableMock", spec=SerializableMock)
def test_deserialize_called_onload(serializable):
    with mock.patch("{}.open".format(builtins), create=True) as open_mock:
        FileMixin(__fileinfo__, serializable.return_value).load()
        assert serializable.return_value._deserialize.called_with(open_mock)

@mock.patch("tests.mixins_test.SerializableMock", spec=SerializableMock)
def test_serialize_called_onflush(serializable):
    _dummy_str = "dummy"
    with mock.patch("{}.open".format(builtins), create=True) as open_mock:
        FileMixin(__fileinfo__, serializable.return_value).flush(_dummy_str)
        assert serializable.return_value._deserialize.called_with(_dummy_str, open_mock)

def test_fileinfo_create_Case1():
    fi = FileInfo.create("foo.json")
    assert fi.name == "foo"
    assert fi.path == "foo.json"
    assert fi.type == "json"

def test_fileinfo_create_Case2():
    fi = FileInfo.create("/usr/foo.json")
    assert fi.name == "foo"
    assert fi.path == "/usr/foo.json"
    assert fi.type == "json"

def test_fileinfo_create_noextension():
    fi = FileInfo.create("/usr/foo")
    assert fi.name == "foo"
    assert fi.path == "/usr/foo"
    assert fi.type == ""

def test_fileinfo_create_period_in_filename():
    fi = FileInfo.create("/usr/foo.bar.json")
    assert fi.name == "foo.bar"
    assert fi.path == "/usr/foo.bar.json"
    assert fi.type == "json"