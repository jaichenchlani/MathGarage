from flask import Flask, render_template, url_for, jsonify, request, redirect
from datetime import datetime
import os
from multiplicationfacts import get_multiplication_facts
from mathfunctions import convert_decimal_to_binary
from sequencepuzzlegenerator import generate_sequence_puzzle
from linearequationsgenerator import generate_linear_equations


print("Entering main.py...")

app = Flask(__name__)

@app.route('/')
def render_index_template():
    print("Entering render_index_template...")
    return render_template('index.html')

@app.route('/multiplication-facts')
def render_multiplication_facts_template():
    print("Entering render_multiplication_facts_template...")
    return render_template('multiplication-facts.html')

@app.route('/get-multiplication-facts/<int:tableof>/<int:limit>', methods=['POST', 'GET'])
def process_multiplication_facts(tableof,limit):
    print("Entering process_multiplication_facts...")
    print("Calling get_multiplication_facts with 2 arguments: table_of({}); limit({}).".format(tableof,limit))
    data = get_multiplication_facts(tableof, limit)
    return jsonify(data), 200

@app.route('/math-functions')
def render_math_functions_template():
    print("Entering render_math_functions_template...")
    return render_template('math-functions.html')

@app.route('/math-functions/d2b/<int:decimal_number>')
def process_decimal_to_binary(decimal_number):
    print("Enterning process_decimal_to_binary...")
    data = convert_decimal_to_binary(decimal_number)
    return jsonify(data), 200

@app.route('/sequence-puzzles')
def render_sequence_puzzles_template():
    print("Entering render_sequence_puzzles_template...")
    return render_template('sequence-puzzles.html')

@app.route('/sequence-puzzles/get', methods=['PUT', 'GET'])
def process_generate_sequence_puzzle():
    print("Enterning process_generate_sequence_puzzle...")
    difficultyLevel = request.json
    data = generate_sequence_puzzle(difficultyLevel)
    return jsonify(data), 200

@app.route('/linear-equations')
def render_linear_equations_template():
    print("Entering render_linear_equations_template...")
    return render_template('linear-equations.html')

@app.route('/linear-equations/get', methods=['PUT', 'GET'])
def process_generate_linear_equations_puzzle():
    print("Enterning process_generate_linear_equations_puzzle...")
    difficultyLevel = request.json
    data = generate_linear_equations(difficultyLevel)
    return jsonify(data), 200

if __name__ == "__main__":
    print("Starting MathGarage Python Flask App on Port 5000...")
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0',port=port)



