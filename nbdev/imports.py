import os,re,json,glob,collections,pickle,shutil,nbformat,inspect,yaml,importlib,tempfile,enum,numpy as np
from pdb import set_trace
from configparser import ConfigParser
from pathlib import Path
from textwrap import TextWrapper
from typing import Union,Optional
from nbformat.sign import NotebookNotary
from functools import partial

def test_eq(a,b): assert a==b, f'{a}, {b}'

def save_config_file(file, d):
    config = ConfigParser()
    config['DEFAULT'] = d
    config.write(open(file, 'w'))

def read_config_file(file):
    config = ConfigParser()
    config.read(file)
    return config

class Config:
    "Store the basic information for nbdev to work"
    def __init__(self, cfg_name='settings.ini'):
        cfg_path = Path.cwd()
        while cfg_path != Path('/') and not (cfg_path/cfg_name).exists(): cfg_path = cfg_path.parent
        self.config_file = cfg_path/cfg_name
        assert self.config_file.exists(), "Use `Config.create` to create a `Config` object the first time"
        self.d = read_config_file(self.config_file)['DEFAULT']

    def __getattr__(self,k):
        if k=='d' or k not in self.d: raise AttributeError
        return self.config_file.parent/self.d[k] if k.endswith('path') else self.d[k]

    def get(self,k,default=None):   return self.d.get(k, default)
    def __setitem__(self,k,v): self.d[k] = str(v)
    def __contains__(self,k):  return k in self.d

    @classmethod
    def create(cls, lib_name, user, path='.', cfg_name='settings.ini', branch='master',
               git_url="https://github.com/%(user)s/%(lib_name)s/tree/%(branch)s/",
               nbs_path='nbs', lib_path='%(lib_name)s', doc_path='docs', tst_flags='', version='0.0.1'):
        g = locals()
        config = {o:g[o] for o in 'lib_name user branch git_url lib_path nbs_path doc_path tst_flags version'.split()}
        save_config_file(Path(path)/cfg_name, config)
        return cls(cfg_name=cfg_name)

    def save(self): save_config_file(self.config_file,self.d)

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

