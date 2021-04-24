CSE 6242 Semester Project - RENDER: Recipes made easy - Tyah Dugger, Jose Garcia, Patrick Mudge, Christopher J. Nemastil, Nicholas Susemiehl 

DESCRIPTION:
A common problem many adults face is deciding what to do for dinner each night. If one intends to cook for themself, then they are also presented with an additional dilemma: what to make. This forces an individual who may already be fatigued from a long day of work to endure the mental exercise of finding a meal they can make from ingredients they have on hand. Our recipe recommender, RENDER, assists with meal planning and preparation by providing recipe recommendations based on the ingredients the user already owns. To utilize the basic functionality of RENDER, users input a list of ingredients they have on-hand via, ingredients they want to avoid, the maximum amount of time they want to spend cooking, target ranges for nutritional values, how important various factors are, and how many recipes they would like to see to our tool’s offline web interface. The recommendation algorithm then returns a list of recipes that are either entirely or mostly comprised of these ingredients in this list. Users can then choose a recipe and follow the instructions presented to prepare their meal. 

INSTALLATION:
Download and Extract Recipe-Recomender-master.zip
Make sure you fulfill requirements.txt.  "pip freeze > requirements.txt" may help with this.
(The program is tested with Python 3.7.6, but may be compatible with other versions)

EXECUTION:
In Windows, from command line:
Navigate to ./Recipe-Recomender-master
>set FLASK_APP=flask_dashboard.py
>python -m flask run

Navigate to the address given by your system.  It typically defaults to http://127.0.0.1:5000/
From there, follow the directions on the UI.
Note: After running one search, the page may need to be refreshed to run a second search.

We did not do extensive testing in MacOS, as we did not have it readily available for develoment and testing.  If MacOS is required, follow these steps:
>cd ./Recipe-Recomender-master
>python3 -m venv flask
>. flask/bin/activate
>pip install Flask
>pip install wheel
>pip install pandas
>export FLASK_APP=flask_dashboard.py
>flask run

Using a virtual Windows environment may also work.

Depending on requirements chosen and computing power, it may take up to a few minutes to return the recipes.

Video for running on Windows: https://youtu.be/sLMzK9bqdlw

RENDER was primarily developed and tested in Windows. Installing Flask on Mac may be different. See this tutorial for assistance: https://phoenixnap.com/kb/install-flask

Raw data and code used to process it are available under the data folder.
