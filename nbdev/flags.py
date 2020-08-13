__all__ = []

from .imports import Config
from fastcore.utils import IN_IPYTHON
import sys, re

def _validate_param(line, magic_name, param_name=None, required=False, fixed_value=None):
    "Checks that `line` contains a single parameter, if required"
    # print warnings, rather than raise exceptions, as we don't want to be intrusive
    line = line.strip()
    if required and line == '':
        print(f'UsageError: {param_name} is missing. Usage `%{magic_name} {param_name}`')
        return False
    if re.search('\s', line):
        print(f'UsageError: {param_name} "{line}" must not contain whitespace')
        return False
    if fixed_value is not None and line != '' and line != fixed_value:
        print(f'UsageError: Invalid option "{line}". Usage `%{magic_name} [{fixed_value}]`')
    return True

def _validate_no_param(line, magic_name):
    "Checks that `line` contains no parameters"
    line = line.strip()
    if line != '':
        print(f'UsageError: Invalid option "{line}". Usage `%{magic_name}`')

def nbdev_default_export(line):
    """One cell should contain a `%nbdev_default_export` magic followed by the name of the module
    (with points for submodules and without the py extension) everything should be exported in.
    If one specific cell needs to be exported in a different module, just indicate it after the
    `%nbdev_export` magic: `%nbdev_export special.module`"""
    if not _validate_param(line, 'nbdev_default_export', 'module_name', True): return
    print(f'Cells will be exported to {Config().get("lib_name", "lib_name")}.{line},')
    print('unless a different module is specified after an export flag: `%nbdev_export special.module`')

def nbdev_export(line):
    """Put an `%nbdev_export` magic on each cell you want exported but not shown in the docs.
    Optionally override `%nbdev_default_export` by specifying a module: `%nbdev_export special.module`"""
    _validate_param(line, 'nbdev_export', 'module_name')

def nbdev_export_and_show(line):
    """Put an `%nbdev_export_and_show` magic on each cell you want exported with source code shown in the docs.
    Optionally override `%nbdev_default_export` by specifying a module: `%nbdev_export_and_show special.module`"""
    _validate_param(line, 'nbdev_export_and_show', 'module_name')

def nbdev_export_internal(line):
    """Put an `%nbdev_export_internal` magic on each cell you want exported without it being added to `__all__`,
    and without it showing up in the docs.
    Optionally override `%nbdev_default_export` by specifying a module: `%nbdev_export_internal special.module`"""
    _validate_param(line, 'nbdev_export_internal', 'module_name')

def nbdev_hide(line):
    """Put an `%nbdev_hide` magic at the top of any cell you want to completely hide in the docs"""
    _validate_no_param(line, 'nbdev_hide')

def nbdev_hide_input(line):
    """Put an `%nbdev_hide_input` magic at the top of any cell you want input hidden but output shown in the docs"""
    _validate_no_param(line, 'nbdev_hide_input')

def nbdev_hide_output(line):
    """Put an `%nbdev_hide_output` magic at the top of any cell you want output hidden but input shown in the docs"""
    _validate_no_param(line, 'nbdev_hide_output')

def nbdev_default_class_level(line):
    """Define the default toc level of classes with a `%nbdev_default_class_level` magic followed by a number
    (default is 2)"""
    try:
        class_level = int(line)
        if not 1 <= class_level <= 6: raise ValueError()
    except ValueError:
        print(f'UsageError: Invalid class level "{line}". Usage `%nbdev_default_class_level [int between 1 and 6]`')

def nbdev_collapse_input(line):
    """Put an `%nbdev_collapse_input` magic to include your code in the docs under a collapsable element that is closed by default.
    To make the collapsable element open by default: `%nbdev_collapse_input open`"""
    _validate_param(line, 'nbdev_collapse_input', fixed_value='open')

def nbdev_collapse_output(line):
    """Put an `%nbdev_collapse_output` magic to include output in the docs under a collapsable element that is closed by default.
    To make the collapsable element open by default: `%nbdev_collapse_output open`"""
    _validate_param(line, 'nbdev_collapse_output', fixed_value='open')

def parse_line(line):
    "Convert line magic input to a list of parameters"
    line = line.strip()
    if line.startswith('[') and line.endswith(']'): line=line[1:-1]
    return [s for s in re.split('[ ,]+', line) if s]

def nbdev_add2all(line, local_ns):
    """To add something to `__all__` if it's not picked automatically,
    write an exported cell with something like: `%nbdev_add2all name_1, name_2 ...`"""
    if line.strip() == '':
        print(f'UsageError: List of names is missing. Usage `%nbdev_add2all name_1, name_2`')
        return
    try: [eval(s, local_ns) for s in parse_line(line)]
    except Exception as ex: print(f'UsageError: {ex}')

"""
def _new_test_flag_fn(flag):
    "Create a new test flag function and magic"
    # don't create "empty" test flags if tst_flags is not set, set to whitespace, has trailing | etc
    if not flag.strip(): return
    exec(f'''def nbdev_{flag}_test(line):
    "Put an `%nbdev_{flag}_test` magic on each "{flag}" test cell that you do not want to be run by default."
    _validate_param(line, 'nbdev_{flag}_test', fixed_value='all')''')
    exec(f'sys.modules[__name__].nbdev_{flag}_test = nbdev_{flag}_test')
    exec(f'register_line_magic(nbdev_{flag}_test)')
"""

if IN_IPYTHON:
    from IPython.core.magic import register_line_magic, needs_local_scope
    fns = [nbdev_default_export, nbdev_export, nbdev_export_and_show, nbdev_export_internal,
           nbdev_hide, nbdev_hide_input, nbdev_hide_output, nbdev_default_class_level,
           nbdev_collapse_input, nbdev_collapse_output, needs_local_scope(nbdev_add2all)]
    for fn in fns: register_line_magic(fn)
    #for flag in Config().get('tst_flags', '').split('|'): _new_test_flag_fn(flag)

