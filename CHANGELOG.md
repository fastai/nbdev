# Release notes

<!-- do not remove -->
## 1.0.10

### New Features

- Auto-generate CHANGELOG from GitHub issues ([#236](https://api.github.com/repos/fastai/nbdev/issues/236))
  - Use labels to create sub-headings in CHANGELOG

- Support for `doc_path` ([#235](https://api.github.com/repos/fastai/nbdev/issues/235))

- re-write of test flags ([#232](https://api.github.com/repos/fastai/nbdev/issues/232))
  - Magics flags for tests

- Add ability to have Colab badges on pages ([#210](https://api.github.com/repos/fastai/nbdev/issues/210))
  - EDIT: this is ready for review now    This closes issue #209

- Remove colab vendor specific tags which cause nbdev_build_docs to fail ([#207](https://api.github.com/repos/fastai/nbdev/issues/207))
  - This adds an additional routine to find and remove the colab
    specific vendor tags which causes the `nbdev_build_lib` to fail.
    Also modified clean notebook tests to add condition for additional
    colab specific vendor tags being removed by `nbdev_clean_nbs`
    command.    Fixes #206

### Bugs Squashed

- hooks folder inside .git must be manually created before nbdev_install_git_hooks ([#230](https://api.github.com/repos/fastai/nbdev/issues/230))
  - Platform for reproduction: Paperspace gradient - P5000 Free GPU -
    FastAI template    I was following the tutorial at
    https://nbdev.fast.ai/tutorial.html to develop my own library and
    when i run nbdev_install_git_hooks as stated in "Install git
    hooks" section i run into the following error:    ```  Traceback
    (most recent call last):    File
    "/opt/conda/envs/fastai/bin/nbdev_install_git_hooks", line 8, in
    <module>      sys.exit(nbdev_install_git_hooks())    File
    "/opt/conda/envs/fastai/lib/python3.8/site-
    packages/fastscript/core.py", line 76, in _f
    func(**args.__dict__)    File
    "/opt/conda/envs/fastai/lib/python3.8/site-packages/nbdev/cli.py",
    line 337, in nbdev_install_git_hooks      with open(fn, 'w') as f:
    FileNotFoundError: [Errno 2] No such file or directory:
    '/notebooks/.git/hooks/post-merge'  ```    After i created
    manually the .git/hooks folder the error went away and the command
    returned the following, as it's supposed to be:  ```  Executing:
    git config --local include.path ../.gitconfig  Success: hooks are
    installed and repo's .gitconfig is now trusted  ```

- updates to how backtick names are converted to doc links ([#218](https://api.github.com/repos/fastai/nbdev/issues/218))
  - Hi @jph00     this one takes care of
    https://github.com/fastai/nbdev/issues/200 by  - checking that a
    module name is also a valid doc name before linking  - not
    converting parameter names to links    few other things  - should
    "isnter" be "enter" in the following?      - "Search for doc links
    for any item between backticks in `text` and isnter them"  -
    should we write a map of module to notebook names to _nbdev.py -
    so `doc_link` doesn't have to assume these names correspond   -
    the "not converting parameter names to links" idea works for
    show_doc calls for now - would you like to extend this behavior to
    markdown following a show_doc call too?

## Version 1.0.0

- Initial release

