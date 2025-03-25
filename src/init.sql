CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL
)

CREATE table category (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(20) NOT NULL
)

CREATE TABLE timelog (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp time NOT NULL,
    date DATE NOT NULL,
    category_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES category(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
)

insert into users (username,password,email ) VALUES ('admin','admin','admin@admin.de')

insert into category (name) VALUES ('work')
insert into category (name) VALUES ('break')
insert into category (name) VALUES ('meeting')
insert into category (name) VALUES ('overtime')
insert into category (name) VALUES ('vacation')
insert into category (name) VALUES ('sick')