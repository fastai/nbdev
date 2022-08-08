# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/15_migrate.ipynb.

# %% auto 0
__all__ = ['migrate_nb_fm', 'migrate_md_fm', 'nbdev_migrate']

# %% ../nbs/15_migrate.ipynb 2
from .process import first_code_ln
from .read import *
from .processors import construct_fm, yml2dict, filter_fm
from .read import read_nb, config_key
from .sync import write_nb
from .clean import process_write
from .showdoc import show_doc
from fastcore.all import *
import shutil

# %% ../nbs/15_migrate.ipynb 4
def _cat_slug(d):
    "Get the partial slug from the category front matter."
    return '/' + '/'.join(sorted(d.get('categories', '')))

# %% ../nbs/15_migrate.ipynb 6
def _file_slug(fname): 
    "Get the partial slug from the filename."
    p = Path(fname)
    dt = '/'+p.name[:10].replace('-', '/')+'/'
    return dt + p.stem[11:]    

# %% ../nbs/15_migrate.ipynb 8
def _add_alias(fm:dict, path:Path):
    if 'permalink' in fm: fm['aliases'] = [f"{fm.pop('permalink').strip()}"]
    else: fm['aliases'] = [f'{_cat_slug(fm) + _file_slug(path)}']

# %% ../nbs/15_migrate.ipynb 10
def migrate_nb_fm(path, overwrite=True):
    "Migrate fastpages front matter in notebooks to a raw cell."
    nb = nread_nb(path)
    _add_alias(nb.raw_fm_dict, path)
    if overwrite: write_nb(nb, path)
    return nb

# %% ../nbs/15_migrate.ipynb 14
_re_fm_md = re.compile(r'^---(.*\S+.)?---', flags=re.DOTALL)

def _md_fmdict(txt):
    "Get front matter as a dict from a markdown file."
    m = _re_fm_md.match(txt)
    if m: return yml2dict(m.group(1))
    else: return {}

# %% ../nbs/15_migrate.ipynb 17
def migrate_md_fm(path, overwrite=True):
    "Make fastpages front matter in markdown files quarto compliant."
    p = Path(path)
    md = p.read_text()
    fm = _md_fmdict(md)
    if fm:
        _add_alias(fm, path)
        txt = _re_fm_md.sub(construct_fm(filter_fm(fm)), md)
        if overwrite: p.write_text(txt)
        return txt
    else: return md 

# %% ../nbs/15_migrate.ipynb 25
_alias = merge({k:'code-fold: true' for k in ['collapse', 'collapse_input', 'collapse_hide']}, {'collapse_show':'code-fold: show'})
def _subv1(s): return _alias.get(s, s)

# %% ../nbs/15_migrate.ipynb 26
def _re_v1():
    d = ['default_exp', 'export', 'exports', 'exporti', 'hide', 'hide_input', 'collapse_show', 'collapse',
         'collapse_hide', 'collapse_input', 'hide_output',  'default_cls_lvl']
    d += L(config_key('tst_flags', path=False)).filter()
    d += [s.replace('_', '-') for s in d] # allow for hyphenated version of old directives
    _tmp = '|'.join(list(set(d)))
    return re.compile(f"^[ \f\v\t]*?(#)\s*({_tmp})(?!\S)", re.MULTILINE)

def _repl_directives(code_str): 
    def _fmt(x): return f"#| {_subv1(x[2].replace('-', '_').strip())}"
    return _re_v1().sub(_fmt, code_str)

# %% ../nbs/15_migrate.ipynb 30
def _repl_v1dir(nb):
    "Replace nbdev v1 with v2 directives."
    for cell in nb['cells']:
        if cell.get('source') and cell.get('cell_type') == 'code':
            ss = cell['source'].copy()
            first_code = first_code_ln(ss, re_pattern=_re_v1())
            if not first_code: first_code = len(ss)
            if not ss: pass
            else: cell['source'] = [_repl_directives(c) for c in ss[:first_code]] + ss[first_code:]

# %% ../nbs/15_migrate.ipynb 33
_re_callout = re.compile(r'^>\s(Warning|Note|Important|Tip):(.*)', flags=re.MULTILINE)
def _co(x): return ":::{.callout-"+x[1].lower()+"}\n\n" + f"{x[2].strip()}\n\n" + ":::"
def _convert_callout(s): 
    "Convert nbdev v1 to v2 callouts."
    return _re_callout.sub(_co, s)

# %% ../nbs/15_migrate.ipynb 39
def _repl_v1callouts(nb):
    "Replace nbdev v1 with v2 callouts."
    for cell in nb['cells']:
        if cell.get('source') and cell.get('cell_type') == 'markdown':
            cell['source'] = [_convert_callout(c) for c in cell['source'].copy()]
    return nb

# %% ../nbs/15_migrate.ipynb 40
@call_parse
def nbdev_migrate(
    fname:str=None, # A notebook name or glob to migrate
    disp:bool=False,  # Print the outputs with newly formatted directives
    stdin:bool=False, # Read notebook from input stream
    no_skip:bool=False, # Do not skip directories beginning with an underscore
):
    "Convert all directives and callouts in `fname` from v1 to v2"
    _migrate = compose(_repl_v1callouts, _repl_v1dir)
    _write = partial(process_write, warn_msg='Failed to replace directives', proc_nb=_migrate)
    if stdin: _write(f_in=sys.stdin, f_out=sys.stdout)
    _skip_re = None if no_skip else '^[_.]'
    if fname is None: fname = config_key("nbs_path")
    for f in globtastic(fname, file_glob='*.ipynb', skip_folder_re=_skip_re): _write(f_in=f, disp=disp)
