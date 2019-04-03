"""
This script prepares the panel data for 2013-2015 to be used for 2017-2019.

We assume that aggregate totals have already been calcuated for the full data.
They must be saved in some form, and we will store them in agg_results.

For now, we produce the sample weight and blow-up factors for the entire sample.
A subsequent improvement should produce aggregate results by industry/sector,
and produce weights and blow-up factors by industry/sector.

We may also want to consider weight adjustments to target other results, such
as totals for other measures and the distribution of firm sizes.

We also apply a process for organically advancing 2013 losses carried forward.
"""

import pandas as pd
import numpy as np
import copy

# Get full panel data
data_full = pd.read_excel('ITR6_2017_2013_BAL_PANEL_FINAL.xlsx',
                          sheet_name='Sheet2')

# Rename some variables
renames = {'SHORT_TERM_15PER': 'ST_CG_AMT_1', 'SHORT_TERM_30PER': 'ST_CG_AMT_2',
           'LONG_TERM_10PER': 'LT_CG_AMT_1', 'LONG_TERM_20PER': 'LT_CG_AMT_2',
           'SHORT_TERM_APPRATE': 'ST_CG_AMT_APPRATE',
           'TOTAL_INCOME_ALL':'GTI_BEFORE_LOSSES', 'PAN_NO_HASH': 'ID_NO',
           'AY_0910_AMT_AMT_LOSS_BUSOTHSPL': 'AY_0910_AMT_LOSS_BUSOTHSPL'}
data_full = data_full.rename(renames, axis=1)
data_full = data_full.fillna(0)

data_full['ST_CG_AMT_1'] = np.where(data_full.ASSESSMENT_YEAR == 2013,
         np.maximum(data_full['STCG_SEC111A'], 0.), data_full['ST_CG_AMT_1'])
data_full['ST_CG_AMT_2'] = np.where(data_full.ASSESSMENT_YEAR == 2013,
         np.maximum(data_full['STCG_OTHERS'], 0.), data_full['ST_CG_AMT_2'])
data_full['LT_CG_AMT_1'] = np.where(data_full.ASSESSMENT_YEAR == 2013,
         np.maximum(data_full['LTCG_NO_INDEXATION'], 0.), data_full['LT_CG_AMT_1'])
data_full['LT_CG_AMT_2'] = np.where(data_full.ASSESSMENT_YEAR == 2013,
         np.maximum(data_full['LTCG_INDEXATION'], 0.), data_full['LT_CG_AMT_2'])


"""
The following code (commented out) is a temporary fix for strange observations
on capital gains.

stcg1 = np.array(data_full.ST_CG_AMT_1)
stcg2 = np.array(data_full.ST_CG_AMT_2)
stcg3 = np.array(data_full.ST_CG_AMT_APPRATE)
stcgT = np.array(data_full.TOTAL_SCTG)
ltcg1 = np.array(data_full.LT_CG_AMT_1)
ltcg2 = np.array(data_full.LT_CG_AMT_2)
ltcgT = np.array(data_full.TOTAL_LTCG)
stcg_miss = stcgT - stcg1 - stcg2 - stcg3
ltcg_miss = ltcgT - ltcg1 - ltcg2
data_full['ST_CG_AMT_1'] = data_full['ST_CG_AMT_1'] + 0.5 * stcg_miss
data_full['ST_CG_AMT_2'] = data_full['ST_CG_AMT_2'] + 0.5 * stcg_miss
data_full['LT_CG_AMT_1'] = data_full['LT_CG_AMT_1'] + 0.5 * ltcg_miss
data_full['LT_CG_AMT_2'] = data_full['LT_CG_AMT_2'] + 0.5 * ltcg_miss
"""



data13 = data_full[data_full.ASSESSMENT_YEAR == 2013].reset_index()
data14 = data_full[data_full.ASSESSMENT_YEAR == 2014].reset_index()
data15 = data_full[data_full.ASSESSMENT_YEAR == 2015].reset_index()
data16 = data_full[data_full.ASSESSMENT_YEAR == 2016].reset_index()




"""
The following code handles the losses.
"""
# Create empty loss variables
loss_lag8 = np.zeros(len(data13))
loss_lag7 = np.zeros(len(data13))
loss_lag6 = np.zeros(len(data13))
loss_lag5 = np.zeros(len(data13))
loss_lag4 = np.zeros(len(data13))
loss_lag3 = np.zeros(len(data13))
loss_lag2 = np.zeros(len(data13))
loss_lag1 = np.zeros(len(data13))

