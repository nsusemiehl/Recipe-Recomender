# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import re
from collections import defaultdict
import sys

recipes = { 
    0 : {
        'Recipe' : 'Chicken Tacos',
        'Ingredients' : ["chicken breast", "rice", "tortillas", "shredded cheese"],
        'Number of Ingredients': 4,
        'Steps' : "Cook this..",
        'Number of Steps': 6,
        'Cooking Time' : 45,
        'Calories': 1234,
        'Protein' : 25,
        'Carbs' : 50,
        'Cholesterol' : 15,
        'Sodium' : 350
        },
    1 : {
        'Recipe' : 'Chicken Spaghetti',
        'Ingredients' : ["chicken", "spaghetti noodles", "shredded cheese", "spaghetti sauce"],
        'Number of Ingredients': 4,
        'Steps' : "Boil this...",
        'Number of Steps': 8,
        'Cooking Time' : 110,
        'Calories': 2443,
        'Protein' : 30,
        'Carbs' : 45,
        'Cholesterol' : 8,
        'Sodium' : 230
        },
    2 : {
        'Recipe' : 'Chicken Alfredo',
        'Ingredients' : ["chicken breast", "alfredo sauce", "linguine noodles", "broccoli", "parmesan cheese"],
        'Number of Ingredients': 5,
        'Steps' : "Stir this...",
        'Number of Steps': 8,
        'Cooking Time' : 120,
        'Calories': 1890,
        'Protein' : 37,
        'Carbs' : 43,
        'Cholesterol' : 12,
        'Sodium' : 289
        }
}
recipes_df = pd.DataFrame(recipes)
recipes_df = recipes_df.transpose()



##Initalize dictionary with all of the recipe names and a proportion of 0
recipe_list = defaultdict.fromkeys([recipe["Recipe"] for id, recipe in recipes.items()], 0)
all_ingredients = defaultdict(int)


"""Populate dictionary of all ingredients in recipe csv"""
for id, recipe in recipes.items():
        ingred_list = recipe["Ingredients"]
        for l in ingred_list:
            all_ingredients[l] += 1

all_ingredients_df = pd.DataFrame(list(all_ingredients.items()), columns = ["Ingredient", "Count"])

print(all_ingredients_df.head(11))

# def menu():
    

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
user_chols = int(input("Cholesterol (mg): "))
user_pro = int(input("Protein (g): "))
user_sod = int(input("Sodium (mg): "))

for user_rec in user_ingred_list:
    pattern = ".*(" + user_rec + ").*"
    for id, recipe in recipes.items():
        ingre_list = recipe["Ingredients"]
        for l in ingre_list:
            result = re.match(pattern, l, flags=re.IGNORECASE)
            if result:
                recipe_list[recipe["Recipe"]] += 1/len(user_ingred_list)
            
            
recipes_prop = pd.DataFrame(list(recipe_list.items()), columns = ['Recipe', 'P'])
recipes_prop = pd.merge(recipes_df[["Recipe", "Cooking Time", "Calories", "Protein", "Carbs", "Cholesterol", "Sodium"]], recipes_prop, on = "Recipe", how = "inner")
recipes_prop = recipes_prop.loc[recipes_prop['P'] > 0.00].reset_index(drop = True)




def filter_recipes(proportion_df, cals, carbs, chols, pro, sod):
    filter_df = proportion_df.copy(deep = True)
    
    if cals > 0:
        filter_df = filter_df.loc[filter_df['Calories'] <= cals]
    if carbs > 0:
        filter_df = filter_df.loc[filter_df['Carbs'] <= carbs]
    if chols > 0:
        filter_df = filter_df.loc[filter_df['Cholesterol'] <= chols]
    if pro > 0:
        filter_df = filter_df.loc[filter_df['Protein'] >= pro]
    if sod > 0:
        filter_df = filter_df.loc[filter_df['Sodium'] <= sod]      
        
    return filter_df



def nutrition_score(df):
    
    df['N'] = 0.710 - 0.00398*df['Cholesterol'] - 0.00254*df['Sodium'] - 0.0300*df['Carbs'] + 0.123*df["Protein"]
    return df


def recipe_scorer(df):
    
   df['Score'] = df['P'] * df['Cooking Time'] + df['N']
   return df


def sort_final(df):
    
    df = df.sort_values(by=['Score', 'P'], ascending = False).reset_index(drop = True)
    return df

def final_df(df, ca, cb, ch, p, s):
    
    filtered_df = filter_recipes(df, ca, cb, ch, p, s)
    nutrit_df = nutrition_score(filtered_df)
    scored_df = recipe_scorer(nutrit_df)
    sorted_df = sort_final(scored_df)
    
    return sorted_df[['Recipe','Cooking Time', 'Calories', 'Protein', 'Carbs', 'Cholesterol', 'Sodium', 'Score']]
    


##Interactive on-click feature to expand recipe and instructions
def get_details(recipe_name):
    
    cook_time = recipes_df.loc[recipes_df['Recipe'] == recipe_name, 'Cooking Time'].iloc[0]
    instructions = recipes_df.loc[recipes_df['Recipe'] == recipe_name, 'Steps'].iloc[0]
    ingredients = recipes_df.loc[recipes_df['Recipe'] == recipe_name, 'Ingredients'].iloc[0]
    pass



### MAIN ###

test = final_df(recipes_prop, user_cals, user_carbs, user_chols, user_pro, user_sod)
print(test)
    
    
#selection = input("Select recipe for ingredients and instuctions: ")
