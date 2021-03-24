import pandas as pd


file = pd.read_csv('core-data_recipe.csv')

n = file["nutritions"][0]
n = n.replace("u'", "'")
n = n.replace("\'", "\"")
n = n[:-1]

file['ingredients'] = file['ingredients'].str.split('^')

import ast


file['nutritions'] = file['nutritions'].apply(lambda x: ast.literal_eval(x.replace("u'", "'").replace("\'",'\"')[:-1]))