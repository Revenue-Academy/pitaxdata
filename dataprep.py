import pandas as pd
import numpy as np

useable_columns = ['WT', 'RO5', 'IN13S1', 'IN13S2', 'IN13S3', 'IN13S6',
                   'INCCROP', 'INCAGPROP', 'INCAG', 'INCBUS', 'INCOTHER',
                   'INCOME', 'WS10ANNUAL', 'WSEARNNONAG', 'STATEID', 'DISTID',
                   'PSUID']
data = pd.read_csv('36151-0001-Data.tsv', sep='\t', na_values=' ',
                   usecols=useable_columns)
# add column to create age group
data['age_group'] = np.where(data['RO5'] < 60, 0,
                             np.where(data['RO5'] < 80, 1, 2))
data.to_csv('taxdata.csv', index=False)
