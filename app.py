from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, Enum
from flask_marshmallow import Marshmallow
import os
import enum

# Init app
app = Flask(__name__)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@localhost:3306/employees'.format(
    'root', '1234')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Product Class/Model

class Employees(db.Model):
    emp_no = db.Column(db.Integer, primary_key=True)
    birth_date = db.Column(db.Date())
    first_name = db.Column(db.String())
    last_name = db.Column(db.String(200))
    gender = db.Column(db.String(1))
    hire_date = db.Column(db.Date())

    def __repr__(self):
        return '<Post %s>' % self.title

    def __init__(self, emp_no, birth_date, first_name, last_name, gender, hire_date):
        self.emp_no = emp_no
        self.birth_date = birth_date
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.hire_date = hire_date

# Product Schema

class EmployeesSchema(ma.Schema):
    class Meta:
        fields = ('emp_no', 'birth_date', 'first_name',
                  'last_name', 'gender', 'hire_date')


# Init schema single and plural
employeeschema = EmployeesSchema()
employeesschema = EmployeesSchema(many=True)


# Create an Employee
@app.route('/createemoloyee', methods=['POST'])
def add_product():
    data = request.json
    emp_no = data['emp_no']
    birth_date = data['birth_date']
    first_name = data['first_name']
    last_name = data['last_name']
    gender = data['gender']
    hire_date = data['hire_date']

    new_employee = Employees(emp_no, birth_date, first_name,
                             last_name, gender, hire_date)

    db.session.add(new_employee)
    db.session.commit()

    return employeeschema.jsonify(new_employee)


#####Endpoints#####

# Get All Exployees
@app.route('/allemployees', methods=['GET'])
def get_employees():
    all_products = Employees.query.all()
    result = employeesschema.dump(all_products)
    return jsonify(result)


# Get Single Employee
@app.route('/employee/<emp_no>', methods=['GET'])
def get_employee(emp_no):
    employee = Employees.query.get(emp_no)
    return employeeschema.jsonify(employee)


# Update an Employee
@app.route('/employee/<emp_no>', methods=['PUT'])
def update_employee(emp_no):
    employee = Employees.query.get(emp_no)
    data = request.json
    emp_no = data['emp_no']
    birth_date = data['birth_date']
    first_name = data['first_name']
    last_name = data['last_name']
    gender = data['gender']
    hire_date = data['hire_date']

    employee.emp_no = emp_no
    employee.birth_date = birth_date
    employee.first_name = first_name
    employee.last_name = last_name
    employee.gender = gender
    employee.hire_date = hire_date

    db.session.commit()

    return employeeschema.jsonify(employee)

# Delete an Employee
@app.route('/employee/<emp_no>', methods=['DELETE'])
def delete_product(emp_no):
    employee = Employees.query.get(emp_no)
    db.session.delete(employee)
    db.session.commit()

    return employeeschema.jsonify(employee)


# Run Server
if __name__ == '__main__':
    app.run(debug=False)


##########Comments#################

# class MyEnum(enum.Enum):
#      male = "one"
#      female = "two"

# basedir = os.path.abspath(os.path.dirname(__file__))

###################################
