#!/usr/bin/env python
# coding: utf-8

# In[99]:


import pandas as pd
import numpy as np


# In[100]:


recipe_count = 4


# In[101]:


recipe_list = []
carb_list = []


# ### pull recipes

# In[102]:


# xlsx_path = 'C:\Users\Kevin\DS\Dinner Randomizer\meals.xlsx'
xlsx_path = 'meals.xlsx'
df_meals = pd.read_excel(xlsx_path)


# In[103]:


df_meals.head()


# ### split into sub-lists

# In[104]:


df_moderate = df_meals[(df_meals['Ease'] == "moderate") | (df_meals['Ease'] == "complex") | (df_meals['Ease'] == "slow cooker")].reset_index(drop=True)
df_moderate.head()


# In[105]:


df_easy = df_meals[df_meals['Ease'] == "quick"].reset_index(drop=True)
df_easy.head()


# In[106]:


df_fish = df_meals[df_meals['Protein'] == "fish"].reset_index(drop=True)
df_fish


# In[107]:


df_veg = df_meals[df_meals['Protein'] == "veg"].reset_index(drop=True)
df_veg


# ### randomly select 1 moderate/hard recipe

# In[108]:


# get recipe count
moderate_ct = df_moderate.shape[0]
moderate_ct


# In[109]:


rng = np.random.default_rng()
rints = rng.integers(low=0, high=moderate_ct, size=1)
print(df_moderate.loc[rints[0]])


# In[110]:


df_moderate.loc[rints[0]].MealID
recipe_list.append(df_moderate.loc[rints[0]].MealID)
recipe_list


# In[111]:


df_this_week = df_meals[df_meals['MealID'] == df_moderate.loc[rints[0]].MealID]
df_this_week


# ### find the carb of the selected moderate/hard recipe and remove from fish

# In[112]:


df_this_week['Carb']


# In[113]:


#df_easy = df_easy[df_easy['Carb'] != carb_list[0]]
#df_easy = df_easy[df_easy['Carb'] != df_this_week['Carb']]
#df_easy.head()
#df_easy['Carb'].values != df_this_week['Carb'].values
#df_fish[df_fish['Carb'].values != df_this_week['Carb'].values]
df_fish = df_fish[df_fish['Carb'].values != df_this_week['Carb'].values].reset_index(drop=True)
df_fish


# In[114]:


fish_ct = df_fish.shape[0]
fish_ct


# ### select 1 fish recipe

# In[115]:


rints = rng.integers(low=0, high=fish_ct, size=1)
#rints[0]
#df_fish.loc[1]
df_fish.loc[rints[0]]


# In[116]:


df_this_week = df_this_week.append(df_meals[df_meals['MealID'] == df_fish.loc[rints[0]].MealID])
df_this_week


# ### remove carb from veg recipes

# In[130]:


#df_this_week['Carb'].values
#df_veg['Carb'].values
#df_veg['Carb'].values != df_this_week['Carb'].values
#df_veg['Carb'].isin(df_this_week['Carb'].values)
#condition = df_veg['Carb'].isin(df_this_week['Carb'].values)
#condition
#df_veg[~condition]
#df_veg[~df_veg['Carb'].isin(df_this_week['Carb'].values)]
#df_veg[df_veg['Carb'].values != df_this_week['Carb'].values]
#df_veg = df_veg[df_veg['Carb'].values != df_this_week['Carb'].values]
df_veg = df_veg[~df_veg['Carb'].isin(df_this_week['Carb'].values)]
df_veg


# In[131]:


veg_ct = df_veg.shape[0]
veg_ct


# ### select 1 veg recipe

# In[132]:


rints = rng.integers(low=0, high=veg_ct, size=1)
df_veg.loc[rints[0]]


# In[133]:


#df_meals[df_meals['MealID'] == df_fish.loc[rints[0]].MealID]
#df_choice = df_meals[df_meals['MealID'] == df_veg.loc[rints[0]].MealID]
#df_choice
#df_this_week = df_this_week.append(df_choice)
#df_this_week.append(df_meals[df_meals['MealID'] == df_veg.loc[rints[0]].MealID])
df_this_week = df_this_week.append(df_meals[df_meals['MealID'] == df_veg.loc[rints[0]].MealID])
df_this_week


# ### randomly select 1 easy recipe

# In[134]:


rints = rng.integers(low=0, high=easy_ct, size=1)
#rints[0]
df_easy.loc[rints[0]]


# In[135]:


df_this_week = df_this_week.append(df_meals[df_meals['MealID'] == df_easy.loc[rints[0]].MealID])
df_this_week


# ### if any recipe is null, start over

# In[136]:


df_this_week.shape[0]


# In[137]:


if (df_this_week.shape[0] < recipe_count):
    print("Oops, I need to start over!")
else:
    print(df_this_week['MealName'])


# In[ ]:


# print selected recipes


# ### prompt user to accept recipes

# In[ ]:


while True:
    answer = input("Are you happy with this selection? Y or N")
    cap_answer = answer.upper()
    if (cap_answer == 'Y') or (cap_answer == 'N'):
        break


# In[ ]:


# if a recipe is rejected, 
#   1. if moderate/hard receipe rejected, prompt user if prefer an easy one
#   2. recreate new list (so the rejected carb can be selected again) and select another random recipe


# In[ ]:


# after 3 recipes generated and accepted, print shopping list

