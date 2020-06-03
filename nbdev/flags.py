__all__ = []

from .imports import Config, IN_IPYTHON
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

def nbdev_collapse_input(line):
    """Put an `%nbdev_collapse_input` magic to inlcude your code in the docs under a collapsable element that is closed by default.
    To make the collapsable element open by default: `%nbdev_collapse_input open`"""
    _validate_param(line, 'nbdev_collapse_input', fixed_value='open')

def nbdev_collapse_output(line):
    """Put an `%nbdev_collapse_output` magic to inlcude output in the docs under a collapsable element that is closed by default.
    To make the collapsable element open by default: `%nbdev_collapse_output open`"""
    _validate_param(line, 'nbdev_collapse_output', fixed_value='open')
    
def _new_test_flag_fn(flag):
    "Create a new test flag function and magic"
    # don't create "empty" test flags if tst_flags is not set, set to whitespace, has trailing | etc
    if not flag.strip(): return
    exec(f'''def nbdev_{flag}_test(line):
    """Put an `%nbdev_{flag}_test` magic on each "{flag}" test cell that you do not want to be run by default.
    To apply this flag to all tests in a notebook, one cell should contain: `%nbdev_{flag}_test all`
    These tests can be executed with the command line tool: `nbdev_test_nbs --flags {flag}`'."""
    _validate_param(line, 'nbdev_{flag}_test', fixed_value='all')''')
    exec(f'sys.modules[__name__].nbdev_{flag}_test = nbdev_{flag}_test')
    exec(f'register_line_magic(nbdev_{flag}_test)')

if IN_IPYTHON:
    from IPython.core.magic import register_line_magic
    fns = [nbdev_default_export, nbdev_export, nbdev_export_and_show, nbdev_export_internal,
           nbdev_collapse_input, nbdev_collapse_output]
    for fn in fns: register_line_magic(fn)
    for flag in Config().get('tst_flags', '').split('|'): _new_test_flag_fn(flag)