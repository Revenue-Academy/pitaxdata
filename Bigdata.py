import numpy as np
import pandas as pd
from datetime import datetime

data = pd.read_csv('pitreformed.csv')

data['AGEGRP'] = np.where(data.AGE < 60, 0,
                          np.where((data.AGE < 80) & (data.AGE >= 60), 1, 2))
renames = {'SHORT_TERM_15PER': 'ST_CG_AMT_1', 'SHORT_TERM_30PER': 'ST_CG_AMT_2',
           'LONG_TERM_10PER': 'LT_CG_AMT_1', 'LONG_TERM_20PER': 'LT_CG_AMT_2',
           'SHORT_TERM_APPRATE': 'ST_CG_AMT_APPRATE',
           'TOTAL_INCOME_ALL':'GTI_BEFORE_LOSSES'}
data = data.rename(renames, axis=1)
data = data.fillna(0)
data.to_csv('pitBigData.csv', index=False)
