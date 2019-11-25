# CLI commands

Console commands added by the nbdev library

<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
# export
from nbdev.imports import *
from nbdev.export import *
from nbdev.sync import *
from nbdev.export2html import *
from nbdev.test import *
from fastscript.fastscript import call_parse, Param
```

</div>

</div>

## Navigating from notebooks to script and back
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
#export
@call_parse
def nbdev_build_lib(fname:Param("A notebook name or glob to convert", str)=None):
    notebook2script(fname=fname)
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
#export
@call_parse
def nbdev_update_lib(fname:Param("A notebook name or glob to convert", str)=None):
    script2notebook(fname=fname)
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
#export
@call_parse
def nbdev_diff_nbs(): diff_nb_script()
```

</div>

</div>

## Parallel execution
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
#export
from multiprocessing import Process, Queue
import concurrent
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
#export
def num_cpus():
    "Get number of cpus"
    try:                   return len(os.sched_getaffinity(0))
    except AttributeError: return os.cpu_count()
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
#export 
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
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
#export 
def parallel(f, items, *args, n_workers=None, **kwargs):
    "Applies `func` in parallel to `items`, using `n_workers`"
    if n_workers is None: n_workers = min(16, num_cpus())
    with ProcessPoolExecutor(n_workers) as ex:
        r = ex.map(f,items, *args, **kwargs)
        return list(r)
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
import time,random

def add_one(x, a=1): 
    time.sleep(random.random()/100)
    return x+a

inp,exp = range(50),range(1,51)
test_eq(parallel(add_one, inp, n_workers=2), list(exp))
test_eq(parallel(add_one, inp, n_workers=0), list(exp))
test_eq(parallel(add_one, inp, n_workers=1, a=2), list(range(2,52)))
test_eq(parallel(add_one, inp, n_workers=0, a=2), list(range(2,52)))
```

</div>

</div>

## Extracting tests
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
# export
def _test_one(fname, flags=None):
    time.sleep(random.random())
    print(f"testing: {fname}")
    try: test_nb(fname, flags=flags)
    except Exception as e: print(e)
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
# export
@call_parse
def nbdev_test_nbs(fname:Param("A notebook name or glob to convert", str)=None,
                   flags:Param("Space separated list of flags", str)=None):
    if flags is not None: flags = flags.split(' ')
    if fname is None: 
        files = [f for f in Config().nbs_path.glob('*.ipynb') if not f.name.startswith('_')]
    else: files = glob.glob(fname)
        
    # make sure we are inside the notebook folder of the project
    os.chdir(Config().nbs_path)
    parallel(_test_one, files, flags=flags)
```

</div>

</div>

## Building documentation
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
#export
import time,random,warnings
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
#export
def _leaf(k,v):
    url = 'external_url' if "http" in v else 'url'
    if url=='url': v=v+'.html'
    return {'title':k, url:v, 'output':'web,pdf'}
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
#export
_k_names = ['folders', 'folderitems', 'subfolders', 'subfolderitems']
def _side_dict(title, data, level=0):
    k_name = _k_names[level]
    level += 1
    res = [(_side_dict(k, v, level) if isinstance(v,dict) else _leaf(k,v))
        for k,v in data.items()]
    return ({k_name:res} if not title
            else res if title.startswith('empty')
            else {'title': title, 'output':'web', k_name: res})
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
#export
def make_sidebar():
    "Making sidebar for the doc website"
    if not (Config().doc_path/'sidebar.json').exists():
        warnings.warn("No data for the sidebar available")
        sidebar_d = {}
    else: sidebar_d = json.load(open(Config().doc_path/'sidebar.json', 'r'))
    res = _side_dict('Sidebar', sidebar_d)
    res = {'entries': [res]}
    res_s = yaml.dump(res, default_flow_style=False)
    res_s = res_s.replace('- subfolders:', '  subfolders:').replace(' - - ', '   - ')
    res_s = f"""
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# Instead edit {Config().doc_path/'sidebar.json'}
"""+res_s
    open(Config().doc_path/'_data/sidebars/home_sidebar.yml', 'w').write(res_s)
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
# export
def convert_one(fname):
    time.sleep(random.random())
    print(f"converting: {fname}")
    try: convert_nb(fname)
    except Exception as e: print(e)
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
# export
def convert_all(fname=None, force_all=False):
    "Convert all notebooks matching `fname` to html files"
    if fname is None: 
        files = [f for f in Config().nbs_path.glob('*.ipynb') if not f.name.startswith('_')]
    else: files = glob.glob(fname)
    if not force_all:
        # only rebuild modified files
        files,_files = [],files.copy()
        for fname in _files:
            fname_out = Config().doc_path/'.'.join(fname.with_suffix('.html').name.split('_')[1:])
            if not fname_out.exists() or os.path.getmtime(fname) >= os.path.getmtime(fname_out):
                files.append(fname)
    if len(files)==0: print("No notebooks were modified")          
    parallel(convert_one, files)
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
# export
_re_index = re.compile(r'^\d*_index\.ipynb$')
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
# export
def make_readme():
    index_fn = None
    for f in Config().nbs_path.glob('*.ipynb'):
        if _re_index.match(f.name): index_fn = f
    assert index_fn is not None, "Could not locate index notebook"
    convert_md(f, Config().config_file.parent, jekyll=False)
    n = Config().config_file.parent/f.with_suffix('.md').name
    shutil.move(n, Config().config_file.parent/'README.md')
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
# export
@call_parse
def nbdev_build_docs(fname:Param("A notebook name or glob to convert", str)=None,
                     force_all:Param("Rebuild even notebooks that haven't changed", bool)=False,
                     mk_readme:Param("Also convert the index notebook to README", bool)=True,):
    convert_all(fname=fname, force_all=force_all)
    make_sidebar()
    if mk_readme: make_readme()
