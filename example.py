
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 09:25:21 2017

@author: Ilia Rushkin

This script takes as input a data frame where each row is a user
The list "variables" shows which columns will be used for the activity calculation.
These variables should be all numeric and non-negative, with 0 indicating no activity and higher values indicating higher activity.

The function to call from the module ilia_activity is:
    activity(df,variables,max_iter,n_levels)
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
"""

import ilia_activity
import pandas as pd

##The list of variables used to index activity. They should be numeric and non-negative. Higher value indicates more activity, 0 indicates no activity.
variables=['nevents','nchapters','nplay_video','nproblem_check']
#Max iterations in the EFA routine. If exceeded before convergence, resort to PCA
max_iter=1000
#Number of activity levels in addition to the zeroth one.
n_levels=4


file_to_write='example_output.csv'

pcs = pd.read_csv('example_data.csv', dtype={'user_id': str})

df,vs,weights,method=ilia_activity.activity(pcs,variables, max_iter=max_iter, n_levels=n_levels)
df.to_csv(file_to_write)
print 'Variables:',vs,'\nWeights:',weights,'\nMethod:',method
print 'Output written to:',file_to_write


##############################
