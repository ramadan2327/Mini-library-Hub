# operations.py
# Mini Library Management System - stable implementation
from datetime import date, timedelta

# ------------- Global Data -------------
# Pre-populated books (ISBN -> details)
books = {
    "B001": {"title": "Python Basics", "author": "John Doe", "genre": "Non-Fiction", "total_copies": 3},
    "B002": {"title": "Data Science 101", "author": "Jane Smith", "genre": "Non-Fiction", "total_copies": 2},
    "B003": {"title": "Web Development", "author": "Alice Brown", "genre": "Non-Fiction", "total_copies": 4},
}

# Members list
members = [
    {"member_id": "S001", "name": "Slimzy", "email": "slimzy@example.com", "borrowed_books": []},
    {"member_id": "S002", "name": "Lexicon", "email": "lexicon@example.com", "borrowed_books": []},
    {"member_id": "S003", "name": "Galma", "email": "galma@example.com", "borrowed_books": []},
    {"member_id": "ST001", "name": "Briel", "email": "briel@library.com", "borrowed_books": []},
    {"member_id": "ST002", "name": "Favour", "email": "favour@library.com", "borrowed_books": []},
]

GENRES = ("Fiction", "Non-Fiction", "Sci-Fi", "Biography", "Education")

# Borrow history: list of records
# record = {
#   "isbn", "member_id", "member_name", "title", "date_borrowed", "due_date", "date_returned" (or None)
# }
borrow_history = []

# Users: username -> {password, role, member_id (optional)}
users = {
    # admins
    "ramadan": {"password": "128", "role": "admin"},
    "love": {"password": "126", "role": "admin"},
    # staff (linked to member IDs)
    "Briel": {"password": "briel01", "role": "staff", "member_id": "ST001"},
    "Favour": {"password": "sia02", "role": "staff", "member_id": "ST002"},
    # students (linked)
    "slimzy": {"password": "slimzypass", "role": "student", "member_id": "S001"},
    "lexicon": {"password": "lexiconpass", "role": "student", "member_id": "S002"},
    "galma": {"password": "galmapass", "role": "student", "member_id": "S003"},
}

# Borrow policy
BORROW_LIMIT = 3
BORROW_DAYS = 7

# ------------- Helper functions -------------
def find_member(member_id):
    return next((m for m in members if m["member_id"] == member_id), None)

def find_member_by_username(username):
    u = users.get(username)
    if u and "member_id" in u:
        return find_member(u["member_id"])
    return None

# ------------- Books CRUD -------------
def add_book(isbn, title, author, genre, total_copies):
    """Add a new book. Return True if added, False otherwise."""
    if isbn in books:
        return False
    if genre not in GENRES:
        return False
    books[isbn] = {"title": title, "author": author, "genre": genre, "total_copies": int(total_copies)}
    return True

def update_book(isbn, title=None, author=None, genre=None, total_copies=None):
    """Update an existing book. Return True if success."""
    book = books.get(isbn)
    if not book:
        return False
    if genre and genre not in GENRES:
        return False
    if title: book["title"] = title
    if author: book["author"] = author
    if genre: book["genre"] = genre
    if total_copies is not None:
        # Ensure new total_copies >= currently borrowed copies
        borrowed_count = sum(1 for r in borrow_history if r["isbn"] == isbn and r["date_returned"] is None)
        if int(total_copies) < borrowed_count:
            return False
        book["total_copies"] = int(total_copies)
    return True

def delete_book(isbn):
    """Delete book only if no copies are currently borrowed."""
    if isbn not in books:
        return False
    borrowed_count = sum(1 for r in borrow_history if r["isbn"] == isbn and r["date_returned"] is None)
    if borrowed_count > 0:
        return False
    del books[isbn]
    return True

# ------------- Members CRUD -------------
def add_member(member_id, name, email):
    """Add a member. Return True if added."""
    if find_member(member_id):
        return False
    members.append({"member_id": member_id, "name": name, "email": email, "borrowed_books": []})
    return True

def update_member(member_id, name=None, email=None):
    m = find_member(member_id)
    if not m:
        return False
    if name: m["name"] = name
    if email: m["email"] = email
    return True

def delete_member(member_id):
    m = find_member(member_id)
    if not m:
        return False
    if m["borrowed_books"]:
        return False
    members.remove(m)
    return True

# ------------- Search -------------
def search_books(query, by="title"):
    q = query.lower()
    results = []
    for isbn, book in books.items():
        if by == "author" and q in book["author"].lower():
            results.append((isbn, book.copy()))
        elif by == "title" and q in book["title"].lower():
            results.append((isbn, book.copy()))
    return results

# ------------- Borrow / Return -------------
def borrow_book(isbn, member_id):
    """
    Borrow a book for member_id. Return True on success.
    Updates borrow_history and member.borrowed_books and decrements available copy.
    """
    if isbn not in books:
        print("Book not found.")
        return False
    member = find_member(member_id)
    if not member:
        print("Member not found.")
        return False

    # currently borrowed copies for isbn
    borrowed_count = sum(1 for r in borrow_history if r["isbn"] == isbn and r["date_returned"] is None)
    available = books[isbn]["total_copies"] - borrowed_count
    if available <= 0:
        print("No copies available.")
        return False

    if len(member["borrowed_books"]) >= BORROW_LIMIT:
        print(f"Borrow limit reached ({BORROW_LIMIT}).")
        return False

    today = date.today()
    due = today + timedelta(days=BORROW_DAYS)
    record = {
        "isbn": isbn,
        "member_id": member_id,
        "member_name": member["name"],
        "title": books[isbn]["title"],
        "date_borrowed": today,
        "due_date": due,
        "date_returned": None
    }
    borrow_history.append(record)
    member["borrowed_books"].append(isbn)
    print(f"Borrowed '{books[isbn]['title']}' — due {due.isoformat()}.")
    return True

def return_book(isbn, member_id):
    """Return book for member. Updates history and member borrowed_books. Return True on success."""
    member = find_member(member_id)
    if not member:
        print("Member not found.")
        return False
    # find most recent active record
    record = next((r for r in reversed(borrow_history) if r["isbn"] == isbn and r["member_id"] == member_id and r["date_returned"] is None), None)
    if not record:
        print("No active borrow record found for that ISBN and member.")
        return False
    record["date_returned"] = date.today()
    if isbn in member["borrowed_books"]:
        member["borrowed_books"].remove(isbn)
    print(f"Returned '{record['title']}' on {record['date_returned'].isoformat()}.")
    return True

# ------------- History / Utilities -------------
def get_member_borrow_history(member_id):
    return [r.copy() for r in borrow_history if r["member_id"] == member_id]

def get_active_borrows():
    return [r.copy() for r in borrow_history if r["date_returned"] is None]

def get_all_borrow_history():
    return [r.copy() for r in borrow_history]

def list_all_books():
    return {isbn: book.copy() for isbn, book in books.items()}

def list_all_members():
    return [m.copy() for m in members]

# ------------- Login helper -------------
def verify_login(username, password):
    """Return (True, role) if valid, otherwise (False, None)"""
    u = users.get(username)
    if u and u["password"] == password:
        return True, u["role"]
    return False, None
