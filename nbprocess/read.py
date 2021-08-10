# %% auto 0
__all__ = ['display_json', 'NbCell', 'dict2nb', 'read_nb', 'nbprocess_create_config', 'get_config', 'add_init', 'basic_export_nb']


# %% ../nbs/00_read.ipynb 2
from fastcore.imports import *
from fastcore.foundation import *
from fastcore.utils import *
from fastcore.test import *
from fastcore.script import *
from fastcore.xtras import *

import json,ast,functools


# %% ../nbs/00_read.ipynb 7
def display_json(d):
    "Formatter to reduce vertical space used by JSON display"
    s = pformat(d, indent=2, width=120, compact=True, sort_dicts=False)
    return Markdown(f"```python\n{s}\n```")


# %% ../nbs/00_read.ipynb 12
class NbCell(AttrDict):
    def __init__(self, idx, cell):
        super().__init__(cell)
        self.idx_ = idx
        if 'source' in self: self.set_source(self.source)

    def __repr__(self): return self.source

    def set_source(self, source):
        self.source = ''.join(source)
        if '_parsed_' in self: del(self['_parsed_'])

    def parsed_(self):
        if self.cell_type!='code' or self.source[:1]=='%': return
        if '_parsed_' not in self: self._parsed_ = ast.parse(self.source).body
        return self._parsed_


# %% ../nbs/00_read.ipynb 14
def dict2nb(js):
    "Convert a dict to an `AttrDict`, "
    nb = dict2obj(js)
    nb.cells = nb.cells.enumerate().starmap(NbCell)
    return nb


# %% ../nbs/00_read.ipynb 25
def read_nb(path):
    "Return notebook at `path`"
    return dict2nb(Path(path).read_json())


# %% ../nbs/00_read.ipynb 29
@call_parse
def nbprocess_create_config(
    user:str, # Repo username
    host:str='github', # Repo hostname
    lib_name:str=None, # Name of library
    path:str='.', # Path to create config file
    cfg_name:str='settings.ini', # Name of config file to create
    branch:str='master', # Repo branch
    git_url:str="https://github.com/%(user)s/%(lib_name)s/tree/%(branch)s/", # Repo URL
    custom_sidebar:bool_arg=False, # Create custom sidebar?
    nbs_path:str='.', # Name of folder containing notebooks
    lib_path:str='%(lib_name)s', # Folder name of root module
    doc_path:str='docs', # Folder name containing docs
    tst_flags:str='', # Test flags
    version:str='0.0.1', # Version number
    **kwargs
):
    "Creates a new config file for `lib_name` and `user` and saves it."
    if lib_name is None:
        parent = Path.cwd().parent
        lib_name = parent.parent.name if parent.name=='nbs' else parent.name
    g = locals()
    config = {o:g[o] for o in 'host lib_name user branch git_url lib_path nbs_path doc_path \
        tst_flags version custom_sidebar'.split()}
    config = merge(config, kwargs)
    save_config_file(Path(path)/cfg_name, config)


# %% ../nbs/00_read.ipynb 31
@functools.lru_cache(maxsize=None)
def get_config(cfg_name='settings.ini', path=None):
    "`Config` for ini file found in `path` (defaults to `cwd`)"
    cfg_path = Path.cwd() if path is None else path
    while cfg_path != cfg_path.parent and not (cfg_path/cfg_name).exists(): cfg_path = cfg_path.parent
    return Config(cfg_path, cfg_name=cfg_name)


# %% ../nbs/00_read.ipynb 35
_init = '__init__.py'

def _has_py(fs): return any(1 for f in fs if f.endswith('.py'))

def add_init(path):
    "Add `__init__.py` in all subdirs of `path` containing python files if it's not there already"
    # we add the lowest-level `__init__.py` files first, which ensures _has_py succeeds for parent modules
    path = Path(path)
    path.mkdir(exist_ok=True)
    if not (path/_init).exists(): (path/_init).touch()
    for r,ds,fs in os.walk(path, topdown=False):
        r = Path(r)
        subds = (os.listdir(r/d) for d in ds)
        if _has_py(fs) or any(filter(_has_py, subds)) and not (r/_init).exists(): (r/_init).touch()


# %% ../nbs/00_read.ipynb 39
def basic_export_nb(fname, dest=None):
    "Basic exporter to bootstrap nbprocess"
    if dest is None: dest = get_config().lib_path
    fname,dest = Path(fname),Path(dest)
    nb = read_nb(fname)

    # grab the source from all the cells that have an `export` comment
    cells = L(cell for cell in nb.cells if re.match(r'#\s*export', cell.source))
    
    # find all the exported functions, to create `__all__`:
    trees = cells.map(NbCell.parsed_).concat()
    funcs = trees.filter(risinstance((ast.FunctionDef,ast.ClassDef))).attrgot('name')
    exp_funcs = [f for f in funcs if f[0]!='_']

    # write out the file
    dest.mkdir(exist_ok=True)
    hdr = f"# %% {fname.relpath(dest)}"
    with (dest/'read.py').open('w') as f:
        f.write(f"# %% auto 0\n__all__ = {exp_funcs}\n\n\n")
        for cell in cells:
            source = re.sub(r'^#\s*export\s*\n', '', cell.source)
            f.write(f'{hdr} {cell.idx_}\n{source}\n\n\n')


