create table users(id serial not null primary key,
                   email varchar(50) unique,
                   first_name varchar(50) not null,
                   last_name varchar(50) not null
                  );

create table books(id serial not null primary key,
                   book_author varchar(100) not null,
                   book_name varchar(100) not null,
                   img text not null,
                   description text not null,
                   url varchar(300) not null,
                   comment_count integer default 0
                  );

create table common(id serial not null primary key,
                    "key" varchar(50) not null unique,
                    value varchar(50) not null
                   );

create table progress(id serial not null primary key,
                      timestamp timestamp not null,
                      book_id integer not null references books on delete cascade on update cascade,
                      user_id integer not null references users on delete cascade on update cascade,
                      progress integer not null
                     );

create table comments(id serial not null primary key,
                      timestamp timestamp not null,
                      book_id integer not null references books on delete cascade on update cascade,
                      user_id integer not null references users on delete cascade on update cascade,
                      comment text not null
                     );

create view comments_detailed(id,
                              timestamp,
                              book_id,
                              user_first_name,
                              user_last_name,
                              comment
                              )
  as select comments.id, comments.timestamp, comments.book_id,
            users.first_name, users.last_name, comments.comment from comments inner join users on comments.user_id=users.id;

create table blog(id serial not null primary key,
                  timestamp timestamp not null,
                  last_update timestamp not null,
                  user_id integer not null references users on delete cascade on update cascade,
                  topic text not null,
                  content text not null,
                  tags text not null
                 );

create view blog_detailed(id,
                          timestamp,
                          last_update,
                          user_first_name,
                          user_last_name,
                          topic,
                          content,
                          tags
                          )
  as select blog.id, blog.timestamp, blog.last_update,
            users.first_name, users.last_name,
            blog.topic, blog.content, blog.tags from blog inner join users on blog.user_id=users.id;

create table tags(id serial not null primary key,
                  blog_id integer not null references blog on delete cascade on update cascade,
                  tag varchar(50) not null
                 );
