#!/usr/bin/python3

import json
import typing
import mysql.connector
from classes import Student, Room

class Model:
    def __init__(self, **kwargs):
        self.connection = mysql.connector.connect(
                                user =      kwargs.get('user') or 'root', 
                                password=   kwargs.get('root') or 'root',
                                host =      kwargs.get('host') or '127.0.0.1',
                                database =  kwargs.get('database') or 'leverx_task4_db',
                                auth_plugin=kwargs.get('auth_plugin') or 'mysql_native_password')
    
    def insert_student(self, student : Student) -> None:
        my_cursor = self.connection.cursor()
        sql = "INSERT INTO Students (id, name, sex, birthday, room_id) VALUES (%s, %s, %s, %s, %s)"
        val = (student.id, student.name, student.sex, student.birthday, student.room)
        my_cursor.execute(sql, val)
        self.connection.commit()

    def insert_room(self, room : Room) -> None:
        my_cursor = self.connection.cursor()
        sql = "INSERT INTO Rooms (id, name) VALUES (%s, %s)"
        val = (room.id, room.name)
        my_cursor.execute(sql, val)
        self.connection.commit()
    
    def insert_students_from_room(self, room: Room) -> None:
        my_cursor = self.connection.cursor()
        sql = "INSERT INTO Students (id, name, sex, birthday, room_id) VALUES (%s, %s, %s, %s, %s)"
        val = [
            (s.id, s.name, s.sex, s.birthday, s.room) for s in room.students
            ]
        my_cursor.executemany(sql, val)
        self.connection.commit()

    def insert_rooms(self, rooms: typing.Iterable[Room]) -> None:
        my_cursor = self.connection.cursor()
        sql = "INSERT INTO Rooms (id, name) VALUES (%s, %s)"
        val = [
            (room.id, room.name) for room in rooms
            ]
        my_cursor.executemany(sql, val)
        self.connection.commit()

    def insert_students(self, students: typing.Iterable[Student]) -> None:
        my_cursor = self.connection.cursor()
        sql = "INSERT INTO Students (id, name, sex, birthday, room_id) VALUES (%s, %s, %s, %s, %s)"
        val = [
            (s.id, s.name, s.sex, s.birthday, s.room) for s in students
            ]
        my_cursor.executemany(sql, val)
        self.connection.commit()

    

    def __del__(self):
        self.connection.close()

class Controller:

    def __init__(self, students_path, rooms_path):
        
        # chech files existens
        if self.check_file_not_exists(students_path) and self.check_file_not_exists(rooms_path):
            exit()

        self._model = Model()
        self.students_path = students_path
        self.rooms_path = rooms_path
        self.rooms = {}

    # add students to rooms
    def concatinate_students_to_rooms_from_json(self) -> None:
        
        # add rooms
        for room in self.import_rooms_from_json():
            self.rooms[room.id] = room
        
        # add students to rooms
        for student in self.import_students_from_json():
            self.rooms[student.room].addStudent(student)
    
    def import_rooms_from_json(self) -> None:
        with open(self.rooms_path, 'r') as rooms_file: 
            for room in json.load(rooms_file):
                yield Room(**room)

    def import_students_from_json(self) -> None:
        with open(self.students_path, 'r') as students_file:
            for student in json.load(students_file):
                yield Student(**student)

    def export_json(self, output_path : str) -> None:
        
        if not output_path:
            output_path = 'solution.json'

        with open(output_path, 'w') as outfile:
            json.dump(list(self.rooms.values()), outfile, indent=2, default=self.my_jsonEncoder)
    
    def export_xml(self, output_path : str) -> None:

        if not output_path:
            output_path = 'solution.xml'

        with open(output_path, 'w') as outfile:
            for r in self.rooms.values():
                # generator of students in rooms write
                for i in r.to_xml():
                    outfile.write(i)

    def import_to_db(self) -> None:
        self._model.insert_rooms(self.import_rooms_from_json())
        self._model.insert_students(self.import_students_from_json())

    @staticmethod
    def my_jsonEncoder(obj: object):
        return obj.to_json()

    # check files existense
    def check_file_not_exists(self, path : str) -> bool:
        try:
            open(path, "r")
            return False
        except FileNotFoundError:
            print("File " + path + " not exist")
            return True


if __name__ == "__main__":
    # check input
    import sys

    if len(sys.argv) < 3:
        print('give 3 arguments - path to students.json, path to rooms.json, output_path path (<name>.json,xml)')
        exit()

    # init controller
    controll = Controller(students_path = sys.argv[1], rooms_path = sys.argv[2])

    # students to rooms & file export
    controll.concatinate_students_to_rooms_from_json()

    if sys.argv[3][-3:] == 'xml':
        controll.export_xml(output_path = sys.argv[3])
    else:
        controll.export_json(output_path = sys.argv[3])


    # db import
    #controll.import_to_db()

    
        