import os, six, abc
from app_settings import filename_parser

def __file_exists__(filename):
    return os.path.isfile(filename)

def __create_file__(filename):
    _dir = os.path.dirname(filename)
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    with open(filename, "w"):
        pass

class FileMixin(object):
    def __init__(self, fileinfo, serializer, auto_create=False):
        assert isinstance(fileinfo, FileInfo)
        assert isinstance(serializer, Serializable)
        if auto_create:
            self._ensure_file(fileinfo.path)
        self.fileinfo = fileinfo
        self.auto_create = auto_create
        self._serializer = serializer

    @property
    def name(self):
        return self.fileinfo.name

    def load(self):
        try:
            with open(self.fileinfo.path, "r") as _file:
                return self._serializer._deserialize(_file)
        except:
            raise Exception("An error occured while loading file.")

    def flush(self, s):
        try:
            with open(self.fileinfo.path, "w") as fs:
                self._serializer._serialize(s, fs)
        except:
            raise Exception("An error occurred while saving file.")

    def _ensure_file(self, filename):
        if not __file_exists__(filename):
            __create_file__(filename)


class FileInfo(object):
    def __init__(self, name, path, type):
        self.name = name
        self.path = path
        self.type = type

    @staticmethod
    def create(path):
        _name, _type, _ = filename_parser(path)
        return FileInfo(_name, path, _type)


@six.add_metaclass(abc.ABCMeta)
class Serializable(object):
    def __init__(self):
        pass
    
    @abc.abstractmethod
    def _deserialize(self, fs):
        pass

    @abc.abstractmethod
    def _serialize(self, s, fs):
        pass