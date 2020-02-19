CREATE DATABASE IF NOT EXISTS leverx_task4_db COLLATE utf8_general_ci;

CREATE TABLE IF NOT EXISTS leverx_task4_db.Rooms (
    id int UNSIGNED NOT NULL PRIMARY KEY,
    name varchar(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS leverx_task4_db.Students (
    id int UNSIGNED NOT NULL PRIMARY KEY,
    name varchar(50) NOT NULL,
    sex varchar(1) NOT NULL,
    birthday date NOT NULL,
    room_id int UNSIGNED,
    FOREIGN KEY (room_id) REFERENCES Rooms(id)
        ON DELETE SET NULL
);