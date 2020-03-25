import os,re,json,glob,collections,pickle,shutil,nbformat,inspect,yaml,tempfile,enum,stat,time,random
import importlib.util
from pdb import set_trace
from configparser import ConfigParser
from pathlib import Path
from textwrap import TextWrapper
from typing import Union,Optional
from nbformat.sign import NotebookNotary
from functools import partial,lru_cache
from base64 import b64decode,b64encode

def test_eq(a,b): assert a==b, f'{a}, {b}'

def save_config_file(file, d):
    "Write settings dict to a new config file, or overwrite the existing one."
    config = ConfigParser()
    config['DEFAULT'] = d
    config.write(open(file, 'w'))

def read_config_file(file):
    config = ConfigParser()
    config.read(file)
    return config

_defaults = {"doc_host": "https://%(user)s.github.io", "doc_baseurl": "/%(lib_name)s/"}


def add_new_defaults(cfg, file):
    for k,v in _defaults.items():
        if cfg.get(k, None) is None: 
            cfg[k] = v
            save_config_file(file, cfg)


@lru_cache(maxsize=128)
class Config:
    "Store the basic information for nbdev to work"
    def __init__(self, cfg_name='settings.ini'):
        cfg_path = Path.cwd()
        while cfg_path != cfg_path.parent and not (cfg_path/cfg_name).exists(): cfg_path = cfg_path.parent
        self.config_file = cfg_path/cfg_name
        assert self.config_file.exists(), "Use `create_config` to create settings.ini for the first time"
        self.d = read_config_file(self.config_file)['DEFAULT']
        add_new_defaults(self.d, self.config_file)

    def __getattr__(self,k):
        if k=='d' or k not in self.d: raise AttributeError(k)
        return self.config_file.parent/self.d[k] if k.endswith('_path') else self.d[k]

    def get(self,k,default=None):   return self.d.get(k, default)
    def __setitem__(self,k,v): self.d[k] = str(v)
    def __contains__(self,k):  return k in self.d
    def save(self): save_config_file(self.config_file,self.d)

def create_config(lib_name, user, path='.', cfg_name='settings.ini', branch='master',
               git_url="https://github.com/%(user)s/%(lib_name)s/tree/%(branch)s/", custom_sidebar=False,
               nbs_path='nbs', lib_path='%(lib_name)s', doc_path='docs', tst_flags='', version='0.0.1', **kwargs):
    "Creates a new config file for `lib_name` and `user` and saves it."
    g = locals()
    config = {o:g[o] for o in 'lib_name user branch git_url lib_path nbs_path doc_path tst_flags version custom_sidebar'.split()}
    config = {**config, **kwargs}
    save_config_file(Path(path)/cfg_name, config)

def last_index(x, o):
    "Finds the last index of occurence of `x` in `o` (returns -1 if no occurence)"
    try: return next(i for i in reversed(range(len(o))) if o[i] == x)
    except StopIteration: return -1

def in_ipython():
    "Check if the code is running in the ipython environment (jupyter including)"
    program_name = os.path.basename(os.getenv('_', ''))
    if ('jupyter-notebook' in program_name or # jupyter-notebook
        'ipython'          in program_name or # ipython
        'JPY_PARENT_PID'   in os.environ):    # ipython-notebook
        return True
    else:
        return False

IN_IPYTHON = in_ipython()

def in_colab():
    "Check if the code is running in Google Colaboratory"
    try:
        from google import colab
        return True
    except: return False

IN_COLAB = in_colab()

def in_notebook():
    "Check if the code is running in a jupyter notebook"
    if in_colab(): return True
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell': return True   # Jupyter notebook, Spyder or qtconsole
        elif shell == 'TerminalInteractiveShell': return False  # Terminal running IPython
        else: return False  # Other type (?)
    except NameError: return False      # Probably standard Python interpreter

IN_NOTEBOOK = in_notebook()

def compose(*funcs, order=None):
    "Create a function that composes all functions in `funcs`, passing along remaining `*args` and `**kwargs` to all"
    if len(funcs)==0: return noop
    if len(funcs)==1: return funcs[0]
    def _inner(x, *args, **kwargs):
        for f in funcs: x = f(x, *args, **kwargs)
        return x
    return _inner

from multiprocessing import Process, Queue
import concurrent.futures

def num_cpus():
    "Get number of cpus"
    try:                   return len(os.sched_getaffinity(0))
    except AttributeError: return os.cpu_count()

class ProcessPoolExecutor(concurrent.futures.ProcessPoolExecutor):
    "Like `concurrent.futures.ProcessPoolExecutor` but handles 0 `max_workers`."
    def __init__(self, max_workers=None, on_exc=print, **kwargs):
        self.not_parallel = max_workers==0
        self.on_exc = on_exc
        if self.not_parallel: max_workers=1
        super().__init__(max_workers, **kwargs)

    def map(self, f, items, *args, **kwargs):
        g = partial(f, *args, **kwargs)
        if self.not_parallel: return map(g, items)
        try: return super().map(g, items)
        except Exception as e: self.on_exc(e)

def parallel(f, items, *args, n_workers=None, **kwargs):
    "Applies `func` in parallel to `items`, using `n_workers`"
    if n_workers is None: n_workers = min(16, num_cpus())
    with ProcessPoolExecutor(n_workers) as ex:
        r = ex.map(f,items, *args, **kwargs)
        return list(r)

#export
class ReLibName():
    "Regex expression that's compiled at first use but not before since it needs `Config().lib_name`"
    def __init__(self, pat, flags=0): self._re,self.pat,self.flags = None,pat,flags
    @property
    def re(self):
        if not hasattr(Config(), 'lib_name'): raise Exception("Please fill in the library name in settings.ini.")
        self.pat = self.pat.replace('LIB_NAME', Config().lib_name)
        if self._re is None: self._re = re.compile(self.pat, self.flags)
        return self._re
