create table users(id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
                   email VARCHAR(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci,
                   first_name VARCHAR(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
                   last_name VARCHAR(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL
                  );

create table books(id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
                   book_author VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
                   book_name VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci UNIQUE NOT NULL,
                   img TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
                   description TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
                   url VARCHAR(300) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
                   comment_count INTEGER DEFAULT 0);

create table common(id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
                    `key` VARCHAR(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci UNIQUE NOT NULL,
                    value VARCHAR(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL);

create table progress(id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
                      timestamp DATETIME NOT NULL,
                      book_id INTEGER NOT NULL,
                      user_id INTEGER NOT NULL,
                      progress INTEGER NOT NULL,
                      FOREIGN KEY (book_id) REFERENCES books(id)
                      ON DELETE CASCADE
                      ON UPDATE CASCADE,
                      FOREIGN KEY (user_id) REFERENCES users(id)
                      ON DELETE CASCADE
                      ON UPDATE CASCADE);

create table comments(id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
                      timestamp DATETIME NOT NULL,
                      book_id INTEGER NOT NULL,
                      user_id INTEGER NOT NULL,
                      comment TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
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
            users.first_name, users.last_name, comments.comment FROM comments INNER JOIN users ON comments.user_id=users.id;

create table blog(id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
                  timestamp DATETIME NOT NULL,
                  last_update DATETIME NOT NULL,
                  user_id INTEGER NOT NULL,
                  topic TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL, 
                  content TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
                  tags TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
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
            blog.topic, blog.content, blog.tags FROM blog INNER JOIN users ON blog.user_id=users.id;

create table tags(id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
                  blog_id INTEGER NOT NULL,
                  tag VARCHAR(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
                  FOREIGN KEY (blog_id) REFERENCES blog(id)
                  ON DELETE CASCADE
                  ON UPDATE CASCADE);