USE library_db;

-- F2.1 Search books (WHERE): title keyword, min/max price, category, cheapest first
SELECT * FROM BOOK 
WHERE title LIKE '%a%' 
  AND price BETWEEN 10 AND 30 
  AND category_id = 1 
ORDER BY price ASC;

-- F2.2 Catalogue (JOIN): Books with author name, publisher name, and category name
SELECT b.book_id, b.title, b.price, b.publish_year, 
       a.name AS author_name, 
       p.name AS publisher_name, 
       c.name AS category_name
FROM BOOK b
JOIN AUTHOR a ON b.author_id = a.author_id
JOIN PUBLISHER p ON b.publisher_id = p.publisher_id
JOIN CATEGORY c ON b.category_id = c.category_id;

-- F2.3 Reports (GROUP BY, HAVING):
-- (a) Number of books and average price of each category
SELECT c.name AS category_name, COUNT(b.book_id) AS total_books, AVG(b.price) AS average_price
FROM CATEGORY c
LEFT JOIN BOOK b ON c.category_id = b.category_id
GROUP BY c.category_id, c.name;

-- (b) Authors who wrote at least 2 books
SELECT a.name AS author_name, COUNT(b.book_id) AS book_count
FROM AUTHOR a
JOIN BOOK b ON a.author_id = b.author_id
GROUP BY a.author_id, a.name
HAVING COUNT(b.book_id) >= 2;

-- (c) Total, smallest, and largest price of the whole library
SELECT SUM(price) AS total_price, MIN(price) AS smallest_price, MAX(price) AS largest_price
FROM BOOK;

-- F2.4 Loans (JOIN, LEFT JOIN):
-- (a) Loans not returned yet, with book title and member name
SELECT l.loan_id, b.title AS book_title, m.name AS member_name, l.loan_date
FROM LOAN l
JOIN BOOK b ON l.book_id = b.book_id
JOIN MEMBER m ON l.member_id = m.member_id
WHERE l.return_date IS NULL;

-- (b) Members who never borrowed a book
SELECT m.member_id, m.name, m.email
FROM MEMBER m
LEFT JOIN LOAN l ON m.member_id = l.member_id
WHERE l.loan_id IS NULL;

-- (c) Books that were never borrowed
SELECT b.book_id, b.title
FROM BOOK b
LEFT JOIN LOAN l ON b.book_id = l.book_id
WHERE l.loan_id IS NULL;

-- F2.5 Most borrowed (GROUP BY, ORDER BY, LIMIT):
-- (a) Top 3 books with the most loans
SELECT b.book_id, b.title, COUNT(l.loan_id) AS loan_count
FROM BOOK b
JOIN LOAN l ON b.book_id = l.book_id
GROUP BY b.book_id, b.title
ORDER BY loan_count DESC
LIMIT 3;

-- (b) Member with the most loans
SELECT m.member_id, m.name, COUNT(l.loan_id) AS loan_count
FROM MEMBER m
JOIN LOAN l ON m.member_id = l.member_id
GROUP BY m.member_id, m.name
ORDER BY loan_count DESC
LIMIT 1;

-- F2.6 Authors and books (LEFT JOIN, JOIN):
-- (a) Every author with the number of books, including authors with 0
SELECT a.author_id, a.name, COUNT(b.book_id) AS book_count
FROM AUTHOR a
LEFT JOIN BOOK b ON a.author_id = b.author_id
GROUP BY a.author_id, a.name;

-- (b) Books whose author and publisher come from the same country
SELECT b.book_id, b.title, a.name AS author_name, a.country AS author_country, 
       p.name AS publisher_name, p.country AS publisher_country
FROM BOOK b
JOIN AUTHOR a ON b.author_id = a.author_id
JOIN PUBLISHER p ON b.publisher_id = p.publisher_id
WHERE a.country = p.country;