# -*- coding: utf-8 -*-
"""
Spyder Editor
Python 3.7.9 v.1916

This is a temporary script file.
"""
"""
########################################## RENDER ALGORITHM ##########################################################

DESCRIPTION OF USER'S VARIABLES:

strict --> "y" for strict filtering of ingredients, "n" for more ordinary recommender

user_ingred_list --> list of ingredients the user wants the recipe to contain

user_banned_ingre --> list of ingredients the user does not want the recipe to contain

time_constraint --> filter recipes that require more time (in minutes)  than the user's especification (0 if no constraint)


user_cals --> user nutrition preferences, maximum number of calories (0, if no preferences)
user_carbs --> user nutrition preferences, maximum number of grams of carbohydrates (0, if no preferences)
user_pro --> user nutrition preferences, minimum number of  grams of proteins(0, if no preferences)
user_sod --> --> user nutrition preferences, maximum number of miligrams of sodium (0, if no preferences)


cal_wgt --> how much emphasis on calories (choose from low, med, high) 
carbs_wgt --> how much emphasis on carbohydrates (choose from low, med, high) 
pro_wgt --> how much emphasis on proteins (choose from low, med, high) 
sod_wgt --> how much emphasis on sodium (choose from low, med, high) 

########################################################################################################################
"""

####################### Defining and initializing variables#########################################

strict ="y"

   
#user_ingred_list = ["chicken","oil","onion", "tomatoe","garlic"]     
#user_ingred_list = ["salmon", "lemon pepper", "garlic"]
#user_ingred_list = ["chicken","lemon","onion","garlic","pepper"]
#user_ingred_list = ["curry", "chicken", "onion","oil"]
#user_ingred_list = ["potato", "egg", "spinach", "tomato", "oil"]
#user_ingred_list = ["potato", "chicken", "spinach", "tomato", "oil"]
#user_ingred_list =["chicken","oil"]      
user_ingred_list = ["spinach","carrot"]


user_banned_ingre = []
#use_banned_ingre = ["water"]


####Time constrain (enter 0, if none)
time_constraint = 12


####Get user nutrition preferences (0, if none)
user_cals = 0
user_carbs = 0
user_pro = 0
user_sod = 0


####How much emphasis on nutritients: (choose from low, med, high)
nutri_dict = {'low': 1, 'med': 5, 'high': 10}
cal_wgt = 1
carbs_wgt = 1
pro_wgt = 1
sod_wgt = 1


#######################################################################################################

import pandas as pd
import re
from collections import defaultdict
import time
from ast import literal_eval
import sys
from statistics import mean

#### This is for visualization on the console when testing
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

#### To measure performance
s_time = time.time()

###################################### FUNCTIONS #########################

def recipes_prop_f(recipe_list,thousands):
    recipes_prop = pd.DataFrame(list(recipe_list.items()), columns = ['recipe_name', 'p'])
    recipes_prop = pd.merge(recipes_df, recipes_prop, on = "recipe_name", how = "inner")
    recipes_prop = recipes_prop.loc[recipes_prop['p'] > 0 ].reset_index(drop = True)
    recipes_prop = recipes_prop.sort_values(by=['p'], ascending = False).reset_index(drop = True)
    recipes_prop = recipes_prop.iloc[:thousands*1000]
    if recipes_prop.shape[0] < 1:
        print("I am sorry the are not recipes matching your preferences")
        sys.exit()
    
    print("\nNumber of recipes to choose from now... ", len(recipes_prop))
    #test_df = recipes_prop[["recipe_name","ingredients","p"]]
    #print("recipes proportiond", recipes_prop.head())
    return recipes_prop

def filter_recipes(proportion_df, cals, carbs, pro, sod, wcals, wcarbs, wpro, wsod, time_constraint):
    filter_df = proportion_df.copy(deep = True)
    
    if cals > 0:
        filter_df = filter_df.loc[filter_df['calories'] <= cals]
    if carbs > 0:
        filter_df = filter_df.loc[filter_df['carbs'] <= carbs]
    if pro > 0:
        filter_df = filter_df.loc[filter_df['protein'] >= pro]
    if sod > 0:
        filter_df = filter_df.loc[filter_df['sodium'] <= sod]
        
    if time_constraint > 0:
        filter_df = filter_df.loc[filter_df["total_time"] <= time_constraint]
        
                        # denominators are average values for all the recipies 
    filter_df['nutr'] = (wcals)/(1 + abs(cals - filter_df['calories'])/avg_cals) + \
                      (wcarbs)/(1 + abs(carbs - filter_df['carbs'])/avg_carbs) + \
                      (wpro)/(1 + abs(pro - filter_df['protein'])/avg_pro) + \
                      (wsod)/(1 + abs(sod - filter_df['sodium'])/avg_sod)
    
    return filter_df



def recipe_scorer(df, coeff_p = 1,coeff_tt = 1, coeff_ni = 1, coeff_nutr = 1):  
    
    df['score'] = coeff_p * df['p'] + coeff_tt * (1/(df['total_time']/avg_tt)\
                  + coeff_ni * (1/df['n_ingredients']/avg_ni) + coeff_nutr * df['nutr'])
    return df

