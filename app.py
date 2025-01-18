from flask import Flask, jsonify, request
from sqlalchemy import DateTime, Boolean, Column, ForeignKey, Integer, String, and_, create_engine, func
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, relationship
from datetime import date, datetime, timedelta
from flask_cors import CORS



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "DELETE", "PUT", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})
engine = create_engine('sqlite:///library.db')
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

#DB CLASSES
class Customer(Base):
        __tablename__ = 'customers'
        customerid = Column(Integer, primary_key=True)
        customername = Column(String(50), unique=True)
        city = Column(String(120), unique=False)
        age = Column(Integer,unique=True)
        active = Column(Boolean,default=True)
        def to_dict(self):
            return {
                "id": self.customerid,
                "customername": self.customername,
                "city": self.city,
                "age": self.age
            }
        def __init__(self, customername=None, city=None, age=None):
            self.customername = customername
            self.city = city
            self.age = age
class Book(Base):
        __tablename__ = 'books'
        bookid = Column(Integer, primary_key=True)
        bookname = Column(String(50), unique=True)
        author = Column(String(120), unique=False)
        yearPublished = Column(Integer,unique=False)
        type = Column(Integer, unique=False)
        amount = Column(Integer, unique=False)
        instock = Column(Boolean,default=True)
        def to_dict(self):
            return {
                "bookid": self.bookid,
                "bookname": self.bookname,
                "author": self.author,
                "yearPublished": self.yearPublished,
                "type": self.type,
                "amount": self.amount,
                "instock": self.instock
            }
        def __init__(self, bookname=None, author=None,yearPublished =None, type=None, amount=None):
            self.bookname = bookname 
            self.author = author
            self.yearPublished = yearPublished
            self.type = type
            self.amount = amount
class Loan(Base):
        __tablename__ = 'loans'
        loanid = Column(Integer, primary_key=True)
        bookid = Column(Integer, ForeignKey('books.bookid'))
        customerid = Column(Integer, ForeignKey('customers.customerid'))
        loandate = Column(DateTime, unique= False)
        returndate = Column(DateTime, unique= False)
        returnstatus = Column(Boolean,default=False)

        book = relationship("Book", backref="loans")
        customer = relationship("Customer", backref="loans")
        def to_dict(self):
            return {
                "loanid": self.loanid,
                "bookname": self.book.bookname,
                "customername": self.customer.customername,
                "loandate": self.loandate,
                "returndate": self.returndate,
                "returnstatus": self.returnstatus,
            }
        def __init__(self, bookid=None, customerid=None,loandate =None, returndate=None):
            self.bookid = bookid 
            self.customerid = customerid
            self.loandate = loandate
            self.returndate = returndate


###CRUD on db

#C - create(checks if user in the db, if not add him, then book loan, record loan and update amount of books left)
#converted to ORM
def create_loan():
    data = request.get_json()
    customer_name = data.get("customername")
    book_name = data.get("bookname")
    existing_member = Customer.query.filter(func.lower(Customer.customername) == customer_name.lower()).first()
    existing_book = Book.query.filter(func.lower(Book.bookname) == book_name.lower()).first()
    if existing_member and existing_book: 
        customer_id = existing_member.customerid
        user_book_loan = existing_book.bookid
        loan_date = datetime.now().date()
        if existing_book.type == 1:
            return_date = (datetime.now() + timedelta(days=10)).date()
        if existing_book.type == 2:
            return_date = (datetime.now() + timedelta(days=5)).date()
        if existing_book.type == 3:
            return_date = (datetime.now() + timedelta(days=2)).date()
        amount_to_subtract = 1
        existing_book.amount -= amount_to_subtract
        db_session.add(Loan(user_book_loan, customer_id,loan_date, return_date))
        db_session.commit()
    else: return {'status': 404}
# C- creating a new customer id if doesnt exist in db - converted to ORM
def create_member():
        data = request.get_json()
        name = data.get("customername")
        city = data.get("city")
        age = data.get("age")
        db_session.add(Customer(name ,city , age))
        db_session.commit()
# C- create a new book in the system - converted to ORM
def create_new_book():
    data = request.get_json()
    book_name = data.get("bookname")
    author = data.get("author")
    publish_year = data.get("yearPublished")
    categoty = data.get("type")
    amount = data.get("amount")
    db_session.add(Book(book_name, author, publish_year, categoty, amount))
    db_session.commit()
# C - customer returns a book - converted to ORM
def return_book(loanid):
    existing_loans = Loan.query.filter(Loan.loanid ==loanid).first()
    if existing_loans:
        existing_loans.returnstatus = 1
        db_session.commit()
    else: return {'status': 404}
    return {'status': 200}
        
#R - displaying all matrics
def get_metrics():
    total_books = Book.query.count()

    total_customers = Customer.query.count()

    active_loans = Loan.query.filter(Loan.returndate >= datetime.now(), Loan.returnstatus == 0 ).count()

    overdue_loans = Loan.query.filter(Loan.returndate < datetime.now(), Loan.returnstatus == 0).count()

    metrics = {
        'totalBooks': total_books,
        'totalCustomers': total_customers,
        'activeLoans': active_loans,
        'overdueLoans': overdue_loans
    }

    return jsonify(metrics)
