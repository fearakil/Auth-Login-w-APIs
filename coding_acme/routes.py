from coding_acme import app, db
from coding_acme.models import Employee, employee_schema, employees_schema, User, check_password_hash
from coding_acme.forms import UserForm, LoginForm
from coding_acme.token_verification import token_required

from flask import jsonify, request, render_template, redirect, url_for
from flask_login import login_required, login_user, current_user, logout_user

import jwt

@app.route('/employees/create', methods = ['POST'])
@token_required
def create_employee():
    name = request.json['full_name']
    address = request.json['address']
    ssn = request.json['ssn']
    role = request.json['role']
    email = request.json['email']
    birthday = request.json['birthday']

    employee = Employee(name,address,ssn,role,email,birthday)

    db.session.add_all(employee)
    db.session.commit()
    results = employee_schema.dump(employee)
    return jsonify(results)

@app.route('/employees', methods = ['GET'])
@token_required
def get_employees(current_user_token):
        employees = Employee.query.all()
        return jsonify(employees_schema.dump(employees))

@app.route('/employees/<id>', methods = ['GET'])
@token_required
def get_employee(current_user_token,id):
    employee = Employee.query.get(id)
    result = employee_schema.dump(employee)
    return jsonify(result)

@app.route('/employees/update/<id>', methods = ['POST', 'PUT'])
@token_required
def update_employee(current_user_token,id):
    employee = Employee.query.get(id)

    employee.name = request.json['full_name']
    employee.address = request.json['address']
    employee.ssn = request.json['ssn']
    employee.role = request.json['role']
    employee.email = request.json['email']
    employee.birthday = request.json['birthday']

    db.session.commit()

    return employee_schema.jsonify(employee)

@app.route('/employees/delete/<id>', methods = ['DELETE'])
@token_required
def delete_employee(current_user_token,id):
    employee = Employee.query.get(int(id))
    db.session.delete(employee)
    db.session.commit()
    result = employee_schema.dump(employee)
    return jsonify(result)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/users/register', methods = ['GET','POST'])
def register():
    form = UserForm()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        user = User(name,email,password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html', user_form = form)

@app.route('/users/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    email = form.email.data
    password = form.password.data

    logged_user = User.query.filter(User.email == email).first()
    if logged_user and check_password_hash(logged_user.password, password):
        login_user(logged_user)
        return redirect(url_for('get_key'))
    return render_template('login.html', login_form = form)

@app.route('/users/getkey', methods = ['GET'])
def get_key():
    token = jwt.encode({'public_id':current_user.id,'email':current_user.email}, app.config['SECRET_KEY'])
    user = User.query.filter_by(email = current_user.email).first()
    user.token = token

    db.session.add(user)
    db.session.commit()
    results = token.decode('utf-8')
    return render_template('token.html',results = results)

@app.route('/updatekey', methods = ['GET', 'POST', 'PUT'])
def refresh_key():
    refresh_key = {'refreshToken': jwt.encode({'public_id':current_user.id,'email':current_user.email}, app.config['SECRET_KEY'])}
    temp = refresh_key.get('refreshToken')
    new_token = temp.decode('utf-8')

    user = User.query.filter_by(email = current_user.email).first()
    user.token = new_token

    db.session.add(user)
    db.session.commit()
    return render_template('token_refresh.html', new_token = new_token)
