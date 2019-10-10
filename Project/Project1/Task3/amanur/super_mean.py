#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math
from collections import deque
import pandas as pd
import numpy as np
import random


# In[2]:


#To store super mean
RT_mean=[]
NRT_mean=[]
RT_perc=[]
NRT_perc=[]


# In[3]:


for i in range(10,45,5):
    filename =str(i)+".csv"
    df=pd.read_csv(filename)
    del df['Unnamed: 0']
    RT_mean.append(np.mean(df['meanRT']))
    NRT_mean.append(np.mean(df['MeanNRT']))
    RT_perc.append(np.mean(df['percRT']))
    NRT_perc.append(np.mean(df['percNRT']))


# In[4]:


res = pd.DataFrame(list(zip(RT_mean,NRT_mean,RT_perc,NRT_perc)),
                      columns=["meanRT","MeanNRT","percRT","percNRT"])
res.to_csv("result.csv", sep=',')

