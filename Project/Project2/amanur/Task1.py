#!/usr/bin/env python
# coding: utf-8

# In[54]:


import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns


# In[55]:


col = ['X1', 'X2','X3','X4','X5','Y']
data=pd.read_csv('amanur.csv', names=col)

print (data.head(5))


# In[56]:


#Histogram
data.hist(figsize=(8,8))


# In[57]:


#Mean
data.mean()


# In[58]:


#Variance
data.var()


# In[59]:


# Outliers - Z score

z = np.abs(stats.zscore(data))
threshold = 3
print ("Number of outliers: ",len(np.where(z > 3)[0]))

#Removing outliers
print ("Number of rows before removing outliers:", len(data))
df = data[(z < 3).all(axis=1)]
print ("Number of rows after removing outliers:", len(df))


# In[60]:


corr = df.corr()
corr.style.background_gradient(cmap='coolwarm')


# In[61]:


def heatmap(x, y, size):
    fig, ax = plt.subplots()
    

    # Mapping from column names to integer coordinates
    x_labels = [v for v in sorted(x.unique())]
    y_labels = [v for v in sorted(y.unique())]
    x_to_num = {p[1]:p[0] for p in enumerate(x_labels)} 
    y_to_num = {p[1]:p[0] for p in enumerate(y_labels)} 
    
    

    
    size_scale = 1000
    ax.scatter(
        x=x.map(x_to_num), # Use mapping for x
        y=y.map(y_to_num), # Use mapping for y
        s=size * size_scale, # Vector of square sizes, proportional to size parameter
        marker='s' # Use square as scatterplot marker
    )
    
    # Show column labels on the axes
    ax.set_xticks([x_to_num[v] for v in x_labels])
    ax.set_xticklabels(x_labels, rotation=45, horizontalalignment='right')
    ax.set_yticks([y_to_num[v] for v in y_labels])
    ax.set_yticklabels(y_labels)
    
    ax.grid(False, 'major')
    ax.grid(True, 'minor')
    ax.set_xticks([t + 0.5 for t in ax.get_xticks()], minor=True)
    ax.set_yticks([t + 0.5 for t in ax.get_yticks()], minor=True)
    ax.set_xlim([-0.5, max([v for v in x_to_num.values()]) + 0.5]) 
    ax.set_ylim([-0.5, max([v for v in y_to_num.values()]) + 0.5])
    


corr = data.corr()
corr = pd.melt(corr.reset_index(), id_vars='index') # Unpivot the dataframe, so we can get pair of arrays for x and y
corr.columns = ['x', 'y', 'value']
heatmap(
    x=corr['x'],
    y=corr['y'],
    size=corr['value'].abs()
)


# In[62]:


df.to_csv('data.csv', sep=',')

