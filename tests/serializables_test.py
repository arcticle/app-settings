import pytest
from tests.testsetup import mock, builtins
from app_settings.serializables import JsonFile, YamlFile, FileFactory
from app_settings.mixins import FileInfo

__filename__ = "usr/test/filename.json"
__fileinfo__ = FileInfo.create(__filename__)

json_str = '{"foo": "bar", "ham": "eggs"}'
json_obj = {"foo":"bar", "ham":"eggs"}

@mock.patch("app_settings.mixins.__create_file__")
def test_json_deserialize_autocreate(createfile):
    with mock.patch("{}.open".format(builtins), mock.mock_open(read_data=json_str)):
        read_obj = JsonFile(__fileinfo__, auto_create=True).load()
        assert read_obj == json_obj

def test_json_deserialize_no_autocreate():
    read_obj = JsonFile(__fileinfo__).load()
    assert read_obj == {}

def test_json_serialize():
    with mock.patch("{}.open".format(builtins), mock.mock_open()) as mockopen:
        JsonFile(__fileinfo__).flush(json_obj)
        assert mockopen.return_value.write.called_with(json_str)

def test_filefactory_create_supported():
    file = FileFactory.create("usr/foo.json")
    assert isinstance(file, JsonFile)
    assert file.name == "foo"

def test_filefactory_create_ussupported():
    with pytest.raises(Exception):
        FileFactory.create("usr/foo.xml")

def test_filefactory_create_supported_with_default_type_resolver():
    file = FileFactory.create("usr/foo", lambda t: "yaml")
    assert isinstance(file, YamlFile)
    assert file.name == "foo"

def test_filefactory_create_unsupported_with_default_type_resolver():
    with pytest.raises(Exception):
        FileFactory.create("usr/foo", lambda t: None)