def get_loss_type(year, lagnum, losstype):
    """
    Returns an array of the given loss type with the appropriate lag from the
    given year.
    """
    loss = np.zeros(len(data_full))
    lagyear = year - lagnum
    if lagyear < 2007:
        loss = np.zeros(len(data_full))
    elif lagyear == 2007:
        loss = np.array(data_full['AY_0708_AMT_LOSS_' + losstype])
    elif lagyear == 2008:
        loss = np.array(data_full['AY_0809_AMT_LOSS_' + losstype])
    elif lagyear == 2009:
        loss = np.array(data_full['AY_0910_AMT_LOSS_' + losstype])
    elif lagyear == 2010:
        loss = np.array(data_full['AY_1011_AMT_LOSS_' + losstype])
    elif lagyear == 2011:
        loss = np.array(data_full['AY_1112_AMT_LOSS_' + losstype])
    elif lagyear == 2012:
        loss = np.array(data_full['AY_1213_AMT_LOSS_' + losstype])
    elif lagyear == 2013:
        loss = np.array(data_full['AY_1314_AMT_LOSS_' + losstype])
    elif lagyear == 2014:
        loss = np.array(data_full['AY_1415_AMT_LOSS_' + losstype])
    else:
        loss = np.zeros(len(data_full))
    loss2 = loss[data_full.ASSESSMENT_YEAR == year]
    return loss2

losstypelist = ['HPL', 'BUSOTHSPL', 'LSPCLTVBUS', 'LSPCFDBUS', 'STCL', 'LTCL',
                'OSLHR']

# Produce the loss lags for 2013
for losstype in losstypelist:
    loss_lag1 += get_loss_type(2013, 1, losstype)
    loss_lag2 += get_loss_type(2013, 2, losstype)
    loss_lag3 += get_loss_type(2013, 3, losstype)
    loss_lag4 += get_loss_type(2013, 4, losstype)
    loss_lag5 += get_loss_type(2013, 5, losstype)
    loss_lag6 += get_loss_type(2013, 6, losstype)
    loss_lag7 += get_loss_type(2013, 7, losstype)
    loss_lag8 += get_loss_type(2013, 8, losstype)


def calc_new_lags(dat):
    """
    Calculates the new lags
    """
    LOSS_LAGS = [dat.LOSS_LAG1, dat.LOSS_LAG2, dat.LOSS_LAG3, dat.LOSS_LAG4,
                 dat.LOSS_LAG5, dat.LOSS_LAG6, dat.LOSS_LAG7, dat.LOSS_LAG8]
    PRFT_GAIN_BP_INC_115BBF = np.zeros(len(dat))
    Income_BP = (dat.PRFT_GAIN_BP_OTHR_SPECLTV_BUS + dat.PRFT_GAIN_BP_SPECLTV_BUS +
                 dat.PRFT_GAIN_BP_SPCFD_BUS + PRFT_GAIN_BP_INC_115BBF)
    GTI_Before_Loss = (dat.INCOME_HP + Income_BP + dat.ST_CG_AMT_1 + dat.ST_CG_AMT_2 +
                       dat.ST_CG_AMT_APPRATE + dat.LT_CG_AMT_1 + dat.LT_CG_AMT_2 +
                       dat.TOTAL_INCOME_OS)
    CY_Losses = np.array(dat['CYL_SET_OFF'])
    GTI1 = np.maximum(GTI_Before_Loss - CY_Losses, 0.)
    newloss1 = GTI1 - GTI_Before_Loss + CY_Losses
    USELOSS = [np.zeros(len(dat))] * 8
    for i in range(8, 0, -1):
        USELOSS[i-1] = np.minimum(GTI1, LOSS_LAGS[i-1])
        GTI1 = GTI1 - USELOSS[i-1]
    dat['newloss1'] = newloss1
    dat['newloss2'] = LOSS_LAGS[0] - USELOSS[0]
    dat['newloss3'] = LOSS_LAGS[1] - USELOSS[1]
    dat['newloss4'] = LOSS_LAGS[2] - USELOSS[2]
    dat['newloss5'] = LOSS_LAGS[3] - USELOSS[3]
    dat['newloss6'] = LOSS_LAGS[4] - USELOSS[4]
    dat['newloss7'] = LOSS_LAGS[5] - USELOSS[5]
    dat['newloss8'] = LOSS_LAGS[6] - USELOSS[6]
    return(dat)


