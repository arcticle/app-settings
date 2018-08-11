import os, six, abc


def __file_exists__(filename):
    return os.path.isfile(filename)

def __create_file__(filename):
    _dir = os.path.dirname(filename)
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    with open(filename, "w"):
        pass

class FileMixin(object):
    def __init__(self, filename, serializer, auto_create=False):
        assert isinstance(serializer, Serializable)
        if auto_create:
            self._ensure_file(filename)
        self.filename = filename
        self._serializer = serializer

    def load(self):
        try:
            with open(self.filename, "r") as _file:
                return self._serializer._deserialize(_file)
        except:
            raise Exception("An error occured while loading file.")

    def flush(self, s):
        try:
            with open(self.filename, "w") as fs:
                self._serializer._serialize(s, fs)
        except:
            raise Exception("An error occurred while saving file.")

    def _ensure_file(self, filename):
        if not __file_exists__(filename):
            __create_file__(filename)

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