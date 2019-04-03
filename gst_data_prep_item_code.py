import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


df_cons_cereal_full = pd.read_stata('Consumption of cereals-pulses- milk and milk products  during the last 30 days  - Block 5.1- 5.dta')
print(df_cons_cereal_full.dtypes)
df_cons_cereal_full.to_csv('consumer_expend_cereal_2011.csv')

df_cons_cereal_all = df_cons_cereal_full[["Item_Code", "Home_Produce_Quantity",
                                          "Home_Produce_Value", "HHID",
                                          "Total_Consumption_Quantity",
                                          "Total_Consumption_Value"]]
df_cons_cereal_all.to_csv('consumer_expend_cereal_2011_short.csv', index=False)

df_cons_cereal_all['Purchased_Consumption_Quantity'] = (df_cons_cereal_all['Total_Consumption_Quantity'] -
                                                        df_cons_cereal_all['Home_Produce_Quantity'])
df_cons_cereal_all['Purchased_Consumption_Value'] = (df_cons_cereal_all['Total_Consumption_Value'] -
                                                     df_cons_cereal_all['Home_Produce_Value'])
df_cons_cereal_all = df_cons_cereal_all[["Item_Code", "Purchased_Consumption_Quantity", "Purchased_Consumption_Value", "HHID"]]
df_cons_cereal_all.to_csv('consumer_expend_cereal_2011_short1.csv', index=False)
"""
household_bl3_l2_file = "Household Characteristics - Block 3 -  Level 2 -  68.dta"
df_hh_bl3_l2_data = pd.read_stata(household_bl3_l2_file, preserve_dtypes=False)
print(df_hh_bl3_l2_data.dtypes)
df_hh_bl3_l2_data.to_csv('hh_characteristics_block3_level2_2011.csv', index=False)

df_hh_bl3_l2_data["URBAN"] = np.where(df_hh_bl3_l2_data["Sector"] == 2,
                                      1, 0)
df_hh_bl3_l2_short = df_hh_bl3_l2_data[['HHID', 'HH_Size', 'URBAN',
                                       'District', 'State_code', 'Combined_multiplier']]
df_hh_bl3_l2_short.to_csv('hh_characteristics_block3_level2_2011_short.csv')

# household_bl3_l3_file = "Household characteristics - Block 3 - Level 3.dta"
# df_hh_bl3_l3_data = pd.read_stata(household_bl3_l3_file, preserve_dtypes=False)
# print(df_hh_bl3_l3_data.dtypes)
# df_hh_bl3_l3_data.to_csv('hh_characteristics_block3_level3_2011.csv')
# df_hh_bl3_l3_short = df_hh_bl3_l3_data[['HHID', 'HH_Size',
#                                  'Combined_multiplier']]
"""

df_hh_bl3_l2_short = pd.read_csv('hh_characteristics_block3_level2_2011_short.csv')
df_hh_bl3_l2_short = df_hh_bl3_l2_short.drop('Unnamed: 0', axis=1)
df_cons_cereal_all = pd.read_csv('consumer_expend_cereal_2011_short1.csv')


# df_survey_mpc = df_cons_summ_all[df_cons_summ_all["Srl_no"] == 49]
# df_survey_mpc.index = pd.RangeIndex(len(df_survey_mpc.index))
# df_survey_mpc = df_survey_mpc.drop(df_survey_mpc.columns[0], axis = 1)
# sns.distplot(tuple(df_survey_mpc['Value']), hist = False, kde = True,
#             kde_kws = {'linewidth': 3},
#             label = "consumption")

# df_rates = pd.read_csv('GST Rates India 2019-work.csv', encoding='cp1252')
df_rates = pd.read_csv('GST Rates India 2019-work.csv')
df_item_rates = df_rates[['item_code', 'item_category_1', 'duration', 'gst_rate']]
df_item_rates['item_code'] = 'item_' + df_item_rates['item_code']

# df_item_rates_category.sort_values('Srl_no')
"""
Generate JSON File for Policy by looping through the variables
"""
df_item_rates_for_json = df_item_rates.pivot(columns='item_code', values='gst_rate')
df_item_rates_for_json.iloc[0,:]=df_item_rates_for_json[df_item_rates_for_json.columns].max()
df_item_rates_for_json = df_item_rates_for_json.iloc[0:1,:]
df_item_rates_for_json.columns= "_gst_rate_" + df_item_rates_for_json.columns
for i in range(0,17):
   df_item_rates_for_json = pd.concat([df_item_rates_for_json, pd.DataFrame([[np.nan] *
                                      df_item_rates_for_json.shape[1]], columns=df_item_rates_for_json.columns)], ignore_index=True)
 
