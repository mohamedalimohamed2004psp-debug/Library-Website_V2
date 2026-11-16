from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'sql2304105',
    'database': 'library_db'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM AUTHOR")
    authors = cursor.fetchall()
    
    cursor.execute("""
        SELECT b.*, a.name AS author_name, p.name AS publisher_name, c.name AS category_name 
        FROM BOOK b
        LEFT JOIN AUTHOR a ON b.author_id = a.author_id
        LEFT JOIN PUBLISHER p ON b.publisher_id = p.publisher_id
        LEFT JOIN CATEGORY c ON b.category_id = c.category_id
    """)
    books = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('dashboard.html', user_name="Admin", authors=authors, books=books)

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        country = request.form['country']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO AUTHOR (name, country) VALUES (%s, %s)", (name, country))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))
        
    return render_template('add_author.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        publish_year = request.form['publish_year']
        author_id = request.form['author_id']
        publisher_id = request.form['publisher_id']
        category_id = request.form['category_id']
        
        cursor.execute(
            "INSERT INTO BOOK (title, price, publish_year, author_id, publisher_id, category_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (title, price, publish_year, author_id, publisher_id, category_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))
        
    cursor.execute("SELECT * FROM AUTHOR")
    authors = cursor.fetchall()
    cursor.execute("SELECT * FROM PUBLISHER")
    publishers = cursor.fetchall()
    cursor.execute("SELECT * FROM CATEGORY")
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('add_book.html', authors=authors, publishers=publishers, categories=categories)

@app.route('/edit_author/<int:author_id>', methods=['GET', 'POST'])
def edit_author(author_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form['name']
        country = request.form['country']
        cursor.execute("UPDATE AUTHOR SET name = %s, country = %s WHERE author_id = %s", (name, country, author_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))
        
    cursor.execute("SELECT * FROM AUTHOR WHERE author_id = %s", (author_id,))
    author = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not author:
        return redirect(url_for('dashboard'))
        
    return render_template('edit_author.html', author=author)

@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        publish_year = request.form['publish_year']
        author_id = request.form['author_id']
        publisher_id = request.form['publisher_id']
        category_id = request.form['category_id']
        cursor.execute(
            "UPDATE BOOK SET title = %s, price = %s, publish_year = %s, author_id = %s, publisher_id = %s, category_id = %s WHERE book_id = %s",
            (title, price, publish_year, author_id, publisher_id, category_id, book_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))
        
    cursor.execute("SELECT * FROM BOOK WHERE book_id = %s", (book_id,))
    book = cursor.fetchone()
    
    if not book:
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))
        
    cursor.execute("SELECT * FROM AUTHOR")
    authors = cursor.fetchall()
    cursor.execute("SELECT * FROM PUBLISHER")
    publishers = cursor.fetchall()
    cursor.execute("SELECT * FROM CATEGORY")
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('edit_book.html', book=book, authors=authors, publishers=publishers, categories=categories)

@app.route('/delete_author/<int:author_id>', methods=['POST'])
def delete_author(author_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM AUTHOR WHERE author_id = %s", (author_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM BOOK WHERE book_id = %s", (book_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', '')
    min_price = request.args.get('min_price', 0, type=float)
    max_price = request.args.get('max_price', 999999, type=float)
    category_id = request.args.get('category_id', '')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM CATEGORY")
    categories = cursor.fetchall()

    query = """
        SELECT b.*, a.name AS author_name, p.name AS publisher_name, c.name AS category_name
        FROM BOOK b
        JOIN AUTHOR a ON b.author_id = a.author_id
        JOIN PUBLISHER p ON b.publisher_id = p.publisher_id
        JOIN CATEGORY c ON b.category_id = c.category_id
        WHERE b.title LIKE %s AND b.price BETWEEN %s AND %s
    """
    params = [f"%{keyword}%", min_price, max_price]

    if category_id:
        query += " AND b.category_id = %s"
        params.append(category_id)

    query += " ORDER BY b.price ASC"

    cursor.execute(query, tuple(params))
    books = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('search.html', books=books, categories=categories, keyword=keyword, min_price=min_price, max_price=max_price, selected_category=category_id)

@app.route('/catalogue')
def catalogue():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT b.book_id, b.title, b.price, b.publish_year, 
               a.name AS author_name, p.name AS publisher_name, c.name AS category_name
        FROM BOOK b
        JOIN AUTHOR a ON b.author_id = a.author_id
        JOIN PUBLISHER p ON b.publisher_id = p.publisher_id
        JOIN CATEGORY c ON b.category_id = c.category_id
    """)
    books = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('catalogue.html', books=books)

@app.route('/reports')
def reports():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT c.name AS category_name, COUNT(b.book_id) AS total_books, AVG(b.price) AS average_price
        FROM CATEGORY c
        LEFT JOIN BOOK b ON c.category_id = b.category_id
        GROUP BY c.category_id, c.name
    """)
    category_stats = cursor.fetchall()

    cursor.execute("""
        SELECT a.name AS author_name, COUNT(b.book_id) AS book_count
        FROM AUTHOR a
        JOIN BOOK b ON a.author_id = b.author_id
        GROUP BY a.author_id, a.name
        HAVING COUNT(b.book_id) >= 2
    """)
    prolific_authors = cursor.fetchall()

    cursor.execute("""
        SELECT SUM(price) AS total_price, MIN(price) AS smallest_price, MAX(price) AS largest_price
        FROM BOOK
    """)
    price_summary = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('reports.html', category_stats=category_stats, prolific_authors=prolific_authors, price_summary=price_summary)

@app.route('/loans')
def loans():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT l.loan_id, b.title AS book_title, m.name AS member_name, l.loan_date
        FROM LOAN l
        JOIN BOOK b ON l.book_id = b.book_id
        JOIN MEMBER m ON l.member_id = m.member_id
        WHERE l.return_date IS NULL
    """)
    active_loans = cursor.fetchall()

    cursor.execute("""
        SELECT m.member_id, m.name, m.email
        FROM MEMBER m
        LEFT JOIN LOAN l ON m.member_id = l.member_id
        WHERE l.loan_id IS NULL
    """)
    inactive_members = cursor.fetchall()

    cursor.execute("""
        SELECT b.book_id, b.title
        FROM BOOK b
        LEFT JOIN LOAN l ON b.book_id = l.book_id
        WHERE l.loan_id IS NULL
    """)
    unborrowed_books = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('loans.html', active_loans=active_loans, inactive_members=inactive_members, unborrowed_books=unborrowed_books)

@app.route('/most_borrowed')
def most_borrowed():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT b.book_id, b.title, COUNT(l.loan_id) AS loan_count
        FROM BOOK b
        JOIN LOAN l ON b.book_id = l.book_id
        GROUP BY b.book_id, b.title
        ORDER BY loan_count DESC
        LIMIT 3
    """)
    top_books = cursor.fetchall()

    cursor.execute("""
        SELECT m.member_id, m.name, COUNT(l.loan_id) AS loan_count
        FROM MEMBER m
        JOIN LOAN l ON m.member_id = l.member_id
        GROUP BY m.member_id, m.name
        ORDER BY loan_count DESC
        LIMIT 1
    """)
    top_member = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('most_borrowed.html', top_books=top_books, top_member=top_member)

@app.route('/authors_books')
def authors_books():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT a.author_id, a.name, COUNT(b.book_id) AS book_count
        FROM AUTHOR a
        LEFT JOIN BOOK b ON a.author_id = b.author_id
        GROUP BY a.author_id, a.name
    """)
    authors_count = cursor.fetchall()

    cursor.execute("""
        SELECT b.book_id, b.title, a.name AS author_name, a.country AS author_country, 
               p.name AS publisher_name, p.country AS publisher_country
        FROM BOOK b
        JOIN AUTHOR a ON b.author_id = a.author_id
        JOIN PUBLISHER p ON b.publisher_id = p.publisher_id
        WHERE a.country = p.country
    """)
    same_country_books = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('authors_books.html', authors_count=authors_count, same_country_books=same_country_books)

if __name__ == '__main__':
    app.run(debug=True)