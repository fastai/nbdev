# Release notes

<!-- do not remove -->

## 1.1.20

### New Features

- skip symlinks in recursive glob ([#515](https://github.com/fastai/nbdev/issues/515))


## 1.1.15

### Breaking Changes

- make recursive behavior for `nbdev_build_docs` consistent with `nbdev_build_lib` ([#467](https://github.com/fastai/nbdev/pull/467)), thanks to [@hamelsmu](https://github.com/hamelsmu)

### New Features

- Allow for a one-time only (potentially) .py -> .ipynb generation ([#369](https://github.com/fastai/nbdev/issues/369))

### Bugs Squashed

- Images with `attachment:` break export ([#501](https://github.com/fastai/nbdev/pull/501)), thanks to [@yacchin1205](https://github.com/yacchin1205)
- Docs nav doesn't work on gitlab ([#488](https://github.com/fastai/nbdev/pull/488)), thanks to [@tcapelle](https://github.com/tcapelle)
- clean up all instances of recursive ([#470](https://github.com/fastai/nbdev/pull/470)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- After 'conda install -c fastai nbdev', error "`HTMLExporter` object has no attribute `template_path`" ([#431](https://github.com/fastai/nbdev/issues/431))


## 1.1.13

### New Features

- support windows ([#392](https://github.com/fastai/nbdev/pull/392)), thanks to [@mszhanyi](https://github.com/mszhanyi)
- `nbdev_new`: get template from latest release asset ([#382](https://github.com/fastai/nbdev/pull/382)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- Add more license options

### Bugs Squashed

- Fix recursive flag ([#433](https://github.com/fastai/nbdev/pull/433)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- conda not installing nbdev properly on WSL2 ([#430](https://github.com/fastai/nbdev/issues/430))
- fix nb2md ([#424](https://github.com/fastai/nbdev/pull/424)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- `nbdev_build_lib` seems to convert more notebooks than expected ([#423](https://github.com/fastai/nbdev/issues/423))
- fix default arg issue with `nbdev_update_lib` ([#416](https://github.com/fastai/nbdev/pull/416)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- `nbdev_update_lib` errors out when fname not supplied ([#415](https://github.com/fastai/nbdev/issues/415))
- `nbdev_new` fails on calling the GitHub API without guidance ([#404](https://github.com/fastai/nbdev/issues/404))
- fix recurse issue ([#391](https://github.com/fastai/nbdev/pull/391)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- `nbdev_build_docs`----ModuleNotFoundError: No module named 'fastcore' ([#390](https://github.com/fastai/nbdev/issues/390))
- `nbdev_test_nbs` --fname broke in 1.1.7 ([#388](https://github.com/fastai/nbdev/issues/388))
- set recursive=True for docs ([#387](https://github.com/fastai/nbdev/pull/387)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- fix url for getting branch ([#386](https://github.com/fastai/nbdev/pull/386)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- `nbdev_nb2md` throws error when called in a notebook ([#381](https://github.com/fastai/nbdev/issues/381))


## 1.1.12

### New Features

- `nbdev_new` should grab files from a release asset in `nbdev_template` ([#383](https://github.com/fastai/nbdev/issues/383))
- Use Jekyll Theme instead of vendoring all required files ([#379](https://github.com/fastai/nbdev/issues/379))
- Create relevant directories in `docs/_data` if do not already exist ([#377](https://github.com/fastai/nbdev/issues/377))


## 1.1.6

### New Features

- Clean Google Colab metadata and line endings ([#364](https://github.com/fastai/nbdev/pull/364)), thanks to [@muellerzr](https://github.com/muellerzr)
- add ability to find notebooks recursively ([#359](https://github.com/fastai/nbdev/pull/359)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- Add `bare` flag to `nbdev_build_lib` ([#336](https://github.com/fastai/nbdev/issues/336))
- install git hooks in `nbdev_new` ([#308](https://github.com/fastai/nbdev/issues/308))
- `nbdev_new` now works on an existing cloned repo, instead of creating a new repo ([#307](https://github.com/fastai/nbdev/issues/307))

### Bugs Squashed

- `nbdev_update_lib --fname notebook.ipynb` crashes (while `nbdev_update_lib` works) ([#341](https://github.com/fastai/nbdev/issues/341))
- Copy new files only if they don't exist for nbdev_new ([#309](https://github.com/fastai/nbdev/issues/309))


## 1.1.3

### New Features

- Place source code below heading on #exports ([#265](https://github.com/fastai/nbdev/pull/265)), thanks to [@hamelsmu](https://github.com/hamelsmu)


## 1.1.2

### Bugs Squashed

- update fastcore requirement ([#281](https://github.com/fastai/nbdev/issues/281))


## 1.1.1

### New Features

- Make CLI faster by removing unneeded imports and moving CLI commands to source modules ([#271](https://github.com/fastai/nbdev/issues/271))
- Move `Config` to fastcore ([#280](https://github.com/fastai/nbdev/issues/280))

## 1.1.0
### Breaking Changes

- Remove magics ([#269](https://github.com/fastai/nbdev/issues/269))
- Removed callbacks ([#253](https://github.com/fastai/nbdev/pull/253)), thanks to [@pete88b](https://github.com/pete88b)
- move conda packager to `fastrelease` ([#252](https://github.com/fastai/nbdev/issues/252))

### New Features

- Place source code below heading on #exports ([#265](https://github.com/fastai/nbdev/pull/265)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- always skip cells labeled "skip" in test ([#257](https://github.com/fastai/nbdev/issues/257))

## 1.0.17

### Bugs Squashed

- restrict nbconvert<6 to avoid upgrade problems ([#249](https://github.com/fastai/nbdev/issues/249))

## 1.0.16

### Bugs Squashed

- When generating docs, import cells are run even if not exported ([#248](https://github.com/fastai/nbdev/issues/248))

## 1.0.15

### New Features

- add option to not exec nb for fastpages ([#244](https://github.com/fastai/nbdev/issues/244))
- Enable Codespaces for nbdev ([#243](https://github.com/fastai/nbdev/issues/243))

### Bugs Squashed

- Fix: correct notebook2html path operation for Windows. ([#239](https://github.com/fastai/nbdev/issues/239))

## 1.0.13

### New Features

- remove numpy conda dep and update to fastcore 1.0.5 ([#241](https://github.com/fastai/nbdev/issues/241))

### Bugs Squashed

- allow nbdev imports when not in an nbdev project ([#238](https://github.com/fastai/nbdev/issues/238))

## 1.0.10

### New Features

- Magic flags for tests ([#232](https://github.com/fastai/nbdev/pull/232))
- Add ability to have Colab badges on pages ([#210](https://github.com/fastai/nbdev/pull/210))
- Support for `doc_path` ([#235](https://github.com/fastai/nbdev/pull/235))

### Bugs Squashed

- Remove colab vendor specific tags which cause `nbdev_build_docs` to fail ([#207](https://github.com/fastai/nbdev/pull/207))
- hooks folder inside .git must be manually created before `nbdev_install_git_hooks` ([#230](https://github.com/fastai/nbdev/pull/230))
- updates to how backtick names are converted to doc links ([#218](https://github.com/fastai/nbdev/pull/218))

## Version 1.0.0

- Initial release


