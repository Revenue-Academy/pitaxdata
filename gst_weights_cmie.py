import pandas as pd

data = pd.read_csv("gst_cmie_august_2020.csv")

# total_households = 101662

# Calculate weights
# Assume 8% growth rate in consumption year on year
cons_growth_rate = 1.00

weights_df = data[['WEIGHT']]
weights_df = weights_df.rename(columns = {'WEIGHT':'WT2020'})
weights_df['WT2021'] = weights_df['WT2020'] * cons_growth_rate
weights_df['WT2022'] = weights_df['WT2021'] * cons_growth_rate
weights_df['WT2023'] = weights_df['WT2022'] * cons_growth_rate
# Export results
weights_df.to_csv('gst_weights_cmie_august_2020.csv', index=False)
