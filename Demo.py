# demo.py
# Interactive demo with improved login experience
from operations import (
    verify_login, users, list_all_books, list_all_members,
    add_book, update_book, delete_book,
    add_member, update_member, delete_member,
    borrow_book, return_book, search_books,
    get_member_borrow_history, get_active_borrows, get_all_borrow_history
)
import operations

def input_non_empty(prompt):
    while True:
        v = input(prompt).strip()
        if v:
            return v
        print("Input cannot be empty.")

# ----------- NEW LOGIN FLOW -----------
def login_prompt():
    print("\n==============================")
    print("  WELCOME TO THE LIBRARY HUB  ")
    print("==============================")
    print("Who is logging in?")
    print("1) Admin")
    print("2) Staff")
    print("3) Student")
    print("0) Exit System")

    role_map = {"1": "admin", "2": "staff", "3": "student"}

    while True:
        choice = input("Enter your choice: ").strip()
        if choice == "0":
            print("Goodbye 👋")
            exit()
        role = role_map.get(choice)
        if not role:
            print("Invalid choice. Please enter 1, 2, 3, or 0.")
            continue

        print(f"\nWelcome, {role.capitalize()}! Please enter your login details below.\n")
        while True:
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            ok, user_role = verify_login(username, password)

            # Check both credentials and matching role type
            if ok and user_role == role:
                print(f"\n✅ Login successful! Welcome {username} ({role.capitalize()})\n")
                return username, role
            elif ok and user_role != role:
                print(f"⚠️ That username belongs to a {user_role}. Please select the correct category.")
                break  # go back to role choice
            else:
                print("❌ Invalid username or password. Please try again.\n")
        # If incorrect role, loop to main menu again
        print("\nLet's try again from the beginning...\n")
        return login_prompt()

# ------------------- MENUS -------------------

def admin_menu(username):
    while True:
        print("\n=== ADMIN MENU ===")
        print("1) List books")
        print("2) Add book")
        print("3) Update book")
        print("4) Delete book")
        print("5) List members")
        print("6) Add member")
        print("7) Update member")
        print("8) Delete member")
        print("9) View active borrows")
        print("10) View full borrow history")
        print("0) Logout")
        choice = input("Choice: ").strip()
        if choice == "1":
            for isbn, b in list_all_books().items():
                print(f"{isbn}: {b}")
        elif choice == "2":
            isbn = input_non_empty("ISBN: ")
            title = input_non_empty("Title: ")
            author = input_non_empty("Author: ")
            genre = input_non_empty("Genre: ")
            total = int(input_non_empty("Total copies: "))
            ok = add_book(isbn, title, author, genre, total)
            print("✅ Added." if ok else "❌ Failed (duplicate ISBN or invalid genre).")
        elif choice == "3":
            isbn = input_non_empty("ISBN to update: ")
            title = input("New title (or skip): ").strip() or None
            author = input("New author (or skip): ").strip() or None
            genre = input("New genre (or skip): ").strip() or None
            total = input("New total copies (or skip): ").strip()
            total = int(total) if total else None
            ok = update_book(isbn, title, author, genre, total)
            print("✅ Updated." if ok else "❌ Failed.")
        elif choice == "4":
            isbn = input_non_empty("ISBN to delete: ")
            ok = delete_book(isbn)
            print("✅ Deleted." if ok else "❌ Failed (maybe borrowed or not found).")
        elif choice == "5":
            for m in list_all_members():
                print(f"{m['member_id']}: {m['name']} | {m['email']} | borrowed: {m['borrowed_books']}")
        elif choice == "6":
            mid = input_non_empty("Member ID: ")
            name = input_non_empty("Name: ")
            email = input_non_empty("Email: ")
            ok = add_member(mid, name, email)
            print("✅ Member added." if ok else "❌ Failed.")
        elif choice == "7":
            mid = input_non_empty("Member ID to update: ")
            name = input("New name (or skip): ").strip() or None
            email = input("New email (or skip): ").strip() or None
            ok = update_member(mid, name, email)
            print("✅ Updated." if ok else "❌ Failed.")
        elif choice == "8":
            mid = input_non_empty("Member ID to delete: ")
            ok = delete_member(mid)
            print("✅ Deleted." if ok else "❌ Failed (has borrowed books or not found).")
        elif choice == "9":
            active = get_active_borrows()
            print("\n📚 Active Borrows:")
            if not active: print("None")
            for r in active: print(r)
        elif choice == "10":
            hist = get_all_borrow_history()
            print("\n📖 Borrow History:")
            if not hist: print("No history.")
            for r in hist: print(r)
        elif choice == "0":
            print("👋 Logging out Admin...")
            break
        else:
            print("Invalid choice.")

def staff_menu(username):
    user = users.get(username)
    member_id = user.get("member_id")
    if not member_id:
        print("❌ No member ID linked to this staff account.")
        return
    while True:
        print("\n=== STAFF MENU ===")
        print("1) List books")
        print("2) Borrow book (for yourself)")
        print("3) Return book")
        print("4) Search books")
        print("0) Logout")
        choice = input("Choice: ").strip()
        if choice == "1":
            for isbn, b in list_all_books().items():
                print(f"{isbn}: {b}")
        elif choice == "2":
            isbn = input_non_empty("ISBN to borrow: ")
            borrow_book(isbn, member_id)
        elif choice == "3":
            isbn = input_non_empty("ISBN to return: ")
            return_book(isbn, member_id)
        elif choice == "4":
            q = input_non_empty("Search query: ")
            by = input("By title or author (title default): ").strip().lower() or "title"
            res = search_books(q, by)
            if not res: print("No matches found.")
            for isbn, b in res: print(f"{isbn}: {b}")
        elif choice == "0":
            print("👋 Logging out Staff...")
            break
        else:
            print("Invalid choice.")

def student_menu(username):
    user = users.get(username)
    member_id = user.get("member_id")
    if not member_id:
        print("❌ No member ID linked to this student account.")
        return
    while True:
        print("\n=== STUDENT MENU ===")
        print("1) List books")
        print("2) Borrow book")
        print("3) Return book")
        print("4) View borrowed books")
        print("5) View borrow history")
        print("0) Logout")
        choice = input("Choice: ").strip()
        if choice == "1":
            for isbn, b in list_all_books().items():
                print(f"{isbn}: {b}")
        elif choice == "2":
            isbn = input_non_empty("ISBN to borrow: ")
            borrow_book(isbn, member_id)
        elif choice == "3":
            isbn = input_non_empty("ISBN to return: ")
            return_book(isbn, member_id)
        elif choice == "4":
            for m in list_all_members():
                if m["member_id"] == member_id:
                    print(f"Borrowed: {m['borrowed_books']}")
                    break
        elif choice == "5":
            hist = get_member_borrow_history(member_id)
            if not hist: print("No history.")
            for r in hist: print(r)
        elif choice == "0":
            print("👋 Logging out Student...")
            break
        else:
            print("Invalid choice.")

# ------------------- MAIN LOOP -------------------
def main():
    print("\n📘 Mini Library Management System - Interactive Demo")
    while True:
        username, role = login_prompt()
        if role == "admin":
            admin_menu(username)
        elif role == "staff":
            staff_menu(username)
        elif role == "student":
            student_menu(username)
        print("\nSession ended. Returning to login menu...\n")

if __name__ == "__main__":
    main()
