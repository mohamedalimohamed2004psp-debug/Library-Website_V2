USE library_db;

INSERT INTO AUTHOR (name, country) VALUES 
('Naguib Mahfouz', 'Egypt'),
('Ahmed Khaled Tawfik', 'Egypt'),
('William Shakespeare', 'England'),
('Agatha Christie', 'England'),
('Empty Author', 'France');

INSERT INTO PUBLISHER (name, country) VALUES 
('Dar El Shorouk', 'Egypt'),
('Dar El Maaref', 'Egypt'),
('Penguin Books', 'England');

INSERT INTO CATEGORY (name) VALUES 
('Fiction'),
('Science Fiction'),
('Mystery');

INSERT INTO BOOK (title, price, publish_year, author_id, publisher_id, category_id) VALUES 
('Palace Walk', 18.50, 1956, 1, 1, 1),
('The Mirror Experiment', 12.00, 2010, 2, 1, 2),
('Utopia', 25.00, 2008, 2, 2, 2),
('Hamlet', 30.00, 1603, 3, 3, 1),
('Romeo and Juliet', 22.00, 1597, 3, 3, 1),
('And Then There Were None', 16.00, 1939, 4, 3, 3),
('The Murder of Roger Ackroyd', 14.00, 1926, 4, 3, 3),
('Extra Book 1', 10.00, 2020, 1, 2, 1),
('Extra Book 2', 11.00, 2021, 1, 1, 1),
('Never Borrowed Book', 19.99, 2022, 3, 3, 1);

INSERT INTO MEMBER (name, email, join_date) VALUES 
('Mohamed Ali', 'mohamed@gmail.com', '2026-01-10'),
('Hossam Ahmed', 'hossam@gmail.com', '2026-02-15'),
('Waleed Ibrahim', 'waleed@gmail.com', '2026-03-01'),
('Sarah Mahmoud', 'sarah@gmail.com', '2026-03-10'),
('No Loans Member', 'noloans@gmail.com', '2026-04-01');

INSERT INTO LOAN (book_id, member_id, loan_date, return_date) VALUES 
(1, 1, '2026-03-01', '2026-03-10'),
(2, 1, '2026-03-12', '2026-03-20'),
(3, 2, '2026-03-05', '2026-03-15'),
(4, 2, '2026-03-18', '2026-03-25'),
(5, 3, '2026-03-02', '2026-03-10'),
(6, 3, '2026-03-11', '2026-03-19'),
(7, 4, '2026-03-04', '2026-03-14'),
(8, 4, '2026-03-15', '2026-03-22'),
(1, 2, '2026-03-22', '2026-03-30'),
(2, 3, '2026-03-25', '2026-04-02'),
(3, 4, '2026-04-01', '2026-04-10'),
(4, 1, '2026-04-05', NULL);