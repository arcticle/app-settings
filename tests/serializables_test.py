import pytest
import tests.testsetup
from app_settings.serializables import JsonFile, YamlFile


''' mock has been included in the built-in unittest library since Python 3.3
    This block intends to support Python 2.7 builds in which mock resides
    as a standalone package.'''
try:
    from unittest import mock
except:
    import mock

__filename__ = "usr/test/filename.json"


json_str = '{"foo": "bar", "ham": "eggs"}'
json_obj = {"foo":"bar", "ham":"eggs"}

def test_json_deserialize():
    with mock.patch("builtins.open", mock.mock_open(read_data=json_str)):
        read_obj = JsonFile(__filename__).load()
        assert read_obj == json_obj

def test_json_serialize():
    with mock.patch("builtins.open", mock.mock_open()) as mockopen:
        JsonFile(__filename__).flush(json_obj)
        assert mockopen.return_value.write.called_with(json_str)