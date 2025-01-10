### base of db 
# loans = [
#     (4, 4, "2025-01-04", None),  # Loaned book 4 to customer 4
#     (5, 5, "2025-01-05", "2025-01-10"),  # Returned
#     (6, 6, "2025-01-06", None),  # Loaned book 6 to customer 6
#     (7, 7, "2025-01-07", "2025-01-12"),  # Returned
#     (8, 8, "2025-01-08", None),  # Loaned book 8 to customer 8
#     (1, 1, "2025-01-01", None),  # Loaned book 1 to customer 1
#     (2, 2, "2025-01-02", "2025-01-05"),  # Returned
#     (3, 3, "2025-01-03", None)
# ]
# customers = [
#     ("John Doe", "New York", 30),
#     ("Jane Smith", "San Francisco", 25),
#     ("Michael Brown", "Chicago", 40),
#     ("Emily White", "Los Angeles", 35),
# ]
# books = [
#     ("Poker Strategy", "David Sklansky", 1987, 1, 15, True),
#     ("The Mathematics of Poker", "Bill Chen", 2006, 1, 12, True),
#     ("Modern Poker Theory", "Michael Acevedo", 2019, 1, 10, True),
#     ("Formula 1: The Pinnacle", "Maurice Hamilton", 2020, 2, 8, True),
#     ("Senna Versus Prost", "Malcolm Folley", 2009, 2, 5, True),
#     ("Cryptoassets", "Chris Burniske", 2017, 3, 20, True),
#     ("The Bitcoin Standard", "Saifedean Ammous", 2018, 3, 18, True),
#     ("Uncommon Grounds", "Mark Pendergrast", 1999, 4, 10, True),
#     ("Coffee: A Global History", "Jonathan Morris", 2019, 4, 7, True),
# ]




#create db:
# def test():
#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS books (
#         bookid INTEGER PRIMARY KEY AUTOINCREMENT,
#         bookname TEXT NOT NULL,
#         author TEXT NOT NULL,
#         yearPublished INTEGER,
#         type INTEGER,
#         amount INTEGER,
#         instock boolean DEFAULT TRUE
        
#     )
#     """)
#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS customers (
#         customerid INTEGER PRIMARY KEY AUTOINCREMENT,
#         customername TEXT NOT NULL,
#         city TEXT NOT NULL,
#         age INTEGER
#     )
#     """),
#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS loans (
#         loanid INTEGER PRIMARY KEY AUTOINCREMENT,
#         bookid INTEGER,
#         customerid INTEGER,
#         loandate DATE,
#         returndate DATE,
#         FOREIGN KEY (bookid) REFERENCES books(bookid),
#         FOREIGN KEY (customerid) REFERENCES customers(customerid)
#     )
#     """),
#     for book in books:
#         cur.execute("""
#             INSERT INTO books (bookname, Author, YearPublished, Type, amount, instock)
#             VALUES (?, ?, ?, ?, ?, ?)
#         """, book)
#     for customer in customers:
#         cur.execute("""
#             INSERT INTO customers (customername, City, Age)
#             VALUES (?, ?, ?)
#         """, customer)
#     for loan in loans:
#         cur.execute("""
#             INSERT INTO loans (bookId, customerId, loanDate, returnDate)
#             VALUES (?, ?, ?, ?)
#         """, loan)
#     conn.commit()


## CLASSES AND MENUS
# class Actions(Enum):
#     ADD = 1
#     DISPLAY = 2
#     FIND = 3
#     DELETE = 4 
#     EXIT = 5
# class Create(Enum):
#     LOAN = 1
#     MEMBER = 2
#     BOOK = 3
#     RETURN = 4
#     MENU = 5
# class Display(Enum):
#     CUSTOMERS = 1
#     LOANS = 2
#     LATE_LOANS = 3
#     BOOKS = 4
#     MENU = 5
# class Find(Enum):
#     CUSTOMER = 1
#     BOOK = 2
#     MENU = 3
# class Delete(Enum):
#     CUSTOMER = 1
#     BOOK = 2
#     MENU = 3
# def action_menu():
#     for act in Actions:
#         print(f"{act.value} -- {act.name}")
# def create_menu():
#     for act in Create:
#         print(f"{act.value} -- {act.name}")
# def display_menu():
#     for act in Display:
#         print(f"{act.value} -- {act.name}")
# def find_menu():
#     for act in Find:
#         print(f"{act.value} -- {act.name}")
# def delete_menu():
#     for act in Delete:
#         print(f"{act.value} -- {act.name}")
# def clear_terminal():
#  if platform.system() == "Windows":
#         os.system("cls")  # For Windows
#     else:
#         os.system("clear")  # For Unix-based systems like macOS and Linux




#     # while True:
#     #     action_menu()
#     #     user_selection = Actions(int(input("Select desired action: ")))
#     #     clear_terminal()
#     #     if user_selection == Actions.EXIT:exit()
#     #     elif user_selection == Actions.ADD:
#     #         create_menu()
#     #         create_selection = Create(int(input("Select desired action: ")))
#     #         clear_terminal()
#     #         if create_selection == Create.LOAN:create_loan()
#     #         if create_selection == Create.MEMBER:create_member()
#     #         if create_selection == Create.BOOK:create_new_book()
#     #         if create_selection == Create.RETURN:return_book()
#     #         if create_selection == Create.MENU:action_menu()
#     #     elif user_selection == Actions.DISPLAY:
#     #         display_menu()
#     #         display_selection = Display(int(input("Select desired action: ")))
#     #         clear_terminal()
#     #         if display_selection == Display.CUSTOMERS:display_customers()
#     #         if display_selection == Display.BOOKS:display_books()
#     #         if display_selection == Display.LOANS:display_loans()
#     #         if display_selection== Display.LATE_LOANS:display_late_loans()
#     #         if display_selection== Display.MENU:action_menu()
#     #     elif user_selection == Actions.FIND:
#     #         find_menu()
#     #         find_selection = Find(int(input("Select desired action: ")))
#     #         clear_terminal()
#     #         if find_selection == Find.CUSTOMER:find_customer_name()
#     #         if find_selection == Find.BOOK:find_book_name()
#     #         if find_selection == Find.MENU:action_menu()
#     #     elif user_selection == Actions.DELETE:
#     #         delete_menu()
#     #         delete_selection = Delete(int(input("Select desired action: ")))
#     #         clear_terminal()
#     #         if delete_selection == Delete.CUSTOMER:delete_customer()
#     #         if delete_selection == Delete.BOOK:delete_book()
#     #         if delete_selection == Delete.MENU:action_menu()
#     #     else: print("Choose only from given actions")

    