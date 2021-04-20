from flask import Flask, request, render_template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/container-left', methods=['GET', 'POST'])
def ingredient_input():
    if request.method == 'POST':

        raw_ingredient_list = request.form.getlist('ingredient_input_text')
        processed_text = str(raw_ingredient_list)
        print(processed_text)

        raw_exclusions_list = request.form.getlist('exclusions_input_text')
        processed_text = str(raw_exclusions_list)
        print(processed_text)

        raw_time = request.form['time_input_text']
        if raw_time != "":
	        time = int(raw_time)
	        print(time)
        else:
        	time = 1e100

        raw_cals = request.form['calories']
        processed_cals = raw_cals.split(" - ")
        lower_cals = processed_cals[0]
        upper_cals = processed_cals[1]
        print(lower_cals, upper_cals)

        raw_carbs = request.form['carbs']
        processed_carbs = raw_carbs.split(" - ")
        lower_carbs = processed_carbs[0]
        upper_carbs = processed_carbs[1]
        print(lower_carbs, upper_carbs)

        raw_protein = request.form['protein']
        processed_protein = raw_protein.split(" - ")
        lower_protein = processed_protein[0]
        upper_protein = processed_protein[1]
        print(lower_protein, upper_protein)

        raw_sodium = request.form['sodium']
        processed_sodium = raw_sodium.split(" - ")
        lower_sodium = processed_sodium[0]
        upper_sodium = processed_sodium[1]
        print(lower_sodium, upper_sodium)

        # print(ingredient_list, time)
        return render_template('index.html', recipe=processed_text)


if __name__ == "__main__":
    app.run(debug=True)