#df_item_rates_for_json.iloc[13,:] = '['+ str(df_item_rates_for_json.iloc[0,:]) + ']'

df_item_rates_for_json.iloc[13,:] = df_item_rates_for_json.iloc[0,:]/100
d = [[i] for i in df_item_rates_for_json.iloc[13,:]]
df_item_rates_for_json.loc[len(df_item_rates_for_json)]=d
df_item_rates_for_json.iloc[13,:] = df_item_rates_for_json.iloc[18,:]
df_item_rates_for_json = df_item_rates_for_json[:-1]

df_item_rates_for_json.iloc[0,:] = df_item_rates_for_json.columns.str.replace('_gst_rate_','GST Rate for ')
df_item_rates_for_json.iloc[1,:] = df_item_rates_for_json.columns.str.replace('_gst_rate_','GST Rate relevant for consumption of ')
df_item_rates_for_json.iloc[2,:] = "GST Rules"
df_item_rates_for_json.iloc[3,:] = ""
df_item_rates_for_json.iloc[4,:] = "AYEAR"
df_item_rates_for_json.iloc[5,:] = '["2017"]'
df_item_rates_for_json.iloc[6,:] = 2017
df_item_rates_for_json.iloc[7,:] = False
df_item_rates_for_json.iloc[8,:] = False
df_item_rates_for_json.iloc[9,:] = ""
df_item_rates_for_json.iloc[10,:] = ""
df_item_rates_for_json.iloc[11,:] = False
df_item_rates_for_json.iloc[12,:] = False
df_item_rates_for_json.iloc[14,:] = '{"min": 0, "max": 1}'
df_item_rates_for_json.iloc[15,:] = ""
df_item_rates_for_json.iloc[16,:] = ""
df_item_rates_for_json.iloc[17,:] = "stop"

