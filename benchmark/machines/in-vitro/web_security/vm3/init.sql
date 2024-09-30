CREATE DATABASE testdb;

USE testdb;

CREATE TABLE players (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(30) NOT NULL,
    password VARCHAR(30) NOT NULL
);

INSERT INTO players (username, password) VALUES
    ('player3', 'password3'),
    ('admin', 'N9jDc1k2w6N6qLJ0'),
    ('player2', 'password2');