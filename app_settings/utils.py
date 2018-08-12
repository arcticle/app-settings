import os


def filename_parser(filename, default=None):
    _dir, _file = os.path.split(filename)
    _name, _ext = os.path.splitext(_file)
    _type = _ext[1:]
    return (_name, _type, _dir)


def file_search(root_dir, filter=None, recursive=False):
    assert isinstance(root_dir, str)
    assert os.path.isdir(root_dir)
    if filter and not isinstance(filter, list):
        filter = [filter]
    def recursive_lookup(parent_dir, filter=None, recursive=False):
        result=[]
        for f in os.listdir(parent_dir):
            _dir = os.path.join(parent_dir, f)
            if recursive and os.path.isdir(_dir):
                result.extend(recursive_lookup(_dir, filter, recursive))
            elif filter and os.path.splitext(f)[-1] in filter:
                result.append(_dir)
            elif not filter:
                result.append(_dir)
        return result
    return recursive_lookup(root_dir, filter, recursive)


def product(iterables):
    res = []
    def rec(iterables, level=0, items=[]):
        for i in iterables[level]:
            c_items = list(items)
            c_items.append(i)
            if level < len(iterables)-1:
                    lv = level+1
                    rec(iterables, lv, c_items)
            else:
                    res.append(tuple(c_items))
    rec(iterables)
    return res



