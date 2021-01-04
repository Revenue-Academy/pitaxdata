import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
import numpy as np
import json

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Data Preparation to read Household Survey Files and generate csv files to use

filename = "India GST Rates Dec-2020.xlsx"
df_rates = pd.read_excel(filename,sheet_name="CMIE", index_col=None, header=0)
cons_list = df_rates['cons_amt'].values.tolist()
cons_category = df_rates['category'].values.tolist()
df_rates = df_rates[['item','gst_rate']]
df_rates = df_rates.set_index('item')
df_item_rates_for_json = df_rates.T
df_item_rates_for_json.columns= "_gst_rate_" + df_item_rates_for_json.columns.str.lower()
for i in range(0,17):
   df_item_rates_for_json = pd.concat([df_item_rates_for_json, pd.DataFrame([[np.nan] *
                                      df_item_rates_for_json.shape[1]], columns=df_item_rates_for_json.columns)], ignore_index=True)

df_item_rates_for_json.iloc[13,:] = df_item_rates_for_json.iloc[0,:]
d = [[i] for i in df_item_rates_for_json.iloc[13,:]]
df_item_rates_for_json.loc[len(df_item_rates_for_json)]=d
df_item_rates_for_json.iloc[13,:] = df_item_rates_for_json.iloc[18,:]
df_item_rates_for_json = df_item_rates_for_json[:-1]

df_item_rates_for_json['gst_rate_benchmark']= ""
row_label_year = [["2020"] for i in df_item_rates_for_json.iloc[13,:]]
range_rate = [{"min": 0, "max": 1} for i in df_item_rates_for_json.iloc[13,:]]

df_item_rates_for_json.iloc[0,:] = df_item_rates_for_json.columns.str.replace('_gst_rate_','GST Rate for ')
df_item_rates_for_json.iloc[1,:] = df_item_rates_for_json.columns.str.replace('_gst_rate_','GST Rate relevant for consumption of ')
df_item_rates_for_json.iloc[2,:] = "GST Rules"
df_item_rates_for_json.iloc[3,:] = ""
df_item_rates_for_json.iloc[4,:] = "AYEAR"
df_item_rates_for_json.iloc[5,:] = row_label_year
df_item_rates_for_json.iloc[6,:] = 2020
df_item_rates_for_json.iloc[7,:] = False
df_item_rates_for_json.iloc[8,:] = False
df_item_rates_for_json.iloc[9,:] = ""
df_item_rates_for_json.iloc[10,:] = ""
df_item_rates_for_json.iloc[11,:] = False
df_item_rates_for_json.iloc[12,:] = False
df_item_rates_for_json.iloc[14,:] = range_rate
df_item_rates_for_json.iloc[15,:] = ""
df_item_rates_for_json.iloc[16,:] = ""
df_item_rates_for_json.iloc[17,:] = "stop"

