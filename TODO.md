## Docs export

- Implement [show_doc](https://github.com/fastai/nbdev/blob/master/nbs/02_showdoc.ipynb) in markdown/HTML
  - Pluggable parsers for parameter docs
    - docments
    - numpy
- Optionally execute show_doc cells
- Remove `#export` and `#hide` cells
- Remove all cell comments
- auto-add `show_doc`
  - support `#default_cls_lvl`
- implement #collapse_input, #collapse_output, #hide_output, #hide_input
- Back-tick linking
- implement stuff from nbdev export2html, e.g.(?):
  - remove_widget_state
  - make_readme
- hide headings that end in ' -'

## Other

- Some way to extend preprocessors, e.g. Metaflow-specific stuff
