import pandas as pd


def decile_group(position):
    if position <= 6069:
        return 1
    elif position <= 17448:
        return 2
    elif position <= 30211:
        return 3
    elif position <= 44018:
        return 4
    elif position <= 59538:
        return 5
    elif position <= 77535:
        return 6
    elif position <= 98589:
        return 7
    elif position <= 124322:
        return 8
    elif position <= 158424:
        return 9
    elif position <= 247485:
        return 10
    elif position > 247485:
        return 11

data = pd.read_csv("pitBigData.csv")

# sort by gross_total_income
data.sort_values('GROSS_TOTAL_INCOME', inplace=True)
data.reset_index(drop=True)
data['position'] = data.index + 1
data['decile_group'] = data['position'].apply(decile_group)

# define weights
ns = [6069, 11379, 12763 , 13807, 15520, 17997, 21054, 25733, 34102, 89061]
nreturns = 4949718
weights_dict = {}
for i in range(len(ns)):
    n = ns[i]
    weights_dict[i + 1] = nreturns / n
weights_dict[11] = 1

weights = pd.DataFrame()
weights['WT2017'] = [weights_dict[x] for x in data['decile_group']]
weights['WT2018'] = weights['WT2017'] * 1.1
weights['WT2019'] = weights['WT2018'] * 1.1
data = data.fillna(0)
data.to_csv('pitBigData.csv', index=False)
weights.to_csv('pit_weightsBD.csv', index=False)
