# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import re
from collections import defaultdict
import time
from ast import literal_eval


s_time = time.time()
recipes_df = pd.read_csv(r'C:\Users\Nick\Desktop\data\full_dataframe.csv', na_values=['< 1']).fillna(0)
recipes_df['ingredients'] = recipes_df.ingredients.apply(literal_eval)
recipes_df['recipe_name'] = recipes_df['recipe_name'].astype(str)

recipes_df = recipes_df[recipes_df['total_time'] != 0]


##Initalize dictionary with all of the recipe names and a proportion of 0
recipe_list = defaultdict.fromkeys(recipes_df['recipe_name'].to_list(), 0)


all_ingredients = defaultdict(int)


"""Populate dictionary of all ingredients in recipe csv"""
for ind in recipes_df.index:
    temp_list = recipes_df['ingredients'][ind]
    #li = ast.literal_eval(temp_list)
    for item in temp_list:
        all_ingredients[str(item)] += 1
        
all_ingredients_df = pd.DataFrame(list(all_ingredients.items()), columns = ["Ingredient", "Count"])

    

"""Get n ingredients from user"""
n = int(input("How many main ingredients do you have? "))
user_ingred_list = []
for i in range(0,n):
      user_ingred_list.append(input("Ingredient: "))
    

print("\nUser ingredients: ", user_ingred_list)


"""Get user nutrition preferences"""
print("\n\nAny nutrition preferences? (enter 0, if none)")
user_cals = int(input("Calories: "))
user_carbs = int(input("Carbs (g): "))
user_pro = int(input("Protein (g): "))
user_sod = int(input("Sodium (mg): "))

print("\nPlease wait...\n")

for user_rec in user_ingred_list:
      pattern = ".*(" + user_rec + ").*"
      for i in recipes_df.index:
          ingre_list = recipes_df["ingredients"][i]
          for l in ingre_list:
              result = re.match(pattern, l, flags=re.IGNORECASE)
              if result:
                  recipe_nm = recipes_df['recipe_name'][i]
                  recipe_list[recipe_nm] += 1/n
            

recipes_prop = pd.DataFrame(list(recipe_list.items()), columns = ['recipe_name', 'p'])
recipes_prop = pd.merge(recipes_df, recipes_prop, on = "recipe_name", how = "inner")
recipes_prop = recipes_prop.loc[recipes_prop['p'] > 0.00].reset_index(drop = True)

print("\nNumber of recipes to choose from now... ", len(recipes_prop))


print("\nHow much emphasis on nutritients: (choose from low, med, high) ")


##nutrient weights
nutri_dict = {'low': 1, 'med': 5, 'high': 10}

cal_wgt = nutri_dict[input("Calories? ")]
carbs_wgt = nutri_dict[input("Carbs? ")]
pro_wgt = nutri_dict[input("Protein? ")]
sod_wgt = nutri_dict[input("Sodium? ")]


def filter_recipes(proportion_df, cals, carbs, pro, sod, wcals, wcarbs, wpro, wsod):
    filter_df = proportion_df.copy(deep = True)
    
    if cals > 0:
        filter_df = filter_df.loc[filter_df['calories'] <= cals]
    if carbs > 0:
        filter_df = filter_df.loc[filter_df['carbs'] <= carbs]
    if pro > 0:
        filter_df = filter_df.loc[filter_df['protein'] >= pro]
    if sod > 0:
        filter_df = filter_df.loc[filter_df['sodium'] <= sod]      


    filter_df['n'] = (wcals)/(1 + abs(cals - filter_df['calories'])) + \
                     (wcarbs)/(1 + abs(carbs - filter_df['carbs'])) + \
                     (wpro)/(1 + abs(pro - filter_df['protein'])) + \
                     (wsod)/(1 + abs(sod - filter_df['sodium']))
    
    return filter_df



def recipe_scorer(df):
    
    df['score'] = df['p'] * ((1/(df['total_time'] * df['n_ingredients'])) + df['n'])
    return df


def sort_final(df):
    
    df = df.sort_values(by=['score', 'p'], ascending = False).reset_index(drop = True)
    return df


def final_df(df, ca, cb, p, s, cw, cbw, pw, sw):
    
    filtered_df = filter_recipes(df, ca, cb, p, s, cw, cbw, pw, sw)
    scored_df = recipe_scorer(filtered_df)
    sorted_df = sort_final(scored_df)
    
    return sorted_df[['recipe_name','total_time','ingredients','steps', 'calories', 'protein', 'carbs', 'sodium', 'score']]
    


# ### MAIN ###

test = final_df(recipes_prop, user_cals, user_carbs, user_pro, user_sod, cal_wgt, carbs_wgt, pro_wgt, sod_wgt)
print(test.head(10))
    
e_time = time.time()
print("Time to execute", e_time - s_time)   

