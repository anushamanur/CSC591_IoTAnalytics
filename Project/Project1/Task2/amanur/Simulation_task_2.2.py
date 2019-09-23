#!/usr/bin/env python
# coding: utf-8

# In[33]:


import random, math
import pandas as pd
import numpy as np


# In[34]:


# mean values
iat_RT_mean = 10.0
iat_NRT_mean = 5.0
st_RT_mean =2.0
st_NRT_mean = 4.0

data=[]


# In[35]:


# Set initial conditions
RTCL = 3.0
nonRTCL=5.0
nRT =0
nNonRT=0
s=2
SCL=4.0

MC=0.0
rem_time=0
max_iter=200.00
random.seed(7)


# In[36]:


def return_time(mean):
    r=random.random()
    time= -(mean)*math.log(r) 
    return round(time,4)


# In[37]:


row=[round(MC,4),round(RTCL,4),round(nonRTCL,4),nRT,nNonRT,round(SCL,4),s,round(rem_time,4)]
data.append(row)
while MC <= max_iter:

    if SCL<RTCL and SCL<nonRTCL :
        MC=SCL
        
        if nRT!=0:
            nRT-=1
            s=1
            
            st_RT=return_time(st_RT_mean)
            SCL=MC+st_RT
            
        elif nNonRT!=0:
            nNonRT-=1
            s=2
            
            if rem_time!=0:
                SCL=MC+rem_time
                rem_time=0
            else:
                st_NRT=return_time(st_NRT_mean)
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
        iat_RT=return_time(iat_RT_mean)        
        RTCL=MC+iat_RT
        s=1
        
        st_RT=return_time(st_RT_mean)
        SCL=MC+st_RT
        
        
    elif RTCL < SCL and RTCL <= nonRTCL:
        MC=RTCL
        
        iat_RT=return_time(iat_RT_mean) 
        RTCL=MC+iat_RT        
        
        if s==1:
            nRT+=1
            
        elif s==0:
            st_RT=return_time(st_RT_mean)
            SCL=MC+st_RT
            s=1
            
        elif s==2:
            nNonRT+=1
            rem_time=SCL-MC
            s=1
            
            st_RT=return_time(st_RT_mean)
            SCL=MC+st_RT
     
    elif nonRTCL <= SCL or nonRTCL < RTCL:
        MC=nonRTCL
        
        iat_NRT=return_time(iat_NRT_mean) 
        nonRTCL=MC+iat_NRT
        
        if s==0:
            st_NRT=return_time(st_NRT_mean)
            SCL=MC+st_NRT
            s=2  
            
        if s==1 or s==2:
            nNonRT+=1    
            
    row=[round(MC,4),round(RTCL,4),round(nonRTCL,4),nRT,nNonRT,round(SCL,4),s,round(rem_time,4)]
    data.append(row)

df = pd.DataFrame(data, columns=["MCL","RTCL","non-RTCL","N(RT)","N(nonRT)","SCL","s","remaining time"])

df.loc[df['SCL'] == max_iter+1000, 'SCL'] = np.nan
print(df.to_string())


# In[38]:


df.to_csv("Output_task_2.2.csv", sep='\t')


# In[ ]:




