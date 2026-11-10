
from abc import ABC, abstractmethod


# Tuple: fixed menu options
MENU_OPTIONS = (
    "Add Book",
    "Register Member",
    "View All Books",
    "Search Books",
    "Borrow Book",
    "Return Book",
    "View Members",
    "Library Report",
    "Exit"
)


# 1. BOOK CLASS
class Book:

    def __init__(self, isbn, title, author, category, copies):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.category = category

        # Encapsulation: private attributes
        self.__total_copies = copies
        self.__available_copies = copies

    def get_available_copies(self):
        return self.__available_copies

    def get_total_copies(self):
        return self.__total_copies

    def add_copies(self, copies):
        self.__total_copies += copies
        self.__available_copies += copies

    def borrow_one(self):
        if self.__available_copies > 0:
            self.__available_copies -= 1
            return True
        return False

    def return_one(self):
        if self.__available_copies < self.__total_copies:
            self.__available_copies += 1
            return True
        return False

    def display(self):
        print("\nISBN:", self.isbn)
        print("Title:", self.title)
        print("Author:", self.author)
        print("Category:", self.category)
        print("Total Copies:", self.__total_copies)
        print("Available Copies:", self.__available_copies)


# 2. ABSTRACT PARENT CLASS
class LibraryUser(ABC):

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    @abstractmethod
    def borrowing_limit(self):
        pass

    @abstractmethod
    def role(self):
        pass


# 3. STUDENT CLASS: INHERITANCE
class StudentMember(LibraryUser):

    def borrowing_limit(self):
        return 2

    def role(self):
        return "Student"


# 4. FACULTY CLASS: INHERITANCE
class FacultyMember(LibraryUser):

    def borrowing_limit(self):
        return 5

    def role(self):
        return "Faculty"


