import pandas as pd
import numpy as np
from statmatch import counts, reg, predict, match


def matchfiles(verbose=False):
    """
    Run all statistical matching logic
    """
    income_file = "36151-0002-Data.tsv"
    consumption_file = "Household Characteristics - Block 3 -  Level 2 -  68.dta"
    consumption_file2 = "Household characteristics - Block 3 - Level 3.dta"
    consumption_summary = "Summary of Consumer Expenditure - Block 12 - Level 11 - 68.dta"

    if verbose:
        print("Reading Data")
    income_data = pd.read_csv(income_file, sep="\t", na_values=" ")
    if verbose:
        print("Finished Reading Income Data")
    consumption_data = pd.read_stata(consumption_file, preserve_dtypes=False)
    # pull ration card data from other file
    consumption_data2 = pd.read_stata(consumption_file2)
    consumption_data = pd.merge(consumption_data,
                                consumption_data2[["Possess_ration_card",
                                                   "HHID"]],
                                on="HHID", how="inner")
    del consumption_data2
    consump_summary_data = pd.read_stata(consumption_summary)
    # only use the summary data on monthly per capita expenditure
    consump_summary_data = consump_summary_data[["Value", "HHID"]][
        consump_summary_data["Srl_no"] == "49"
    ]
    consumption_data = pd.merge(consumption_data, consump_summary_data,
                                how="inner", on="HHID")
    del consump_summary_data
    if verbose:
        print("Finished Reading Consumption Data")
        print("Cleaning Data")

    # perform general data cleaning

    # convert listed variables to integers
    int_vars = ["HH_Size", "State_code", "Sector"]
    for var in int_vars:
        consumption_data[var] = consumption_data[var].astype(int)

    # rename variables in data to match names
    income_renames = {"URBAN2011": "urban",
                      "RC1": "ration_card"}
    income_data.rename(income_renames, axis=1, inplace=True)

    # normalize data
    consumption_data["urban"] = np.where(consumption_data["Sector"] == 2,
                                         1, 0)
    ration_card = np.where(consumption_data["Possess_ration_card"] == 2,
                           1, 0)
    consumption_data["ration_card"] = ration_card
    owns_land = np.where(consumption_data["whether_Land_owned"] == 2, 1, 0)
    consumption_data["owns_land"] = owns_land
    caste = np.where(consumption_data["Social_Group"] == "9", 4,
                     consumption_data["Social_Group"])
    consumption_data["caste"] = caste
    
    owns_land = income_data[["FM4A", "FM4B", "FM4C"]].sum(axis=1).astype(bool)
    income_data["owns_land"] = owns_land * 1

    caste = np.where(income_data["ID13"] == 5, 1,
                     np.where(income_data["ID13"] == 4, 2,
                              np.where(income_data["ID13"] == 3, 3,
                                       4)))
    income_data["caste"] = caste
    # top code household size because of the lack of records with
    # higher household sizes
    consumption_data["hh_size_tc"] = np.where(consumption_data["HH_Size"] > 10,
                                              11, consumption_data["HH_Size"])
    income_data["hh_size_tc"] = np.where(income_data["NPERSONS"] > 10,
                                         11, income_data["NPERSONS"])

    # create dummy variables
    caste_dummies = pd.get_dummies(income_data["caste"], prefix="caste")
    income_data[caste_dummies.columns] = caste_dummies
    caste_dummies = pd.get_dummies(consumption_data["caste"],
                                   prefix="caste")
    consumption_data[caste_dummies.columns] = caste_dummies
    caste_dummy_vars = list(caste_dummies.columns)
    # remove variable representing missing caste data
    caste_dummy_vars.remove("caste_ ")
    
    state_dummies = pd.get_dummies(consumption_data["State_code"],
                                   prefix="stateid")
    consumption_data[state_dummies.columns] = state_dummies
    state_dummies = pd.get_dummies(income_data["STATEID"], prefix="stateid")
    income_data[state_dummies.columns] = state_dummies

    # determine partition groups and unweighted counts in each
    if verbose:
        print("Partitioning Data")
    partition_vars = ["urban", "hh_size_tc"]
    income_counts = counts(income_data, partition_vars, "WT")
    consumption_counts = counts(consumption_data, partition_vars,
                                "Combined_multiplier")
    income_counts.rename(columns={"count": "i_count",
                                  "wt": "i_wt"},
                         inplace=True)
    consumption_counts.rename(columns={"count": "c_count",
                                       "wt": "c_wt"},
                              inplace=True)
    full_count = pd.merge(income_counts, consumption_counts,
                          how="inner", on=partition_vars)
    full_count["cell_id"] = full_count.index + 1
    # Factor for adjusting weight in each cell
    full_count["factor"] = (full_count["c_wt"] /
                            full_count["i_wt"]).astype(float)
    
    # merge cell_id onto each data file
    income_data = pd.merge(income_data, full_count, how="inner",
                           on=partition_vars)
    consumption_data = pd.merge(consumption_data, full_count,
                                how="inner", on=partition_vars)
    # ensure that income data weights total consumption data
    income_data["wt"] = income_data["WT"] * income_data["factor"]
    consumption_data["wt"] = consumption_data["Combined_multiplier"]
    consumption_data["const"] = np.ones(len(consumption_data))

    # define variables for the regression
    indep_vars = (["owns_land", "ration_card"] +
                  list(state_dummies.columns)[:-1] +
                  caste_dummy_vars[1:])

    # find model parameters for each group
    if verbose:
        print("Running Regression")
    gdf = consumption_data.groupby("cell_id", as_index=False)
    params = gdf.apply(reg, dep_var="Value", indep_vars=indep_vars,
                       wt="Combined_multiplier")
    params = params.add_prefix("param_")
    params["cell_id"] = params.index + 1
    
    income_data = pd.merge(income_data, params, how="inner",
                           on="cell_id")
    consumption_data = pd.merge(consumption_data, params,
                                how="inner", on="cell_id")

    # calculate yhate values
    if verbose:
        print("Predicting Consumption")

    income_data["const"] = np.ones(len(income_data))
    income_data["yhat"] = predict(income_data, indep_vars)
    consumption_data["yhat"] = predict(consumption_data,
                                       indep_vars)

    # perform match
    if verbose:
        print("Matching Data")
    match_index = match(income_data, consumption_data,
                        "IDHH", "HHID", "wt", "wt")
    if verbose:
        print("Match Complete")
    return match_index


if __name__ == "__main__":
    matchfiles(True)
