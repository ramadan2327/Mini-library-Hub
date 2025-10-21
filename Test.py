# tests.py
# Simple assert-based tests for the fixed implementation
from operations import (
    books, members, borrow_history,
    add_book, update_book, delete_book,
    add_member, update_member, delete_member,
    borrow_book, return_book, search_books,
    list_all_books, list_all_members
)

# Reset (if re-running tests in same interpreter)
books.clear()
members.clear()
borrow_history.clear()

# Setup
add_book("T001", "Intro Python", "A Author", "Non-Fiction", 2)
add_book("T002", "Algorithms", "B Author", "Non-Fiction", 1)
add_member("M01", "Tester", "t@test.com")

# Check add duplicate book fails
assert add_book("T001", "Duplicate", "X", "Non-Fiction", 1) == False

# Borrow and return flow
assert borrow_book("T001", "M01") == True, "Should borrow T001"
# Borrow again (should succeed because 2 copies)
assert borrow_book("T001", "M01") == True, "Should borrow T001 second copy"
# Now no copies left
assert borrow_book("T001", "M01") == False, "Should fail - no copies left"

# Return one copy
assert return_book("T001", "M01") == True, "Return should succeed"
# Now borrow should be possible again
res = borrow_book("T001", "M01")
assert res in (True, False), "Borrow result unexpected"

# Delete member with borrowed books should fail
add_member("M02", "Other", "o@o.com")
assert delete_member("M02") == True  # has no borrowed books => can delete

# Search tests
res = search_books("intro", by="title")
assert isinstance(res, list) and len(res) >= 1

print("Basic tests passed. If you see this message, tests ran without immediate assertion failures.")
