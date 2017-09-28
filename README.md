# activity-index

Module ilia_activity contains the main function:
    activity(df,variables,max_iter,n_levels, try_EFA)
Inputs:
    1) df: dataframe with users as rows
    2) variables (default all columns in df): which variables to use in the calculation
    3) max_iter (default 1000): max number of iterations to be attempted in the EFA routine. If convergence was not achieved, the method will switch to PCA
    4) n_levels (default 4): number of non-zero levels to be used in ilia_activity_levels
    5) try_EFA (default True): whether or not to try EFA as method

Outputs: [df1,variables,weights,method]
    1) df1: dataframe df with two extra columns: ilia_activity_index and ilia_activity_level
    2) variables: variables used in the calculation (same as the input, except that duplicate variable names are removed)
    3) weights: weights of variables in the activity index (a list of numbers whose sum is 1)
    4) method: which method produced the result: 
            'single variable' if only one variable with non-zero variance was available
            'EFA' if the EFA routine converged
            'PCA' if the EFA routine did not converge and the calculation switched to using PCA.
