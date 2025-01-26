from datetime import date, datetime, timedelta
from sqlalchemy import DateTime, Boolean, Column, ForeignKey, Integer, String, and_, create_engine, func
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, relationship
from dbClasses import *
import google.generativeai as genai
from flask_jwt_extended import create_access_token
from io import BytesIO
from PIL import Image
import requests
import uuid
from bs4 import BeautifulSoup


loan_type_to_days = {
    "1": 10,
    "2": 5,
    "3": 2
}


permissions_level = {
    "customer": "read_only",
    "librarian": "read_write"
}


def create_access_token_for_user(existing_user_name):
    if existing_user_name.permission == 'read_write':
        additional_claims = {
            "permissions_level": existing_user_name.permission,
            "user_name": existing_user_name.user_name,
            "user_id": existing_user_name.user_id,
            "customer_name": None,
        }
    else:
        user_name_full_name = Customer.query.filter(existing_user_name.customer_id == Customer.customer_id).first()
        additional_claims = {
            "permissions_level": existing_user_name.permission,
            "user_name": existing_user_name.user_name,
            "customer_name": user_name_full_name.customer_name,
        }
    access_token = create_access_token(identity=str(existing_user_name.customer_id), additional_claims=additional_claims)
    return access_token

def save_img_to_db_and_folder(image_url, book):
    image_response = requests.get(image_url)
    image_response.raise_for_status()

    # Ensure the directory exists
    directory = os.path.join( "instances")
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Generate a unique filename
    file_name = f"{uuid.uuid4()}.jpg"
    file_path = os.path.join(directory, file_name)

    # Save the image to the file system
    with open(file_path, 'wb') as f:
        f.write(image_response.content)

    # Create an UploadedFile instance (assuming it's your database model)
    book_image = UploadedFile(file_name=file_name, book_id=book.book_id)
    db_session.add(book_image)
    db_session.commit()

def create_new_user(customer_name, user_name, password):
    customer_from_db = get_customer_from_db(customer_name)
    if customer_from_db:
        
        db_session.add(User(customer_id=customer_from_db.customer_id,user_name=user_name,password=password, permission=permissions_level['customer']))
        db_session.commit()
    else: 
        db_session.add(User(customer_id=None,user_name=user_name,password=password, permission=permissions_level['librarian']))
        db_session.commit()
        return {"msg": "new librarian added"}
    return {"msg": "new user added"}




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
        if existing_book.amount == 0:
            existing_book.instock = False
        db_session.add(Loan(customer_book_loan, customer_id,loan_date, return_date))
        db_session.commit()
    else: return {'status': 404}

def create_customer(name, city, age):
    db_session.add(Customer(name, city, age))
    db_session.commit()
    return True
    

def create_new_book(book_name, author, publish_year, type, amount):
    db_session.add(Book(book_name, author, publish_year, type, amount))
    db_session.commit()

def update_loan(loan_id):
    existing_loan = Loan.query.filter(Loan.loan_id ==loan_id).first()
    if existing_loan:
        existing_loan.return_status = True
        db_session.commit()
        return {'status': 200}
    else: 
        return {'status': 404}
    



def get_book_image(book_name):
    """
    Fetches an image of the specified book from Google Images.

    Args:
        book_name: The name of the book to search for.

    Returns:
        The URL of the image if found, otherwise None.
    """
    try:
        search_url = f"https://www.google.com/search?q={book_name}+book+cover&tbm=isch"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')
        for img_tag in img_tags:
            if 'src' in img_tag.attrs:
                image_url = img_tag['src']
                if image_url.startswith('http'):
                    return image_url

        print(f"No image found for '{book_name}'")
        return None

    except Exception as e:
        print(f"Error fetching image for '{book_name}': {e}")
        return None

def get_book_intro(book_name):
    genai.configure(api_key="AIzaSyDeG2vU-st-hpTaBjykwyLh_6FbNlfZ244")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"write a few lines about the book {book_name} for information about it")
    return response.text

def get_customer_from_db(customer_name):
    customer_from_db = Customer.query.filter(func.lower(Customer.customer_name) == customer_name.lower()).first()
    return customer_from_db

def get_book_from_db(book_name):
    book_from_db = Book.query.filter(func.lower(Book.book_name) == book_name.lower()).first()
    return book_from_db





def get_metrics():
    total_books = Book.query.filter(Book.instock == 1).count()

    total_customers = Customer.query.filter(Customer.active == 1).count()

    active_loans = Loan.query.filter(Loan.return_date >= datetime.now(), Loan.return_status == 0 ).count()

    overdue_loans = Loan.query.filter(Loan.return_date < datetime.now(), Loan.return_status == 0).count()

    metrics = {
        'totalBooks': total_books,
        'totalCustomers': total_customers,
        'activeLoans': active_loans,
        'overdueLoans': overdue_loans
    }

    return metrics
    
def get_active_customers():
    customers = Customer.query.filter_by(active = 1).all()
    customers_get = [customer.to_dict() for customer in customers]
    return customers_get

def get_active_loans():
    loans = Loan.query.filter_by(return_status = 0).all()
    all_loans = [loan.to_dict() for loan in loans]
    return all_loans

def get_late_loans():
    true_date_time = datetime.now().strftime('%Y-%m-%d')
    late_loans = Loan.query.filter(Loan.return_date < true_date_time, Loan.return_status == 0).all()
    get_late = [loan.to_dict() for loan in late_loans]
    return get_late

def get_instock_books():
    books = Book.query.filter(and_(Book.instock == 1, Book.amount > 0))
    all_books = [book.to_dict() for book in books]
    return all_books

def get_book_by_name(book_name):
    book_exist = get_book_from_db(book_name)
    if book_exist:
        return book_exist.to_dict()
    else: return {'message': 'Book not found'}

def get_customer_by_name(customer_name):
    customer_exist = get_customer_from_db(customer_name)
    if customer_exist:
        return customer_exist.to_dict()
    else: return {'message': 'Customer not found'}

def get_customer_active_loans(customer_name):
    customer_exist = get_customer_from_db(customer_name)
    if customer_exist:
        customer_loans = Loan.query.filter(Loan.customer_id == customer_exist.customer_id, Loan.return_status == 0).all()
        all_customer_loans = [loan.to_dict() for loan in customer_loans]
        return all_customer_loans
    
        
    else: return {'message': 'Customer not found'}





    pass


def delete_book(book_id):
    book_exist = Book.query.filter(Book.book_id == book_id, Book.instock == 1).first()
    if book_exist:
        book_exist.instock = False
        db_session.commit()
        return {'status': 200}
    else: return {'status': 404}

def delete_customer(customer_id):
    customer_exist = Customer.query.filter(Customer.customer_id == customer_id, Customer.active == 1).first()
    if customer_exist:
        customer_exist.active = False
        db_session.commit()
        return {'status': 200}
    else: return {'status': 404}


