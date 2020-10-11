# Release notes

<!-- do not remove -->

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

