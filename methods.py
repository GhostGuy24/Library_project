from datetime import date, datetime, timedelta
from sqlalchemy import DateTime, Boolean, Column, ForeignKey, Integer, String, and_, create_engine, func
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, relationship
from dbClasses import *
# engine = create_engine('sqlite:///library.db')
# db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
# Base = declarative_base()
# Base.query = db_session.query_property()




def get_customer_from_db(customer_name):
    customer_from_db = Customer.query.filter(func.lower(Customer.customer_name) == customer_name.lower()).first()
    return customer_from_db

def get_book_from_db(book_name):
    book_from_db = Book.query.filter(func.lower(Book.book_name) == book_name.lower()).first()
    return book_from_db

###CRUD on db
#dict for loan types
loan_type_to_days = {
    "1": 10,
    "2": 5,
    "3": 1
}

#C - create(checks if user in the db, if not add him, then book loan, record loan and update amount of books left)
#converted to ORM
def create_loan(customer_name, book_name):
    existing_customer = get_customer_from_db(customer_name)
    existing_book = get_book_from_db(book_name)
    if existing_customer and existing_book: 
        customer_id = existing_customer.customer_id
        customer_book_loan = existing_book.book_id
        loan_date = datetime.now().date()
        return_date = (datetime.now() + timedelta(days=loan_type_to_days[str(existing_book.type)]))
        amount_to_subtract = 1
        existing_book.amount -= amount_to_subtract
        db_session.add(Loan(customer_book_loan, customer_id,loan_date, return_date))
        db_session.commit()
    else: return {'status': 404}
# C- creating a new customer id if doesnt exist in db - converted to ORM
def create_customer(name, city, age):
    db_session.add(Customer(name, city, age))
    db_session.commit()
# C- create a new book in the system - converted to ORM
def create_new_book(book_name, author, publish_year, type, amount):
    db_session.add(Book(book_name, author, publish_year, type, amount))
    db_session.commit()
# u - customer returns a book - converted to ORM
def update_loan(loan_id):
    existing_loan = Loan.query.filter(Loan.loan_id ==loan_id).first()
    if existing_loan:
        existing_loan.return_status = True
        db_session.commit()
        return {'status': 200}
    else: 
        return {'status': 404}
    
        
#R - displaying all metrics
def get_metrics():
    total_books = Book.query.count()

    total_customers = Customer.query.count()

    active_loans = Loan.query.filter(Loan.return_date >= datetime.now(), Loan.return_status == 0 ).count()

    overdue_loans = Loan.query.filter(Loan.return_date < datetime.now(), Loan.return_status == 0).count()

    metrics = {
        'totalBooks': total_books,
        'totalCustomers': total_customers,
        'activeLoans': active_loans,
        'overdueLoans': overdue_loans
    }

    return metrics
    
#R - displaying all customers - converted to ORM
def get_active_customers():
    customers = Customer.query.filter_by(active = 1).all()
    customers_get = [customer.to_dict() for customer in customers]
    return customers_get
#R - get all loans - converted to ORM
def get_active_loans():
    loans = Loan.query.filter_by(return_status = 0).all()
    all_loans = [loan.to_dict() for loan in loans]
    return all_loans
# R - get late loans - converted to ORM
def get_late_loans():
    true_date_time = datetime.now().strftime('%Y-%m-%d')
    late_loans = Loan.query.filter(Loan.return_date < true_date_time, Loan.return_status == 0).all()
    get_late = [loan.to_dict() for loan in late_loans]
    return get_late
# R - geting books - converted to ORM
def get_instock_books():
    books = Book.query.filter(and_(Book.instock == 1, Book.amount > 0))
    all_books = [book.to_dict() for book in books]
    return all_books
# r - get book by name
def get_book_by_name(book_name):
    book_exist = get_book_from_db(book_name)
    if book_exist:
        return book_exist.to_dict()
    else: return {'message': 'Book not found'}
#r - get customer by name
def get_customer_by_name(customer_name):
    customer_exist = get_customer_from_db(customer_name)
    if customer_exist:
        return customer_exist.to_dict()
    else: return {'message': 'Customer not found'}
# r - get customer active loans by customer name 
def get_customer_active_loans(customer_name):
    customer_exist = get_customer_from_db(customer_name)
    if customer_exist:
        customer_loans = Loan.query.filter(Loan.customer_id == customer_exist.customer_id, Loan.return_status == 0).all()
        all_customer_loans = [loan.to_dict() for loan in customer_loans]
        return all_customer_loans
    
        
    else: return {'message': 'Customer not found'}



# U -update, not yet
def update():
    pass

# d - delete book 
def delete_book(book_id):
    book_exist = Book.query.filter(Book.book_id == book_id, Book.instock == 1).first()
    if book_exist:
        book_exist.instock = False
        db_session.commit()
        return {'status': 200}
    else: return {'status': 404}
# d - delete customer
def delete_customer(customer_id):
    customer_exist = Customer.query.filter(Customer.customer_id == customer_id, Customer.active == 1).first()
    if customer_exist:
        customer_exist.active = False
        db_session.commit()
        return {'status': 200}
    else: return {'status': 404}


