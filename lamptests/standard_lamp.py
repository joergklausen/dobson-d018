# -*- coding: utf-8 -*-
"""
Define a class SL to read, process and evaluate O3Dobson standard lamp test files.

@author: joerg.klausen@meteoswiss.ch
"""

import os
import pandas as pd

class StandardLamp:
    """
    O3Dobson standard lamp data proceessor.
    """

    def __init__(self, config):
        try:
            print("__init__")

        except Exception as err:
            print(err)

    
    def read_file(self, path: str) -> pd.DataFrame:
        try:
            print("read_file")

       except Exception as err:
            print(err)


    def plot_data(self, df: pd.DataFrame, path=None) -> None:
        try:
            print("plot_data")

       except Exception as err:
            print(err)
