from fastcore.foundation import L

def qmd_meta(md, classes=None, style=None, **kwargs):
  if style: kwargs['style'] = "; ".join(f'{k}: {v}' for k,v in style.items())
  props = ' '.join(f'{k}="{v}"' for k,v in kwargs.items())
  classes = ' '.join('.'+c for c in L(classes))
  meta = []
  if classes: meta.append(classes)
  if props: meta.append(props)
  meta = ' '.join(meta)
  return md + ("{" + meta + "}" if meta else "")

def qmd_div(txt, classes=None, style=None, **kwargs): return qmd_meta("::: ", classes=classes, style=style, **kwargs) + f"\n\n{txt}\n\n:::\n\n"

def img(fname, classes=None, style=None, height=None, relative=None, link=False, **kwargs):
    kwargs,style = kwargs or {}, style or {}
    if height: kwargs["height"]= f"{height}px"
    if relative:
        pos,px = relative
        style["position"] = "relative"
        style[pos] = f"{px}px"
    res = f'![](images/{fname})'
    res = qmd_meta(res, classes=classes, style=style, **kwargs)
    if link: res = f'[{res}](images/{fname})'
    return res

def btn(txt, link):
    classes = ['btn-action-primary', 'btn-action', 'btn', 'btn-success', 'btn-lg']
    return qmd_meta(f'[{txt}]({link})', classes, role="button")

def banner(txt, classes=None, style=None): return qmd_div(txt, L('hero-banner')+classes, style=style)

features = L(
    ('docs', 'Beautiful technical documentation and scientific articles with Quarto'),
    ('testing', 'Out-of-the-box continuous integration with GitHub Actions'),
    ('packaging', 'Publish code to PyPI and conda, and prose to GitHub Pages'),
    ('vscode', 'Two-way sync with your favourite IDEs'),
    ('jupyter', 'Write prose, code, and tests in notebooks — no context-switching'),
    ('git', 'Git-friendly notebooks: human-readable merge conflicts; no unwanted metadata')
)

testms = L(
    ('chris-lattner.png', 'Chris Lattner', 'Inventor of Swift and LLVM', 'I really do think [nbdev] is a huge step forward for programming environments.'),
    ('fernando-pérez.jpeg', 'Fernando Pérez', 'Creator of Jupyter', '[nbdev] should be celebrated and used a lot more — I have kept a tab with your original nbdev blog post open for months in Chrome because of how often I refer to it and point others to this work.'),
    ('david-berg.jpeg', 'David Berg', 'Software Engineer, Netflix', 'Prior to using nbdev, documentation was the most cumbersome aspect of our software development process… Using nbdev allows us to spend more time creating rich prose around the many code snippets guaranteeing the whole experience is robust.<br><br>nbdev has turned what was once a chore into a natural extension of the notebook-based testing we were already doing.'),
    ('erik-gaasedelen.jpeg', 'Erik Gaasedelen', 'Software Engineer, Lyft', 'I use this in production at my company. It’s an awesome tool… nbdev streamlines everything so I can write docs, tests, and code all in one place… The packaging is also really well thought out.<br><br>From my point of view it is close to a Pareto improvement over traditional Python library development.'),
    ('roxanna-pourzand.jpeg', 'Roxanna Pourzand', 'Product Manager, Transform', 'We’re so excited about using nbdev. Our product is technical so our resulting documentation includes a lot of code-based examples. Before nbdev, we had no way of maintaining our code examples and ensuring that it was up-to-date for both command inputs and outputs. It was all manual. With nbdev, we now have this under control in a sustainable way. Since we’ve deployed these docs, we also had a situation where we were able to identify a bug in one of our interfaces, which we found by seeing the error that was output in the documentation.'),
    ('hugo-bowne-anderson.jpeg', 'Hugo Bowne-Anderson', 'Head of Developer Relations, Outerbounds', 'Nbdev has transformed the way we write documentation. Gone are the days of worrying about broken code examples when our API changes or due to human errors associated with copying & pasting code into markdown files. The authoring experience of nbdev is also powerful, allowing us to write prose and live code in a unified interface, which allows more experimentation with technical content. On top of this,  nbdev allows us to include unit tests in our documentation which mitigates the burden of maintaining the docs over time.')
)

def industry(im, **kwargs): return qmd_div(img(im, **kwargs), ["g-col-12", "g-col-sm-6", "g-col-md-3"])

def testm(im, nm, detl, txt):
    return qmd_div(f"""{img(im, link=True)}

# {nm}

## {detl}

### {txt}""", ["testimonial", "g-col-12", "g-col-md-6"])

expert_d = qmd_div('\n'.join(testms.starmap(testm)), ['content-block', 'grid', 'gap-4'])

def feature(im, desc): return qmd_div(f"{img(im+'.svg')}\n\n{desc}\n", ['feature', 'g-col-12', 'g-col-sm-6', 'g-col-md-4'])

feature_d = qmd_div('\n'.join(features.starmap(feature)), ['grid', 'gap-4'], style={"padding-bottom": "60px"})

def b(*args, **kwargs): print(banner (*args, **kwargs))
def d(*args, **kwargs): print(qmd_div(*args, **kwargs))

