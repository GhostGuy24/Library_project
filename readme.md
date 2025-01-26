# Library Management System - Backend

This project is the backend for a library management system, designed to help librarians manage books, customers, and loans efficiently. It includes features such as JWT-based authentication, bcrypt password hashing, and an integration with the Gimeni API for fetching book introductions and images.

---

## Features
- **Book Management**: Add, view, delete, and manage books in the library.
- **Customer Management**: Add, view, and manage customer records.
- **Loan Management**: Manage book loans, including creating, returning, and tracking late loans.
- **Authentication**: Secure user login with JWT authentication and bcrypt for password encryption.
- **Gimeni API Integration**:
  - Automatically fetch book introductions.
  - Search, download, and upload book images with a single action.
- **Role-Based Access**:
  - `Librarian`: Full access to all functionalities.
  - `Read-Only Users`: Limited access to viewing functionalities.

---

## Technologies Used
- **Flask**: Web framework for building the backend.
- **Flask-JWT-Extended**: For managing user authentication and authorization.
- **Flask-Bcrypt**: For secure password hashing.
- **Flask-CORS**: To enable cross-origin requests.
- **SQLAlchemy**: ORM for database management.
- **Gimeni API**: For fetching book details and images.
- **Logging**: For error tracking and debugging.

---

## How to Use

### Prerequisites
- Python 3.x installed on your system.
- Database set up (SQLAlchemy scoped session is used).

### Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/GhostGuy24/Library_Project_Final.git
   cd libraryproject/backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure the app:
   - Update `app.config['UPLOAD_FOLDER']` in the code to point to the desired folder for storing book images.

### Database Setup
1. Run the app with the following code block:
   ```python
   if __name__ == "__main__":
       # with app.app_context():
       #     db.drop_all()
       #     db.create_all()
       #     unit_test()
   ```
   This will set up and populate the database with sample data for testing.


### Users for Testing 
- **Librarian**:
  - Username: `sara`
  - Password: `123456`
  - Permissions: Full access.
- **Read-Only Users**:
  - Username: `guy` 
  - Password: `123456`
  - Permissions: Limited access.

### Running the App
1. Start the backend server:
   ```bash
   python app.py
   ```
2. The server will be available at `http://localhost:5001`.

### Testing the App
You can test the app using the HTML pages provided in the `frontend` folder. These pages interact with the backend API to perform various actions like viewing books, managing loans, and more.

---

## API Endpoints

### Authentication
- **`POST /signup`**: Register a new user.
- **`POST /login`**: Log in and obtain an access token.

### Book Management
- **`GET /books`**: View all books in stock.
- **`POST /books`**: Add a new book (requires `librarian` access).
- **`DELETE /books/<int:book_id>`**: Delete a book by ID.
- **`GET /books/<string:book_name>`**: Fetch details about a specific book.
- **`GET /books/intro/<string:book_name>`**: Fetch a book introduction using the Gimeni API.
- **`POST /books/img`**: Upload a book image using the Gimeni API.

### Customer Management
- **`GET /customers`**: View all active customers.
- **`POST /customers`**: Add a new customer (requires `librarian` access).
- **`DELETE /customers/<int:customer_id>`**: Delete a customer by ID.
- **`GET /customers/<string:customer_name>`**: Fetch details about a specific customer.

### Loan Management
- **`GET /loans`**: View all active loans.
- **`POST /loans`**: Create a new loan (requires `librarian` access).
- **`DELETE /loans/<int:loan_id>`**: Return a book and update the loan status.
- **`GET /loans/<string:customer_name>`**: View active loans for a specific customer.
- **`GET /loans/late`**: Fetch all late loans.

---

## Notes
- The project includes detailed error handling and logging to ensure smooth operation.
- Make sure to configure the database and API keys correctly before deployment.
- The provided HTML pages in the `frontend` folder are ready to use for testing the app.

---

