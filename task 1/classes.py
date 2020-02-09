import json
from json import JSONEncoder

class Controller:

    def __init__(self, students_path, rooms_path):
        print("{} = {}".format(students_path, rooms_path))
        
        if self.check_file_not_exists(students_path) and self.check_file_not_exists(rooms_path):
            exit()
        
        self.students_path = students_path
        self.rooms_path = rooms_path
        self.rooms = {}

    def add_rooms_from_json(self):
        with open(self.rooms_path, 'r') as myfile: 
            for room in json.load(myfile):
                self.rooms[room['id']] = Room(room['id'],room['name'])
        
        with open(self.students_path, 'r') as myfile:
            for student in json.load(myfile):
                self.rooms[student['room']].addStudent(Student(student['id'],student['name'],student['room']))

    def import_json(self):
        with open('formated.json', 'w') as outfile:
            json.dump([ r.to_json() for r in self.rooms.values() ], outfile, indent=2)
    

    def print_json_file(self, path):
        with open(path, "r") as file: 
            data = json.load(file)
            print(data)

    def check_file_not_exists(self, path):
        try:
            open(path, "r")
            return False
        except FileNotFoundError:
            print("File " + path + " not exist")
            return True

class Student:
    
    def __init__(self, id, name, room):
        self._id = id
        self._name = name
        self._room = room

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def room(self):
        return self._room

    def to_json(self):
        return {'id': self._id, 'name':self._name}


class Room:
    
    def __init__(self, id, name):
        self._id = id
        self._name = name
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