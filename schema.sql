create table users(id INTEGER PRIMARY KEY, email TEXT UNIQUE, first_name TEXT, last_name TEXT);
create table books(id INTEGER PRIMARY KEY, book_author TEXT, book_name TEXT UNIQUE, img TEXT, description TEXT, url TEXT);
create table common(id INTEGER PRIMARY KEY, key TEXT UNIQUE, value TEXT);
create table progress(id INTEGER PRIMARY KEY, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, book_id INTEGER, user_id INTEGER, progress INTEGER);
create table comments(id INTEGER PRIMARY KEY, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, book_id INTEGER, user_id INTEGER, comment TEXT);