"""---
title: RenderScripts
---"""

from nbdev.qmd import *
def im(fn, width, **kw): return img(f"/images/{fn}", width=f"{width}%", **kw)
r=[]; a=r.append

a("""*RenderScripts* are regular Python scripts, except that:

- Rather than just having the extension `.py`, they have an extension like `.qmd.py`
- They contain a module docstring containing [frontmatter](https://quarto.org/docs/tools/jupyter-lab.html#yaml-front-matter) (i.e three hyphens on a line, then some yaml, then another three hyphens on a line).

These scripts are run when your site is rendered. Anything that they print to stdout becomes a new file in your site. The name of the file is the same as the name of the .py script, but without the `.py` extension. For instance, the page you're reading right now page is created by a script called `renderscript.qmd.py`, which you'll [find here](https://github.com/fastai/nbdev/blob/master/nbs/tutorials/renderscript.qmd.py).

Hot/live reloading even works with these .py scripts -- so as soon as you save the script, you'll see the new output in your web browser.

This approach can be particularly helpful for generating data-driven documents. For instance, consider this table, containing a list of the people with testimonials on nbdev's home page:
""")

testms = [
    ('chris-lattner.png', 'Chris Lattner', 'Inventor of Swift and LLVM'),
    ('fernando-pérez.jpeg', 'Fernando Pérez', 'Creator of Jupyter'),
    ('david-berg.jpeg', 'David Berg', 'Software Engineer, Netflix'),
    ('erik-gaasedelen.jpeg', 'Erik Gaasedelen', 'Software Engineer, Lyft'),
    ('roxanna-pourzand.jpeg', 'Roxanna Pourzand', 'Product Manager, Transform'),
    ('hugo-bowne-anderson.jpeg', 'Hugo Bowne-Anderson', 'Head of Developer Relations, Outerbounds')
]
r += tblhdr(['','Name','Position'], [1,3,4])
r += [tblrow([im(fn, 60), nm, ps]) for fn,nm,ps in testms]

a("""
When creating a table like this, it can be tricky to ensure that markdown is correct and consistent for every row. It can be easier and more maintainable to programatically generate it. The table above is generated from the following python list:

::: {.column-screen-inset-right}
```python
testms = [
    ('chris-lattner.png', 'Chris Lattner', 'Inventor of Swift and LLVM'),
    ('fernando-pérez.jpeg', 'Fernando Pérez', 'Creator of Jupyter'),
    ('david-berg.jpeg', 'David Berg', 'Software Engineer, Netflix'),
    ('erik-gaasedelen.jpeg', 'Erik Gaasedelen', 'Software Engineer, Lyft'),
    ('roxanna-pourzand.jpeg', 'Roxanna Pourzand', 'Product Manager, Transform'),
    ('hugo-bowne-anderson.jpeg', 'Hugo Bowne-Anderson', 'Head of Developer Relations, Outerbounds')
]
```
:::

To produce the table from this python list, the following two lines of code are used:

```python
r += tblhdr(['','Name','Position'], [1,3,4])
r += [tblrow([im(fn, 60), nm, ps]) for fn,nm,ps in testms]
```

`r` is a list which is printed at the end of the script, and [`tblhdr`](https://nbdev.fast.ai/api/qmd.html#tblhdr) and [`tblrow`](https://nbdev.fast.ai/api/qmd.html#tblrow) are two functions imported from the module `nbdev.qmd`. [`nbdev.qmd`](https://nbdev.fast.ai/api/qmd.html) is a small module that has some convenient functions for creating `.qmd` documents, such as the table creation functions used above. You can see more examples of their use in [index.qmd.py](https://github.com/fastai/nbdev/blob/master/nbs/index.qmd.py), which is the RenderScript which creates the [nbdev home page](https://nbdev.fast.ai).

You can use RenderScripts to create any kind of file. For instance, the SVG below is created dynamically using [this script](https://github.com/fastai/nbdev/blob/master/nbs/images/circles.svg.py):
""")

a(im('circles.svg', 40))

a("""
Once you've run `nbdev_preview` or `nbdev_docs` you'll find your rendered document in the `_proc` directory, along with all of your processed notebooks. This can be helpful for debugging. You can also simply call your script directly from the shell (e.g. `python renderscript.qmd.py`) to view the printed output.""")

print('\n'.join(r))

