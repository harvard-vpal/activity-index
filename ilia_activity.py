# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 19:41:07 2017

@author: Ilia Rushkin
"""

import pandas as pd
import numpy as np
import scipy.stats as ss
from matplotlib.mlab import PCA
from sklearn.decomposition import FactorAnalysis
from sklearn.cluster import KMeans

###SETTINGS####


#Transformation of variables to be used before EFA (to unskew them)
def prelim_transform(x):
    return (np.log(1+x))

###END OF SETTINGS####



##Main function 
##Input df is the data frame containing whose columns are the variables to be collapsed.
##Outputs: df with two additional columns - activity index and level, and loading - vector of weights for the collapsed variables
def activity(df,variables=None,max_iter=1000,n_levels=4,try_EFA=True):
    df.index=range(np.shape(df)[0])
    
    if variables==None:
        variables=df.columns
    ##Remove duplicate variables if any
    uniq,index=np.unique(variables,return_index=True)
    variables=uniq[index.argsort()].tolist()
        
    df1=df.loc[:,variables]
    df1=df1.fillna(0.)
    ind=np.where(df1.sum(axis=1)>0)[0]
    
    
    df.loc[:,'ilia_activity_index']=np.nan
    df.loc[:,'ilia_activity_level']=0
    
    if len(ind)>0:
        df1=df1.loc[ind,variables]
        df1.index=range(np.shape(df1)[0])
        df1=df1.apply(prelim_transform)
        sdevs=df1.apply(np.std)
        valid_vars=np.where(sdevs>0)[0].tolist()
        
        loading=np.repeat(0.0,len(variables))
        
        
        if len(valid_vars)>0:
            for i in valid_vars:
                df1[variables[i]]/=sdevs[i]
                df1[variables[i]]-=np.mean(df1[variables[i]])
            
            if len(valid_vars)==1:
                method='single variable'
                df.loc[ind,'ilia_activity_index']=df1.loc[:,[variables[i] for i in valid_vars]].values
                loading[valid_vars]=1.0
            else:
                #Perform the factor analysis. But if that fails to converge, resort to PCA
                n_iter=0
                if try_EFA:
                    fa=FactorAnalysis(n_components=1, max_iter=max_iter).fit(df1[[variables[i] for i in valid_vars]])
                    n_iter=fa.n_iter_
                if (n_iter<max_iter)&try_EFA:
                    method='EFA'
                    loading[valid_vars]=fa.components_.flatten()
                    df.loc[ind,'ilia_activity_index']=fa.transform(df1[[variables[i] for i in valid_vars]])*np.sign(sum(loading))
                else:
                    method='PCA'
                    pr=PCA(df1[[variables[i] for i in valid_vars]])
                    loading[valid_vars]=pr.Wt[0]
                    df.loc[ind,'ilia_activity_index']=pr.Y[:,0]*np.sign(sum(loading))
            #Normalize activity to unit variance
            df.loc[ind,'ilia_activity_index']/=np.std( df.loc[ind,'ilia_activity_index'])
            df.loc[ind,'ilia_activity_index']-=np.mean( df.loc[ind,'ilia_activity_index'])
            
            #Perform kmeans clustering
            cl=KMeans(n_clusters=n_levels).fit(df.loc[ind,'ilia_activity_index'].values.reshape(-1,1))
            df.loc[ind,'ilia_activity_level']=ss.rankdata(cl.cluster_centers_).astype(int)[cl.labels_]
            loading*=loading
            loading/=sum(loading)
    
    return df, variables, loading.tolist(), method






