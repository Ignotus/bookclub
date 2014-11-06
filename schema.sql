create table users(id INTEGER PRIMARY KEY, email TEXT UNIQUE, first_name TEXT, last_name TEXT);
create table books(id INTEGER PRIMARY KEY, book_name TEXT UNIQUE, book_author TEXT, img TEXT, description TEXT);
create table progress(id INTEGER PRIMARY KEY, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, book_id INTEGER, name TEXT, progress INTEGER);
