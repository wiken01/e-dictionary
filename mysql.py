#mysql.py
# create history
create table hist(
id int auto_increment primary key,
name varchar(32) not null,
word varchar(32) not null,
time varchar(64));

# create words
create table words(
id int auto_increment primary key,
word varchar(32) not null,
interpret text not null);