data13['LOSS_LAG1'] = loss_lag1
data13['LOSS_LAG2'] = loss_lag2
data13['LOSS_LAG3'] = loss_lag3
data13['LOSS_LAG4'] = loss_lag4
data13['LOSS_LAG5'] = loss_lag5
data13['LOSS_LAG6'] = loss_lag6
data13['LOSS_LAG7'] = loss_lag7
data13['LOSS_LAG8'] = loss_lag8
data13c = calc_new_lags(data13)


carryforward_df = pd.DataFrame({'ID_NO': data13c.ID_NO,
                                'newloss1': data13c.newloss1,
                                'newloss2': data13c.newloss2,
                                'newloss3': data13c.newloss3,
                                'newloss4': data13c.newloss4,
                                'newloss5': data13c.newloss5,
                                'newloss6': data13c.newloss6,
                                'newloss7': data13c.newloss7,
                                'newloss8': data13c.newloss8})
# Update loss lags for 2014 data
data14a = data14.merge(right=carryforward_df, how='outer', on='ID_NO', indicator=True)
merge_info = np.array(data14a['_merge'])
to_update = np.where(merge_info == 'both', True, False)
to_keep = np.where(merge_info != 'right_only', True, False)
data14a['LOSS_LAG1'] = np.where(to_update, data14a['newloss1'], 0)
data14a['LOSS_LAG2'] = np.where(to_update, data14a['newloss2'], 0)
data14a['LOSS_LAG3'] = np.where(to_update, data14a['newloss3'], 0)
data14a['LOSS_LAG4'] = np.where(to_update, data14a['newloss4'], 0)
data14a['LOSS_LAG5'] = np.where(to_update, data14a['newloss5'], 0)
data14a['LOSS_LAG6'] = np.where(to_update, data14a['newloss6'], 0)
data14a['LOSS_LAG7'] = np.where(to_update, data14a['newloss7'], 0)
data14a['LOSS_LAG8'] = np.where(to_update, data14a['newloss8'], 0)
data14b = data14a[to_keep].reset_index()
data14c = calc_new_lags(data14b)

# Repeat for 2015
carryforward_df = pd.DataFrame({'ID_NO': data14c.ID_NO,
                                'newloss1': data14c.newloss1,
                                'newloss2': data14c.newloss2,
                                'newloss3': data14c.newloss3,
                                'newloss4': data14c.newloss4,
                                'newloss5': data14c.newloss5,
                                'newloss6': data14c.newloss6,
                                'newloss7': data14c.newloss7,
                                'newloss8': data14c.newloss8})
# Update loss lags for 2015 data
data15a = data15.merge(right=carryforward_df, how='outer', on='ID_NO', indicator=True)
merge_info = np.array(data15a['_merge'])
to_update = np.where(merge_info == 'both', True, False)
to_keep = np.where(merge_info != 'right_only', True, False)
data15a['LOSS_LAG1'] = np.where(to_update, data15a['newloss1'], 0)
data15a['LOSS_LAG2'] = np.where(to_update, data15a['newloss2'], 0)
data15a['LOSS_LAG3'] = np.where(to_update, data15a['newloss3'], 0)
data15a['LOSS_LAG4'] = np.where(to_update, data15a['newloss4'], 0)
data15a['LOSS_LAG5'] = np.where(to_update, data15a['newloss5'], 0)
data15a['LOSS_LAG6'] = np.where(to_update, data15a['newloss6'], 0)
data15a['LOSS_LAG7'] = np.where(to_update, data15a['newloss7'], 0)
data15a['LOSS_LAG8'] = np.where(to_update, data15a['newloss8'], 0)
data15b = data15a[to_keep].reset_index()
data15c = calc_new_lags(data15b)

# Repeat for 2016
carryforward_df = pd.DataFrame({'ID_NO': data15c.ID_NO,
                                'newloss1': data15c.newloss1,
                                'newloss2': data15c.newloss2,
                                'newloss3': data15c.newloss3,
                                'newloss4': data15c.newloss4,
                                'newloss5': data15c.newloss5,
                                'newloss6': data15c.newloss6,
                                'newloss7': data15c.newloss7,
                                'newloss8': data15c.newloss8})
