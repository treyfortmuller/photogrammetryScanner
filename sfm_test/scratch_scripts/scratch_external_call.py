# Test the calling of a python script within a python script
# Trey Fortmuller

import os

cwd = os.path.join(os.getcwd(), "scratch_external_called.py")

os.system('{} {}'.format('python', cwd))
