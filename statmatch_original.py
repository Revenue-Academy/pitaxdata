import pandas as pd
import numpy as np
import statsmodels.api as sm


def counts(df, groupby, wt):
    gdf = df.groupby(groupby)
    count = gdf.size().reset_index(name="count")
    wt = gdf[wt].sum().reset_index(name="wt")
    return pd.concat([count, wt["wt"]], axis=1, sort=False)


def reg(df, dep_var, indep_vars, wt):
    if "const" not in indep_vars:
        indep_vars.append("const")
    model = sm.WLS(df[dep_var], df[indep_vars], weights=df[wt])
    results = model.fit()
    print(results.rsquared)
    return results.params


def predict(df, indep_vars):
    """
    Assumes that both the independent variables and parameters
    are in the DataFrame
    """
    params = list("param_" + pd.Series(indep_vars))
    x = df[indep_vars]
    p = df[params]
    yhat = x.mul(p.values, axis="index").sum(axis=1)
    return yhat


def match(donor, recipient, donor_id, recipient_id,
          donor_wt, recipient_wt, yhat="yhat",
          cell_id="cell_id"):
    """
    Function to iterate through both files and match them with their
    closest record
    """
    epsilon = 0.001  # tolerance for using up weights
    donor_list = []  # list to store IDs from donor file
    recipient_list = []  # list to store IDs from recipient
    cwt_list = []  # list to hold the new weights
    cell_ids = np.unique(recipient[cell_id])

    # loop through each cell ID and find matches
    for cid in cell_ids:
        _donor = donor[donor[cell_id] == cid]
        _recipient = recipient[recipient[cell_id] == cid]
        _donor = _donor.sort_values(yhat, kind="mergesort")
        _recipient = _recipient.sort_values(yhat, kind="mergesort")
        
        # convert to list of dictionaries
        _donor = _donor.to_dict("records")
        _recipient = _recipient.to_dict("records")
        
        j = 0
        bwt = _donor[j][donor_wt]
        count = len(_donor) - 1
        for record in _recipient:
            awt = record[recipient_wt]
            while awt > epsilon:
                # weight of new record will be min of
                # records being matched
                cwt = min(awt, bwt)
                recipient_seq = record[recipient_id]
                donor_seq = _donor[j][donor_id]
                # append each sequence to respective list
                donor_list.append(donor_seq)
                recipient_list.append(recipient_seq)
                cwt_list.append(cwt)
                # recalculate weights
                awt = max(0, awt - cwt)
                bwt = max(0, bwt - cwt)
                if bwt <= epsilon:
                    if j < count:
                        j += 1
                        bwt = _donor[j][donor_wt]

    match = pd.DataFrame({"donor_seq": donor_list,
                          "recipient_seq": recipient_list,
                          "cwt": cwt_list})
    return match