d=[0.18]
df_item_rates_for_json['gst_rate_benchmark']= ""
df_item_rates_for_json.iloc[0,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= "GST Benchmark Rate"
df_item_rates_for_json.iloc[1,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= "GST Benchmark Rate to calculate Policy Gap"
df_item_rates_for_json.iloc[2,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= "Benchmark Rate"
df_item_rates_for_json.iloc[3,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= ""
df_item_rates_for_json.iloc[4,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= "AYEAR"
df_item_rates_for_json.iloc[5,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= '["2017"]'
df_item_rates_for_json.iloc[6,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= 2017
df_item_rates_for_json.iloc[7,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= False
df_item_rates_for_json.iloc[8,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= False
df_item_rates_for_json.iloc[9,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= ""
df_item_rates_for_json.iloc[10,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= ""
df_item_rates_for_json.iloc[11,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= False
df_item_rates_for_json.iloc[12,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= False
df_item_rates_for_json.iloc[13,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= d
df_item_rates_for_json.iloc[14,df_item_rates_for_json.columns.get_loc('gst_rate_benchmark')]= '{"min": 0, "max": 1}'
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
df_item_rates_for_json.to_json('gst_policy1.json')

"""
Generate gst.csv which contains consumption information from Summary table 
Block 12 - One record for each household  
"""
df_cons_summ = df_cons_summ_all[['HHID','Srl_no','Value']]

df_cons_summ = pd.merge(df_cons_summ, df_item_rates_category,
                            how="inner", on="Srl_no")
"""
Adjusting monthly consumption to yearly consumption for 
certian items of monthly recall period
"""
df_cons_summ['Value'] = np.where(df_cons_summ['duration']=="monthly",
                                 df_cons_summ['Value']*(365/30),
                                 df_cons_summ['Value'])

"""
Gross Private Final Consumption Expenditure in 2011 and in 
Assessment Year 2017 or financial year 2016 - 
Source: Annual Estimate of GDP at Current Prices base 2011-12 
Ministry of Statistics and Program Implementation MOSPI
mospi.nic.in/data
"""

HHS_TOTAL_WEIGHT = 2210659 
GPFCE_2011 = 4910447
GPFCE_2016 = 9004904
GPFCE_2017 = 10083000
GPFCE_2018 = 11333000
INFLATOR_2011 = (GPFCE_2011/HHS_TOTAL_WEIGHT)
"""
Extraploating 2011 data to assessment year 2017
"""
#df_cons_summ['Value'] = df_cons_summ['Value'] * (GPFCE_2016/GPFCE_2011)
df_cons_summ['Value'] = df_cons_summ['Value'] * INFLATOR_2011
df_cons_summ['Value'] = df_cons_summ['Value'] * (GPFCE_2016/GPFCE_2011)


df_cons_summ['item_category_1'] = "cons_" + df_cons_summ['item_category_1']

df_cons_summ_trans = df_cons_summ.pivot(index='HHID', columns='item_category_1', values='Value')

df_cons_summ_trans = df_cons_summ_trans.fillna(0)

df_cons_summ_trans = df_cons_summ_trans.reset_index()

df_cons_summ_trans = pd.merge(df_cons_summ_trans, df_hh_bl3_l2_short,
                              how="inner", on="HHID")
df_cons_summ_trans.columns = df_cons_summ_trans.columns.str.upper()

df_cons_summ_trans = df_cons_summ_trans.rename(columns={'HHID': 'ID_NO'})
df_cons_summ_trans = df_cons_summ_trans.rename(columns={'COMBINED_MULTIPLIER': 'WEIGHT'})
df_cons_summ_trans['ASSESSMENT_YEAR'] = 2017
# df_cons_summ_trans['CONS_OTHER'] = df_cons_summ_trans[df_cons_summ_trans.columns[df_cons_summ_trans.columns.str.startswith('CONS_')]].sum(axis=1)
# df_cons_summ_trans['CONS_OTHER'] = df_cons_summ_trans['CONS_OTHER'] - df_cons_summ_trans['CONS_CEREAL']
df_cons_summ_trans.to_csv('gst.csv', index=False)

"""
Generate JSON File for the gst record variables which declares all variables
used in gst.csv
"""
df_gst_for_json_read = df_cons_summ_trans.drop(df_cons_summ_trans.index)
df_gst_for_json_read = pd.concat([df_gst_for_json_read, pd.DataFrame([[np.nan] * df_gst_for_json_read.shape[1]], columns=df_gst_for_json_read.columns)], ignore_index=True)
df_gst_for_json_read = pd.concat([df_gst_for_json_read, pd.DataFrame([[np.nan] * df_gst_for_json_read.shape[1]], columns=df_gst_for_json_read.columns)], ignore_index=True)
df_gst_for_json_read = pd.concat([df_gst_for_json_read, pd.DataFrame([[np.nan] * df_gst_for_json_read.shape[1]], columns=df_gst_for_json_read.columns)], ignore_index=True)

df_gst_for_json_calc = df_gst_for_json_read

df_gst_for_json_read.loc[0, df_gst_for_json_read.columns.str.startswith('CONS_')]="float"
df_gst_for_json_read.loc[1, :] = df_gst_for_json_read.columns.str.replace('CONS_','CONSUMPTION OF ')
df_gst_for_json_read.iloc[2, :] ='{"2017": "Household Survey 48th Round Block 12"}'

df_gst_for_json_read = df_gst_for_json_read.rename(columns={'WEIGHT': 'weight'})
df_gst_for_json_read.iloc[0,df_gst_for_json_read.columns.get_loc('weight')]= "float"
df_gst_for_json_read.iloc[1,df_gst_for_json_read.columns.get_loc('weight')]= "Household unit sampling weight"
df_gst_for_json_read.iloc[2,df_gst_for_json_read.columns.get_loc('weight')]= '{"2017": "not used in filing unit tax calculations"}'

df_gst_for_json_read.iloc[0,df_gst_for_json_read.columns.get_loc('ID_NO')]= "int"
df_gst_for_json_read.iloc[1,df_gst_for_json_read.columns.get_loc('ID_NO')]= "Household ID HHID"
df_gst_for_json_read.iloc[0,df_gst_for_json_read.columns.get_loc('HH_SIZE')]= "int"
df_gst_for_json_read.iloc[1,df_gst_for_json_read.columns.get_loc('HH_SIZE')]= "Household Size"
df_gst_for_json_read.iloc[2,df_gst_for_json_read.columns.get_loc('HH_SIZE')]= '{"2017": "Household Survey 48th Round Block 3 Level 2"}'

df_gst_for_json_read.iloc[0,df_gst_for_json_read.columns.get_loc('URBAN')]= "int"
df_gst_for_json_read.iloc[1,df_gst_for_json_read.columns.get_loc('URBAN')]= "URBAN=1, RURAL=0"
df_gst_for_json_read.iloc[2,df_gst_for_json_read.columns.get_loc('URBAN')]= '{"2017": "Household Survey 48th Round Block 3 Level 2"}'

df_gst_for_json_read.iloc[0,df_gst_for_json_read.columns.get_loc('DISTRICT')]= "int"
df_gst_for_json_read.iloc[1,df_gst_for_json_read.columns.get_loc('DISTRICT')]= "District Code"
df_gst_for_json_read.iloc[2,df_gst_for_json_read.columns.get_loc('DISTRICT')]= '{"2017": "Household Survey 48th Round Block 3 Level 2"}'

df_gst_for_json_read.iloc[0,df_gst_for_json_read.columns.get_loc('STATE_CODE')]= "int"
df_gst_for_json_read.iloc[1,df_gst_for_json_read.columns.get_loc('STATE_CODE')]= "State Code"
df_gst_for_json_read.iloc[2,df_gst_for_json_read.columns.get_loc('STATE_CODE')]= '{"2017": "Household Survey 48th Round Block 3 Level 2"}'

df_gst_for_json_read.iloc[0,df_gst_for_json_read.columns.get_loc('ASSESSMENT_YEAR')]= "int"
df_gst_for_json_read.iloc[1,df_gst_for_json_read.columns.get_loc('ASSESSMENT_YEAR')]= "Year of Consumption"
df_gst_for_json_read.iloc[2,df_gst_for_json_read.columns.get_loc('ASSESSMENT_YEAR')]= '{"2017": "Household Survey 48th Round Block 3 Level 2"}'

df_gst_for_json_read['ind'] = "type"
df_gst_for_json_read.iloc[1, df_gst_for_json_read.columns.get_loc('ind')] = "desc"
df_gst_for_json_read.iloc[2, df_gst_for_json_read.columns.get_loc('ind')] = "form"
df_gst_for_json_read.set_index('ind', inplace=True)
df_gst_for_json_read.to_json('gst_read_rec.json')

calc_cols = df_gst_for_json_calc.columns[df_gst_for_json_calc.columns.str.startswith('CONS_')]
df_gst_for_json_calc = df_gst_for_json_calc[calc_cols]
calc_cols = calc_cols.str.replace('CONS_', 'gst_').str.lower()
df_gst_for_json_calc.columns = calc_cols


df_gst_for_json_calc.iloc[0, :] = "float"
df_gst_for_json_calc.iloc[1, :] = df_gst_for_json_calc.columns.str.replace('gst_','GST Collection from ')
df_gst_for_json_calc.iloc[2, :] ='{"2017": "Calculated"}'

df_gst_for_json_calc['total consumption']= "float"
df_gst_for_json_calc.iloc[1, df_gst_for_json_calc.columns.get_loc('total consumption')]= "Total Consumption of Household"
df_gst_for_json_calc.iloc[2, df_gst_for_json_calc.columns.get_loc('total consumption')]= '{"2017": "Calculated"}'

df_gst_for_json_calc['gst']= "float"
df_gst_for_json_calc.iloc[1, df_gst_for_json_calc.columns.get_loc('gst')]= "Potential Collection of GST paid by Household"
df_gst_for_json_calc.iloc[2, df_gst_for_json_calc.columns.get_loc('gst')]= '{"2017": "Calculated"}'

df_gst_for_json_calc['ind'] = "type"
df_gst_for_json_calc.iloc[1, df_gst_for_json_calc.columns.get_loc('ind')] = "desc"
df_gst_for_json_calc.iloc[2, df_gst_for_json_calc.columns.get_loc('ind')] = "form"
df_gst_for_json_calc.set_index('ind', inplace=True)
df_gst_for_json_calc.to_json('gst_calc_rec.json')









# df_survey = pd.read_csv('consumer_expenditure_summary_2011.csv', encoding='cp1252', engine='python')
# df_survey = pd.read_csv('consumer_summary_expenditure_2011.csv', encoding='cp1252', engine='python')
