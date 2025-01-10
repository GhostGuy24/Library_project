from flask import Flask, jsonify, request
import sqlite3
from sqlalchemy import DateTime, Boolean, Column, ForeignKey, Integer, String, and_, create_engine, func
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from datetime import date, datetime, timedelta

app = Flask(__name__)
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
                "name": self.customername,
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
        def to_dict(self):
            return {
                "loanid": self.loanid,
                "bookid": self.bookid,
                "customerid": self.customerid,
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
    name = data.get("name")
    existing_member = Customer.query.filter(func.lower(Customer.customername) == name.lower()).first()
    if existing_member: 
        display_books()
        customer_id = existing_member.customerid
        user_book_loan = data.get("bookid")
        chosen_book = Book.query.filter(Book.bookid == user_book_loan).first()
        if chosen_book:
            loan_date = datetime.now().date()
            return_date = (datetime.now() + timedelta(days=7)).date()
            amount_to_subtract = 1
            chosen_book.amount -= amount_to_subtract
            db_session.add(Loan(chosen_book.bookid, customer_id,loan_date, return_date))
            db_session.commit()
        else: return {'status': 404}
    else: create_member()
# C- creating a new customer id if doesnt exist in db - converted to ORM
def create_member():
        data = request.get_json()
        name = data.get("name")
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
    # display_book_types() - left aside
    categoty = data.get("type")
    amount = data.get("amount")
    db_session.add(Book(book_name, author, publish_year, categoty, amount))
    db_session.commit()
# C - customer returns a book - converted to ORM
def return_book():
    data = request.get_json()
    name = data.get("name")
    loan_to_close = data.get("loanid")
    existing_member = Customer.query.filter(func.lower(Customer.customername) == name.lower()).first()
    if existing_member: 
        existing_loans = Loan.query.filter(existing_member.customerid == Loan.customerid, Loan.loanid ==loan_to_close).first()
        if existing_loans:
            existing_loans.returnstatus = 1
            db_session.commit()
        else: return {'status': 404}
    else: return {'status': 404}
        


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
    late_loans = Loan.query.filter(Loan.returndate < true_date_time).all()
    display_late = [loan.to_dict() for loan in late_loans]
    return(display_late)
#R - displaying book types(categories) - left aside
def display_book_types():
    cur.execute("SELECT type FROM books WHERE instock = 1 GROUP BY type")
    book_types = cur.fetchall()
    for type in book_types:
        if type[0] == 1:
            print(f"{type[0]} - Poker Books\n")
        if type[0] == 2:
            print(f"{type[0]} - F1 Books\n")
        if type[0] == 3:
            print(f"{type[0]} - Crypto Books\n")
        if type[0] == 4:
            print(f"{type[0]} - Coffee Books\n")
# R - displaying books - converted to ORM
def display_books():
    books = Book.query.filter(and_(Book.instock == 1, Book.amount > 0))
    all_books = [book.to_dict() for book in books]
    return jsonify(all_books)



# FIND book by name - converted to ORM
def find_book_name():
    data = request.get_json()
    name = data.get("bookname")
    book_exist = Book.query.filter(func.lower(Book.bookname) == name.lower()).first()
    if book_exist:
        return jsonify(book_exist.to_dict())
    else: return {'status': 404}
# FIND customer by name - converted to ORM
def find_customer_name():
    data = request.get_json()
    name = data.get("customername")
    customer_exist = Customer.query.filter(func.lower(Customer.customername) == name.lower()).first()   
    if customer_exist:
        return jsonify(customer_exist.to_dict())



# U -update, not yet
def update():
    pass



# D -delete book (not really delete we deactive books) - converted to ORM
def delete_book():
    data = request.get_json()
    name = data.get("bookname")
    book_exist = Book.query.filter(func.lower(Book.bookname) == name.lower(), Book.instock == 1).first()
    if book_exist:
        book_exist.instock = False
        db_session.commit()
        return {'status': 200}
    else: return {'status': 404}
# D - delete customer( """") - converted to ORM
def delete_customer():
    data = request.get_json()
    name = data.get("customername")
    customer_exist = Customer.query.filter(func.lower(Customer.customername) == name.lower(), Customer.active == 1).first()
    if customer_exist:
        customer_exist.active = False
        db_session.commit()
        return {'status': 200}
    else: return {'status': 404}


@app.route('/')
def home():
    return "Welcome"

@app.route('/library',methods=['GET','POST','DELETE','PUT'])
def library_actions():
    if request.method == 'GET':
        #display_customers() 
        # display_loans()
        # display_late_loans()
        # display_books()
        return  
    if request.method == 'POST':
        # create_loan()
        # create_new_book()
        # find_customer_name()
        # find_book_name()
        return {'status': 201}
    if request.method == 'DELETE':
        # return_book()
        #delete_book()
        # delete_customer()
        return 
    if request.method == 'PUT':
        pass


if __name__ == "__main__":
    app.run(debug=True)




    