import os, re, collections
from attrdict import AttrDict
from app_settings import file_search
from app_settings import FileFactory

__all__ = ["Config"]


class Config(object):
    def __init__(self, files=None, dir=None, default=None, filter=None, **kwargs):
        self._validate(files, dir, default)
        self._create_files(files, dir, filter, default, **kwargs)
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

    def __getitem__(self, key):
        return self._get_config(key)

    def _create_files(self, files, dir, filter, default, **kwargs):
        self._files = {}
        files = self._get_files(files, dir, filter)
        for f in files:
            _file = FileFactory.create(f, default, **kwargs)
            _name = self._transform_invalid_name(_file.name)
            self._files[_name] = _file

    def _get_files(self, files, dir, filter):
        if isinstance(files, str):
            return [files]
        if isinstance(files, collections.Iterable):
            return files
        if dir:
            return file_search(dir, filter, recursive=True)
        return []

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

    def _transform_invalid_name(self, filename):
        return re.sub(r"[^A-Za-z]", "_", filename)

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
