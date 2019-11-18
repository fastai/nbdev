import os,re,json,glob,collections,pickle,shutil
from pathlib import Path
from textwrap import TextWrapper
import numpy as np

def test_eq(a,b): assert a==b, f'{a}, {b}'