# Update loss lags for 2016 data
data16a = data16.merge(right=carryforward_df, how='outer', on='ID_NO', indicator=True)
merge_info = np.array(data16a['_merge'])
to_update = np.where(merge_info == 'both', True, False)
to_keep = np.where(merge_info != 'right_only', True, False)
data16a['LOSS_LAG1'] = np.where(to_update, data16a['newloss1'], 0)
data16a['LOSS_LAG2'] = np.where(to_update, data16a['newloss2'], 0)
data16a['LOSS_LAG3'] = np.where(to_update, data16a['newloss3'], 0)
data16a['LOSS_LAG4'] = np.where(to_update, data16a['newloss4'], 0)
data16a['LOSS_LAG5'] = np.where(to_update, data16a['newloss5'], 0)
data16a['LOSS_LAG6'] = np.where(to_update, data16a['newloss6'], 0)
data16a['LOSS_LAG7'] = np.where(to_update, data16a['newloss7'], 0)
data16a['LOSS_LAG8'] = np.where(to_update, data16a['newloss8'], 0)
data16b = data16a[to_keep].reset_index()
data16c = calc_new_lags(data16b)

# Extract the losses to be carried forward into 2017, and update the 2013 data
carryforward_df = pd.DataFrame({'ID_NO': data16c.ID_NO,
                                'ASSESSMENT_YEAR': 2013,
                                'newloss1': data16c.newloss1,
                                'newloss2': data16c.newloss2,
                                'newloss3': data16c.newloss3,
                                'newloss4': data16c.newloss4,
                                'newloss5': data16c.newloss5,
                                'newloss6': data16c.newloss6,
                                'newloss7': data16c.newloss7,
                                'newloss8': data16c.newloss8})
data13['LOSS_LAG1'] = loss_lag1
data13['LOSS_LAG2'] = loss_lag2
data13['LOSS_LAG3'] = loss_lag3
data13['LOSS_LAG4'] = loss_lag4
data13['LOSS_LAG5'] = loss_lag5
data13['LOSS_LAG6'] = loss_lag6
data13['LOSS_LAG7'] = loss_lag7
data13['LOSS_LAG8'] = loss_lag8
data13a = data13.merge(right=carryforward_df, how='outer', on='ID_NO', indicator=True)
merge_info = np.array(data13a['_merge'])
to_update = np.where(merge_info == 'both', True, False)
to_keep = np.where(merge_info != 'right_only', True, False)
data13a['LOSS_LAG1'] = np.where(to_update, data13a['newloss1_y'], data13a['LOSS_LAG1'])
data13a['LOSS_LAG2'] = np.where(to_update, data13a['newloss2_y'], data13a['LOSS_LAG2'])
data13a['LOSS_LAG3'] = np.where(to_update, data13a['newloss3_y'], data13a['LOSS_LAG3'])
data13a['LOSS_LAG4'] = np.where(to_update, data13a['newloss4_y'], data13a['LOSS_LAG4'])
data13a['LOSS_LAG5'] = np.where(to_update, data13a['newloss5_y'], data13a['LOSS_LAG5'])
data13a['LOSS_LAG6'] = np.where(to_update, data13a['newloss6_y'], data13a['LOSS_LAG6'])
data13a['LOSS_LAG7'] = np.where(to_update, data13a['newloss7_y'], data13a['LOSS_LAG7'])
data13a['LOSS_LAG8'] = np.where(to_update, data13a['newloss8_y'], data13a['LOSS_LAG8'])

dataf1 = data_full.merge(right=carryforward_df, how='outer', on=['ID_NO', 'ASSESSMENT_YEAR'], indicator=True)
merge_info = np.array(dataf1['_merge'])
to_update = np.where(merge_info == 'both', True, False)
to_keep = np.where(merge_info != 'right_only', True, False)
dataf1['LOSS_LAG1'] = np.where(to_update, dataf1.newloss1, 0)
dataf1['LOSS_LAG2'] = np.where(to_update, dataf1.newloss2, 0)
dataf1['LOSS_LAG3'] = np.where(to_update, dataf1.newloss3, 0)
dataf1['LOSS_LAG4'] = np.where(to_update, dataf1.newloss4, 0)
dataf1['LOSS_LAG5'] = np.where(to_update, dataf1.newloss5, 0)
dataf1['LOSS_LAG6'] = np.where(to_update, dataf1.newloss6, 0)
dataf1['LOSS_LAG7'] = np.where(to_update, dataf1.newloss7, 0)
dataf1['LOSS_LAG8'] = np.where(to_update, dataf1.newloss8, 0)
dataf1.drop(['newloss1', 'newloss2', 'newloss3', 'newloss4', 'newloss5',
             'newloss6', 'newloss7', 'newloss8', '_merge'], axis=1, inplace=True)
