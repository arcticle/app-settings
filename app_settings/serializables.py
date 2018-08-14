import json, yaml
from ast import literal_eval
from app_settings import FileMixin, Serializable, FileInfo

__all__ = []


class JsonFile(FileMixin):
    def __init__(self, fileinfo, **kwargs):
        super(JsonFile, self).__init__(fileinfo, JSonSerializer(), **kwargs)

    def load(self):
        if self.auto_create:
            return super(JsonFile, self).load()
        return {}


class YamlFile(FileMixin):
    def __init__(self, fileinfo, default_flow_style=False, **kwargs):
        super(YamlFile, self).__init__(fileinfo, YamlSerializer(default_flow_style), **kwargs)
        self._default_flow_style = default_flow_style
    
    def load(self):
        if self.auto_create:
            return super(YamlFile, self).load()
        return {}


class JSonSerializer(Serializable):
    def _deserialize(self, fs):
        s = fs.read()
        return json.loads(s if s != "" else "{}")

    def _serialize(self, s, fs):
        fs.write(json.dumps(s))


class YamlSerializer(Serializable):
    def __init__(self, default_flow_style):
        self._default_flow_style = default_flow_style

    def _deserialize(self, fs):
        s = yaml.load(fs.read())
        if not s:
            s = "{}"
        if isinstance(s, str):
            s = literal_eval(s)
        return s

    def _serialize(self, s, fs):
        yaml.dump(s, fs, default_flow_style=self._default_flow_style)


class FileFactory(object):
    _supported_file_types = {
        "json" : JsonFile,
        "yaml" : YamlFile
    }
    
    @staticmethod
    def create(file, default=None, **kwargs):
        fi = FileInfo.create(file)
        if fi.type in FileFactory._supported_file_types:
            return FileFactory._supported_file_types[fi.type](fi, **kwargs)
        elif default:
            fi.type = default(file)
        if not fi.type in FileFactory._supported_file_types:
            raise Exception("Unsupported file type has been requested")
        return FileFactory._supported_file_types[fi.type](fi, **kwargs)
        
        
