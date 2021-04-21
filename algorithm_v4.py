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
import sys

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


s_time = time.time()
recipes_df = pd.read_csv('full_dataframe.csv', na_values=['< 1']).fillna(0)
recipes_df['ingredients'] = recipes_df.ingredients.apply(literal_eval)
recipes_df['recipe_name'] = recipes_df['recipe_name'].astype(str)

recipes_df = recipes_df[recipes_df['total_time'] != 0]
recipes_df = recipes_df.drop_duplicates(subset=['recipe_name'])




##Initalize dictionary with all of the recipe names and a proportion of 0
recipe_list = defaultdict.fromkeys(recipes_df['recipe_name'].to_list(), 0)


all_ingredients = defaultdict(int)


"""Populate dictionary of all ingredients in recipe csv"""
for ind in recipes_df.index:
    temp_list = recipes_df['ingredients'][ind]
    #li = ast.literal_eval(temp_list)
    for item in temp_list:
        all_ingredients[str(item)] += 1
        
#all_ingredients_df = pd.DataFrame(list(all_ingredients.items()), columns = ["Ingredient", "Count"])
#all_ingredients_df.to_csv(r'ingredient_list.csv', index= False, header = True)

    

"""Get n ingredients from user"""
#n = int(input("How many main ingredients do you have? "))#
user_ingred_list = []
#for i in range(0,n):
      #user_ingred_list.append(input("Ingredient: "))    
      #pass
      
#user_ingred_list = ["chicken","oil","onion", "tomatoe","garlic"]     
#user_ingred_list = ["salmon", "lemon pepper", "garlic"]
#user_ingred_list = ["chicken","lemon","onion","garlic","pepper"]
#user_ingred_list = ["curry", "chicken", "onion","oil"]
#user_ingred_list = ["potato", "egg", "spinach", "tomato", "oil"]
user_ingred_list = ["potato", "chicken", "spinach", "tomato", "oil"]
#user_ingred_list =["chicken","oil"]
n=len(user_ingred_list)

print("\nUser ingredients: ", user_ingred_list)


print("\nPlease wait...\n")

'''
def strict_filter():
    for index, row in recipes_df.iterrows():
        ingre_list = row['ingredients']
        for user_rec in user_ingred_list:
            r = re.compile(".*(" + user_rec + ").*", flags=re.IGNORECASE)
            match = list(filter(r.match, ingre_list))
            if match:
                pass
'''                

""" Recipe strictly for ingredients?"""
strict = "y"# input("Do you want a recipe strictly for your ingredients?(y/n)")

if strict == "y":
    recipes_df = recipes_df[recipes_df["n_ingredients"] <= n]
    
    pass
    

    
#print(strict_df.head())

"""
# Method 1
for index, row in recipes_df.iterrows():
    ingre_list = row['ingredients']
    nn = len(ingre_list)
    if strict == "y":
        nn=n * 0.00001
    for user_rec in user_ingred_list:
        r = re.compile(".*(" + user_rec + ").*", flags=re.IGNORECASE)
        match = list(filter(r.match, ingre_list))
        if match:
            recipe_list[row['recipe_name']] += 1/nn
            # To consider that the ingredient is in the recipe name
            #temp = " " + user_rec + " "
            #temp1 = " " + user_rec
            #temp2 = user_rec + " "
            #if (temp in row['recipe_name']) or (temp1 in row['recipe_name']) or (temp in row['recipe_name']):
             #   recipe_list[row['recipe_name']] += 5/nn
        else:
            recipe_list[row['recipe_name']] -= 1/nn
"""            
#Method 2
for index, row in recipes_df.iterrows():
    ingre_list = row['ingredients'].copy()
    nn = len(ingre_list)
    if strict == "y":
        nn = len(ingre_list) * 0.001 # the priority is: the ingredients in recipe are in user's ingredients --> Minimalist list of ingredients
    else:
        nn = n # the priority is: the user´s ingredients are in recipe's ingredients -->  Long list of ingredients
    for user_rec in user_ingred_list:
        #r = re.compile(".*(" + user_rec + ").*", flags=re.IGNORECASE)
        r = re.compile(r".*\b("+user_rec+")\\b", flags=re.IGNORECASE)
        match = list(filter(r.match, ingre_list))
        if match:
            recipe_list[row['recipe_name']] += 1/nn
            ingre_list.remove(match[0])
            # To consider that the ingredient is in the recipe name
            #temp = " " + user_rec + " "
            #temp1 = " " + user_rec
            #temp2 = user_rec + " "
            #if (temp in row['recipe_name']) or (temp1 in row['recipe_name']) or (temp in row['recipe_name']):
            #    recipe_list[row['recipe_name']] += 2/nn
        
          
                  