data_full = dataf1[to_keep].reset_index()
data_full.drop(['index'], axis=1, inplace=True)



"""
The following code deals with the calculation of blow-up factors.
The blow-up factors are calculated to match 2013 results to 2017 results, with
2017 results calculated from the complete data and 2013 from the sample.

For subsequent years, we can either use the natural growth process that
occurred beginning in 2013 or use the growthfactors specified in
pitaxcalc-demo. To use the latter, set match_gfactors to True.
"""

match_gfactors = True

# Separate the datasets
data13 = data_full[data_full['ASSESSMENT_YEAR'] == 2013].reset_index()
data14 = data_full[data_full['ASSESSMENT_YEAR'] == 2014].reset_index()
data15 = data_full[data_full['ASSESSMENT_YEAR'] == 2015].reset_index()
data16 = data_full[data_full['ASSESSMENT_YEAR'] == 2016].reset_index()
data17 = data_full[data_full['ASSESSMENT_YEAR'] == 2017].reset_index()

# Read in the growth factors
gfactors = pd.read_csv('../pitaxcalc-demo/taxcalc/growfactors.csv')
gfactors.set_index('YEAR', inplace=True)
count = [0] * len(gfactors)
count[0] = len(data13)
count[1] = len(data14)
count[2] = len(data15)
count[3] = len(data16)
count[4] = len(data17)

datasets = [data13, data14, data15, data16, data17]


# Variable list we need to use
varlist = ['INCOME_HP', 'PRFT_GAIN_BP_OTHR_SPECLTV_BUS',
           'PRFT_GAIN_BP_SPECLTV_BUS', 'PRFT_GAIN_BP_SPCFD_BUS',
           #'PRFT_GAIN_BP_INC_115BBF',
           'ST_CG_AMT_1', 'ST_CG_AMT_2', 'ST_CG_AMT_APPRATE', 'LT_CG_AMT_1',
           'LT_CG_AMT_2', 'TOTAL_INCOME_OS', 'CYL_SET_OFF', 'TOTAL_DEDUC_VIA',
           'DEDUCT_SEC_10A_OR_10AA', 'NET_AGRC_INCOME', 'AGGREGATE_LIABILTY',
           'BFL_SET_OFF_BALANCE']
# Average amounts for various measures
agg_results = {'no_returns': 543310.,
               'INCOME_HP': 134403176952 / 790443.,
               'PRFT_GAIN_BP_OTHR_SPECLTV_BUS': 11650386829465 / 783662.,
               'PRFT_GAIN_BP_SPECLTV_BUS': 2850073821 / 783662.,
               'PRFT_GAIN_BP_SPCFD_BUS': 27604158172 / 783662.,
               'PRFT_GAIN_BP_INC_115BBF': 147539582 / 783662.,
               'ST_CG_AMT_1': 82338302877 / 781141.,
               'ST_CG_AMT_2': 4641554226 / 781141.,
               'LT_CG_AMT_1': 250513034751 / 781141.,
               'LT_CG_AMT_2': 485197199930 / 781141.,
               'ST_CG_AMT_APPRATE': 209659446475 / 781141.,
               'TOTAL_INCOME_OS': 1469424739773 / 782060.,
               'CYL_SET_OFF': 376486955786 / 790443.,
               'TOTAL_DEDUC_VIA': 716950424561 / 790443.,
               'DEDUCT_SEC_10A_OR_10AA': 567899906850 / 790443.,
               'NET_AGRC_INCOME': 20689305576 / 790443.,
               'AGGREGATE_LIABILTY': 3954771854602 / 790443.,
               'BFL_SET_OFF_BALANCE': 1125891121508 / 790443.}
agg_results2 = copy.deepcopy(agg_results)

# Rename some growthfactors
gfactors.rename({'RENT': 'INCOME_HP',
                 'BP_NONSPECULATIVE': 'PRFT_GAIN_BP_OTHR_SPECLTV_BUS',
                 'BP_SPECULATIVE': 'PRFT_GAIN_BP_SPECLTV_BUS',
                 'BP_SPECIFIED': 'PRFT_GAIN_BP_SPCFD_BUS',
                 'STCG_APPRATE': 'ST_CG_AMT_APPRATE',
                 'OINCOME': 'TOTAL_INCOME_OS', 'LOSSES_CY': 'CYL_SET_OFF',
                 'AGRI_INCOME': 'NET_AGRC_INCOME',
                 'DEDU_SEC_10A_OR_10AA': 'DEDUCT_SEC_10A_OR_10AA',
                 'DEDUCTIONS': 'TOTAL_DEDUC_VIA',
                 'CORP': 'AGGREGATE_LIABILTY',
                 'LOSSES_BF': 'BFL_SET_OFF_BALANCE'},
                axis=1, inplace=True)
