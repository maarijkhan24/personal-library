# 📚 Personal Library Manager

A stylish and user-friendly **Streamlit** app to manage your personal book collection, powered by **MongoDB**.

---

## 🌟 Features

- **Add New Books**: Input title, author, year, genre, and whether you’ve read it.
- **Search Books**: Find books by title or author.
- **View All Books**: Browse your entire collection with a clean card layout.
- **Remove Books**: Easily delete books from your library.
- **Library Statistics**: Visualize the number of read and unread books with metrics and charts.
- **Modern UI**: Tailwind CSS-inspired custom styling.

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **MongoDB (Atlas)**
- **PyMongo**
- **Pandas**
- **Custom HTML/CSS for styling**

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
https://github.com/armeennadeem197/personal-library.git
```
2. Install Dependencies
  ```
3. pip install streamlit pymongo pandas

```
3. Run the App
streamlit run library
```
🔐 MongoDB Setup
```
This project uses MongoDB Atlas. Update the connection string in your code:
client = MongoClient("your_mongodb_connection_string")
Ensure your cluster is accessible and your IP is whitelisted.

```
📁 Folder Structure
c-manager/
│
├── library app.py             # Main application file
├── README.md          # Project description
├── requirements.txt   # (Optional) Python dependencies

```
🙌 Author
Armeen Nadeem

GitHub: @armeennadeem197

