import json

class Controller:

    def __init__(self, students, rooms):
        print("{} = {}".format(students, rooms))
        if self.check_file_not_exists(students) and self.check_file_not_exists(rooms):
            exit()


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