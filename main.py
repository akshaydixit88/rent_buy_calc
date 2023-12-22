from flask import Flask, request, jsonify, render_template
from break_even_rent import find_break_even_rent # Import your Python function
import logging

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/calculate_breakeven', methods=['POST'])
def calculate_breakeven():
    house_price = float(request.form['houseprice'])
    interest_rate = float(request.form['interestrate'])
    own_term = int(request.form['tenure'])
    mortgage_rate = interest_rate/100
    monthly_rent=1000
    step_size=100
    max_iterations=500
    print (house_price)
    break_even_rent = find_break_even_rent(monthly_rent, house_price, mortgage_rate,own_term,step_size, max_iterations)
    print (break_even_rent)
    return jsonify({'total_value': break_even_rent})

if __name__ == "__main__":
    app.run(debug=True)

