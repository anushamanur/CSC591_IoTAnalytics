#!/usr/bin/env python
# coding: utf-8

# In[12]:


import math
from collections import deque
import pandas as pd
import numpy as np
import random


# In[13]:


##### Taking input from user

iat_RT_mean = int(input("Enter mean inter-arrival time of RT messages : "))
iat_NRT_mean = int(input("Enter mean inter-arrival time of nonRT messages : "))
st_RT_mean =int(input("Enter mean service time of an RT message : "))
st_NRT_mean = int(input("Enter mean service time of a nonRT message : "))
num_batch = int(input("Enter number of batches : "))
batch_size = int(input("Enter batch size : "))


# In[14]:


#create Qs
RT_Q = deque() 
NRT_Q = deque()  

#To store arrival times
RT=[]
NRT=[2]

#Time of completion
resa=[]
resb=[]

#Response times
respA=[]
respB=[]

#Mean
meanRT=[]
meanNRT=[]

#Percentile
percA=[]
percB=[]


# In[15]:


# Set initial conditions

#Store arrival times
RT_Q.appendleft(3)
NRT_Q.appendleft(5)

s=2
SCL=4
rem_time=0
data=[]
MC=0
i,j=0,0
random.seed(7)


# In[16]:


def return_time(mean):
    r=random.random()
    time= -(mean)*math.log(r) 
    return round(time,4)


# In[17]:


### METHOD USED ###

# if an RT event arrives, it is serviced immediately if s=0,2
# if an RT event arrives, it is added to Q, otherwise
# if an NRT event arrives, it is serviced immediately if s=0
# if an NRT event arrives, it is added to Q, otherwise

#If there is SCL, if ther are other events whcih have already arrived, they are chosen to be serviced
# in the order - RT, NRT

# A new event is added to the Q, whenever an event arrives.


# In[18]:


row=[round(MC,4),SCL,s,round(rem_time,4)]
data.append(row)