d=[0.18]
#yr=["2020"]
#df_item_rates_for_json['gst_rate_benchmark']= ""
df_item_rates_for_json.iloc[0,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= "GST Benchmark Rate"
df_item_rates_for_json.iloc[1,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= "GST Benchmark Rate to calculate Policy Gap"
df_item_rates_for_json.iloc[2,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= "Benchmark Rate"
df_item_rates_for_json.iloc[3,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= ""
df_item_rates_for_json.iloc[4,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= "AYEAR"
#df_item_rates_for_json.iloc[5,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= row_label_year
df_item_rates_for_json.iloc[6,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= 2020
df_item_rates_for_json.iloc[7,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= False
df_item_rates_for_json.iloc[8,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= False
df_item_rates_for_json.iloc[9,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= ""
df_item_rates_for_json.iloc[10,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= ""
df_item_rates_for_json.iloc[11,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= False
df_item_rates_for_json.iloc[12,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= False
df_item_rates_for_json.iloc[13,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= d
#df_item_rates_for_json.iloc[14,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= range_rate
df_item_rates_for_json.iloc[15,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= ""
df_item_rates_for_json.iloc[16,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= ""
df_item_rates_for_json.iloc[17,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= "stop"


df_item_rates_for_json['ind'] = ""
df_item_rates_for_json.iloc[0, df_item_rates_for_json.columns.get_loc('ind')] = "long_name"
df_item_rates_for_json.iloc[1, df_item_rates_for_json.columns.get_loc('ind')] = "description"
df_item_rates_for_json.iloc[2, df_item_rates_for_json.columns.get_loc('ind')] = "itr_ref"
df_item_rates_for_json.iloc[3, df_item_rates_for_json.columns.get_loc('ind')] = "notes"
df_item_rates_for_json.iloc[4, df_item_rates_for_json.columns.get_loc('ind')] = "row_var"
df_item_rates_for_json.iloc[5, df_item_rates_for_json.columns.get_loc('ind')] = "row_label"
df_item_rates_for_json.iloc[6, df_item_rates_for_json.columns.get_loc('ind')] = "start_year"
df_item_rates_for_json.iloc[7, df_item_rates_for_json.columns.get_loc('ind')] = "cpi_inflatable"
df_item_rates_for_json.iloc[8, df_item_rates_for_json.columns.get_loc('ind')] = "cpi_inflated"
df_item_rates_for_json.iloc[9, df_item_rates_for_json.columns.get_loc('ind')] = "col_var"
df_item_rates_for_json.iloc[10, df_item_rates_for_json.columns.get_loc('ind')] = "col_label"
df_item_rates_for_json.iloc[11, df_item_rates_for_json.columns.get_loc('ind')] = "boolean_value"
df_item_rates_for_json.iloc[12, df_item_rates_for_json.columns.get_loc('ind')] = "integer_value"
df_item_rates_for_json.iloc[13, df_item_rates_for_json.columns.get_loc('ind')] = "value"
df_item_rates_for_json.iloc[14, df_item_rates_for_json.columns.get_loc('ind')] = "range"
df_item_rates_for_json.iloc[15, df_item_rates_for_json.columns.get_loc('ind')] = "out_of_range_minmsg"
df_item_rates_for_json.iloc[16, df_item_rates_for_json.columns.get_loc('ind')] = "out_of_range_maxmsg"
df_item_rates_for_json.iloc[17, df_item_rates_for_json.columns.get_loc('ind')] = "out_of_range_action"
df_item_rates_for_json.set_index('ind', inplace=True)

item_rates_dict_for_json = df_item_rates_for_json.to_dict()

with open('current_law_policy_pit_cit.json', 'r') as f:
    current_law_policy_dict = json.load(f)

current_law_policy_dict.update(item_rates_dict_for_json)

with open("current_law_policy_cmie.json", "w") as f:
    json.dump(current_law_policy_dict, f, indent=4, sort_keys=False)

"""
Generate gst.csv which contains consumption information from Consumption
Pyramid Data - One record for each household  
"""
filename = "consumption_pyramids_20200831_MS_rev.csv"
df_cons_summ = pd.read_csv(filename)

df_cons_summ['HH_WEIGHT_ADJ'] = df_cons_summ['HH_NON_RESPONSE_MS']*df_cons_summ['HH_WEIGHT_MS']

df_cons_summ = df_cons_summ.replace(-99, 0)
df_cons_summ['ASSESSMENT_YEAR'] = 2020
df_cons_summ['HH_SIZE'] = 0
SIZE_GROUP_LIST = ['1 Member', '2 Members', '3 Members', '4 Members', '5 Members', '6 Members',
                   '7 Members', '8-10 Members', '11-15 Members', '> 15 Members', 'Data Not Available']
SIZE_GROUP_NUM = [1,2,3,4,5,6,7,9,13,16,0]

i=0
for hhsize in SIZE_GROUP_LIST:
    df_cons_summ['HH_SIZE'] = np.where(df_cons_summ['SIZE_GROUP']==hhsize, 
                SIZE_GROUP_NUM[i],df_cons_summ['HH_SIZE'])
    i = i+1
df_cons_summ.drop(['HH_NON_RESPONSE_MS', 'SIZE_GROUP'], axis=1, inplace=True)

cols = ['ASSESSMENT_YEAR', 'HH_ID', 'STATE', 'REGION_TYPE', 'DISTRICT', 'STRATUM',
        'HH_WEIGHT_ADJ', 'HH_WEIGHT_MS', 'HH_SIZE', 'TOTAL_EXPENDITURE'] + cons_list
        
df_cons_summ = df_cons_summ[cols]
df_cons_summ.columns = df_cons_summ.columns.str.replace('MONTHLY_EXPENSE_ON_','CONS_')
df_cons_summ = df_cons_summ.rename(columns={'HH_ID': 'ID_NO'})
df_cons_summ = df_cons_summ.rename(columns={'HH_WEIGHT_ADJ': 'WEIGHT'})
df_cons_summ = df_cons_summ.rename(columns={'HH_WEIGHT_MS': 'WEIGHT0'})

cols_second_level= cols = ['ASSESSMENT_YEAR', 'ID_NO', 'STATE', 'REGION_TYPE', 'DISTRICT', 'STRATUM',
        'WEIGHT', 'WEIGHT0', 'HH_SIZE', 'TOTAL_EXPENDITURE'] + cons_category

"""
HH_ID, STATE, HR, REGION_TYPE, MONTH_SLOT, MONTH ,REASON_FOR_NON_RESPONSE
DISTRICT, RESPONSE_STATUS, FAMILY_SHIFTED, STRATUM, PSU_ID, HH_WEIGHT_MS
HH_WEIGHT_FOR_COUNTRY_MS, HH_WEIGHT_FOR_STATE_MS, HH_NON_RESPONSE_MS, 
HH_NON_RESPONSE_FOR_COUNTRY_MS, HH_NON_RESPONSE_FOR_STATE_MS
AGE_GROUP, OCCUPATION_GROUP, EDUCATION_GROUP, GENDER_GROUP
, TOTAL_EXPENDITURE
"""

df_cons_summ.to_csv('gst_cmie_august_2020.csv', index=False)

"""
Gross Private Final Consumption Expenditure in 2011 and in 
Assessment Year 2020 or financial year 2016 - 
Source: Annual Estimate of GDP at Current Prices base 2011-12 
Ministry of Statistics and Program Implementation MOSPI
mospi.nic.in/data
"""

HHS_TOTAL_WEIGHT = 2210659 
GPFCE_2011 = 4910447
GPFCE_2016 = 9004904
GPFCE_2020 = 10083000
GPFCE_2018 = 11333000
INFLATOR_2011 = (GPFCE_2011/HHS_TOTAL_WEIGHT)
"""
Extraploating 2011 data to assessment year 2020
"""
#df_cons_summ['Value'] = df_cons_summ['Value'] * (GPFCE_2016/GPFCE_2011)
#df_cons_summ['Value'] = df_cons_summ['Value'] * INFLATOR_2011
#df_cons_summ['Value'] = df_cons_summ['Value'] * (GPFCE_2016/GPFCE_2011)

"""
Generate JSON File for the gst record variables which declares all variables
used in gst.csv
"""
df_gst_for_json_read = df_cons_summ.drop(df_cons_summ.index)
df_gst_for_json_read.columns = pd.MultiIndex.from_arrays([cols_second_level, df_gst_for_json_read.columns])
df_gst_for_json_read = pd.concat([df_gst_for_json_read, pd.DataFrame([[np.nan] * df_gst_for_json_read.shape[1]], columns=df_gst_for_json_read.columns)], ignore_index=True)
df_gst_for_json_read = pd.concat([df_gst_for_json_read, pd.DataFrame([[np.nan] * df_gst_for_json_read.shape[1]], columns=df_gst_for_json_read.columns)], ignore_index=True)
df_gst_for_json_read = pd.concat([df_gst_for_json_read, pd.DataFrame([[np.nan] * df_gst_for_json_read.shape[1]], columns=df_gst_for_json_read.columns)], ignore_index=True)
df_gst_for_json_read = pd.concat([df_gst_for_json_read, pd.DataFrame([[np.nan] * df_gst_for_json_read.shape[1]], columns=df_gst_for_json_read.columns)], ignore_index=True)

form_cons_data = [{"2020-July": "Household Survey CMIE Consumer Pyramid"} for i in df_gst_for_json_read.iloc[0,:]]
form_hh_data = [{"2020-July": "Household Survey CMIE Consumer Pyramid"} for i in df_gst_for_json_read.iloc[0,:]]

df_gst_for_json_read.loc[len(df_gst_for_json_read)]=form_hh_data
#df.loc[0, idx[:, ['b','c']]] = 12.3
idx = pd.IndexSlice
df_gst_for_json_read.loc[0, idx[:, df_gst_for_json_read.columns.levels[1][df_gst_for_json_read.columns.levels[1].str.startswith('CONS_')]]]="float"
df_gst_for_json_read.loc[1, :] = [df_gst_for_json_read.columns.levels[0][i] for i in df_gst_for_json_read.columns.labels[0]]
df_gst_for_json_read.columns = df_gst_for_json_read.columns.droplevel(0)
df_gst_for_json_read.loc[2, :] = df_gst_for_json_read.columns.str.replace('CONS_','CONSUMPTION OF ')
df_gst_for_json_read.iloc[3, :] = form_cons_data

df_gst_for_json_read.iloc[0,df_gst_for_json_read.columns.get_loc('TOTAL_EXPENDITURE')]= "float"
df_gst_for_json_read.iloc[1,df_gst_for_json_read.columns.get_loc('TOTAL_EXPENDITURE')]= "NONE"
df_gst_for_json_read.iloc[2,df_gst_for_json_read.columns.get_loc('TOTAL_EXPENDITURE')]= "Household Total Consumption"
df_gst_for_json_read.at[3,'TOTAL_EXPENDITURE'] = df_gst_for_json_read.at[4,'TOTAL_EXPENDITURE']

df_gst_for_json_read = df_gst_for_json_read.rename(columns={'WEIGHT': 'weight'})
df_gst_for_json_read.iloc[0,df_gst_for_json_read.columns.get_loc('weight')]= "float"
df_gst_for_json_read.iloc[1,df_gst_for_json_read.columns.get_loc('weight')]= "NONE"
df_gst_for_json_read.iloc[2,df_gst_for_json_read.columns.get_loc('weight')]= "Household unit sampling weight adjusted for Non-Response"
df_gst_for_json_read.at[3,'weight'] = df_gst_for_json_read.at[4,'weight']

#df_gst_for_json_read = df_gst_for_json_read.rename(columns={'WEIGHT0': 'weight0'})
df_gst_for_json_read.iloc[0,df_gst_for_json_read.columns.get_loc('WEIGHT0')]= "float"
df_gst_for_json_read.iloc[1,df_gst_for_json_read.columns.get_loc('WEIGHT0')]= "NONE"
df_gst_for_json_read.iloc[2,df_gst_for_json_read.columns.get_loc('WEIGHT0')]= "Household unit sampling weight unadjusted"
df_gst_for_json_read.at[3,'WEIGHT0'] = df_gst_for_json_read.at[4,'WEIGHT0']

df_gst_for_json_read.iloc[0,df_gst_for_json_read.columns.get_loc('ID_NO')]= "int"
df_gst_for_json_read.iloc[1,df_gst_for_json_read.columns.get_loc('ID_NO')]= "None"
df_gst_for_json_read.iloc[2,df_gst_for_json_read.columns.get_loc('ID_NO')]= "Household ID HHID"
df_gst_for_json_read.at[3,'ID_NO'] = df_gst_for_json_read.at[4,'ID_NO']

df_gst_for_json_read.iloc[0,df_gst_for_json_read.columns.get_loc('HH_SIZE')]= "int"
df_gst_for_json_read.iloc[1,df_gst_for_json_read.columns.get_loc('HH_SIZE')]= "None"
df_gst_for_json_read.iloc[2,df_gst_for_json_read.columns.get_loc('HH_SIZE')]= "Household Size"
df_gst_for_json_read.at[3,'HH_SIZE'] = df_gst_for_json_read.at[4,'HH_SIZE']

df_gst_for_json_read.iloc[0,df_gst_for_json_read.columns.get_loc('REGION_TYPE')]= "string"
df_gst_for_json_read.iloc[1,df_gst_for_json_read.columns.get_loc('REGION_TYPE')]= "None"
df_gst_for_json_read.iloc[2,df_gst_for_json_read.columns.get_loc('REGION_TYPE')]= "URBAN, RURAL"
df_gst_for_json_read.at[3,'TOTAL_EXPENDITURE'] = df_gst_for_json_read.at[4,'REGION_TYPE']

df_gst_for_json_read.iloc[0,df_gst_for_json_read.columns.get_loc('DISTRICT')]= "string"
df_gst_for_json_read.iloc[1,df_gst_for_json_read.columns.get_loc('DISTRICT')]= "None"
df_gst_for_json_read.iloc[2,df_gst_for_json_read.columns.get_loc('DISTRICT')]= "District Name"
df_gst_for_json_read.at[3,'DISTRICT'] = df_gst_for_json_read.at[4,'DISTRICT']

df_gst_for_json_read.iloc[0,df_gst_for_json_read.columns.get_loc('STATE')]= "string"
df_gst_for_json_read.iloc[1,df_gst_for_json_read.columns.get_loc('STATE')]= "None"
df_gst_for_json_read.iloc[2,df_gst_for_json_read.columns.get_loc('STATE')]= "State Name"
df_gst_for_json_read.at[3,'STATE'] = df_gst_for_json_read.at[4,'STATE']

df_gst_for_json_read.iloc[0,df_gst_for_json_read.columns.get_loc('STRATUM')]= "string"
df_gst_for_json_read.iloc[1,df_gst_for_json_read.columns.get_loc('STRATUM')]= "None"
df_gst_for_json_read.iloc[2,df_gst_for_json_read.columns.get_loc('STRATUM')]= "Strata Details; (HR)Homogenous Region(110 in number);Rural/Urban;(R)Rural,(VL)Very Large Town,(L)Large Town,(M)Medium Sized Town,(S)Small Town"
df_gst_for_json_read.at[3,'STRATUM'] = df_gst_for_json_read.at[4,'STRATUM']

df_gst_for_json_read.iloc[0,df_gst_for_json_read.columns.get_loc('ASSESSMENT_YEAR')]= "int"
df_gst_for_json_read.iloc[1,df_gst_for_json_read.columns.get_loc('ASSESSMENT_YEAR')]= "None"
df_gst_for_json_read.iloc[2,df_gst_for_json_read.columns.get_loc('ASSESSMENT_YEAR')]= "Year of Consumption"
df_gst_for_json_read.at[3,'ASSESSMENT_YEAR'] = df_gst_for_json_read.at[4,'ASSESSMENT_YEAR']


df_gst_for_json_read = df_gst_for_json_read[:-1]

df_gst_for_json_read['ind'] = "type"
df_gst_for_json_read.iloc[1, df_gst_for_json_read.columns.get_loc('ind')] = "category"
df_gst_for_json_read.iloc[2, df_gst_for_json_read.columns.get_loc('ind')] = "desc"
df_gst_for_json_read.iloc[3, df_gst_for_json_read.columns.get_loc('ind')] = "form"
df_gst_for_json_read.set_index('ind', inplace=True)
# Create json ditionary for read variables
dict_gst_read = df_gst_for_json_read.to_dict()

df_gst_for_json_calc = df_gst_for_json_read

calc_cols = df_gst_for_json_calc.columns[df_gst_for_json_calc.columns.str.startswith('CONS_')]
df_gst_for_json_calc = df_gst_for_json_calc[calc_cols]
calc_cols = calc_cols.str.replace('CONS_', 'gst_').str.lower()
df_gst_for_json_calc.columns = calc_cols
form_calc_data = [{"2020": "Calculated"} for i in df_gst_for_json_calc.iloc[0,:]]

df = pd.DataFrame(columns = calc_cols)
df1 = pd.concat([df, pd.DataFrame([[np.nan] *
                 len(calc_cols)], columns=calc_cols)], ignore_index=True)
df1.iloc[0,:] = "float"
df1 = pd.concat([df1, pd.DataFrame([[np.nan] *
                 len(calc_cols)], columns=calc_cols)], ignore_index=True)
df1.loc[1,:] = cons_category
df1 = pd.concat([df1, pd.DataFrame([[np.nan] *
                 len(calc_cols)], columns=calc_cols)], ignore_index=True)
cols = df1.columns.str.upper()
df1.iloc[2,:] = cols.str.replace('GST_','GST paid by Household on consumption of ')
df1 = pd.concat([df1, pd.DataFrame([[np.nan] *
                 len(calc_cols)], columns=calc_cols)], ignore_index=True)
df1.iloc[3,:] = form_calc_data

df2 = pd.DataFrame({'ind':["type", "category", "desc", "form"],
                   'total_consumption_food':["float", "None", "Total Consumption inclusive of GST by Household on Food during the month in Rupees", {"2020": "Calculated"}],
                   'total_consumption_non_food':["float", "None", "Total Consumption inclusive of GST by Household on Non-Food during the month in Rupees", {"2020": "Calculated"}],
                   'total_consumption':["float", "None", "Total Consumption inclusive of GST by Household during the month in Rupees", {"2020": "Calculated"}],                   
                   'total_consumption_education':["float", "None", "Total Consumption inclusive of GST by Household on Education during the month in Rupees", {"2020": "Calculated"}],
                   'total_consumption_health':["float", "None", "Total Consumption inclusive of GST by Household on Health during the month in Rupees", {"2020": "Calculated"}],
                   'gst_food':["float","None", "Potential GST paid by Household during the month on Food in Rupees", {"2020": "Calculated"}],
                   'gst_non_food':["float","None", "Potential GST paid by Household during the month on Non-Food in Rupees", {"2020": "Calculated"}],                
                   'gst_education':["float","None", "Potential GST paid by Household during the month on Education in Rupees", {"2020": "Calculated"}],
                   'gst_health':["float","None", "Potential GST paid by Household during the month on Health in Rupees", {"2020": "Calculated"}],
                   'gst':["float","None", "Potential GST paid by Household during the month in Rupees", {"2020": "Calculated"}]})

df_gst_for_json_calc = pd.concat([df1,df2], axis=1)
df_gst_for_json_calc.set_index('ind', inplace=True)
# Create json ditionary for calc variables
dict_gst_calc = df_gst_for_json_calc.to_dict()

# Merging the two dictionary along with adding "read" and "calc" 
dict_gst_rec = {"read": dict_gst_read, "calc": dict_gst_calc}

# Pretty Print dictionary into json file
with open("gstrecords_variables_cmie.json", "w") as f:
    json.dump(dict_gst_rec, f, indent=4, sort_keys=True)
    
