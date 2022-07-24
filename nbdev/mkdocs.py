import re
from mkdocs.plugins import BasePlugin

_re_digits = re.compile(r'^\d+_')

class RmNumPrefix(BasePlugin):
    def on_pre_page(self, page, config, files): page.title = _re_digits.sub('', page.url)[:-1]

