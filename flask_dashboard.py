from flask import Flask, request, render_template

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
        print(ingredient_list)


        return render_template('index.html', recipe=processed_text)


if __name__ == "__main__":
    app.run(debug=True)