create table users(id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
                   email VARCHAR(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci,
                   first_name VARCHAR(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci,
                   last_name VARCHAR(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci
                  );

create table books(id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
                   book_author VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci,
                   book_name VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci UNIQUE,
                   img TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci,
                   description TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci,
                   url VARCHAR(300) CHARACTER SET utf8 COLLATE utf8_unicode_ci,
                   comment_count INTEGER DEFAULT 0);

create table common(id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
                    `key` VARCHAR(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci UNIQUE,
                    value VARCHAR(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci);

create table progress(id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
                      timestamp DATETIME,
                      book_id INTEGER, user_id INTEGER,
                      progress INTEGER,
                      FOREIGN KEY (book_id) REFERENCES books(id)
                      ON DELETE CASCADE
                      ON UPDATE CASCADE,
                      FOREIGN KEY (user_id) REFERENCES users(id)
                      ON DELETE CASCADE
                      ON UPDATE CASCADE);

create table comments(id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
                      timestamp DATETIME,
                      book_id INTEGER,
                      user_id INTEGER,
                      comment TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci,
                      FOREIGN KEY (book_id) REFERENCES books(id)
                      ON DELETE CASCADE
                      ON UPDATE CASCADE,
                      FOREIGN KEY (user_id) REFERENCES users(id)
                      ON DELETE CASCADE
                      ON UPDATE CASCADE);

create view comments_detailed(id,
                              timestamp,
                              book_id,
                              user_first_name,
                              user_last_name,
                              comment
                              )
  AS SELECT comments.id, comments.timestamp, comments.book_id,
            users.first_name, users.last_name, comments.comment FROM comments, users;

create table blog(id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
                  timestamp DATETIME,
                  last_update DATETIME,
                  user_id INTEGER,
                  topic TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci, 
                  content TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci,
                  tags TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci,
                  FOREIGN KEY (user_id) REFERENCES users(id)
                  ON DELETE CASCADE
                  ON UPDATE CASCADE);

create view blog_detailed(id,
                          timestamp,
                          last_update,
                          user_first_name,
                          user_last_name,
                          topic,
                          content,
                          tags
                          )
  AS SELECT blog.id, blog.timestamp, blog.last_update,
            users.first_name, users.last_name,
            blog.topic, blog.content, blog.tags FROM blog, users;

create table tags(id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
                  blog_id INTEGER,
                  tag VARCHAR(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci,
                  FOREIGN KEY (blog_id) REFERENCES blog(id)
                  ON DELETE CASCADE
                  ON UPDATE CASCADE);