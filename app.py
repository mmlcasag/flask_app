from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g
import sqlite3

app = Flask(__name__)

# app.config['DEBUG'] = True # it did not work i do not know why
app.config['SECRET_KEY'] = 'a1b2c3d4e5f6g7h8i9j0'

def connect_db():
    sql = sqlite3.connect('/home/mmlcasag/python/flask_app/data/data.db')
    sql.row_factory = sqlite3.Row
    
    return sql

def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/', methods=['GET'], defaults={'name': 'Stranger'})
@app.route('/<name>', methods=['GET'])
def index_handler(name):
    return '<h1>Hello {}!</h1>'.format(name)

@app.route('/home', methods=['GET'], defaults={'name': 'Stranger'})
@app.route('/home/<name>', methods=['GET'])
def home_handler(name):
    db = get_db()
    cur = db.execute(' select id, name, location from users order by id ')
    results = cur.fetchall()

    return render_template('home.html', name=name, display=False, myList=[1,2,3,4], myDictList=[{ 'name': 'Marcio'}, { 'name': 'Fabiana' }], results=results)

@app.route('/student', methods=['GET'], defaults={'name': 'New Student'})
@app.route('/student/<string:name>', methods=['GET'])
def student_handler(name):
    session['student'] = name
    
    return '<h1>Hello {}, welcome to our school!</h1>'.format(name)

@app.route('/class', methods=['GET'], defaults={'id': 1})
@app.route('/class/<int:id>', methods=['GET'])
def class_handler(id):
    return '<h1>Welcome to class number {}!</h1>'.format(id)

@app.route('/json', methods=['GET'])
def json_handler():
    if 'student' in session:
        student = session['student']
    else:
        student = ''

    return jsonify( {'key' : 'value', 'key2': [1, 2, 3], 'student': student } )

@app.route('/query')
def query_handler():
    name = request.args.get('name') #query string name
    location = request.args.get('location') #query string location
    
    return '<h1>Hello {}, from {}. You are on the query page!</h1>'.format(name, location)

@app.route('/theform')
def the_form_handler():
    return render_template('form.html')

@app.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    location = request.form['location']

    return '<h1>Hello {}, from {}. You have submitted the form successfully!</h1>'.format(name, location)

@app.route('/processjson', methods=['POST'])
def process_json():
    data = request.get_json()

    name = data['name']
    location = data['location']
    randomlist = data['randomlist']

    return jsonify({ 'result': 'success', 'data': data, 'name': name, 'location': location, 'randomlist': randomlist })

@app.route('/refactored-form', methods=['GET', 'POST'])
def refactored_form_handler():
    if request.method == 'GET':
        return '''
            <form method="POST" action="/refactored-form">
                <input type="text" name="name">
                <input type="text" name="location">
                <input type="submit">
            </form>
        '''
    elif request.method == 'POST':
        name = request.form['name']
        location = request.form['location']

        db = get_db()
        db.execute(' insert into users ( name, location ) values ( ?, ? ) ', [name, location])
        db.commit()

        #return '<h1>Hello {}, from {}. You have submitted the form successfully!</h1>'.format(name, location)
        
        # redirecting passing query strings
        # return redirect('/query?name={}&location={}'.format(name, location))

        # redirecting using url for and variables
        # return redirect(url_for('home_handler', name=name))

        # redirecting using url for and query strings
        return redirect(url_for('query_handler', name=name, location=location))
    else:
        return jsonify({ 'result': 'error', 'message': 'Invalid request method' })

@app.route('/logout')
def logout_handler():
    session.pop('student')
    return 'You have been successfully logged out'

# creating a virtual environment:
# python3 -m venv env

# activating a virtual environment:
# source env/bin/activate

# installing flask inside a virtual environment:
# pip install flask

# creating a environment variable
# export FLASK_APP=app.py

# creating another environment variable
# export FLASK_DEBUG=1

# running the project
# flask run

# deactivating a virtual environment:
# deactivate

@app.route('/viewresults')
def viewresults():
    db = get_db()
    cur = db.execute(' select id, name, location from users order by id ')
    results = cur.fetchall()

    return 'The ID is {}. The name is {}. The location is {}.'.format(results[0]['id'], results[0]['name'], results[0]['location'])
