import pandas as pd
import ast

file = pd.read_csv('core-data_recipe.csv')


file['ingredients'] = file['ingredients'].str.split('^')
file['nutritions'] = file['nutritions'].apply(lambda x: ast.literal_eval(x.replace("u'", "'").replace("\'",'\"')[:-1]))
