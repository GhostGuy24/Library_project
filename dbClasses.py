from sqlalchemy import DateTime, Boolean, Column, ForeignKey, Integer, String, and_, create_engine, func
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, relationship

engine = create_engine('sqlite:///library.db')
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

#DB CLASSES
class Customer(Base):
        __tablename__ = 'customers'
        customer_id = Column(Integer, primary_key=True)
        customer_name = Column(String(50), unique=True)
        city = Column(String(120), unique=False)
        age = Column(Integer,unique=True)
        active = Column(Boolean,default=True)
        def to_dict(self):
            return {
                "customer_id": self.customer_id,
                "customer_name": self.customer_name,
                "city": self.city,
                "age": self.age
            }
        def __init__(self, customer_name=None, city=None, age=None):
            self.customer_name = customer_name
            self.city = city
            self.age = age
class Book(Base):
        __tablename__ = 'books'
        book_id = Column(Integer, primary_key=True)
        book_name = Column(String(50), unique=True)
        author = Column(String(120), unique=False)
        year_published = Column(Integer,unique=False)
        type = Column(Integer, unique=False)
        amount = Column(Integer, unique=False)
        instock = Column(Boolean,default=True)
        def to_dict(self):
            return {
                "book_id": self.book_id,
                "book_name": self.book_name,
                "author": self.author,
                "year_published": self.year_published,
                "type": self.type,
                "amount": self.amount,
                "instock": self.instock
            }
        def __init__(self, book_name=None, author=None,year_published =None, type=None, amount=None):
            self.book_name = book_name 
            self.author = author
            self.year_published = year_published
            self.type = type
            self.amount = amount
class Loan(Base):
        __tablename__ = 'loans'
        loan_id = Column(Integer, primary_key=True)
        book_id = Column(Integer, ForeignKey('books.book_id'))
        customer_id = Column(Integer, ForeignKey('customers.customer_id'))
        loan_date = Column(DateTime, unique=False)
        return_date = Column(DateTime, unique=False)
        return_status = Column(Boolean, default=False)

        book = relationship("Book", backref="loans")
        customer = relationship("Customer", backref="loans")

        def to_dict(self):
            return {
                "loan_id": self.loan_id,
                "book_name": self.book.book_name,
                "customer_name": self.customer.customer_name,
                "loan_date": self.loan_date,
                "return_date": self.return_date,
                "return_status": self.return_status,
            }
        
        def __init__(self, book_id=None, customer_id=None, loan_date=None, return_date=None, return_status=None):
            self.book_id = book_id 
            self.customer_id = customer_id
            self.loan_date = loan_date
            self.return_date = return_date
            self.return_status = return_status