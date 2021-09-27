#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r'C:\Users\saira\Downloads\My Uber Drives - 2016.csv',encoding='latin1')
df


# In[2]:


df.head()


# In[ ]:


#here column names have * at the end let us remove them


# In[106]:


df.columns= df.columns.str.replace("*","", regex= True)


# In[107]:


df.columns


# In[108]:


df


# In[109]:


df.head()


# In[ ]:


#lets check for missing values


# In[110]:


df.isnull().sum()


# In[111]:


plt.figure(figsize=(15,10))
sns.heatmap(df.isnull(),cmap="magma", yticklabels = False)
plt.show()


# In[ ]:


#from above we can see that mostly purpose has more missing values and in others the missing values are in 1155 row,as that an empty row we can delete it


# In[112]:


df.drop(index=1155,axis=0,inplace=True)


# In[113]:


df.tail()


# In[ ]:


#as purpose has lot many missing values so we can drop it but we cannot do that as it has more than 40% of contribution in analysis


# In[114]:


df['PURPOSE'].fillna(method='ffill',inplace=True)  # i am using forward fill becausethe purpose column is the last column


# In[115]:


df.isnull().sum()


# In[ ]:


#now data is clean we can easily analyse the things AND LET ME LOOK AT SOME INFORMATION OF DATA


# In[116]:


df.info()


# In[ ]:


#everything is non null i.e., no missing values but the date and time are in categorical form let me convert it to numeric form


# In[117]:


df['START_DATE'] = pd.to_datetime(df['START_DATE'],errors='coerce')
df['END_DATE'] = pd.to_datetime(df['END_DATE'],errors='coerce')
df.info()


# In[119]:


category = pd.crosstab(index=df['CATEGORY'],columns = 'count')
category


# In[120]:


category.plot(kind ='bar', color= 'g')
plt.legend
plt.show()


# In[97]:


#let us analyse data related to start


# In[121]:


df.START.unique()


# In[99]:


#we have these many different cities so lets counts which place has maximum and minimum starts by group by


# In[122]:


df.START.unique()


# In[101]:


#here we see that cary has maximum starts lets visualise it


# In[123]:


STARTS = df.START.value_counts()
STARTS


# In[124]:


STARTS.plot(kind='pie',shadow=True)
plt.show()


# In[ ]:


#we see that all the values are clubed and difficult to see all 177 places lets simplify things


# In[125]:


STARTS[STARTS >10]


# In[126]:


STARTS[STARTS >10].plot(kind="pie", shadow = True)


# In[127]:


STARTS[STARTS <=10].plot(kind="pie", shadow = True)


# In[128]:


STARTS[STARTS <= 1]


# In[ ]:


#similarly we can do for stop


# In[129]:


df.START.unique()


# In[130]:


STOP = df.STOP.value_counts()
STOP


# In[131]:


miles = df.MILES.value_counts()
miles


# In[132]:


miles[miles>10].plot(kind='bar')


# In[ ]:


#analysis on PURPOSE of travel


# In[133]:


purpose = df.PURPOSE.value_counts()
purpose


# In[134]:


plt.figure(figsize=(15,6))
sns.countplot(df['PURPOSE'],order = df['PURPOSE'].value_counts().index,palette='viridis')
plt.show()


# In[136]:


df['minutes'] = df.END_DATE -df.START_DATE
df.head()


# In[137]:


df['minutes']= df['minutes'].dt.total_seconds()/60
df.head()


# In[138]:


df.minutes.unique()


# In[70]:


df.minutes.max()


# In[139]:


df.columns= df.columns.str.replace("*","", regex= True)


# In[140]:


pd.DataFrame({'Mean':df.groupby(['PURPOSE'])['MILES'].mean().round(1),
             'Min': df.groupby(['PURPOSE'])['MILES'].min(),
             'Max':df.groupby(['PURPOSE'])['MILES'].max()}).reset_index()


# In[ ]:


#As we have done here the statiscal analysis , i am using boxplot


# In[141]:


plt.figure(figsize=(16,7))
sns.set(rc={'axes.facecolor':'none','figure.facecolor':'yellow'})
plt.subplot(1,2,1)
sns.boxplot(data=df,x=df.PURPOSE, y=df.MILES, palette='pastel')
plt.xticks(rotation=45)
plt.subplot(1,2,2)
sns.boxplot(data=df,x=df.PURPOSE,y=df.minutes,palette='husl')

plt.xticks(rotation=45)


# In[ ]:


#plot without outliers:


# In[142]:


plt.figure(figsize=(16,7))
plt.subplot(1,2,1)
sns.boxplot(data=df,x=df.PURPOSE,y=df.MILES,showfliers=False)
plt.xticks(rotation=45)
plt.subplot(1,2,2)
sns.boxplot(data=df,x=df.PURPOSE,y=df.minutes,showfliers=False)
plt.xticks(rotation=45)


# <font size ="5">Q1 HOW MANY ROUND TRIPS</font>

# In[143]:



def round(x):
    if x['START']==x['STOP']:
        return 'yes'
    else:
        return 'no'
df['Round_TRIP'] = df.apply(round,axis=1)


# In[144]:


df


# In[145]:


df.Round_TRIP.value_counts()


# In[146]:


plt.figure(figsize=(8,5))
sns.set(rc={'axes.facecolor':'none','figure.facecolor':'none'})
def round(x):
    if x['START']==x['STOP']:
        return 'yes'
    else:
        return 'no'
df['Round_TRIP'] = df.apply(round,axis=1)
sns.countplot(df['Round_TRIP'],order = df['Round_TRIP'].value_counts().index)
plt.show()


# <font size ="5">Q2:frequency of trips in each month</font>

# In[147]:


df['month']= pd.DatetimeIndex(df['START_DATE']).month


# In[148]:


df


# In[ ]:


##let me make dictionary for values


# In[149]:


dic = {1:'jan',2:'feb',3:'mar',4:'apr',5:'may',6:'jun',7:'jul',8:'aug',9:'sept',10:'oct',11:'nov',12:'dec'}
df['month'] =df['month'].map(dic)


# In[150]:


df


# In[151]:


plt.figure(figsize=(12,7))
sns.countplot(df['month'],order = df['month'].value_counts().index,palette='deep')
plt.show()


# <font size ="5">Q3 : NUMBER OF ROUND TRIPS IN A MONTH</font>
# 

# In[152]:


plt.figure(figsize=(12,7))
sns.countplot(df['Round_TRIP'],hue=df['month'])
plt.legend()


# <font size ="5">Q4: DISTRIBUTION OF CAB RIDES BASED ON CATEGORY</font>
# 

# In[153]:


plt.figure(figsize=(9,5))
sns.countplot(data=df,x='PURPOSE',hue='CATEGORY',dodge=False)
plt.xticks(rotation=45)


# <font size ="5">Q5 : Where do customers most frequently take cabs Frequency of cab rides start points</font>

# In[154]:


plt.figure(figsize=(15,4))
pd.Series(df['START']).value_counts()[:25].plot(kind='bar')
plt.title('Car rides start location frequency')
plt.xticks(rotation=45)


# <font size ="5">Q6: Where do customers most frequently drop cabs Frequency of cab rides start points</font>
# 
# 

# In[155]:


plt.figure(figsize=(15,4))
pd.Series(df['STOP']).value_counts()[:25].plot(kind='bar')
plt.title('cab rides stop location frequency')
plt.xticks(rotation=45)