def recipes_prop_f(recipe_list,thousands):
    recipes_prop = pd.DataFrame(list(recipe_list.items()), columns = ['recipe_name', 'p'])
    recipes_prop = pd.merge(recipes_df, recipes_prop, on = "recipe_name", how = "inner")
    recipes_prop = recipes_prop.loc[recipes_prop['p'] > 0.00 ].reset_index(drop = True)
    recipes_prop = recipes_prop.sort_values(by=['p'], ascending = False).reset_index(drop = True)
    recipes_prop = recipes_prop.iloc[:thousands*1000]
    return recipes_prop

recipes_prop = recipes_prop_f(recipe_list=recipe_list, thousands = 1)

#print(recipes_prop.head(5))

print("\nNumber of recipes to choose from now... ", len(recipes_prop))
test_df = recipes_prop[["recipe_name","ingredients","p"]]


"""Get user nutrition preferences"""
print("\n\nAny nutrition preferences? (enter 0, if none)")
user_cals = 0#int(input("Calories: "))
user_carbs = 0#int(input("Carbs (g): "))
user_pro = 0# int(input("Protein (g): "))
user_sod = 0 #int(input("Sodium (mg): "))

print("\nHow much emphasis on nutritients: (choose from low, med, high) ")


##nutrient weights
nutri_dict = {'low': 1, 'med': 5, 'high': 10}

cal_wgt = 1#nutri_dict[input("Calories? ")]
carbs_wgt = 1#nutri_dict[input("Carbs? ")]
pro_wgt = 1# nutri_dict[input("Protein? ")]
sod_wgt = 1#nutri_dict[input("Sodium? ")]


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


    # filter_df['n'] = (wcals)/(1 + abs(cals - filter_df['calories'])) + \
    #                  (wcarbs)/(1 + abs(carbs - filter_df['carbs'])) + \
    #                  (wpro)/(1 + abs(pro - filter_df['protein'])) + \
    #                  (wsod)/(1 + abs(sod - filter_df['sodium']))
    filter_df['n'] = (wcals/4)/(1 + abs(cals - filter_df['calories'])/2300) + \
                      (wcarbs/4)/(1 + abs(carbs - filter_df['carbs'])/200) + \
                      (wpro/4)/(1 + abs(pro - filter_df['protein'])/100) + \
                      (wsod/4)/(1 + abs(sod - filter_df['sodium'])/2300)
    
    return filter_df



def recipe_scorer(df):
    
    #df['score'] = df['p'] * ((1/(df['total_time'] * df['n_ingredients'])) + df['n'])
    df['score'] =  10 * df['p'] + (10/(df['total_time']/60)\
                    + (10 /df['n_ingredients']/10) + df['n'])
    return df


def sort_final(df):
    df = df.sort_values(by=['score', 'p'], ascending = False).reset_index(drop = True)
    return df


def final_df(df, ca, cb, p, s, cw, cbw, pw, sw):
    
    filtered_df = filter_recipes(df, ca, cb, p, s, cw, cbw, pw, sw)
    scored_df = recipe_scorer(filtered_df)
    sorted_df = sort_final(scored_df)
    
    return sorted_df[['recipe_name','total_time','ingredients','steps', 'calories', 'protein', 'carbs', 'sodium', 'p', 'score']]
    

time_constraint = 0#int(input("\nTime constraints? (enter 0, if none): "))


# ### MAIN ###
#thousands = 1
#user_recs = final_df(recipes_prop, user_cals, user_carbs, user_pro, user_sod, cal_wgt, carbs_wgt, pro_wgt, sod_wgt)
#if time_contraint != 0:
#    final = user_recs.loc[user_recs['total_time'] <= time_contraint].reset_index(drop = True)
    
        
def check_final(recipes_prop, user_cals, user_carbs, user_pro,\
                user_sod, cal_wgt, carbs_wgt, pro_wgt, sod_wgt,time_constraint, recipe_list, thousands ):
    
    user_recs = final_df(recipes_prop, user_cals, user_carbs, user_pro,\
                         user_sod, cal_wgt, carbs_wgt, pro_wgt, sod_wgt)
    
    if time_constraint !=0:
        final = user_recs.loc[user_recs['total_time'] <= time_constraint]\
        .reset_index(drop = True)
    else:
        final = user_recs
        print("Number of recipes found: ", final.shape[0])
        print("Number of recipes screened:", thousands*1000) 
        
    if final.shape[0]>=20:
        print(final.head(20))
    else:
        if thousands*1000 > len(recipes_df):
            print("Sorry, we couldn't find a recipe fulfilling your preferences")
            sys.exit()
        thousands += 1
        check_final(recipes_prop_f(recipe_list,thousands), user_cals, user_carbs, user_pro,\
                    user_sod, cal_wgt, carbs_wgt, pro_wgt, sod_wgt,time_constraint, recipe_list, thousands)
        
        
check_final(recipes_prop, user_cals, user_carbs, user_pro,\
            user_sod, cal_wgt, carbs_wgt, pro_wgt, sod_wgt,time_constraint, recipe_list, thousands = 1)

e_time = time.time()
print("Time to execute", e_time - s_time)   
