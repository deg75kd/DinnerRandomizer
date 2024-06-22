#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np

# desired recipe count
recipe_count = 4
# pull recipes
#xlsx_path = 'C:\Users\Kevin\DS\Dinner Randomizer\meals.xlsx'
#xlsx_path = 'C:\Users\Kevin\DS\Dinner Randomizer\meals.xlsx'
xlsx_path = 'meals.xlsx'
df_meals = pd.read_excel(xlsx_path)
# df_meals = pd.read_excel("C:/Users/Kevin/DS/Dinner Randomizer/meals.xlsx")

# create empty dataframe for rated recipes
list_col = df_meals.columns.tolist()
df_multi = pd.DataFrame(columns=list_col)

# add recipes with duplicates
for index, row in df_meals.iterrows():
    for i in range(row['Rating']):
        df_multi = df_multi.append(
            {
                'MealID': row['MealID'], 
                'MealName': row['MealName'], 
                'Carb': row['Carb'],
                'Protein': row['Protein'],
                'Veg': row['Veg'],
                'Ease': row['Ease'],
                'Rating': row['Rating']
            },
            ignore_index=True
        )

# start loop
while True:
    # empty dataframe for recipes
    df_this_week = pd.DataFrame()

    # split into sub-lists
    df_moderate = df_multi[(df_multi['Ease'] == "moderate") | (df_multi['Ease'] == "complex") | (df_multi['Ease'] == "slow cooker")].reset_index(drop=True)
    print(df_moderate)
    print("\n")
    df_fish = df_multi[df_multi['Protein'] == "fish"].reset_index(drop=True)
    print(df_fish)
    print("\n")
    df_veg = df_multi[df_multi['Protein'] == "veg"].reset_index(drop=True)
    print(df_veg)
    print("\n")
    df_easy = df_multi[(df_multi['Ease'] == "quick") & (df_multi['Protein'] != "fish") & (df_multi['Protein'] != "veg")].reset_index(drop=True)
    print(df_easy)
    print("\n")

    # remove fish/veg protein
    
    # select 1 veg recipe
    rng = np.random.default_rng()
    veg_ct = df_veg.shape[0]
    rints = rng.integers(low=0, high=veg_ct, size=1)

    print("\nSelected veg recipe {} out of {}".format(rints[0],veg_ct))
    print(df_veg.loc[rints[0]])
    
    df_this_week = df_this_week.append(df_meals[df_meals['MealID'] == df_veg.loc[rints[0]].MealID])
    
    # select 1 fish recipe
    fish_ct = df_fish.shape[0]
    rints = rng.integers(low=0, high=fish_ct, size=1)
    
    print("\nSelected fish recipe {} out of {}".format(rints[0], fish_ct))
    print(df_fish.loc[rints[0]])
    
    df_this_week = df_this_week.append(df_meals[df_meals['MealID'] == df_fish.loc[rints[0]].MealID])
    
    # remove the carb of the fish/veg recipe from moderate/hard
    # df_moderate = df_moderate[df_moderate['Carb'].values != df_this_week['Carb'].values].reset_index(drop=True)
    df_moderate = df_moderate[~df_moderate['Carb'].isin(df_this_week['Carb'].values)].reset_index(drop=True)
    # remove the carb of the fish/veg recipe from 
    df_easy = df_easy[~df_easy['Carb'].isin(df_this_week['Carb'].values)].reset_index(drop=True)
    
    # select 1 moderate/hard recipe
    moderate_ct = df_moderate.shape[0]
    rints = rng.integers(low=0, high=moderate_ct, size=1)
    
    print("\nSelected moderate recipe {} out of {}".format(rints[0], moderate_ct))
    print(df_moderate.loc[rints[0]])
    
    df_this_week = df_this_week.append(df_meals[df_meals['MealID'] == df_moderate.loc[rints[0]].MealID])
    
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
        answer = input("\nAre you happy with these selections? Y or N")
        cap_answer = answer.upper()
        if (cap_answer == 'Y'):
            break

# if a recipe is rejected, 
#   1. if moderate/hard receipe rejected, prompt user if prefer an easy one
#   2. recreate new list (so the rejected carb can be selected again) and select another random recipe

# after 3 recipes generated and accepted, print shopping list

