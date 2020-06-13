from nbdev.imports import IN_IPYTHON
# 1st print in ipython gets appended with rubbish like \x1b[22;0t\x1b]0;IPython
print('ignore')
# so we'll only pay attention to the 2nd print
print(IN_IPYTHON)