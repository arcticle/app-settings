import pytest
from tests.testsetup import mock, builtins
from app_settings.serializables import JsonFile, YamlFile

__filename__ = "usr/test/filename.json"

json_str = '{"foo": "bar", "ham": "eggs"}'
json_obj = {"foo":"bar", "ham":"eggs"}

@mock.patch("app_settings.mixins.__create_file__")
def test_json_deserialize_autocreate(createfile):
    with mock.patch("{}.open".format(builtins), mock.mock_open(read_data=json_str)):
        read_obj = JsonFile(__filename__, auto_create=True).load()
        assert read_obj == json_obj

def test_json_deserialize_no_autocreate():
    read_obj = JsonFile(__filename__).load()
    assert read_obj == {}

def test_json_serialize():
    with mock.patch("{}.open".format(builtins), mock.mock_open()) as mockopen:
        JsonFile(__filename__).flush(json_obj)
        assert mockopen.return_value.write.called_with(json_str)