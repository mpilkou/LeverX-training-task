class Controller:
    import json

    def print_json_file(self, path):
        with open(path, "r") as file: 
            data = self.json.load(file)
            print(data)

    def check_file_existens(self, path):
        try:
            open(path, "r")
            return True
        except FileNotFoundError:
            print("File not exist")
            return False

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