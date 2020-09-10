# Release notes

<!-- do not remove -->

## 1.0.15

### New Features

- add option to not exec nb for fastpages ([#244](https://api.github.com/repos/fastai/nbdev/issues/244))
  - We need ability to skip execution of notebooks in fastpages.
    Discussed in discord : https://discordapp.com/channels/68989236999
    8676007/689892370002870284/753640345731989524

- Enable Codespaces for nbdev ([#243](https://api.github.com/repos/fastai/nbdev/issues/243))
  - Similar to https://github.com/fastai/fastai/pull/2779

- remove numpy conda dep and update to fastcore 1.0.5 ([#241](https://api.github.com/repos/fastai/nbdev/issues/241))

- Automated tag/release process ([#237](https://api.github.com/repos/fastai/nbdev/issues/237))

### Bugs Squashed

- Fix: correct notebook2html path operation for Windows. ([#239](https://api.github.com/repos/fastai/nbdev/issues/239))
  - With the default project structure, the glob() in notebook2html()
    can easilly find a copy of a .ipynb file in .ipynb_checkpoints. In
    this case, running nbdev_build_docs will fail, assuming the .ipynb
    imports the project (the relative path is not correct from this
    dir.) The current code to skip hidden path components searches for
    '/.', whereas str(f) will return the Windows backslash path, so
    the search will fail. f.as_posix() returns a '/' delimited path on
    all platforms.    I verified failure of nbdev_build_docs before
    the fix, and success after installing the fix.

- allow nbdev imports when not in an nbdev project ([#238](https://api.github.com/repos/fastai/nbdev/issues/238))
  - really sorry @jph00 we need this change to fix
    https://forums.fast.ai/t/create-config-when-pip-install-uqq-
    fastbook/78340/6    all the colab testing i did last week was on
    full nbdev projects )o: i'll add "nbdev import from a standalone
    nb" to my pre-PR checklist


## 1.0.13

### New Features

- remove numpy conda dep and update to fastcore 1.0.5 ([#241](https://api.github.com/repos/fastai/nbdev/issues/241))

### Bugs Squashed

- allow nbdev imports when not in an nbdev project ([#238](https://api.github.com/repos/fastai/nbdev/issues/238))

## 1.0.10

### New Features

- Magic flags for tests ([#232](https://github.com/fastai/nbdev/pull/232))
  - See [the docs](https://nbdev.fast.ai/magic_flags.html) for details

- Add ability to have Colab badges on pages ([#210](https://github.com/fastai/nbdev/pull/210))
  - See [the docs](https://nbdev.fast.ai/#Google-Colab-Badges) for details

- Support for `doc_path` ([#235](https://github.com/fastai/nbdev/pull/235))
  - Place doc template in path pointed to by `doc_path` if you need your template in a different location to your built docs

### Bugs Squashed

- Remove colab vendor specific tags which cause `nbdev_build_docs` to fail ([#207](https://github.com/fastai/nbdev/pull/207))

- hooks folder inside .git must be manually created before `nbdev_install_git_hooks` ([#230](https://github.com/fastai/nbdev/pull/230))

- updates to how backtick names are converted to doc links ([#218](https://github.com/fastai/nbdev/pull/218))

## Version 1.0.0

- Initial release

