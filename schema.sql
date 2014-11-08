create table users(id INTEGER PRIMARY KEY,
                   email VARCHAR(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci UNIQUE,
                   first_name VARCHAR(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci,
                   last_name VARCHAR(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci
                  );
create table books(id INTEGER PRIMARY KEY,
                   book_author VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci,
                   book_name VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci UNIQUE,
                   img TEXT, description TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci,
                   url VARCHAR(300) CHARACTER SET utf8 COLLATE utf8_unicode_ci,
                   comment_count INTEGER DEFAULT 0);

create table common(id INTEGER PRIMARY KEY,
                    `key` VARCHAR(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci UNIQUE,
                    value VARCHAR(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci);

create table progress(id INTEGER PRIMARY KEY,
                      timestamp DATETIME,
                      book_id INTEGER, user_id INTEGER,
                      progress INTEGER,
                      FOREIGN KEY (book_id) REFERENCES books(id),
                      FOREIGN KEY (user_id) REFERENCES users(id));

create table comments(id INTEGER PRIMARY KEY,
                      timestamp DATETIME,
                      book_id INTEGER,
                      user_id INTEGER,
                      comment TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci,
                      FOREIGN KEY (book_id) REFERENCES books(id),
                      FOREIGN KEY (user_id) REFERENCES users(id));