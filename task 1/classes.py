import json

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

    def export_json(self):
        with open('formated.json', 'w') as outfile:
            json.dump([ r.to_json() for r in self.rooms.values() ], outfile, indent=2)
    
    
    def export_xml(self):
        with open('formated.xml', 'w') as outfile:
            for r in self.rooms.values():
                outfile.write('<room id=\"{r_id}\"> \n<name>{r_name}</name> \n<students>\n'.format(r_id = r.id, r_name = r.name))
                
                for s in r.students:
                    outfile.write('\t<student id=\"{s_id}\"> {s_name} </student>\n'.format(s_id = s.id ,s_name = s.name))
                
                outfile.write('</students> </room>\n')

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