```

</div>

</div>

## Stripout
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
# export
def rm_execution_count(o):
    "Remove execution count in `o`"
    if 'execution_count' in o: o['execution_count'] = None
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
# export
def clean_cell_output(cell):
    "Remove execution count in `cell`"
    if 'outputs' in cell:
        for o in cell['outputs']: rm_execution_count(o)
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
#export
cell_metadata_keep = ["hide_input"]
nb_metadata_keep   = ["kernelspec", "jekyll"]
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
# export
def clean_cell(cell, clear_all=False):
    "Clen `cell` by removing superluous metadata or everything except the input if `clear_all`"
    rm_execution_count(cell)
    if 'outputs' in cell:
        if clear_all: cell['outputs'] = []
        else:         clean_cell_output(cell)
    cell['metadata'] = {} if clear_all else {k:v for k,v in cell['metadata'].items() if k in cell_metadata_keep}
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
tst = {'cell_type': 'code',
       'execution_count': 26,
       'metadata': {'hide_input': True, 'meta': 23},
       'outputs': [{'execution_count': 2, 'output': 'super'}],
       'source': 'awesome_code'}
tst1 = tst.copy()

clean_cell(tst)
test_eq(tst, {'cell_type': 'code',
              'execution_count': None,
              'metadata': {'hide_input': True},
              'outputs': [{'execution_count': None, 'output': 'super'}],
              'source': 'awesome_code'})

clean_cell(tst1, clear_all=True)
test_eq(tst1, {'cell_type': 'code',
               'execution_count': None,
               'metadata': {},
               'outputs': [],
               'source': 'awesome_code'})
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
# export
def clean_nb(nb, clear_all=False):
    "Clean `nb` from superfulous metadata, passing `clear_all` to `clean_cell`"
    for c in nb['cells']: clean_cell(c, clear_all=clear_all)
    nb['metadata'] = {k:v for k,v in nb['metadata'].items() if k in nb_metadata_keep }
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
tst = {'cell_type': 'code',
       'execution_count': 26,
       'metadata': {'hide_input': True, 'meta': 23},
       'outputs': [{'execution_count': 2, 'output': 'super'}],
       'source': 'awesome_code'}
nb = {'metadata': {'kernelspec': 'some_spec', 'jekyll': 'some_meta', 'meta': 37},
      'cells': [tst]}

clean_nb(nb)
test_eq(nb['cells'][0], {'cell_type': 'code',
              'execution_count': None,
              'metadata': {'hide_input': True},
              'outputs': [{'execution_count': None, 'output': 'super'}],
              'source': 'awesome_code'})
test_eq(nb['metadata'], {'kernelspec': 'some_spec', 'jekyll': 'some_meta'})
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
#export
import io,sys,json
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
# export
def _print_output(nb):
    "Print `nb` in stdout for git things"
    _output_stream = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    x = json.dumps(nb, sort_keys=True, indent=1, ensure_ascii=False)
    _output_stream.write(x)
    _output_stream.write("\n")
    _output_stream.flush()
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
# export
@call_parse
def nbdev_clean_nbs(fname:Param("A notebook name or glob to convert", str)=None, 
                    clear_all:Param("Clean all metadata and outputs", bool)=False,
                    disp:Param("Print the cleaned outputs", bool)=False):
    "Clean all notebooks in `fname` to avoid merge conflicts"
    #Git hooks will pass the notebooks in the stdin
    input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8') if sys.stdin else None
    if input_stream and fname is None:
        nb = json.load(input_stream)
        clean_nb(nb, clear_all=clear_all)
        _print_output(nb)
        return
    files = Config().nbs_path.glob('**/*.ipynb') if fname is None else glob.glob(fname)
    for f in files:
        if not str(f).endswith('.ipynb'): continue
        nb = read_nb(f)
        clean_nb(nb, clear_all=clear_all)
        if disp: _print_output(nb)
        else:
            NotebookNotary().sign(nb)
            nbformat.write(nb, str(f), version=4)
```

