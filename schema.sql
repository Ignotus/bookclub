create table users(id INTEGER PRIMARY KEY, email VARCHAR(50) UNIQUE, first_name VARCHAR(50), last_name VARCHAR(50));
create table books(id INTEGER PRIMARY KEY, book_author VARCHAR(100), book_name VARCHAR(100) UNIQUE, img TEXT, description TEXT, url VARCHAR(300), comment_count INTEGER DEFAULT 0);
create table common(id INTEGER PRIMARY KEY, `key` VARCHAR(50) UNIQUE, value VARCHAR(50));
create table progress(id INTEGER PRIMARY KEY, timestamp DATETIME, book_id INTEGER, user_id INTEGER, progress INTEGER,
  FOREIGN KEY (book_id) REFERENCES books(id),
  FOREIGN KEY (user_id) REFERENCES users(id));
create table comments(id INTEGER PRIMARY KEY, timestamp DATETIME, book_id INTEGER, user_id INTEGER, comment TEXT,
  FOREIGN KEY (book_id) REFERENCES books(id),
  FOREIGN KEY (user_id) REFERENCES users(id));