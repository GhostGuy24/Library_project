# Book Library

A web-based application for managing a book library, including tracking books, customers, and loan records. The project uses a full-stack development approach with Flask for the backend and JavaScript for frontend interactivity.

---

## Table of Contents

1. [About the Project](#about-the-project)  
2. [Main Functions and Abilities](#main-functions-and-abilities)  
3. [Database Structure](#database-structure)  
4. [Technologies Used](#technologies-used)  
5. [Project Status](#project-status)  
6. [Setup Instructions](#setup-instructions)  
7. [Contact](#contact)  

---

## About the Project

This book library application helps to manage books, customers, and loans effectively. It supports features like adding and updating books, customer management, loan tracking, and returning books.

---

## Main Functions and Abilities

- **Manage Books**:
  - Add new books to the library.
  - Edit or delete existing books.
  - View all books and filter by attributes like type or author.

- **Manage Customers**:
  - Add new customers to the system.
  - Edit or delete customer records.
  - View customer lists and search by city or age.

- **Loan Management**:
  - Record when a book is loaned out.
  - Track return dates and overdue books.

---

## Database Structure

### 1. **Books Table**
| Column Name   | Data Type  | Description                      |
|---------------|------------|----------------------------------|
| `bookId`      | INTEGER    | Primary Key, unique identifier.  |
| `bookname`    | TEXT       | Name of the book.                |
| `Author`      | TEXT       | Author of the book.              |
|`YearPublished`| INTEGER    | Year the book was published.     |
| `Type`        | INTEGER    | Book type (1/2/3).               |
| `amount`      | INTEGER    | amount of books in stock         |
| `instcok`     | boolean    | TRUE OR FALSE                    |

---

### 2. **Customers Table**
| Column Name   | Data Type  | Description                       |
|---------------|------------|-----------------------------------|
| `customerId`  | INTEGER    | Primary Key, unique identifier.  |
| `Name`        | TEXT       | Name of the customer.            |
| `City`        | TEXT       | Customer's city of residence.    |
| `Age`         | INTEGER    | Customer's age.                  |

---

### 3. **Loans Table**
| Column Name   | Data Type  | Description                       |
|---------------|------------|-----------------------------------|
| `loanId`      | INTEGER    | Primary Key, unique identifier.  |
| `bookId`      | INTEGER    | Foreign Key, links to `Books`.   |
| `customerId`  | INTEGER    | Foreign Key, links to `customers`|
| `loanDate`    | DATE       | Date when the book was loaned.   |
| `returnDate`  | DATE       | Date when the book was returned. |

---

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript (with Axios for API requests)
- **Template Engine**: Jinja
- **Database**: SQLite
- **Other Tools**: Postman (for API testing)

---

## Project Status

| Task                                      | Status       |
|-------------------------------------------|--------------|
| **Database Creation**                     | Completed    |
| **Basic CRUD Functionality**              | Read, Create completed  |
| **Connecting Flask**                      | Not Started  |
| **Creating endpoints for CRUD operations**| Not Started  |
| **Using JavaScript for DB Changes**       | Planned      |
| **Creating HTML Pages for Library**       | In Progress  |
| **Work on Design**                        | Not Started  | 
| **Bonus: Additional Features**            | Planned      |

---

## Setup Instructions

### Prerequisites
- [Python](https://www.python.org/) version X.X.X
- Virtual environment tool (optional but recommended)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/book-library.git
