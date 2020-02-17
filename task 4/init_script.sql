CREATE DATABASE leverx_task4_db COLLATE utf8_general_ci;
CREATE TABLE Rooms (
    id int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name varchar(50) NOT NULL
);
CREATE TABLE Students (
    id int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name varchar(50) NOT NULL,
    sex varchar(1) NOT NULL,
    birthday date NOT NULL,
    room_id int UNSIGNED NOT NULL,
    FOREIGN KEY (room_id) REFERENCES Rooms(id)
);