def sort_final(df):
    df = df.sort_values(by=['score', 'p'], ascending = False).reset_index(drop = True)
    return df


def final_df(df, ca, cb, p, s, cw, cbw, pw, sw):
    
    filtered_df = filter_recipes(df, ca, cb, p, s, cw, cbw, pw, sw, time_constraint)
    scored_df = recipe_scorer(filtered_df)
    sorted_df = sort_final(scored_df)
    
    return sorted_df[['recipe_name','total_time','ingredients','steps', 'calories', 'protein', 'carbs', 'sodium', 'p', 'score']]

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
            if final.shape[0] > 0:
                print(final.head(final.shape[0]))#it will print whatever it has found
            else:
                print("Sorry, we couldn't find a recipe fulfilling your preferences")
                sys.exit()
        thousands += 1
        check_final(recipes_prop_f(recipe_list,thousands), user_cals, user_carbs, user_pro,\
                    user_sod, cal_wgt, carbs_wgt, pro_wgt, sod_wgt,time_constraint, recipe_list, thousands)
        
############################### END FUNCTIONS ################################

#### Getting the data
recipes_df = pd.read_csv('full_dataframe.csv', na_values=['< 1']).fillna(0)
recipes_df['ingredients'] = recipes_df.ingredients.apply(literal_eval)
recipes_df['recipe_name'] = recipes_df['recipe_name'].astype(str)
recipes_df = recipes_df[recipes_df['total_time'] != 0]
recipes_df = recipes_df.drop_duplicates(subset=['recipe_name'])
recipes_df['n_steps'] = recipes_df['n_steps'].astype(int)

####Getting averages
outliers = int(round(len(recipes_df)*0.05,0)) #used to drop 5% top and bottom outliers

for col in ["n_ingredients","n_steps", "total_time","calories", "carbs", "sodium", "protein"]:
    temp_list = list(recipes_df[col])
    temp_list.sort()
    temp_list = temp_list[outliers:len(recipes_df) - outliers]# droping outliers
    if col == "n_ingredients":
        avg_ni = mean(temp_list)
    if col == "n_steps":
        avg_ns = mean(temp_list)
    if col == "total_time":
        avg_tt = mean(temp_list)
    if col == "calories":
        avg_cals = mean(temp_list)
    if col == "carbs":
        avg_carbs = mean(temp_list)
    if col == "sodium":
        avg_sod = mean(temp_list)
    if col == "protein":
        avg_pro = mean(temp_list)
        
        
#print(avg_ni,avg_ns,avg_tt,avg_cals,avg_carbs,avg_sod,avg_pro)

####Initalize dictionary with all of the recipe names and a proportion of 0
recipe_list = defaultdict.fromkeys(recipes_df['recipe_name'].to_list(), 0)

####Initialize dictionary
all_ingredients = defaultdict(int)


####Populate dictionary of all ingredients in recipe csv
for ind in recipes_df.index:
    temp_list = recipes_df['ingredients'][ind]
    for item in temp_list:
        all_ingredients[str(item)] += 1
          

print("\nUser ingredients: ", user_ingred_list)

print("\nPlease wait...\n")


### Filtering recipe strictly for ingredients
n = len(user_ingred_list)
if strict == "n":
    recipes_df = recipes_df[recipes_df["n_ingredients"] <= n] 
    pass


####Filtering: proportions and banned ingredients
for index, row in recipes_df.iterrows():
    ingre_list = row['ingredients'].copy()
    nn = len(ingre_list)
    if strict == "y":
        nn = len(ingre_list) * 0.001 # the priority is: the ingredients in recipe are in user's ingredients --> Minimalist list of ingredients
    else:
        nn = n # the priority is: the user´s ingredients are in recipe's ingredients -->  Long list of ingredients
    for user_rec in user_ingred_list:
        r = re.compile(r".*\b("+user_rec+")\\b", flags=re.IGNORECASE)
        match = list(filter(r.match, ingre_list))
        if match:
            if user_banned_ingre != []:
                for user_ban in user_banned_ingre:
                    r_1 = re.compile(r".*\b("+user_ban+")\\b", flags=re.IGNORECASE)
                    match_1 = list(filter(r_1.match, ingre_list))
                    if not match_1:
                        recipe_list[row['recipe_name']] += 1/nn
                        ingre_list.remove(match[0])
            else:
               recipe_list[row['recipe_name']] += 1/nn
               ingre_list.remove(match[0])
        


#################### MAIN #############################
  
#### Calling function to sort in chunks of 1000 (or less) recipes with highest proportions
recipes_prop = recipes_prop_f(recipe_list=recipe_list, thousands = 1)


# Calling function for final check     
check_final(recipes_prop, user_cals, user_carbs, user_pro,\
            user_sod, cal_wgt, carbs_wgt, pro_wgt, sod_wgt,time_constraint, recipe_list, thousands = 1)


####Checking time for testing
e_time = time.time()
print("Time to execute", e_time - s_time)   

