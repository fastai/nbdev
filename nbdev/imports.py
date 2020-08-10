from fastcore.utils import *
from fastcore.test import *

import os,re,json,glob,collections,pickle,shutil,nbformat,inspect,yaml,tempfile,enum,stat,time,random,sys
import importlib.util
from pdb import set_trace
from configparser import ConfigParser
from pathlib import Path
from textwrap import TextWrapper
from typing import Union,Optional
from nbformat.sign import NotebookNotary
from functools import partial,lru_cache
from base64 import b64decode,b64encode

def save_config_file(file, d):
    "Write settings dict to a new config file, or overwrite the existing one."
    config = ConfigParser()
    config['DEFAULT'] = d
    config.write(open(file, 'w'))

def read_config_file(file):
    config = ConfigParser()
    config.read(file)
    return config

_defaults = {"host": "github", "doc_host": "https://%(user)s.github.io", "doc_baseurl": "/%(lib_name)s/"}


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

def create_config(host, lib_name, user, path='.', cfg_name='settings.ini', branch='master',
               git_url="https://github.com/%(user)s/%(lib_name)s/tree/%(branch)s/", custom_sidebar=False,
               nbs_path='nbs', lib_path='%(lib_name)s', doc_path='docs', tst_flags='', version='0.0.1', **kwargs):
    "Creates a new config file for `lib_name` and `user` and saves it."
    g = locals()
    config = {o:g[o] for o in 'host lib_name user branch git_url lib_path nbs_path doc_path tst_flags version custom_sidebar'.split()}
    config = {**config, **kwargs}
    save_config_file(Path(path)/cfg_name, config)

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

def call_cb(cb_name, *args):
    "Calls `cb_name` from the `nbdev_callbacks` module but won't fail if it doesn't exist"
    if 'nbdev_callbacks' not in globals():
        _sys_path=sys.path
        try:
            cfg=Config()
            sys.path=[str(cfg.config_file.parent/cfg.get('callbacks_path', '.'))]
            try: import nbdev_callbacks
            except: nbdev_callbacks={}
        finally: sys.path=_sys_path
    if not hasattr(nbdev_callbacks, cb_name): return args[0] if args else None
    return getattr(nbdev_callbacks, cb_name)(*args)
