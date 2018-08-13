import os, collections
from attrdict import AttrDict
from app_settings.utils import filename_parser, file_search, product
from app_settings.serializables import JsonFile, YamlFile

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


def _resolve_file(filename, resolve_file=None):
    type=None
    name, ext, _ = filename_parser(filename)
    if ext in FileFactory._supported_file_types:
        type = ext
    elif resolve_file:
        type = resolve_file(filename)
    return (name, type)


class Config(object):
    def __init__(self, files=None, dir=None, resolve_type=None, filter=None, **kwargs):
        self._validate(files, dir, resolve_type)
        self._resolve_type = resolve_type
        self._create_files(files, dir, filter, **kwargs)
        self._load_files()

    def save(self, config_name):
        if config_name in self._files:
            self._save_config(config_name)
    
    def save_all(self):
        for _name in self._files:
            self.save(_name)

    @property
    def files(self):
        return list(self._files.keys())

    def _create_files(self, files, dir, filter, **kwargs):
        self._files = {}
        specs = self._get_file_props(files, dir, filter)
        for f, type in specs:
            self._files[f[0]] = FileFactory.create_file(type, f[1], **kwargs)

    def _get_file_props(self, files, dir, filter):
        file_props = self._resolve_props_from_file(files)
        if file_props: 
            return file_props
        file_props = self._resolve_props_from_dir(dir, filter)
        if file_props:
            return file_props
        return []

    def _resolve_props_from_file(self, files):
        if not files: return False
        if not isinstance(files, collections.Iterable):
            files = [files]
        files, types = self._resolve_props(files)
        return zip(files, types)
        
    def _resolve_props_from_dir(self, dir, filter):
        if not dir : return None
        files = file_search(dir, filter, recursive=True)
        files, types = self._resolve_props(files) 
        return zip(files, types)

    def _resolve_props(self, files):
        _files, _types = [], []
        for f in files:
            name, type = _resolve_file(f, self._resolve_type)
            if not type: continue
            _files.append((name, f))
            _types.append(type)
        return _files, _types

    def _load_files(self):
        for _name, _file in self._files.items():
            self._add_config(_name, _file.load())

    def _get_config(self, config_name):
        return getattr(self, config_name)

    def _add_config(self, config_name, config):
        setattr(self, config_name, AttrDict(config))

    def _save_config(self, name):
        config_dict = dict(self._get_config(name))
        self._files[name].flush(config_dict)

    def _validate(self, files, dir, resolve_type):
        if not files and not dir:
            raise ValueError("No files or search directory provided.")
        if files:
            if isinstance(files, collections.Iterable):
                for f in files:
                    assert isinstance(f, str)
            else:
                assert isinstance(files, str)
        if dir:
            assert isinstance(dir, str)
            assert os.path.isdir(dir)

