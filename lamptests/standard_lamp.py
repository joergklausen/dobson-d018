# -*- coding: utf-8 -*-
"""
Define a class SL to read, process and evaluate O3Dobson standard lamp test files.

@author: joerg.klausen@meteoswiss.ch
"""

import os
import dateutil
import logging
import pandas as pd
import matplotlib.pyplot as plt
import re

class StandardLamp:
    """
    O3Dobson standard lamp data proceessor.
    """

    def __init__(self):
        try:
            # set up logging to file
            self.logger = logging.getLogger(__name__)
            self.logger.info("Class StandardLamp initialized successfully.")

        except Exception as err:
            self.logger.error("Error initializing class StandardLamp.", err)
        except Exception as err:
            print(err)

    
    def read_file(self, file: str, remove_duplicates=True, verbose=True) -> pd.DataFrame:
        """
        Extract data from standard lamp test file(s)
        
        Args:
            file (str): Full url or path to file
            remove_duplicates (bool, optional): Should (near) duplicates in tbl be removed? . Defaults to True.
            verbose (bool, optional): Should information be logged to a logfile? Defaults to True.

        Returns:
            pd.DataFrame: _description_
        """
        try:
            regex = r'((?:\d{1,2}[\.|/]\d{1,2}[\.|/]\d{2,4})\s(?:(?:(?:0?\d?|1'
            regex += r'[0-2])(?::[0-5]\d){2})\s(?:AM|PM)|(?:[01]?\d|2[0-3])(?:'
            regex += r':[0-5][0-9]){2})).*\nStandard\sLamp\sName:\s(.{3})\s+Instrume'                     
            regex += r'nt\sTemperature:\s([0-9.]+)\s*.+\n'
            regex += (r'Test\s(\w)\s+' + '([-0-9.]+)\s+' * 7) * 3

            msg = f'Extracting from file {file} ...'
            if verbose:
                print(msg)
                self.logger.info(msg)
            with open(file, 'r') as f:
                txt = f.read()
            data = re.findall(regex, txt)
            df = pd.DataFrame(data)
            if not data:
                if verbose:
                    self.logger.warning(f'No data recognized in file {self.file}')
                    return(df)
                
            # create unique column names
            prefix = [df[3][0], df[11][0], df[19][0]]
            labels = ["", "_1", "_2", "_3", "_mean", "_N", "_N_ref", "_dN"]            
            columns = ['dtm', 'lamp', 'T']
            columns += [prefix[0] + x for x in labels]
            columns += [prefix[1] + x for x in labels]
            columns += [prefix[2] + x for x in labels]
            df.columns = columns
            
            # drop 'Test' columns            
            df.drop(prefix, axis=1, inplace=True) 
            
            # drop duplicates in this file
            if remove_duplicates:
                with_dups = len(df)
                df.drop_duplicates(subset = df.columns[1:],
                                   keep = 'first',
                                   inplace=True)
                dups = with_dups - len(df)
                if dups > 0 and verbose:
                    msg = '%s duplicate records removed from file %s' % (dups, file)
                    self.logger.info(msg)

            # add source column
            source = [file for x in df.index]
            
            # convert various time formats to ISO, then datetime, set index           
            dtm_ori = []
            dtm = []
            for item in df['dtm'].items():
                dtm_ori.append(item[1])
                dtm.append(dateutil.parser.parse(item[1], dayfirst=True))
            df['dtm_ori'] = dtm_ori
            df['dtm'] = dtm
            df['source'] = source            
            df.sort_values(by='dtm', inplace=True, ascending=True)

            return(df)            
            
        except Exception as err:
            self.logger.error(err)
            print(err)


    def plot_data(self, df: pd.DataFrame, path=None, verbose=True) -> None:
        """
        Plot standard lamp tests as a function of time
    
        Plot standard V, W, Y, Z lamp tests of as a function of time        
    
        Parameters
        ----------
        df : object
            Pandas dataframe, expected to have an index 'dtm'
        path : str
            If specified, the plot is saved to path as a .png file
        verbose : str
            Should function return info? default=True
    
        Returns
        _______
        nothing
        """
        
    # def plot_sl_data(self, df: pd.DataFrame, figure="sl_tests.png", data="sl_tests_all_years.csv", verbose=True):
        try:
            # select data
            fig, ax = plt.subplots(sharey=True)
            ax.plot(df['dtm'], df['A_mean'], color='r')
            # plt.figure(figsize=(16, 8), dpi=150)
            # df["A_mean"].plot(label="A_mean", color="red")
            # plt.plot(self.data['dtm'], self.df['A_Mean'], 'x')
#             cols = 'XAD'
#             x = df.reset_index()['dtm'].tolist()
#             y = df[cols].tolist()
#             ymin = min(y)
#             ymax = max(y)
        
#             # set up plot, ax1 for XAD coverage
#             fig, ax1 = plt.subplots(nrows=1, ncols=1, sharex=True)
    
#             # configure ax1
#             ax1.set_ylim(ymin, ymax)
#             ax1.set_title('Dobson D018 lamp tests')
#             ax1.set_ylabel("...")
            
#             # colors = cm.Greens(y/ymax)        
#             # ax1.bar(x, y, width=-1, align='edge', color = colors, edgecolor = colors)
#             ax1.plot(df.loc[:, cols], label=cols, marker=".", linewidth=0.3)
#             ax1.xaxis_date()
            
#             ax1.legend([cols], prop={'size':6}, loc='best')
    
#             plt.gcf().autofmt_xdate()
#             plt.tight_layout()
#             path = os.path.join(os.path.expanduser(self.config['results']), 
#                                 self.config['wsi'], 'dobson')
#             os.makedirs(path, exist_ok=True)
                
# #            plt.show()
#             plt.savefig(os.path.join(path, figure), dpi=300)
    
#             if ".csv" in data.lower():
#                 df.to_csv(os.path.join(path, data))
    
        except Exception as err:
            print(err)