</div>

</div>

## Other utils
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
# export
@call_parse
def nbdev_read_nbs(fname:Param("A notebook name or glob to convert", str)=None):
    "Check all notebooks in `fname` can be opened"
    files = Config().nbs_path.glob('**/*.ipynb') if fname is None else glob.glob(fname)
    for nb in files:
        try: _ = read_nb(nb)
        except Exception as e:
            print(f"{nb} is corrupted and can't be opened.")
            raise e
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
# export
@call_parse
def nbdev_trust_nbs(fname:Param("A notebook name or glob to convert", str)=None,
                    force:Param("Trust even notebooks that haven't changed", bool)=False):
    check_fname = Config().nbs_path/".last_checked"
    last_checked = os.path.getmtime(check_fname) if check_fname.exists() else None
    files = Config().nbs_path.glob('**/*.ipynb') if fname is None else glob.glob(fname)
    for fn in files:
        if last_checked and not force:
            last_changed = os.path.getmtime(fn)
            if last_changed < last_checked: continue
        nb = read_nb(fn)
        if not NotebookNotary().check_signature(nb): NotebookNotary().sign(nb)
    check_fname.touch(exist_ok=True)
```

</div>

</div>

## Git hooks
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
# export
import subprocess
```

</div>

</div>
<div class="codecell" markdown="1">
<div class="input_area" markdown="1">

```python
# export
@call_parse
def nbdev_install_git_hooks():
    "Install git hooks to clean/trust notebooks automatically"
    path = Config().config_file.parent
    #Trust notebooks after merge
    with open(path/'.git'/'hooks'/'post-merge', 'w') as f:
        f.write("""#!/bin/bash
echo "Trusting notebooks"
nbdev_trust_nbs
"""
        )
    #Clean notebooks on commit/diff
    with open(path/'.gitconfig', 'w') as f:
        f.write("""# Generated by nbdev_install_git_hooks
#
# If you need to disable this instrumentation do:
#
# git config --local --unset include.path
#
# To restore the filter
#
# git config --local include.path .gitconfig
#
# If you see notebooks not stripped, checked the filters are applied in .gitattributes
#
[filter "clean-nbs"]
        clean = nbdev_clean_nbs
        smudge = cat
        required = true
[diff "ipynb"]
        textconv = nbdev_clean_nbs --disp True --fname
""")
    cmd = "git config --local include.path ../.gitconfig"
    print(f"Executing: {cmd}")
    result = subprocess.run(cmd.split(), shell=False, check=False, stderr=subprocess.PIPE)
    if result.returncode == 0:
        print("Success: hooks are installed and repo's .gitconfig is now trusted")
    else:
        print("Failed to trust repo's .gitconfig")
        if result.stderr: print(f"Error: {result.stderr.decode('utf-8')}")
    with open(Config().nbs_path/'.gitattributes', 'w') as f:
        f.write("""**/*.ipynb filter=clean-nbs
**/*.ipynb diff=ipynb
"""
               )
```

</div>

</div>
