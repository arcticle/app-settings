import json, yaml
from ast import literal_eval
from app_settings.mixins import FileMixin, Serializable

__all__ = []

class JsonFile(FileMixin):
    def __init__(self, filename, **kwargs):
        super(JsonFile, self).__init__(filename, JSonSerializer(), **kwargs)

    def load(self):
        if self.auto_create:
            return super(JsonFile, self).load()
        return {}


class YamlFile(FileMixin):
    def __init__(self, filename, default_flow_style=False, **kwargs):
        super(YamlFile, self).__init__(filename, YamlSerializer(default_flow_style), **kwargs)
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
