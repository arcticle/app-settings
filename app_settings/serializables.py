import json, yaml
from ast import literal_eval
from mixins import FileMixin, Serializable

__all__ = []

class JsonFile(FileMixin, Serializable):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, self, **kwargs)
    
    def _deserialize(self, fs):
        s = fs.read()
        return json.loads(s if s != "" else "{}")

    def _serialize(self, s, fs):
        fs.write(json.dumps(s))


class YamlFile(FileMixin, Serializable):
    def __init__(self, filename, default_flow_style=False, **kwargs):
        super().__init__(filename, self, **kwargs)
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


