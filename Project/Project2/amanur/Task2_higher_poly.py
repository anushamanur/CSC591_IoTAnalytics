#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
import scipy as sp


# In[8]:


data=pd.read_csv('data.csv', index_col=0)
X=data.iloc[:,:2]
Y=data.iloc[:,5:6]


# In[9]:


X2 = sm.add_constant(X)
est = sm.OLS(Y, X2)
res = est.fit()
print(res.summary())