# Totals in the sample
sample_results = {'no_returns': count}
blowup_results = {}
agg_results3 = {}
"""
for var in varlist:
    # Store empty lists in blowup_results
    blowup_results[var] = []
    for year in range(2017, 2022):
        if match_gfactors:
            # Apply growth factor to aggregate results and use given year
            agg_results2[var] *= gfactors.loc[year, var]
            sample_results[var] = 1.0 * sum(datasets[year-2017][var]) / count[year-2017]
        else:
            # Use the 2013 data only
            sample_results[var] = 1.0 * sum(datasets[0][var]) / count[0]
        if sample_results[var] != 0:
            blowup_results[var].append(min(agg_results2[var] / sample_results[var], 20))
        else:
            blowup_results[var].append(1.0)
"""
for var in varlist:
    # Store empty lists in blowup_results
    blowup_results[var] = []
    agg_results3[var] = sum(datasets[4][var]) / count[4] * gfactors.loc[2017, var]
    for year in range(2017, 2024):
        if match_gfactors:
            # Apply growth factor to aggregate results and use given year
            if (year<=2021):
                agg_results3[var] *= gfactors.loc[year, var]
                sample_results[var] = 1.0 * sum(datasets[year-2017][var]) / count[year-2017]
            else:
            # Use the 2017 data only
                sample_results[var] = 1.0 * sum(datasets[4][var]) / count[4]                
        else:
            # Use the 2013 data only
            sample_results[var] = 1.0 * sum(datasets[0][var]) / count[0]
        if sample_results[var] != 0:
            blowup_results[var].append(min(agg_results3[var] / sample_results[var], 50))
        else:
            blowup_results[var].append(1.0)
agg_results3['INVESTMENT'] = sum(datasets[4]['PADDTNS_180_DAYS__MOR_PY_15P'] + datasets[4]['PADDTNS_LESS_180_DAYS_15P']) / count[4] * gfactors.loc[2017, var]
blowup_results['INVESTMENT'] = []
for year in range(2017, 2024):
    if match_gfactors:
        # Apply growth factor to aggregate results and use given year
        if (year<=2021):
            agg_results3['INVESTMENT'] *= gfactors.loc[year, 'INVESTMENT']
            sample_results['INVESTMENT'] = 1.0 * sum(datasets[year-2017]['PADDTNS_180_DAYS__MOR_PY_15P'] + datasets[year-2017]['PADDTNS_LESS_180_DAYS_15P']) / count[year-2017]
        else:
            # Use the 2017 data only
            sample_results['INVESTMENT'] = 1.0 * sum(datasets[4]['PADDTNS_180_DAYS__MOR_PY_15P'] + datasets[4]['PADDTNS_LESS_180_DAYS_15P']) / count[4]
    else:
        # Use the 2013 data only
        sample_results['INVESTMENT'] = 1.0 * sum(datasets[0]['PADDTNS_180_DAYS__MOR_PY_15P'] + datasets[0]['PADDTNS_LESS_180_DAYS_15P']) / count[0]
    if sample_results['INVESTMENT'] != 0:
        blowup_results['INVESTMENT'].append(min(agg_results3['INVESTMENT'] / sample_results['INVESTMENT'], 50))
    else:
        blowup_results[var].append(1.0)

"""
Fill this in later
wgt13 =


weights_df = pd.DataFrame({'WT2017': [] * count,
                           'WT2018': [WGT2017 * 1.1] * count,
                           'WT2019': [WGT2017 * 1.1**2] * count,
                           'WT2020': [WGT2017 * 1.1**3] * count,
                           'WT2021': [WGT2017 * 1.1**4] * count})
"""

blowup_df = pd.DataFrame.from_dict(blowup_results)
blowup_df.round(6)
blowup_df['YEAR'] = range(2017, 2024)
blowup_df.set_index('YEAR', inplace=True)
blowup_df.to_csv('cit_panel_blowup.csv')

data_full.round(6)
data_full.to_csv('cit_panel.csv', index=False)
