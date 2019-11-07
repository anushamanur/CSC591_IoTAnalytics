#!/usr/bin/env python
# coding: utf-8

# In[51]:


import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
import scipy as sp


# In[52]:


data=pd.read_csv('data.csv',  index_col=0)
X=data.iloc[:,:5]
Y=data.iloc[:,5:6]
X.shape, Y.shape


# In[53]:


X2 = sm.add_constant(X)
est = sm.OLS(Y, X2)
res = est.fit()
print(res.summary())


# In[54]:


#Removing X2
data=pd.read_csv('data.csv',  index_col=0)
X=data.iloc[:,:5]
Y=data.iloc[:,5:6]
del X['X2']


# In[55]:


X2 = sm.add_constant(X)
est = sm.OLS(Y, X2)
res = est.fit()
print(res.summary())


# In[56]:


resi = res.resid 
print ("Variance : ", np.var(resi))
fig = sm.qqplot(resi, line='s')
plt.show()


# In[57]:


freq,bins,_=plt.hist(res.resid, bins=[-1297.4342941 ,  -603.89968445,    89.6349252 ,   783.16953484,
        1476.70414449,  2170.23875414,  2863.77336378,  3557.30797343])
plt.ylabel('Count')
plt.xlabel('Normalized residuals')
bins, freq


# In[58]:


a1, b1 = sp.stats.norm.fit(resi)

scaling_factor = 286*(resi.max()-resi.min())/7
x_middle = 0.5*(bins[1:] + bins[:-1])
expected_values = scaling_factor*sp.stats.norm.pdf(x_middle,a1,b1)
chi,_=sp.stats.chisquare(freq,expected_values,ddof=2)
chi


# In[59]:


cdf = stats.norm.cdf(bins, a1, b1)
expected_values = 286 * np.diff(cdf)
chi,_=sp.stats.chisquare(freq,expected_values,ddof=2)
chi


# In[60]:


pred = res.predict()
# Plot
plt.scatter(pred, resi,  alpha=0.5)
plt.title('Scatter plot')
plt.xlabel('Y^')
plt.ylabel('Residuals')
plt.show()

