# from flask import Flask, jsonify, request, render_template, flash, redirect, url_for, session

# app = Flask(__name__)
# app.secret_key = 'dev'  # Change this to a secure key in production

# # Simple database structure
# dummy_db = {
#     'users': {},  # Format: username: {'password': str, 'balance': float}
# }

# @app.route('/')
# def index():
#     if 'username' not in session:
#         return redirect(url_for('login'))
#     return render_template('index.html', username=session['username'], 
#                          balance=dummy_db['users'][session['username']]['balance'])

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
        
#         if username in dummy_db['users']:
#             flash('Username already exists')
#             return redirect(url_for('register'))
        
#         dummy_db['users'][username] = {'password': password, 'balance': 0.0}
#         flash('Registration successful')
#         return redirect(url_for('login'))
    
#     return render_template('register.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
        
#         if username in dummy_db['users'] and dummy_db['users'][username]['password'] == password:
#             session['username'] = username
#             return redirect(url_for('index'))
#         flash('Invalid credentials')
    
#     return render_template('login.html')

# @app.route('/deposit', methods=['GET', 'POST'])
# def deposit():
#     if 'username' not in session:
#         return redirect(url_for('login'))
    
#     if request.method == 'POST':
#         amount = float(request.form['amount'])
#         if amount > 0:
#             dummy_db['users'][session['username']]['balance'] += amount
#             flash(f'Successfully deposited ${amount}')
#         return redirect(url_for('index'))
    
#     return render_template('deposit.html')

# @app.route('/withdraw', methods=['GET', 'POST'])
# def withdraw():
#     if 'username' not in session:
#         return redirect(url_for('login'))
    
#     if request.method == 'POST':
#         amount = float(request.form['amount'])
#         if amount > 0 and dummy_db['users'][session['username']]['balance'] >= amount:
#             dummy_db['users'][session['username']]['balance'] -= amount
#             flash(f'Successfully withdrew ${amount}')
#         else:
#             flash('Insufficient funds')
#         return redirect(url_for('index'))
    
#     return render_template('withdraw.html')

# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('login'))