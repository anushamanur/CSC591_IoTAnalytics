#!/usr/bin/env python
# coding: utf-8

# In[37]:


import math
import pandas as pd
import numpy as np


# In[38]:


# Taking input from user

iat_RT = int(input("Enter mean inter-arrival time of RT messages : "))
iat_NRT = int(input("Enter mean inter-arrival time of nonRT messages : "))
st_RT =int(input("Enter mean service time of an RT message : "))
st_NRT = int(input("Enter mean service time of a nonRT message : "))
max_iter = int(input("Enter max iteration (MC = 50 or 20) : "))


# In[39]:


# Set initial conditions
RTCL = 3
nonRTCL=5
nRT =0
nNonRT=0
s=2
SCL=4

MC=0
rem_time=0
data=[]


# In[40]:


row=[round(MC,4),round(RTCL,4),round(nonRTCL,4),nRT,nNonRT,round(SCL,4),s,round(rem_time,4)]
data.append(row)
while MC <= max_iter:

    if SCL<RTCL and SCL<nonRTCL :
        MC=SCL
        
        if nRT!=0:
            nRT-=1
            s=1
            SCL=MC+st_RT
            
        elif nNonRT!=0:
            nNonRT-=1
            s=2
            
            if rem_time!=0:
                SCL=MC+rem_time
                rem_time=0
            else:
                SCL=MC+st_NRT
        else:
            s=0
            # Since system is in idle state, there is no SCL. 
            # SCL is being set to a large value for computation purpose.
            # Ideally, SCL will contain no value as no event is being served. 
            #SCL is being set to Nan in final output table
            SCL=max_iter+1000 
        
    elif RTCL == SCL:
        MC=RTCL
        RTCL=MC+iat_RT
        s=1
        SCL=MC+st_RT
        
        
    elif RTCL < SCL and RTCL <= nonRTCL:
        MC=RTCL
        RTCL=MC+iat_RT        
        
        if s==1:
            nRT+=1
            
        elif s==0:
            SCL=MC+st_RT
            s=1
            
        elif s==2:
            nNonRT+=1
            rem_time=SCL-MC
            s=1
            SCL=MC+st_RT
     
    elif nonRTCL <= SCL or nonRTCL < RTCL:
        MC=nonRTCL
        nonRTCL=MC+iat_NRT
        
        if s==0:     
            SCL=MC+st_NRT
            s=2  
            
        if s==1 or s==2:
            nNonRT+=1    
            
    row=[round(MC,4),round(RTCL,4),round(nonRTCL,4),nRT,nNonRT,round(SCL,4),s,round(rem_time,4)]
    data.append(row)
    
df = pd.DataFrame(data, columns=["MCL","RTCL","non-RTCL","N(RT)","N(nonRT)","SCL","s","remaining time"])

df.loc[df['SCL'] == max_iter+1000, 'SCL'] = np.nan
print(df.to_string())


# In[41]:


df.to_csv("Output_task_2.1.csv", sep='\t')


# In[ ]:




