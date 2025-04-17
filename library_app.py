import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId
import pandas as pd
import certifi

# MongoDB connection
client = MongoClient(
    "mongodb+srv://maarijkhan246:fRYUQGIl1cNTjptT@cluster0.mssodvj.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=certifi.where()
)
db = client["library"]
books_collection = db["books"]

# Tailwind-inspired custom CSS
def custom_css():
    st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f1f5f9;
    }

    .stButton > button {
        width: 100%;
        font-weight: 600;
        padding: 12px 24px;
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 10px;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 8px rgba(59, 130, 246, 0.2);
    }

    .stButton > button:hover {
        background-color: #2563eb;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(37, 99, 235, 0.3);
    }

    .book-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        transition: box-shadow 0.2s ease;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.04);
    }

    .book-card:hover {
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
    }

    .book-card h4 {
        margin-bottom: 12px;
        font-size: 22px;
        color: #0f172a;
    }

    .book-card p {
        margin: 6px 0;
        font-size: 16px;
        color: #334155;
    }

    .stTextInput>div>input,
    .stNumberInput>div>input,
    .stSelectbox>div>div>div {
        padding: 12px;
        border-radius: 10px;
        border: 1px solid #cbd5e1;
        background-color: #ffffff;
        font-size: 15px;
    }

    .stCheckbox>div {
        font-size: 16px;
    }

    .stSidebar {
        background-color: #e0f2fe;
        padding: 10px;
    }

    .stMetric {
        background: #ffffff;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
        text-align: center;
    }

    .stMetricLabel {
        color: #64748b;
        font-size: 14px;
    }

    .stMetricValue {
        color: #0f172a;
        font-size: 24px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to display a book
def show_book(book):
    st.markdown(f"""
    <div class='book-card'>
        <h4>📖 {book['title']}</h4>
        <p><b>Author:</b> {book['author']}</p>
        <p><b>Year:</b> {book['year']}</p>
        <p><b>Genre:</b> {book['genre']}</p>
        <p><b>Read:</b> {"✅ Yes" if book['read'] else "❌ No"}</p>
    </div>
    """, unsafe_allow_html=True)

# Page: Add Book
def add_book_page():
    st.subheader("📘 Add a New Book")
    with st.form("add_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=0, max_value=2100, step=1)
        genre = st.text_input("Genre")
        read = st.checkbox("Have you read this book?")
        submitted = st.form_submit_button("Add Book")

        if submitted:
            if title and author and genre:
                book = {
                    "title": title,
                    "author": author,
                    "year": int(year),
                    "genre": genre,
                    "read": read
                }
                books_collection.insert_one(book)
                st.success("✅ Book added successfully!")
            else:
                st.warning("⚠️ Please fill out all fields.")

# Page: Search Books
def search_books_page():
    st.subheader("🔍 Search Books")
    keyword = st.text_input("Enter title or author to search")

    if keyword:
        results = books_collection.find({
            "$or": [
                {"title": {"$regex": keyword, "$options": "i"}},
                {"author": {"$regex": keyword, "$options": "i"}}
            ]
        })
        found = False
        for book in results:
            show_book(book)
            found = True
        if not found:
            st.warning("❌ No books found.")

# Page: All Books
def view_all_books_page():
    st.subheader("📚 All Books in Your Library")
    books = list(books_collection.find())
    if not books:
        st.info("📭 No books in your library yet.")
    else:
        for book in books:
            show_book(book)

# Page: Remove Book
def remove_book_page():
    st.subheader("❌ Remove a Book")
    books = list(books_collection.find())
    book_titles = [f"{book['title']} ({book['author']})" for book in books]
    book_map = {f"{book['title']} ({book['author']})": book["_id"] for book in books}

    if book_titles:
        selected = st.selectbox("Select a book to remove", book_titles)
        if st.button("Remove Book"):
            books_collection.delete_one({"_id": book_map[selected]})
            st.success("✅ Book removed successfully!")
    else:
        st.info("📭 No books to remove.")

# Page: Statistics
def statistics_page():
    st.subheader("📊 Library Statistics")
    total = books_collection.count_documents({})
    read = books_collection.count_documents({"read": True})
    unread = total - read

    st.metric("Total Books", total)
    st.metric("Read Books", read)
    st.metric("Unread Books", unread)

    chart_data = pd.DataFrame({
        "Status": ["Read", "Unread"],
        "Count": [read, unread]
    })
    st.bar_chart(chart_data.set_index("Status"))

# Main App
def main():
    st.set_page_config(page_title="📚 Personal Library Manager", layout="wide")
    custom_css()
    st.title("📚 Personal Library Manager")

    menu = st.sidebar.radio("Navigate", ["Add Book", "Search Books", "All Books", "Remove Book", "Statistics"])

    if menu == "Add Book":
        add_book_page()
    elif menu == "Search Books":
        search_books_page()
    elif menu == "All Books":
        view_all_books_page()
    elif menu == "Remove Book":
        remove_book_page()
    elif menu == "Statistics":
        statistics_page()

if __name__ == "__main__":
    main()
