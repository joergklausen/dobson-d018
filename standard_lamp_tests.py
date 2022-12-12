# -*- coding: utf-8 -*-
"""
Read, process and evaluate O3Dobson standard lamp test files.

@author: joerg.klausen@meteoswiss.ch
"""

# %%
import os
from lamptests.standard_lamp import StandardLamp

file = r"C:\Users\jkl\Documents\git\dobson-d018\data\lamptests\18V.018"

# %%
sl = StandardLamp()
df = sl.read_file(file=file)
# %%
