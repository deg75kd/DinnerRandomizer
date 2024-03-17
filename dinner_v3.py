#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np

# desired recipe count
recipe_count = 4
# empty dataframe for recipes
df_this_week = pd.DataFrame()

# pull recipes
xlsx_path = 'meals.xlsx'
df_meals = pd.read_excel(xlsx_path)

# start loop
while True:
    # split into sub-lists
    df_moderate = df_meals[(df_meals['Ease'] == "moderate") | (df_meals['Ease'] == "complex") | (df_meals['Ease'] == "slow cooker")].reset_index(drop=True)
    print(df_moderate)
    print("\n")
    df_fish = df_meals[df_meals['Protein'] == "fish"].reset_index(drop=True)
    print(df_fish)
    print("\n")
    df_veg = df_meals[df_meals['Protein'] == "veg"].reset_index(drop=True)
    print(df_veg)
    print("\n")
    df_easy = df_meals[(df_meals['Ease'] == "quick") & (df_meals['Protein'] != "fish") & (df_meals['Protein'] != "veg")].reset_index(drop=True)
    print(df_easy)
    print("\n")

    # remove fish/veg protein
    
    # randomly select 1 moderate/hard recipe
    rng = np.random.default_rng()
    moderate_ct = df_moderate.shape[0]
    rints = rng.integers(low=0, high=moderate_ct, size=1)
    
    print("Selected moderate recipe {} out of {}".format(rints[0], moderate_ct))
    print(df_moderate.loc[rints[0]])
    
    df_this_week = df_meals[df_meals['MealID'] == df_moderate.loc[rints[0]].MealID]
    
    # remove the carb of the selected moderate/hard recipe from fish
    df_fish = df_fish[df_fish['Carb'].values != df_this_week['Carb'].values].reset_index(drop=True)
    
    # select 1 fish recipe
    fish_ct = df_fish.shape[0]
    rints = rng.integers(low=0, high=fish_ct, size=1)
    
    print("\nSelected fish recipe {} out of {}".format(rints[0], fish_ct))
    print(df_fish.loc[rints[0]])
    
    df_this_week = df_this_week.append(df_meals[df_meals['MealID'] == df_fish.loc[rints[0]].MealID])
    
    # remove carb from veg recipes
    df_veg = df_veg[~df_veg['Carb'].isin(df_this_week['Carb'].values)].reset_index(drop=True)
    
    # select 1 veg recipe
    veg_ct = df_veg.shape[0]
    rints = rng.integers(low=0, high=veg_ct, size=1)

    print("\nSelected veg recipe {} out of {}".format(rints[0],veg_ct))
    print(df_veg.loc[rints[0]])
    
    df_this_week = df_this_week.append(df_meals[df_meals['MealID'] == df_veg.loc[rints[0]].MealID])
    
    # randomly select 1 easy recipe
    easy_ct = df_easy.shape[0]
    rints = rng.integers(low=0, high=easy_ct, size=1)
    
    print("\nSelected easy recipe {} out of {}".format(rints[0], easy_ct))
    print(df_easy.loc[rints[0]])
    
    df_this_week = df_this_week.append(df_meals[df_meals['MealID'] == df_easy.loc[rints[0]].MealID])

    # if any recipe is null, start over
    if (df_this_week.shape[0] < recipe_count):
        print("\nNot enough recipes. Now starting over.")
    else:
        # print selected recipes
        print("\n*************** Meals selected for next week ***************")
        print(df_this_week['MealName'])
        print("\n************************************************************")

        # prompt user to accept recipes
        answer = input("Are you happy with these selections? Y or N")
        cap_answer = answer.upper()
        if (cap_answer == 'Y'):
            break

# if a recipe is rejected, 
#   1. if moderate/hard receipe rejected, prompt user if prefer an easy one
#   2. recreate new list (so the rejected carb can be selected again) and select another random recipe

# after 3 recipes generated and accepted, print shopping list

