from flask import Flask, render_template, url_for, jsonify, request, redirect
from datetime import datetime
import os
import multiplicationfacts, sequencepuzzlegenerator, linearequationsgenerator
import numberwiki, login, basicarithmaticoperations, dashboard

print("Entering main.py...")

app = Flask(__name__, template_folder='../templates')

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
    data = multiplicationfacts.get_multiplication_facts(tableof, limit)
    return jsonify(data), 200

@app.route('/number-wiki')
def render_number_wiki_template():
    print("Entering render_math_functions_template...")
    return render_template('number-wiki.html')

@app.route('/number-wiki/<int:n>')
def process_number_wiki(n):
    print("Enterning process_number_wiki...")
    data = numberwiki.get_number_wiki(n)
    return jsonify(data), 200

@app.route('/sequence-puzzles')
def render_sequence_puzzles_template():
    print("Entering render_sequence_puzzles_template...")
    return render_template('sequence-puzzles.html')

@app.route('/sequence-puzzles/get', methods=['PUT', 'GET'])
def process_generate_sequence_puzzle():
    print("Enterning process_generate_sequence_puzzle...")
    requestData = request.json
    data = sequencepuzzlegenerator.generate_sequence_puzzle(requestData)
    return jsonify(data), 200

@app.route('/sequence-puzzles/submit', methods=['PUT', 'GET'])
def submit_sequence_puzzles():
    print("Enterning submit_sequence_puzzles...")
    input_sequence_puzzles = request.json
    status = sequencepuzzlegenerator.update_datastore_sequence_puzzles(input_sequence_puzzles)
    return jsonify(status), 200

@app.route('/linear-equations')
def render_linear_equations_template():
    print("Entering render_linear_equations_template...")
    return render_template('linear-equations.html')

@app.route('/linear-equations/get', methods=['PUT', 'GET'])
def process_generate_linear_equations_puzzle():
    print("Enterning process_generate_linear_equations_puzzle...")
    requestData = request.json
    data = linearequationsgenerator.generate_linear_equations(requestData)
    return jsonify(data), 200

@app.route('/linear-equations/submit', methods=['PUT', 'GET'])
def submit_linear_equations():
    print("Enterning submit_linear_equations...")
    input_linear_equations = request.json
    status = linearequationsgenerator.update_datastore_linear_equations(input_linear_equations)
    return jsonify(status), 200

@app.route('/login-initial-load')
def render_login_template():
    print("Entering render_login_template...")
    return render_template('login.html')

@app.route('/login', methods=['PUT', 'GET'])
def process_login():
    print("Enterning process_login...")
    login_credentials = request.json
    data = login.login(login_credentials)
    return jsonify(data), 200

@app.route('/reset-password', methods=['PUT', 'GET'])
def process_reset_password():
    print("Enterning process_reset_password...")
    login_credentials = request.json
    data = login.reset_password(login_credentials)
    return jsonify(data), 200

@app.route('/get-forgot-password-question', methods=['PUT', 'GET'])
def process_get_forgot_password_question():
    print("Enterning process_get_forgot_password_question...")
    login_credentials = request.json
    data = login.get_forgot_password_question(login_credentials)
    return jsonify(data), 200

@app.route('/create-account-initial-load')
def render_create_account_template():
    print("Entering render_create_account_template...")
    return render_template('create-account.html')

@app.route('/create-account', methods=['PUT', 'GET'])
def process_create_account():
    print("Enterning process_create_account...")
    userInfo = request.json
    data = login.create_account(userInfo)
    return jsonify(data), 200

@app.route('/basic-arithematic-operations-initial-load')
def render_basic_arithematic_operations_template():
    print("Entering render_basic_arithematic_operations_template...")
    return render_template('basic-arithematic-operations.html')

@app.route('/basic-arithematic-operations', methods=['PUT', 'GET'])
def process_basic_arithematic_operations():
    print("Enterning process_basic_arithematic_operations...")
    requestData = request.json
    data = basicarithmaticoperations.generate_basic_arithmatic_operations(requestData)
    return jsonify(data), 200

@app.route('/basic-arithematic-operations/submit', methods=['PUT', 'GET'])
def submit_basic_arithematic_operations():
    print("Enterning submit_basic_arithematic_operations...")
    input_basic_arithematic_operation = request.json
    status = basicarithmaticoperations.update_datastore_basic_arithmatic_operations(input_basic_arithematic_operation)
    return jsonify(status), 200

@app.route('/get-dashboard', methods=['PUT', 'GET'])
def process_user_dashboard():
    print("Enterning process_user_dashboard...")
    requestData = request.json
    print(requestData)
    metrics = dashboard.generate_user_dashboard(requestData)
    return jsonify(metrics), 200

if __name__ == "__main__":
    print("Starting MathGarage Python Flask App on Port 5000...")
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0',port=port)



