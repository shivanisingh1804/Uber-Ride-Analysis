#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


dataset  = pd.read_csv("UberDataset.csv")


# In[3]:


dataset


# In[4]:


dataset.shape


# In[5]:


dataset.info()


# # data Preprosessing 

# In[6]:


dataset['PURPOSE'].fillna("NOT",inplace = True)


# In[7]:


dataset.head()


# In[8]:


dataset['START_DATE'] = pd.to_datetime(dataset['START_DATE'],errors = 'coerce')
dataset['END_DATE'] = pd.to_datetime(dataset['END_DATE'],errors = 'coerce')


# In[9]:


dataset.info()


# In[10]:


dataset.head()


# In[11]:


from datetime import datetime
dataset['date'] = pd.to_datetime(dataset['START_DATE']).dt.date
dataset['time'] = pd.to_datetime(dataset['START_DATE']).dt.hour


# In[12]:


dataset.head()


# In[13]:


dataset['day/night'] = pd.cut(
    x=dataset['time'],
    bins=[0, 10, 15, 19, 24],
    labels=['Morning', 'Afternoon', 'Evening', 'Night'],
    right=False  # optional: controls bin edge inclusion
)


# In[14]:


dataset.head()


# In[15]:


dataset.dropna(inplace= True)


# In[16]:


dataset.shape


# # DATA VISUALIZATION

# In[22]:


plt.figure(figsize = (20,5))
plt.subplot(1,2,1)
sns.countplot(x='CATEGORY', data=dataset)
plt.subplot(1,2,2)
sns.countplot(x= 'PURPOSE', data = dataset)


# In[23]:


sns.countplot(x='day/night', data= dataset)


# In[25]:


# Step 1: Extract month from START_DATE
dataset['Month'] = pd.to_datetime(dataset['START_DATE']).dt.month

# Step 2: Create month labels
month_label = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr",
    5: "May", 6: "June", 7: "July", 8: "Aug",
    9: "Sept", 10: "Oct", 11: "Nov", 12: "Dec"
}

# Step 3: Map month number to month name
dataset['Month'] = dataset['Month'].map(month_label)

# Step 4: Count by month
mon = dataset['Month'].value_counts(sort=False)


# In[26]:


dataset.head()


# In[31]:


df = pd.DataFrame({
    "Months" : mon.values,
    "Value Count": dataset.groupby('Month', sort= False)['MILES'].max()
})

p = sns.lineplot(data= df)
p.set(xlabel = "Months" , ylabel = "Value Count")


# In[33]:


dataset.head()


# In[34]:


dataset['Day']= dataset.START_DATE.dt.weekday

day_label = {
    0: 'Mon' , 1:'Tue',2:'Wed',3:'Thrus',4:'Fri',5:'Sat',6:'Sun'}
dataset['Day'] = dataset['Day'].map(day_label)


# In[35]:


dataset.head()


# In[39]:


day_label = dataset.Day.value_counts()

# Bar plot
sns.barplot(x=day_label.index, y=day_label.values)

# Set axis labels
plt.xlabel('Day')
plt.ylabel('COUNT')
plt.title('Count of Records by Day')
plt.xticks(rotation=45)  # Optional: rotate labels if needed
plt.show()


# In[43]:


sns.boxplot(dataset['MILES'])


# In[44]:


sns.boxplot(dataset[dataset['MILES']<100]['MILES'])


# In[46]:


sns.distplot(dataset[dataset['MILES']<40]['MILES'])


# In[ ]:




