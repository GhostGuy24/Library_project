from datetime import date
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from methods import *
from methods import delete_customer as delete_customer_logic, delete_book as delete_book_logic, get_book_intro as get_book_intro_logic
from dbClasses import *
from flask_jwt_extended import JWTManager, create_access_token
from flask import Flask, request, jsonify
from flask_jwt_extended import  jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
import logging
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
logging.basicConfig(level=logging.ERROR)
app.config['SQLALCHEMY_DATABASE_URI'] = str(engine.url)
app.config['JWT_SECRET_KEY'] = 'Guyzaken29'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'instances')

db = SQLAlchemy(app)
jwt = JWTManager(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app, resources={r"/*": {"origins": "https://librarysystemguy.netlify.app/*", "methods": ["GET", "POST", "DELETE", "PUT", "OPTIONS"]}})

# only if db is empty, run the following function in the entry point to populate the database with some data:
def populate_db():
        
        c1 = Customer(customer_name='Guy Zaken', city='Tel Aviv', age=29)
        c2 = Customer(customer_name='Tomer Knoler', city='Tel Aviv', age=30)

        db_session.add_all([c1, c2])


        b1 = Book(book_name='The Great Gatsby', author='F. Scott Fitzgerald',
                  year_published=1925, type=1, amount=3)
        b2 = Book(book_name='1984', author='George Orwell', year_published=1949,
                  type=2, amount=5)
        b3 = Book(book_name='To Kill a Mockingbird', author='Harper Lee',
                  year_published=1960, type=3, amount=4)
        b4 = Book(book_name='Brave New World', author='Aldous Huxley',
                  year_published=1932, type=1, amount=2)
        b5 = Book(book_name='Moby Dick', author='Herman Melville',
                  year_published=1851, type=2, amount=6)
        b6 = Book(book_name='Pride and Prejudice', author='Jane Austen',
                  year_published=1813, type=3, amount=1)

        db_session.add_all([b1, b2, b3, b4, b5, b6])
        
        u1 = User(user_name='guy', password='123456', permission='read_only',customer_id=1)
        u2 = User(user_name='sara', password='123456', permission='read_write',customer_id=None)
        u3 = User(user_name='tomer', password='123', permission='read_only',customer_id=1)

        db_session.add_all([u1, u2, u3])

        db_session.commit()

        l1 = Loan(book_id=b1.book_id, customer_id=c1.customer_id,
                  loan_date=date(2025, 1, 1), return_date=date(2025, 1, 10),
                  return_status=True)
        l2 = Loan(book_id=b3.book_id, customer_id=c2.customer_id,
                  loan_date=date(2025, 1, 5), return_date=date(2025, 1, 15),
                  return_status=False)
        l3 = Loan(book_id=b5.book_id, customer_id=c1.customer_id,
                  loan_date=date(2025, 1, 10), return_date=date(2025, 1, 20),
                  return_status=True)
        l4 = Loan(book_id=b6.book_id, customer_id=c2.customer_id,
                  loan_date=date(2025, 1, 3), return_date=date(2025, 1, 12),
                  return_status=False)
        l5 = Loan(book_id=b2.book_id, customer_id=c1.customer_id,
                  loan_date=date(2025, 1, 7), return_date=date(2025, 1, 17),
                  return_status=True)
        l6 = Loan(book_id=b4.book_id, customer_id=c2.customer_id,
                  loan_date=date(2025, 1, 9), return_date=date(2025, 1, 18),
                  return_status=False)

        db_session.add_all([l1, l2, l3, l4, l5, l6])

        db_session.commit()


@app.route('/signup', methods=['POST'])
def register():
    data = request.get_json()
    customer_name = data.get('customer_name')
    user_name = data.get('user_name')
    password = data.get('password')
    city = data.get('city')
    age = data.get('age')
    existing_customer = get_customer_from_db(customer_name)
    if  existing_customer:
        create_new_user(customer_name, user_name, password)
        return jsonify({"status": "User created successfully"}), 201
    else:
        customer_created = create_customer(customer_name, city, age)
        if customer_created:
            create_new_user(customer_name, user_name, password)
            return {"status": 201}
    return {"status": 201}



    
@app.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    user_name = data.get('user_name')
    password = data.get('password')
    existing_user_name = User.query.filter(user_name == User.user_name).first()
    if existing_user_name is None:
        return {"msg": "user not found"}, 401
    elif not existing_user_name.verify_password(password):
        return {"error": "Invalid credentials"}, 401
    else:
        access_token = create_access_token_for_user(existing_user_name)
        return jsonify(access_token=access_token), 200


   


@app.route('/library')
@jwt_required()
def library_actions():
    try:
        current_user_id = get_jwt_identity()
        customer_exist = db_session.get(User, current_user_id)
        if not customer_exist:
            return jsonify(get_metrics()),200

        if customer_exist.permission == permissions_level['customer']:
            return books_actions(), 200
        else:
            return jsonify({"msg": "Permission denied"}), 403
    except Exception as e:
        logging.error(f"Error in /library route: {str(e)}")
        return jsonify({"error": str(e)}), 422


 
@app.route('/books/<int:book_id>',methods=['DELETE'])
def delete_book(book_id):
    delete_book_logic(book_id)
    return {'status': 201}

@app.route('/books/<string:book_name>')
def get_book(book_name):
    return jsonify(get_book_by_name(book_name))

@app.route('/books/intro/<string:book_name>')
def get_book_intro(book_name):
    return jsonify(get_book_intro_logic(book_name))



@app.route('/customerview')
@jwt_required()
def customer_view():
    current_user_id = get_jwt_identity()
    user_exist = db_session.get(Customer, current_user_id)
    if  user_exist:
        return jsonify(get_instock_books())
    else: 
        return jsonify({"msg": "Permission denied"}), 403

@app.route('/books',methods=['GET','POST','PUT'])
@jwt_required()
def books_actions():
    current_user_id = get_jwt_identity()
    user_exist = db_session.get(User, current_user_id)
    if  user_exist == None:
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
    else: 
        return jsonify({"msg": "Permission denied"}), 403

@app.route('/images/<filename>')
def uploaded_files(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/books/img', methods=['POST'])
@jwt_required()
def upload_book_img():
    current_user_id = get_jwt_identity()
    user_exist = db_session.get(User, current_user_id)
    if  user_exist == None:
        data = request.get_json()
        book_name = data.get('book_name')

        if not book_name:
            return jsonify({"error": "Book name is required"}), 400

        book = Book.query.filter_by(book_name=book_name).first()
        if not book:
            return jsonify({"error": "Book not found"}), 404

        image_url = get_book_image(book_name)
        if image_url:
            try:
                save_img_to_db_and_folder(image_url, book)
                return jsonify({"message": "Image saved successfully"}), 201
            except Exception as e:
                print(f"Error saving image for '{book_name}': {e}")
                return jsonify({"error": "Error saving image"}), 500
        else:
            return jsonify({"error": "Image not found"}), 404
    else: 
        return jsonify({"msg": "Permission denied"}), 403




@app.route('/customers/<string:customer_name>')
def get_customer(customer_name):
    return jsonify(get_customer_by_name(customer_name))


@app.route('/customers/<int:customer_id>',methods=['DELETE'])
def delete_customer(customer_id):
    delete_customer_logic(customer_id)
    return {'status': 404}

@app.route('/customers',methods=['GET','POST','PUT'])
@jwt_required()
def customers_actions():
    current_user_id = get_jwt_identity()
    user_exist = db_session.get(User, current_user_id)
    if  user_exist == None:
        if request.method == 'GET':
            return jsonify(get_active_customers())
        if request.method == 'POST':
            data = request.get_json()
            name = data.get("customer_name")
            city = data.get("city")
            age = data.get("age")
            create_customer(name=name, city=city, age=age)
            return {'status': 200 }
    else: 
        return jsonify({"msg": "Permission denied"}), 403
        
        
@app.route('/loans',methods=['GET','POST','PUT'])
@jwt_required()
def loans_actions():
    current_user_id = get_jwt_identity()
    user_exist = db_session.get(User, current_user_id)
    if  user_exist == None:
        if request.method == 'GET':
            return jsonify(get_active_loans())
        if request.method == 'POST':
            data = request.get_json()
            customer_name = data.get("customer_name")
            book_name = data.get("book_name")
            create_loan(customer_name=customer_name, book_name=book_name)
            return  {'status': 201}
    else: 
        return jsonify({"msg": "Permission denied"}), 403

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
    # with app.app_context():
    #     db.drop_all()
    #     Base.metadata.create_all(engine)        
    #     populate_db()
    app.run(debug=True, port=5001)




    