for m in range(num_batch):
    for b in range(batch_size):
        
        #If there is a service completion
        if SCL<RT_Q[0] and SCL<NRT_Q[0] :  
            
            if s==1:
                resa.append(SCL)
                
            elif s==2:
                resb.append(SCL)
            
            #If RT events have already arrived and waiting to be served,
            #Already arrived RT event is given preference
            if RT_Q[-1]<=SCL:
                MC=SCL  
                arr=RT_Q.pop()
                RT.append(arr)
                s=1
                st_RT=return_time(st_RT_mean)
                SCL=MC+st_RT
                
            elif rem_time!=0:
                MC=SCL
                SCL=MC+rem_time
                rem_time=0
                s=2
                
            #If no RT event is there, NRT event is serviced
            elif NRT_Q[-1]<=SCL:
                MC=SCL  
                arr=NRT_Q.pop()
                NRT.append(arr)
                
                st_NRT=return_time(st_NRT_mean)
                SCL=MC+st_NRT
                
                s=2 
            #If no event is waiting, set s=0
            else:          
                MC=SCL            
                s=0
                SCL=10000000000

        elif RT_Q[0] == SCL: 
            
            if s==1:
                resa.append(SCL)
                
            elif s==2:
                resb.append(SCL)
            
            
            MC=RT_Q.pop()
            RT.append(MC)
            
            iat_RT=return_time(iat_RT_mean)  
            RT_Q.appendleft(MC+iat_RT)
            
            s=1
            st_RT=return_time(st_RT_mean)
            SCL=MC+st_RT

        #If RT arrives
        elif RT_Q[0] < SCL and RT_Q[0] <= NRT_Q[0]:                  
                
            # IS serviced immediately if s=0
            if s==0:
                MC=RT_Q.pop()
                RT.append(MC)
                
                iat_RT=return_time(iat_RT_mean)  
                RT_Q.appendleft(MC+iat_RT)
                
                st_RT=return_time(st_RT_mean)
                SCL=MC+st_RT
                s=1
                
            #NRT event is preempted and RT event is servied immediately
            elif s==2:
                MC=RT_Q.pop()
                RT.append(MC)
                
                iat_RT=return_time(iat_RT_mean)  
                RT_Q.appendleft(MC+iat_RT)
                
                rem_time=SCL-MC
                s=1
                
                st_RT=return_time(st_RT_mean)
                SCL=MC+st_RT
                
            # Added to Q if RT event is being serviced
            elif s==1:
                MC=RT_Q[0]
                
                iat_RT=return_time(iat_RT_mean)  
                RT_Q.appendleft(MC+iat_RT)

                
        # If a NRT arrives, 
        elif  NRT_Q[0] <= SCL and  NRT_Q[0] <  RT_Q[0]:   
            
            if NRT_Q[0] == SCL :
                if s==1:
                    resa.append(SCL)
                
                elif s==2:
                    resb.append(SCL)
            
            #it is serviced immediately
            if s==0:
                MC=NRT_Q.pop()    
                NRT.append(MC)
                
                iat_NRT=return_time(iat_NRT_mean)  
                NRT_Q.appendleft(MC+iat_NRT)
                
                st_NRT=return_time(st_NRT_mean)
                SCL=MC+st_NRT
                s=2  
            else:
                #Or since server is busy, new NRT is added to Q
                MC=NRT_Q[0]
                
                iat_NRT=return_time(iat_NRT_mean)  
                NRT_Q.appendleft(MC+iat_NRT)
                
  
    
        row=[round(MC,4),SCL,s,round(rem_time,4)]
        data.append(row)
  
    resa=list(set(resa))
    a=np.array(RT)
    b=np.array(NRT)
    lenRT=len(resa)
    lenNRT=len(resb)
    
    ra=[]
    rb=[]
    
    x=sorted(resa)
    y=sorted(resb)
    #Calculating response time
    ra=(x-a[:lenRT])
    rb=(y-b[:lenNRT])
    #Leaving out 1st batch
    if m!=0:
        meanRT.append(np.mean(ra))
        meanNRT.append(np.mean(rb))    
        respA.extend(ra)
        respB.extend(rb)   
        percA.append(np.percentile(ra, 95)) 
        percB.append(np.percentile(rb, 95)) 
    
    del RT[:lenRT]
    del NRT[:lenNRT]
    resa=[]
    resb=[]
df = pd.DataFrame(data, columns=["MCL","SCL","s","remaining time"])

df.loc[df['SCL'] == 10000000000, 'SCL'] = np.nan


# In[19]:


df_res = pd.DataFrame(list(zip(meanRT,meanNRT,percA,percB)),
                      columns=["meanRT","MeanNRT","percRT","percNRT"])
df_res.to_csv(str(iat_NRT_mean)+'.csv', sep=',')


# In[20]:


df_resp = pd.DataFrame(list(zip(np.transpose(np.array(respA).flatten()),np.transpose(np.array(respB).flatten()))),columns=["respA","respB"])
df_resp.to_csv(str(iat_NRT_mean)+'r.csv', sep=',')


# In[21]:


def CI(arr):
    x_bar = np.mean(arr) # mean of vector
    s = np.std(arr) # std of vector
    n = len(arr) # number of obs
    z = 1.96 # for a 95% CI
    lower = x_bar - (z * (s/math.sqrt(n)))
    upper = x_bar + (z * (s/math.sqrt(n)))
    return (round(lower,4),round(upper,4))


# In[22]:


#Confidence interval of mean response time
ciA=CI(np.array(respA).flatten())
ciB=CI(np.array(respB).flatten())
print (ciA,ciB)

#Confidence interval of 95th percentile
ciA=CI(np.array(percA).flatten())
ciB=CI(np.array(percB).flatten())
print (ciA,ciB)


# In[ ]:




