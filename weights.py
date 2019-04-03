import pandas as pd

data = pd.read_csv("pit.csv")
n_ITR1 = 26541891
n_ITR3 = 8699285
ITR1_Growthrate = 1.1
ITR3_Growthrate = 1.1
n_ITR_GrowthRate = {'ITR-1':ITR1_Growthrate, 'ITR-3':ITR3_Growthrate}
insample1 = (data['FORM_ID']== 'ITR-1').sum()
weight_ITR1 = n_ITR1/insample1
insample3 = (data['FORM_ID']== 'ITR-3').sum()
weight_ITR3 = n_ITR3/insample3

weight_dict = {'ITR-1':weight_ITR1, 'ITR-3':weight_ITR3}
weights = pd.DataFrame()
weights['WT2017'] = [weight_dict[x] for x in data['FORM_ID']]
weights['WT2018'] = [wt*n_ITR_GrowthRate[x]
                     for (wt,x) in zip(weights['WT2017'], data['FORM_ID'])]
weights['WT2019'] = [wt*n_ITR_GrowthRate[x]
                     for (wt,x) in zip(weights['WT2018'], data['FORM_ID'])]
weights['WT2020'] = [wt*n_ITR_GrowthRate[x]
                     for (wt,x) in zip(weights['WT2019'], data['FORM_ID'])]
weights['WT2021'] = [wt*n_ITR_GrowthRate[x]
                     for (wt,x) in zip(weights['WT2020'], data['FORM_ID'])]
weights['WT2022'] = [wt*n_ITR_GrowthRate[x]
                     for (wt,x) in zip(weights['WT2021'], data['FORM_ID'])]
weights['WT2023'] = [wt*n_ITR_GrowthRate[x]
                     for (wt,x) in zip(weights['WT2022'], data['FORM_ID'])]
weights.to_csv('pit_weights.csv', index=False)
