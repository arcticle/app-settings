import os
from attrdict import AttrDict
from serializables import JsonFile, YamlFile

__all__ = ["Config"]


class FileFactory(object):
    _supported_file_types = {
        "json" : JsonFile,
        "yaml" : YamlFile
    }
    
    @staticmethod
    def create_file(type, filename, **kwargs):
        if not type in FileFactory._supported_file_types:
            raise Exception("Unsupported file type has been requested")
        return FileFactory._supported_file_types[type](filename, **kwargs)


class Config(object):
    def __init__(self, files=None, dir=None, type=None, **kwargs):
        self._create_files(files, type, **kwargs)

    def _create_files(self, files, type, **kwargs):
        self._files = {}
        for _file in files:
            _name, _type, _dir = self._parse_filename(_file)
            if type:
                _type = type
            self._files[_name] = FileFactory.create_file(_type, _file, **kwargs)
        self._load_files()

    def _load_files(self):
        for _name, _file in self._files.items():
            self._add_config(_name, _file.load())

    def _parse_filename(self, filename):
        _dir, _file = os.path.split(filename)
        _name, _ext = os.path.splitext(_file)
        _type = _ext[1:]
        if not _type:
            return "json"
        return (_name, _type, _dir)

    def _get_config(self, config_name):
        return getattr(self, config_name)

    def _add_config(self, config_name, config):
        setattr(self, config_name, AttrDict(config))

    def save(self, config_name=None):
        if config_name:
            if config_name in self._files:
                config_dict = dict(self._get_config(config_name))
                self._files[config_name].flush(config_dict)
        else:
            for _name, _file in self._files.items():
                config_dict = dict(self._get_config(_name))
                _file.flush(config_dict)

files = ["c:\\users\\u2r\\desktop\\test1.yaml", "c:\\users\\u2r\\desktop\\test2.yaml"]

c = Config(files, auto_create=True)

c.test1.count=7
c.test1.path="my custom path"
c.test1["datasets"]={}
c.test1["datasets"]["train"]="train dataset is there"


c.test2.count=8
c.test2.path="my very custom path"

c.save("test1")
c.save("test2")

