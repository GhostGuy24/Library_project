from flask import Flask, jsonify, request

from flask_cors import CORS
from methods import *
from methods import delete_customer as delete_customer_logic, delete_book as delete_book_logic
from dbClasses import *

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "DELETE", "PUT", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})




@app.route('/')
def home():
    return "Welcome"

@app.route('/library')
def library_actions():
    if request.method == 'GET':
        return jsonify(get_metrics())
    



 
@app.route('/books/<int:book_id>',methods=['DELETE'])
def delete_book(book_id):
    delete_book_logic(book_id)
    return {'status': 201}

@app.route('/books/<string:book_name>')
def get_book(book_name):
    return jsonify(get_book_by_name(book_name))

@app.route('/books',methods=['GET','POST','PUT'])
def books_actions():
    if request.method == 'GET':
        return jsonify(get_instock_books())
    if request.method == 'POST':
        data = request.get_json()
        book_name = data.get("book_name")
        author = data.get("author")
        publish_year = data.get("year_published")
        type = data.get("type")
        amount = data.get("amount")
        create_new_book(book_name=book_name, author=author, publish_year=publish_year, type=type, amount=amount)
        return {'status': 201 }
    if request.method == 'PUT':
        return jsonify({"message": "PUT request not implemented yet"}), 200






@app.route('/customers/<string:customer_name>')
def get_customer(customer_name):
    return jsonify(get_customer_by_name(customer_name))


@app.route('/customers/<int:customer_id>',methods=['DELETE'])
def delete_customer(customer_id):
    delete_customer_logic(customer_id)
    return {'status': 404}
@app.route('/customers',methods=['GET','POST','PUT'])
def customers_actions():
    if request.method == 'GET':
        return jsonify(get_active_customers())
    if request.method == 'POST':
        data = request.get_json()
        name = data.get("customer_name")
        city = data.get("city")
        age = data.get("age")
        create_customer(name=name, city=city, age=age)
        return {'status': 200 }
    
    if request.method == 'PUT':
        pass


@app.route('/loans',methods=['GET','POST','PUT'])
def loans_actions():
    if request.method == 'GET':
        return jsonify(get_active_loans())
    if request.method == 'POST':
        data = request.get_json()
        customer_name = data.get("customer_name")
        book_name = data.get("book_name")
        create_loan(customer_name=customer_name, book_name=book_name)
        return  {'status': 201}
    if request.method == 'PUT':
        pass


@app.route('/loans/late')
def get_late():
    return jsonify(get_late_loans())


@app.route('/loans/<int:loan_id>',methods=['DELETE'])
def return_book(loan_id):
    update_loan(loan_id)
    return {'status': 200}


@app.route('/loans/<string:customer_name>')
def get_customer_loans(customer_name):
    return jsonify(get_customer_active_loans(customer_name))


if __name__ == "__main__":
    app.run(debug=True, port=5001)




    