#R - displaying all customers - converted to ORM
def display_customers():
    customers = Customer.query.filter_by(active = 1).all()
    customers_display = [customer.to_dict() for customer in customers]
    return jsonify(customers_display)
#R - display all loans - converted to ORM
def display_loans():
    loans = Loan.query.filter_by(returnstatus = 0).all()
    all_loans = [loan.to_dict() for loan in loans]
    return jsonify(all_loans)
# R - display late loans - converted to ORM
def display_late_loans():
    true_date_time = datetime.now().strftime('%Y-%m-%d')
    late_loans = Loan.query.filter(Loan.returndate < true_date_time, Loan.returnstatus == 0).all()
    display_late = [loan.to_dict() for loan in late_loans]
    return(display_late)
# R - displaying books - converted to ORM
def display_books():
    books = Book.query.filter(and_(Book.instock == 1, Book.amount > 0))
    all_books = [book.to_dict() for book in books]
    return jsonify(all_books)



# U -update, not yet
def update():
    pass




@app.route('/')
def home():
    return "Welcome"

@app.route('/library')
def library_actions():
    if request.method == 'GET':
        return get_metrics()
    



 
@app.route('/books/<int:bookid>',methods=['DELETE'])
# D -delete book (not really delete we deactive books)
def delete_book(bookid):
    if request.method == 'OPTIONS':
        return '', 200
    elif request.method == 'DELETE':
       
            book_exist = Book.query.filter(Book.bookid == bookid, Book.instock == 1).first()
            if book_exist:
                book_exist.instock = False
                db_session.commit()
                return {'status': 201}
            else: return {'status': 404}

@app.route('/books/find')
# FIND book by name 
def find_book_name():
    name = request.args.get("bookname", '').lower()    
    book_exist = Book.query.filter(func.lower(Book.bookname) == name.lower()).first()
    if book_exist:
        return jsonify(book_exist.to_dict())
    else: return jsonify({'message': 'Book not found'})
# R , C - display and add book
@app.route('/books',methods=['GET','POST','PUT'])
def books_actions():
    if request.method == 'GET':
        return display_books()
    if request.method == 'POST':
        create_new_book()
        return {'status': 200 }
    if request.method == 'PUT':
        return jsonify({"message": "PUT request not implemented yet"}), 200






@app.route('/customers/find')
# FIND book by name 
def find_customer_name():
    name = request.args.get("customername")    
    customer_exist = Customer.query.filter(func.lower(Customer.customername) == name.lower()).first()
    if customer_exist:
        return jsonify(customer_exist.to_dict())
    else: return jsonify({'message': 'Customer not found'})

@app.route('/customers/<int:customerid>',methods=['DELETE'])
# D -delete customer (not really delete we deactive books)
def del_customer(customerid):
    # D - delete customer( """")
    if request.method == 'DELETE':
        customer_exist = Customer.query.filter(Customer.customerid == customerid, Customer.active == 1).first()
        if customer_exist:
            customer_exist.active = False
            db_session.commit()
            return {'status': 200}
        else: return {'status': 404}
# R , C - display and add customer
@app.route('/customers',methods=['GET','POST','PUT'])
# R , C - display and add customer

def customers_actions():
    if request.method == 'GET':
        return display_customers()
    if request.method == 'POST':
        create_member()
        return {'status': 200 }
    
    if request.method == 'PUT':
        pass


@app.route('/loans',methods=['GET','POST','PUT'])
# R , C - display and add loan
def loans_actions():
    if request.method == 'GET':
        
        return display_loans()
    if request.method == 'POST':
        create_loan()
        return  {'status': 201}
        
    if request.method == 'PUT':
        pass
@app.route('/loans/late')
# R - display late loans
def display_late():
    return display_late_loans()
@app.route('/loans/<int:loanid>',methods=['DELETE'])
# D - Return book 
def return_book(loanid):
    existing_loans = Loan.query.filter(Loan.loanid ==loanid).first()
    if existing_loans:
        existing_loans.returnstatus = 1
        db_session.commit()
    else: return {'status': 404}
    return {'status': 200}


@app.route('/loans/find')
# FIND customer loans by name 
def find_customer_loans():
    name = request.args.get("customername")    
    customer_exist = Customer.query.filter(func.lower(Customer.customername) == name.lower()).first()
    if customer_exist:
        customer_loans = Loan.query.filter(Loan.customerid == customer_exist.customerid, Loan.returnstatus == 0).all()
        if customer_loans : 
            all_customer_loans = [loan.to_dict() for loan in customer_loans]
            return jsonify(all_customer_loans)
        else: return {"status": 403}
        
    else: return jsonify({'message': 'Customer not found'})



if __name__ == "__main__":
    app.run(debug=True, port=5001)




    