from flask import Flask, request, render_template
import pandas as pd
from ast import literal_eval
import re
from collections import defaultdict
# from algorithm.py import Algorithm as Alg

class Algorithm():
    def init(self):
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        ########
        self.recipes_df = pd.read_csv('full_dataframe.csv', na_values=['< 1']).fillna(0)
        self.recipes_df['ingredients'] = self.recipes_df.ingredients.apply(literal_eval)
        self.recipes_df['recipe_name'] = self.recipes_df['recipe_name'].astype(str)
        
        self.recipes_df = self.recipes_df[self.recipes_df['total_time'] != 0]
        self.recipes_df = self.recipes_df.drop_duplicates(subset=['recipe_name'])
        
        self.recipe_list = defaultdict.fromkeys(self.recipes_df['recipe_name'].to_list(), 0)

        # self.html_ingredient_list = html_ingredient_list

    



        # all_ingredients = defaultdict(int)

        # for ind in self.recipes_df.index:
        #     temp_list = self.recipes_df['ingredients'][ind]
        #     #li = ast.literal_eval(temp_list)
        #     for item in temp_list:
        #         all_ingredients[str(item)] += 1
        

            
        
    def filter_recipes(self,proportion_df, cals, carbs, pro, sod, wcals, wcarbs, wpro, wsod):
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

    def recipe_scorer(self,df):
        #df['score'] = df['p'] * ((1/(df['total_time'] * df['n_ingredients'])) + df['n'])
        df['score'] = 10 * df['p'] + (10/(df['total_time']/60)\
                        + (10 /df['n_ingredients']/10) + df['n'])
        return df

    
    
    def sort_final(self, df):
        
        df = df.sort_values(by=['score', 'p'], ascending = False).reset_index(drop = True)
        return df
    

    def final_df(self, df, ca, cb, p, s, cw, cbw, pw, sw):
        
        filtered_df = self.filter_recipes(df, ca, cb, p, s, cw, cbw, pw, sw)
        scored_df = self.recipe_scorer(filtered_df)
        sorted_df = self.sort_final(scored_df)
        
        return sorted_df[['recipe_name','total_time','ingredients','steps', 'calories', 'protein', 'carbs', 'sodium', 'p', 'score']]
                   
                    
                    
                    
    def recipes_prop_f(self,html_ingredients_list,thousands,n):
        for index, row in self.recipes_df.iterrows():
            ingre_list = row['ingredients']
            for user_rec in html_ingredients_list:
                r = re.compile(".*(" + user_rec + ").*", flags=re.IGNORECASE)
                match = list(filter(r.match, ingre_list))
                if match:
                    self.recipe_list[row['recipe_name']] += 1/n
                    # To consider that the ingredient is in the recipe name
                    temp = " " + user_rec + " "
                    temp1 = " " + user_rec
                    temp2 = user_rec + " "
                    if (temp in row['recipe_name']) or (temp1 in row['recipe_name']) or (temp in row['recipe_name']):
                        self.recipe_list[row['recipe_name']] += 5/n
        
        
        
        recipes_prop = pd.DataFrame(list(self.recipe_list.items()), columns = ['recipe_name', 'p'])
        recipes_prop = pd.merge(self.recipes_df, recipes_prop, on = "recipe_name", how = "inner")
        recipes_prop = recipes_prop.loc[recipes_prop['p'] > 0.00 ].reset_index(drop = True)
        recipes_prop = recipes_prop.sort_values(by=['p'], ascending = False).reset_index(drop = True)
        recipes_prop = recipes_prop.iloc[:thousands*1000]
        return recipes_prop

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
            thousands += 1


