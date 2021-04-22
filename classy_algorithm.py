# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""
"""
########################################## RENDER ALGORITHM ##########################################################
DESCRIPTION OF USER'S VARIABLES:
strict --> "y" for strict filtering of ingredients, "n" for more ordinary recommender
user_ingred_list --> list of ingredients the user wants the recipe to contain
user_banned_ingre --> list of ingredients the user does not want the recipe to contain
time_constraint --> filter recipes that require more time than the user's especification (0 if no constraint)
user_cals --> user nutrition preferences, number of calories (0, if no preferences)
user_carbs --> user nutrition preferences, number of grams of carbohydrates (0, if no preferences)
user_pro --> user nutrition preferences, number of  grams of proteins(0, if no preferences)
user_sod --> --> user nutrition preferences, number of miligrams of sodium (0, if no preferences)
cal_wgt --> how much emphasis on calories (choose from low, med, high) 
carbs_wgt --> how much emphasis on carbohydrates (choose from low, med, high) 
pro_wgt --> how much emphasis on proteins (choose from low, med, high) 
sod_wgt --> how much emphasis on sodium (choose from low, med, high) 
########################################################################################################################
"""
##########################################
import pandas as pd
import re
from collections import defaultdict
import time
from ast import literal_eval
import sys
####################### Defining and initializing variables#########################################

class Algorithm():
    def __init__(self,time_constraint, recipes_df):
        # self.strict = strict
        # self.user_ingred_list = user_ingred_list
        # self.user_banned_ingre = user_banned_ingre
        self.time_constraint = time_constraint
        # self.user_cals = user_cals
        # self.user_carbs = user_carbs
        # self.user_pro = user_pro
        # self.user_sod = user_sod
        # self.nutri_dict = {'low': 1, 'med': 5, 'high': 10}
        # self.cal_wgt = cal_wgt
        # self.carbs_wgt = carbs_wgt
        # self.pro_wgt = pro_wgt
        # self.sod_wgt = sod_wgt
        self.recipes_df = recipes_df
###################################### FUNCTIONS #########################

    def recipes_prop_f(self,recipe_list,thousands):
        recipes_prop = pd.DataFrame(list(recipe_list.items()), columns = ['recipe_name', 'p'])
        recipes_prop = pd.merge(self.recipes_df, recipes_prop, on = "recipe_name", how = "inner")
        recipes_prop = recipes_prop.loc[recipes_prop['p'] > 0.00 ].reset_index(drop = True)
        recipes_prop = recipes_prop.sort_values(by=['p'], ascending = False).reset_index(drop = True)
        recipes_prop = recipes_prop.iloc[:thousands*1000]
        
        print("\nNumber of recipes to choose from now... ", len(recipes_prop))
        #test_df = recipes_prop[["recipe_name","ingredients","p"]]
        #print("recipes proportiond", recipes_prop.head())
        return recipes_prop
    
    def filter_recipes(self,proportion_df, cals, carbs, pro, sod, wcals, wcarbs, wpro, wsod, time_constraint):
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
        filter_df['nutr'] = (wcals)/(1 + abs(cals - filter_df['calories'])/400) + \
                          (wcarbs)/(1 + abs(carbs - filter_df['carbs'])/40) + \
                          (wpro)/(1 + abs(pro - filter_df['protein'])/35) + \
                          (wsod)/(1 + abs(sod - filter_df['sodium'])/600)
        
        return filter_df
    
    
    
    def recipe_scorer(self,df, coeff_p = 1,coeff_tt = 1, coeff_ni = 1, coeff_nutr = 1):  
        
        df['score'] = coeff_p * df['p'] + coeff_tt * (1/(df['total_time']/60)\
                      + coeff_ni * (1/df['n_ingredients']/10) + coeff_nutr * df['nutr'])
        return df
    
    def sort_final(self,df):
        df = df.sort_values(by=['score', 'p'], ascending = False).reset_index(drop = True)
        return df
    
    
    def final_df(self,df, ca, cb, p, s, cw, cbw, pw, sw):
        
        filtered_df = self.filter_recipes(df, ca, cb, p, s, cw, cbw, pw, sw, self.time_constraint)
        scored_df = self.recipe_scorer(filtered_df)
        sorted_df = self.sort_final(scored_df)
        
        return sorted_df[['recipe_name','total_time','ingredients','steps', 'calories', 'protein', 'carbs', 'sodium', 'p', 'score']]
    
    def check_final(self,recipes_prop, user_cals, user_carbs, user_pro,\
                    user_sod, cal_wgt, carbs_wgt, pro_wgt, sod_wgt,time_constraint, recipe_list, thousands ):
        
        user_recs = self.final_df(recipes_prop, user_cals, user_carbs, user_pro,\
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
            if thousands*1000 > len(self.recipes_df):
                if final.shape[0] > 0:
                    print(final.head(final.shape[0]))#it will print whatever it has found
                else:
                    print("Sorry, we couldn't find a recipe fulfilling your preferences")
                    sys.exit()
            thousands += 1
            self.check_final(self.recipes_prop_f(recipe_list,thousands), user_cals, user_carbs, user_pro,\
                        user_sod, cal_wgt, carbs_wgt, pro_wgt, sod_wgt,time_constraint, recipe_list, thousands)
        
############################### END FUNCTIONS ################################

def get_data_and_recipes(user_ingred_list,user_banned_ingre,strict):
    #### Getting the data
    recipes_df = pd.read_csv('full_dataframe.csv', na_values=['< 1']).fillna(0)
    recipes_df['ingredients'] = recipes_df.ingredients.apply(literal_eval)
    recipes_df['recipe_name'] = recipes_df['recipe_name'].astype(str)
    recipes_df = recipes_df[recipes_df['total_time'] != 0]
    recipes_df = recipes_df.drop_duplicates(subset=['recipe_name'])
    
    ####Initalize dictionary with all of the recipe names and a proportion of 0
    recipe_list = defaultdict.fromkeys(recipes_df['recipe_name'].to_list(), 0)
    
    ####Initialize dictionary
    all_ingredients = defaultdict(int)
    
    
    ####Populate dictionary of all ingredients in recipe csv
    for ind in recipes_df.index:
        temp_list = recipes_df['ingredients'][ind]
        for item in temp_list:
            all_ingredients[str(item)] += 1
          

# print("\nUser ingredients: ", user_ingred_list)

# print("\nPlease wait...\n")


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
    return recipe_list, recipes_df


#################### MAIN #############################
  
    
if __name__ == '__main__':
    
    strict = 'y'
    user_ingred_list = ['spinach','carrots','chicken']
    user_banned_ingre = []
    time_constraint = 0
    user_cals = 0
    user_carbs = 0
    user_pro = 0
    user_sod = 0
    cal_wgt = 1
    carbs_wgt = 1
    pro_wgt = 1
    sod_wgt = 1
    thousands = 1

    recipe_list, recipes_df = get_data_and_recipes(user_ingred_list,user_banned_ingre,strict)
     #### Calling function to sort in chunks of 1000 (or less) recipes with highest proportions
    
    ALG = Algorithm(time_constraint, recipes_df)
    
    recipes_prop = ALG.recipes_prop_f(recipe_list, thousands)
    # Calling function for final check     
    output_df = ALG.check_final(recipes_prop, user_cals, user_carbs, user_pro,\
                    user_sod, cal_wgt, carbs_wgt, pro_wgt, sod_wgt,time_constraint, recipe_list, thousands)
    print(output_df)






####Checking time for testing
# e_time = time.time()
# print("Time to execute", e_time - s_time)   