import streamlit as st
import json

# File to store the library data
LIBRARY_FILE = "library.json"

def load_library():
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Load existing books
library = load_library()

st.title("📚 Personal Library Manager")

menu = ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics"]
choice = st.sidebar.selectbox("Select an option", menu)

if choice == "Add a Book":
    st.subheader("Add a New Book")
    title = st.text_input("Enter Book Title")
    author = st.text_input("Enter Author Name")
    year = st.number_input("Enter Publication Year", min_value=0, format="%d")
    genre = st.text_input("Enter Genre")
    read_status = st.radio("Have you read this book?", ("Yes", "No"))
    
    if st.button("Add Book"):
        library.append({
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": True if read_status == "Yes" else False
        })
        save_library(library)
        st.success(f"'{title}' has been added to your library!")

elif choice == "Remove a Book":
    st.subheader("Remove a Book")
    titles = [book["title"] for book in library]
    selected_title = st.selectbox("Select a book to remove", titles)
    if st.button("Remove Book"):
        library = [book for book in library if book["title"] != selected_title]
        save_library(library)
        st.success(f"'{selected_title}' has been removed from your library!")

elif choice == "Search for a Book":
    st.subheader("Search for a Book")
    search_option = st.radio("Search by", ("Title", "Author"))
    search_query = st.text_input("Enter search term")
    
    if st.button("Search"):
        results = [book for book in library if search_query.lower() in book[search_option.lower()].lower()]
        if results:
            for book in results:
                st.write(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
        else:
            st.warning("No books found.")

elif choice == "Display All Books":
    st.subheader("Your Library")
    if library:
        for book in library:
            st.write(f"📖 {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
    else:
        st.info("Your library is empty.")

elif choice == "Display Statistics":
    st.subheader("Library Statistics")
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    
    st.write(f"Total Books: {total_books}")
    st.write(f"Percentage Read: {percentage_read:.2f}%")

st.sidebar.text("Data is auto-saved!")
