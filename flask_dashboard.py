import pandas as pd
import re
from collections import defaultdict
import time
from ast import literal_eval
import sys
import numpy as np
from flask import Flask, request, render_template, url_for

class Algorithm():
    def __init__(self, processed_ingredients, processed_exclusions, time, lower_cals, upper_cals, lower_carbs, upper_carbs, lower_protein, upper_protein, lower_sodium, upper_sodium, priority, num_rec):
        self.strict = "y"

        self.user_ingred_list = processed_ingredients
        self.user_banned_ingre = processed_exclusions
        self.time_constraint = time
        self.num_rec = num_rec

        self.lower_cals = lower_cals
        self.upper_cals = upper_cals
        self.lower_carbs = lower_carbs
        self.upper_carbs = upper_carbs
        self.lower_protein = lower_protein
        self.upper_protein = upper_protein
        self.lower_sodium = lower_sodium
        self.upper_sodium = upper_sodium

        # self.nutri_dict = {'low': 1, 'med': 5, 'high': 10}
        # self.cal_wgt = 1
        # self.carbs_wgt = 1
        # self.pro_wgt = 1
        # self.sod_wgt = 1
        self.thousands = 1

###################################### FUNCTIONS #########################

    def get_data_and_recipes(self):
        #### Getting the data
        recipes_df = pd.read_csv(r'full_dataframe.csv', na_values=['< 1']).fillna(0)
        recipes_df['ingredients'] = recipes_df.ingredients.apply(literal_eval)
        recipes_df['recipe_name'] = recipes_df['recipe_name'].astype(str)
        recipes_df = recipes_df[recipes_df['total_time'] != 0]
        recipes_df = recipes_df.drop_duplicates(subset=['recipe_name'])
        print("total number of recipes:", len(recipes_df))

        ####Initalize dictionary with all of the recipe names and a proportion of 0
        recipe_list = defaultdict.fromkeys(recipes_df['recipe_name'].to_list(), 0)
        
        ####Initialize dictionary
        # all_ingredients = defaultdict(int)
        
        
        # ####Populate dictionary of all ingredients in recipe csv
        # for ind in recipes_df.index:
        #     temp_list = recipes_df['ingredients'][ind]
        #     for item in temp_list:
        #         all_ingredients[str(item)] += 1
              

    # print("\nUser ingredients: ", user_ingred_list)

    # print("\nPlease wait...\n")


        ### Filtering recipe strictly for ingredients
        n = len(self.user_ingred_list)
        if self.strict == "n":
            recipes_df = recipes_df[recipes_df["n_ingredients"] <= n] 
            pass


        ####Filtering: proportions and banned ingredients
        for index, row in recipes_df.iterrows():
            ingre_list = row['ingredients'].copy()
            nn = len(ingre_list)
            if self.strict == "y":
                nn = len(ingre_list) * 0.001 # the priority is: the ingredients in recipe are in user's ingredients --> Minimalist list of ingredients
            else:
                nn = n # the priority is: the user´s ingredients are in recipe's ingredients -->  Long list of ingredients
            for user_rec in self.user_ingred_list:
                r = re.compile(r".*\b("+user_rec+")\\b", flags=re.IGNORECASE)
                match = list(filter(r.match, ingre_list))
                if match:
                    if self.user_banned_ingre != []:
                        for user_ban in self.user_banned_ingre:
                            r_1 = re.compile(r".*\b("+user_ban+")\\b", flags=re.IGNORECASE)
                            match_1 = list(filter(r_1.match, ingre_list))
                            if not match_1:
                                recipe_list[row['recipe_name']] += 1/nn
                                ingre_list.remove(match[0])
                    else:
                       recipe_list[row['recipe_name']] += 1/nn
                       ingre_list.remove(match[0])
        return recipe_list, recipes_df


    def recipes_prop_f(self):
        recipe_list, recipes_df = self.get_data_and_recipes()

        recipes_prop = pd.DataFrame(list(recipe_list.items()), columns = ['recipe_name', 'p'])
        recipes_prop = pd.merge(recipes_df, recipes_prop, on = "recipe_name", how = "inner")
        recipes_prop = recipes_prop.loc[recipes_prop['p'] > 0.00 ].reset_index(drop = True)
        recipes_prop = recipes_prop.sort_values(by=['p'], ascending = False).reset_index(drop = True)
        recipes_prop = recipes_prop.iloc[:self.thousands*1000]
        
        print("\nNumber of recipes to choose from now... ", len(recipes_prop))
        #test_df = recipes_prop[["recipe_name","ingredients","p"]]
        #print("recipes proportiond", recipes_prop.head())
        return recipes_prop
    
    def filter_recipes(self,proportion_df, lower_cals, upper_cals, lower_carbs, upper_carbs, lower_protein, upper_protein, lower_sodium, upper_sodium, time_constraint):
        filter_df = proportion_df.copy(deep = True)
        
        # if cals > 0:
        #     filter_df = filter_df.loc[filter_df['calories'] <= cals]
        # if carbs > 0:
        #     filter_df = filter_df.loc[filter_df['carbs'] <= carbs]
        # if pro > 0:
        #     filter_df = filter_df.loc[filter_df['protein'] <= pro]
        # if sod > 0:
        #     filter_df = filter_df.loc[filter_df['sodium'] <= sod]
        filter_df = filter_df[(filter_df['calories'] >= lower_cals) & (filter_df['calories'] <=  upper_cals)]
        filter_df = filter_df[(filter_df['carbs'] >= lower_carbs) & (filter_df['carbs'] <=  upper_carbs)]
        filter_df = filter_df[(filter_df['protein'] >= lower_protein) & (filter_df['protein'] <=  upper_protein)]
        filter_df = filter_df[(filter_df['sodium'] >= lower_sodium) & (filter_df['sodium'] <=  upper_sodium)]
            
        if time_constraint > 0:
            filter_df = filter_df.loc[filter_df["total_time"] <= time_constraint]
            
                            # denominators are average values for all the recipies 
        # filter_df['nutr'] = (wcals)/(1 + abs(cals - filter_df['calories'])/400) + \
        #                   (wcarbs)/(1 + abs(carbs - filter_df['carbs'])/40) + \
        #                   (wpro)/(1 + abs(pro - filter_df['protein'])/35) + \
        #                   (wsod)/(1 + abs(sod - filter_df['sodium'])/600)
        
        return filter_df
    
    
    
    def recipe_scorer(self,df, coeff_p = 1,coeff_tt = 1, coeff_ni = 1, coeff_nutr = 1):  
        
        df['score'] = coeff_p * df['p'] + coeff_tt * (1/(df['total_time']/np.mean(df['total_time']))\
                      + coeff_ni * (1/df['n_ingredients']/np.mean(df['n_ingredients'])))# + coeff_nutr * df['nutr'])
        return df
    
    def sort_final(self,df):
        df = df.sort_values(by=['score', 'p'], ascending = False).reset_index(drop = True)
        return df
    
    
    def final_df(self,df, lower_cals, upper_cals, lower_carbs, upper_carbs, lower_protein, upper_protein, lower_sodium, upper_sodium):
        
        filtered_df = self.filter_recipes(df, lower_cals, upper_cals, lower_carbs, upper_carbs, lower_protein, upper_protein, lower_sodium, upper_sodium, self.time_constraint)
        scored_df = self.recipe_scorer(filtered_df)
        sorted_df = self.sort_final(scored_df)
        
        return sorted_df[['recipe_name','total_time','ingredients','steps', 'calories', 'protein', 'carbs', 'sodium', 'p', 'score']]
    
    def check_final(self):
        recipes_prop = self.recipes_prop_f()
        user_recs = self.final_df(recipes_prop, self.lower_cals, self.upper_cals, self.lower_carbs, self.upper_carbs, self.lower_protein, self.upper_protein, self.lower_sodium, self.upper_sodium)
        
        if self.time_constraint !=0:
            final = user_recs.loc[user_recs['total_time'] <= self.time_constraint].reset_index(drop = True)
        else:
            final = user_recs
            print("Number of recipes found: ", final.shape[0])
            print("Number of recipes screened:", self.thousands*1000) 
            
        if final.shape[0]>=self.num_rec:
            final_recipes = final.head(self.num_rec)
            return final_recipes.set_index("recipe_name").to_dict(orient="index")
        else:
            if self.thousands*1000 > len(recipes_prop):
                if final.shape[0] > 0:
                    final_recipes = final.head(self.num_rec)#it will print whatever it has found
                    return final_recipes.set_index("recipe_name").to_dict(orient="index")
                else:
                    return None
            self.thousands += 1
            self.check_final()
        

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/container-left', methods=['GET', 'POST'])
def render():
    if request.method == 'POST':

        raw_ingredient_list = request.form.getlist('ingredient_input_text')
        if len(raw_ingredient_list) == 0:
            return render_template('index.html', error="Ingredients list was blank. Please input some ingredients.")
        else:
            processed_ingredients = raw_ingredient_list.copy()
            print(processed_ingredients)

        raw_exclusions_list = request.form.getlist('exclusions_input_text')
        processed_exclusions = raw_exclusions_list.copy()
        for i in processed_exclusions:
        	if i in processed_ingredients:
        		return render_template('index.html', error=f"Excluded ingredient {i} was in the included ingredients list. Please do not exclude ingredients if you input them into the first field.")
        print(processed_exclusions)

        raw_time = request.form['time_input_text']
        if raw_time != "":
	        time = int(raw_time)
	        print(time)
        else:
        	time = 0

        raw_cals = request.form['calories']
        processed_cals = raw_cals.split(" - ")
        lower_cals = int(processed_cals[0])
        upper_cals = int(processed_cals[1])
        print(lower_cals, upper_cals)

        raw_carbs = request.form['carbs']
        processed_carbs = raw_carbs.split(" - ")
        lower_carbs = int(processed_carbs[0])
        upper_carbs = int(processed_carbs[1])
        print(lower_carbs, upper_carbs)

        raw_protein = request.form['protein']
        processed_protein = raw_protein.split(" - ")
        lower_protein = int(processed_protein[0])
        upper_protein = int(processed_protein[1])
        print(lower_protein, upper_protein)

        raw_sodium = request.form['sodium']
        processed_sodium = raw_sodium.split(" - ")
        lower_sodium = int(processed_sodium[0])
        upper_sodium = int(processed_sodium[1])
        print(lower_sodium, upper_sodium)

        try:
            priority = request.form["priority"]
        except:
            priority = None

        raw_num_rec = request.form["num_rec"]
        if raw_num_rec != "":
	        num_rec = int(raw_num_rec)
	        print(num_rec)
        else:
        	print("no num")
        	num_rec = 1


        render_alg = Algorithm(processed_ingredients, processed_exclusions, time, lower_cals, upper_cals, lower_carbs, upper_carbs, lower_protein, upper_protein, lower_sodium, upper_sodium, priority, num_rec)
        recipes = render_alg.check_final()

        if recipes == None:
            return render_template('index.html', error="Sorry, we couldn't find a recipe fulfilling your preferences. Please try again.")
            
        return render_template('index.html', recipes=recipes)


if __name__ == "__main__":
    app.run(debug=True)