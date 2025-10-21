📚 Library Management System (Python Console Application)
🧾 Overview

The Library Management System is a Python-based console application that helps manage book borrowing and returning for Admins, Students, and Staff Members.
It features secure login, book management, borrowing with automatic return deadlines, and an intuitive console interface.

🚀 Features
👤 User Roles
1. Admin

Add, remove, and view books

View members and their borrowed books

Manage library records

2. Student

Log in using student ID and password

Borrow available books (7-day return deadline)

Return borrowed books

3. Staff

Log in using staff ID and password

Borrow and return books just like students

🔑 Login System

When the program starts, you’ll be asked:

Who wants to log in? (admin/student/staff)


Depending on your answer, the system requests a username and password, then displays a personalized welcome message, for example:

Welcome Admin! Please enter your username and password.


If credentials are incorrect, access is denied.

🔐 Default Login Credentials
Role	Username / ID	Password	Description
Admin	admin	1234	Full access to the system
Student	S001	pass123	Can borrow and return books
Student	S002	pass123	Can borrow and return books
Student	S003	pass123	Can borrow and return books
Staff	ST001	staff123	Can borrow and return books
Staff	ST002	staff123	Can borrow and return books

🧠 You can add or edit these credentials in the code under the members dictionary.

📗 Book Management
Admin Functions

Add new books

View all books

Remove books by ISBN

Student/Staff Functions

View available books

Borrow and return books

See return deadlines

⏳ Borrowing & Returning Books

When a student or staff borrows a book:

A 7-day deadline is automatically set

Example:

John borrowed 'Python Programming Basics' on 2025-10-21.
Return Deadline: 2025-10-28


When the book is returned, the system updates availability.

🧮 Data Storage

Data is managed in-memory using Python dictionaries and lists for simplicity.
(You can later upgrade to use SQLite or MySQL for persistence.)

⚙️ Technologies Used

Language: Python 3.x

Modules: datetime, getpass

💡 Example Workflow
Welcome to the Library Management System!

Who wants to log in? admin
Welcome Admin! Please enter your username and password.
Username: admin
Password: *****
Login successful!

1. Add Book
2. View Books
3. View Members
4. Logout
Choose an option: 1

Enter Book Title: Python Programming
Enter Author: Mark Lutz
Enter ISBN: 9780135159941
Enter Copies: 3

Book added successfully!

🧠 Future Improvements

Add database support for data persistence

Include email notifications for overdue books

Add fine system for late returns

Build a graphical user interface (GUI) using Tkinter or Figma

👨‍💻 Author

Ramadan A. Bangura
Limkokwing University of Creative Technology, Sierra Leone
Course: Object-Oriented Programming 1 (PROG211)

🏁 How to Run

Make sure you have Python 3.x installed.

Copy all project files into one folder.

Run the system from the terminal or command prompt:

python demo.py


Follow the prompts to log in and manage the library.