def run_program(html_ingredients_list, calval, carbval, proval, sodval, calw, carbw, prow, sodw):
    recipes_df = pd.read_csv('full_dataframe.csv', na_values=['< 1']).fillna(0)
    recipes_df['ingredients'] = recipes_df.ingredients.apply(literal_eval)
    recipes_df['recipe_name'] = recipes_df['recipe_name'].astype(str)
    
    recipes_df = recipes_df[recipes_df['total_time'] != 0]
    
    
    ##Initalize dictionary with all of the recipe names and a proportion of 05
    recipe_list = defaultdict.fromkeys(recipes_df['recipe_name'].to_list(), 0)
    
    
    all_ingredients = defaultdict(int)
    
    
    """Populate dictionary of all ingredients in recipe csv"""
    for ind in recipes_df.index:
        temp_list = recipes_df['ingredients'][ind] # list of ingredients of each row
        #li = ast.literal_eval(temp_list)
        for item in temp_list:
            all_ingredients[str(item)] += 1 #counts times an ingredient appears
            
    all_ingredients_df = pd.DataFrame(list(all_ingredients.items()), columns = ["Ingredient", "Count"])
    
    
      
    
    """Get n ingredients from user"""
    # n = int(input("How many main ingredients do you have? "))
    # user_ingred_list = []
    user_ingred_list = html_ingredients_list
    n = len(html_ingredients_list)
    
    # if n != 0:
    #     for i in range(0,n):
    #         user_ingred_list.append(input("Ingredient: "))
    # else:
    #     sys.exit()
    
    # print("\nUser ingredients: ", user_ingred_list)
    
    
    # """Get user nutrition preferences"""
    # print("\n\nAny nutrition preferences? (enter 0, if none)")
    user_cals = calval
    user_carbs = carbval
    user_pro = proval
    user_sod = sodval
    # user_cals = int(input("Calories: "))
    # user_carbs = int(input("Carbs (g): "))
    # user_pro = int(input("Protein (g): "))
    # user_sod = int(input("Sodium (mg): "))
    
    # print("\nPlease wait...\n")
    
    for user_rec in user_ingred_list:
          pattern = ".*(" + user_rec + ").*"
          for i in recipes_df.index:
              ingre_list = recipes_df["ingredients"][i]
              for l in ingre_list:
                  result = re.match(pattern, l, flags=re.IGNORECASE)
                  if result:
                      recipe_nm = recipes_df['recipe_name'][i]  #storing names of recipes that contain the ingredient
                      recipe_list[recipe_nm] += 1/n # portion of ingredients that contains
    
    
    recipes_prop = pd.DataFrame(list(recipe_list.items()), columns = ['recipe_name', 'p'])
    recipes_prop = pd.merge(recipes_df, recipes_prop, on = "recipe_name", how = "inner")
    recipes_prop = recipes_prop.loc[recipes_prop['p'] > 1.5].reset_index(drop = True) 
    # recipes proposed dataframe with columns recipe_name and p
    # ATTENTION p>1
    # print(recipes_prop[["recipe_name","ingredients","p"]].head(10))
    
    
    # print("\nNumber of recipes to choose from now... ", len(recipes_prop)) 
    
    
    # print("\nHow much emphasis on nutritients: (choose from low, med, high) ")
    
    
    ##nutrient weights
    nutri_dict = {'low': 1, 'med': 5, 'high': 10}
    
    # Commenting this out until we have weights as a user input in html
    # cal_wgt = nutri_dict[input("Calories? ")]
    # carbs_wgt = nutri_dict[input("Carbs? ")]
    # pro_wgt = nutri_dict[input("Protein? ")]
    # sod_wgt = nutri_dict[input("Sodium? ")]
    
    #TODO remove this hardcoding
    cal_wgt = nutri_dict[calw]
    carbs_wgt = nutri_dict[carbw]
    pro_wgt = nutri_dict[prow]
    sod_wgt = nutri_dict[sodw]
    
    # ### MAIN ###
    Alg = Algorithm()
    test = Alg.final_df(recipes_prop, user_cals, user_carbs, user_pro, user_sod, cal_wgt, carbs_wgt, pro_wgt, sod_wgt)
    return test.head(10) #change the 10 to change number of results



app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/container-left', methods=['GET', 'POST'])
def ingredient_input():
    if request.method == 'POST':
        
        raw_ingredient_list = request.form['ingredient_input_text']
        processed_text = str(raw_ingredient_list)
        ingredient_list = processed_text.split(",") # ingredients: list of strings


        # target_calories = request.form['calories_name'] #How to input here???
        # print(target_calories)


        # print(ingredient_list)
        calval, carbval, proval, sodval = 0, 0, 0, 0
        calw, carbw, prow, sodw = 'low', 'low', 'low', 'low'
        
        output_df = run_program(ingredient_list, calval, carbval, proval, sodval, calw, carbw, prow, sodw)
        print(output_df)
        
        check_final(recipes_prop_f(recipe_list,thousands), user_cals, user_carbs, user_pro,\
            user_sod, cal_wgt, carbs_wgt, pro_wgt, sod_wgt,time_constraint, recipe_list, thousands)
            
        
        
        
        recipe_names = str(list(output_df['recipe_name']))
        # return render_template('index.html', recipe=processed_text)
        return render_template('index.html', recipe=recipe_names)

if __name__ == "__main__":
    app.run(debug=True)