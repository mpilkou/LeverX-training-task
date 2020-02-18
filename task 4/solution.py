#!/usr/bin/python3

import json
import mysql.connector

class Model:
    def __init__(self, **kwargs):
        self.connection = mysql.connector.connect(
                                user =      kwargs.get('user') or 'root', 
                                password=   kwargs.get('root') or 'root',
                                host =      kwargs.get('host') or '127.0.0.1',
                                database =  kwargs.get('database') or 'leverx_task4_db',
                                auth_plugin=kwargs.get('auth_plugin') or 'mysql_native_password')
        
    
    # TODO
    def insert_student(self, student):
        my_cursor = self.connection.cursor()
        sql = "INSERT INTO Students (id, name) VALUES (%s, %s)"
        
        val = (student.id, student.name)
        my_cursor.execute(sql, val)
        self.connection.commit()

    def insert_room(self, room):
        my_cursor = self.connection.cursor()
        sql = "INSERT INTO Rooms (id, name) VALUES (%s, %s)"
        val = (room.id, room.name)
        my_cursor.execute(sql, val)
        self.connection.commit()

    # TODO
    def insert_room_with_students(self, room):
        my_cursor = self.connection.cursor()
        sql = "INSERT INTO Rooms (id, name) VALUES (%s, %s)"
        val = (room.id, room.name)
        my_cursor.execute(sql, val)
        self.connection.commit()

    def __del__(self):
        self.connection.close()

class Controller:

    def __init__(self, students_path, rooms_path):
        
        # chech files existens
        if self.check_file_not_exists(students_path) and self.check_file_not_exists(rooms_path):
            exit()

        self.students_path = students_path
        self.rooms_path = rooms_path
        self.rooms = {}

    # add students to rooms
    def add_rooms_from_json(self):

        # add rooms
        with open(self.rooms_path, 'r') as myfile: 
            for room in json.load(myfile):
                self.rooms[room['id']] = Room(**room)
        
        # add students to rooms
        with open(self.students_path, 'r') as myfile:
            for student in json.load(myfile):
                self.rooms[student['room']].addStudent(Student(**student))

    def export_json(self, output_path = 'solution.json'):
        with open(output_path, 'w') as outfile:
            json.dump(list(self.rooms.values()), outfile, indent=2, default=self.my_jsonEncoder)
    
    def export_xml(self, output_path = 'solution.xml'):
        with open(output_path, 'w') as outfile:
            for r in self.rooms.values():
                # generator of students in rooms write
                for i in r.to_xml():
                    outfile.write(i)

    def export_to_db(self, ):
        pass

    @staticmethod
    def my_jsonEncoder(object):
        return object.to_json()

    # check files existense
    def check_file_not_exists(self, path):
        try:
            open(path, "r")
            return False
        except FileNotFoundError:
            print("File " + path + " not exist")
            return True

class Student:
    
    def __init__(self, **kwargs):
        self._id = kwargs['id']
        self._name = kwargs['name']
        self._room = kwargs['room']
        self._birthday = kwargs['birthday']
        self._sex = kwargs['sex']

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def room(self):
        return self._room

    @property
    def birthday(self):
        return self._birthday

    @property
    def sex(self):
        return self._sex


    def to_json(self):
        return {'id': self._id, 'name':self._name}

    def to_xml(self):
        return '\t\t<student id=\"{s_id}\"> {s_name} </student>\n'.format(s_id = self.id ,s_name = self.name)


class Room:
    
    def __init__(self, **kwargs):
        self._id = kwargs['id']
        self._name = kwargs['name']
        self._students = []

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def students(self):
        return self._students

    def addStudent(self, student):
        self._students.append(student)

    def to_json(self):
        return {'id': self._id, 'name':self._name, 'students': [s.to_json() for s in self._students]}

    def to_xml(self):
        yield '<room id=\"{r_id}\"> \n<name>{r_name}</name> \n\t<students>\n'.format(r_id = self.id, r_name = self.name)
        for s in self.students:
            yield s.to_xml()
        yield '\t</students> \n</room>\n'



if __name__ == "__main__":
    m = Model()
    #r = Room(1, 'Room #1')
    #m.insert_room(r)

    def ddd():
        import sys

        if len(sys.argv) < 3:
            print('give 3 arguments - path to students.json, path to rooms.json, output_path path (<name>.json,xml)')
            exit()

        controll = Controller(students_path = sys.argv[1], rooms_path = sys.argv[2])
        controll.add_rooms_from_json()

        if sys.argv[3][-3:] == 'xml':
            controll.export_xml(output_path = sys.argv[3])
        else:
            controll.export_json(output_path = sys.argv[3])
        