CSE 6242 Semester Project - RENDER: Recipes made easy - Tyah Dugger, Jose Garcia, Patrick Mudge, Christopher J. Nemastil, Nicholas Susemiehl 

RENDER is a program that expedites recipe searching.  It allows for ingredient requirements and exclusion, nutrition targets, and time constraints.

How to run RENDER:

Download and Extract Recipe-Recomender-master.zip
Make sure you fulfill requirements.txt.  "pip freeze > requirements.txt" may help with this.
(The program is tested with Python 3.7.6, but may be compatible with other versions)


In Windows, from command line:
Navigate to .\Recipe-Recomender-master
>set FLASK_APP=flask_dashboard.py
>python -m flask run

In MacOS:


Navigate to the address given by your system.  It typically defaults to http://127.0.0.1:5000/
From there, follow the directions on the UI.

Depending on requirements chosen and computing power, it may take up to a few minutes to return the recipes.