# 5. MAIN LIBRARY CLASS
class Library:

    def __init__(self):

        # Encapsulated library records
        self.__books = {}
        self.__users = {}
        self.__borrowed_records = []

        # Set stores unique book categories
        self.__categories = set()

    # Find a book
    def find_book(self, isbn):
        return self.__books.get(isbn)

    # Find a member
    def find_user(self, user_id):
        return self.__users.get(user_id)

    # ADD BOOK
    def add_book(self):

        print("\n------ ADD NEW BOOK ------")

        isbn = input("Enter ISBN: ").strip()

        if not isbn:
            print("ISBN cannot be empty.")
            return

        if isbn in self.__books:

            try:
                copies = int(input("Enter additional copies: "))

                if copies <= 0:
                    print("Copies must be positive.")
                    return

                self.__books[isbn].add_copies(copies)
                print("Book copies updated successfully!")

            except ValueError:
                print("Enter a valid number.")

            return

        title = input("Enter book title: ").strip()
        author = input("Enter author name: ").strip()
        category = input("Enter category: ").strip()

        if not title or not author or not category:
            print("All book details are required.")
            return

        try:
            copies = int(input("Enter number of copies: "))

            if copies <= 0:
                print("Copies must be positive.")
                return

        except ValueError:
            print("Enter a valid number.")
            return

        book = Book(
            isbn, title.title(), author.title(),
            category.title(), copies
        )

        self.__books[isbn] = book
        self.__categories.add(category.title())

        print("Book added successfully!")

    # REGISTER MEMBER
    def register_member(self):

        print("\n------ MEMBER REGISTRATION ------")

        user_id = input("Enter member ID: ").strip()

        if not user_id:
            print("Member ID cannot be empty.")
            return

        if user_id in self.__users:
            print("Member ID already exists.")
            return

        name = input("Enter member name: ").strip()

        if not name:
            print("Name cannot be empty.")
            return

        print("\n1. Student")
        print("2. Faculty")

        choice = input("Select member type: ")

        if choice == "1":
            member = StudentMember(user_id, name.title())

        elif choice == "2":
            member = FacultyMember(user_id, name.title())

        else:
            print("Invalid member type.")
            return

        self.__users[user_id] = member

        print(member.role(), "registered successfully!")

    # VIEW ALL BOOKS
    def view_books(self):

        print("\n========== BOOK CATALOGUE ==========")

        if not self.__books:
            print("No books available.")
            return

        for book in self.__books.values():
            book.display()
            print("--------------------------------")

    # SEARCH BOOKS
    def search_books(self):

        keyword = input(
            "\nEnter title, author or category: "
        ).strip().lower()

        if not keyword:
            print("Please enter a search term.")
            return

        found = False

        print("\n========== SEARCH RESULTS ==========")

        for book in self.__books.values():

            if (keyword in book.title.lower()
                    or keyword in book.author.lower()
                    or keyword in book.category.lower()):

                book.display()
                found = True

        if not found:
            print("No matching books found.")

    # BORROW BOOK
    def borrow_book(self):

        print("\n========== BORROW BOOK ==========")

        user_id = input("Enter member ID: ").strip()
        member = self.find_user(user_id)

        if member is None:
            print("Member not found.")
            return

        isbn = input("Enter book ISBN: ").strip()
        book = self.find_book(isbn)

        if book is None:
            print("Book not found.")
            return

        # Count books currently borrowed by this member
        active_count = 0

        for record in self.__borrowed_records:

            if record["user_id"] == user_id:
                active_count += 1

        # Polymorphism:
        # The limit depends on the member's actual class.
        if active_count >= member.borrowing_limit():
            print("Borrowing limit reached!")
            print("Your limit is:", member.borrowing_limit())
            return

        if book.borrow_one():

            record = {
                "user_id": user_id,
                "isbn": isbn
            }

            self.__borrowed_records.append(record)

            print("Book borrowed successfully!")
            print("Member:", member.name)
            print("Book:", book.title)

        else:
            print("Sorry, no copies are available.")

    # RETURN BOOK
    def return_book(self):

        print("\n========== RETURN BOOK ==========")

        user_id = input("Enter member ID: ").strip()
        isbn = input("Enter book ISBN: ").strip()

        # Find the matching borrowing record
        for record in self.__borrowed_records:

            if (record["user_id"] == user_id
                    and record["isbn"] == isbn):

                book = self.find_book(isbn)

                if book is not None and book.return_one():

                    self.__borrowed_records.remove(record)

                    print("Book returned successfully!")
                    print("Book:", book.title)

                    return

        print("No matching borrowing record found.")

    # VIEW MEMBERS
    def view_members(self):

        print("\n========== REGISTERED MEMBERS ==========")

        if not self.__users:
            print("No members registered.")
            return

        for member in self.__users.values():

            print("\nMember ID:", member.user_id)
            print("Name:", member.name)
            print("Type:", member.role())
            print("Borrowing Limit:", member.borrowing_limit())

    # LIBRARY REPORT
    def library_report(self):

        total_titles = len(self.__books)

        total_copies = 0
        available_copies = 0

        for book in self.__books.values():

            total_copies += book.get_total_copies()
            available_copies += book.get_available_copies()

        borrowed_copies = len(self.__borrowed_records)

        # Dictionary for category-wise book count
        category_count = {}

        for book in self.__books.values():

            category = book.category

            category_count[category] = (
                category_count.get(category, 0) + 1
            )

        print("\n========== LIBRARY REPORT ==========")

        print("Total Book Titles:", total_titles)
        print("Total Copies:", total_copies)
        print("Available Copies:", available_copies)
        print("Borrowed Copies:", borrowed_copies)
        print("Registered Members:", len(self.__users))

        print("\nUnique Categories:")
        print(", ".join(sorted(self.__categories))
              if self.__categories else "None")

        print("\nBooks by Category:")

        if category_count:
            for category, count in category_count.items():
                print(category, ":", count, "titles")
        else:
            print("No books registered.")

        print("====================================")


# 6. MAIN FUNCTION
def main():

    library = Library()

    while True:

        print("\n")
        print("====================================")
        print("             BOOKNEST")
        print("      LIBRARY MANAGEMENT SYSTEM")
        print("====================================")

        for number, option in enumerate(MENU_OPTIONS, 1):
            print(str(number) + ".", option)

        print("====================================")

        choice = input("Enter your choice (1-9): ")

        if choice == "1":
            library.add_book()

        elif choice == "2":
            library.register_member()

        elif choice == "3":
            library.view_books()

        elif choice == "4":
            library.search_books()

        elif choice == "5":
            library.borrow_book()

        elif choice == "6":
            library.return_book()

        elif choice == "7":
            library.view_members()

        elif choice == "8":
            library.library_report()

        elif choice == "9":
            print("\nThank you for using BOOKNEST!")
            print("Happy Reading!")
            break

        else:
            print("Invalid choice. Select from 1 to 9.")


# PROGRAM EXECUTION
if __name__ == "__main__":
    main()
