import numpy as np
import pandas as pd
from datetime import datetime

def age(dob):
    end_date = datetime(2017,4,1)
    return end_date.year - dob.year - ((end_date.month,end_date.day)<
                                        (dob.month,dob.day))

itr1 = pd.read_csv('SAMPLE_ITR/ITR1-SAMPLE_AY_2017-18.TXT', sep='|')
itr3 = pd.read_csv('SAMPLE_ITR/ITR3-SAMPLE_AY_2017-18.TXT', sep='|')
itr1 = itr1.drop(['STCG_OTHERS', 'STCG_SEC111A'], axis=1)
itr3 = itr3.rename({'TI.TOTAL_DEDUC_VIA': 'TOTAL_DEDUC_VIA',
                    'EDUCATION_CESS':'EDUCATION_CESS_115JC',
                    'EDUCATION_CESS.1':'EDUCATION_CESS'}, axis=1)
itr3['FORM_ID'] = 'ITR-3'
itr3['ASSESSMENT_YEAR'] = 2017
itr3['GENDER'] = 'MISSING'
itr3['RES_STATUS'] = 'MISSING'
dobs = pd.to_datetime(itr1.DOB)
itr1['AGE'] = dobs.apply(age)

data = pd.concat([itr1, itr3], ignore_index=True, sort=False)
data['AGEGRP'] = np.where(data.AGE < 60, 0,
                          np.where((data.AGE < 80) & (data.AGE >= 60), 1, 2))
renames = {'SHORT_TERM_15PER': 'ST_CG_AMT_1', 'SHORT_TERM_30PER': 'ST_CG_AMT_2',
           'LONG_TERM_10PER': 'LT_CG_AMT_1', 'LONG_TERM_20PER': 'LT_CG_AMT_2',
           'SHORT_TERM_APPRATE': 'ST_CG_AMT_APPRATE',
           'TOTAL_INCOME_ALL':'GTI_BEFORE_LOSSES'}
data = data.drop(['PAN','DOB','Unnamed: 83'], axis=1)
data = data.rename(renames, axis=1)
data = data.fillna(0)
data.to_csv('pit.csv', index=False)
