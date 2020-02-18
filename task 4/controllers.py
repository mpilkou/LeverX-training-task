import json
import typing
from models import Model
from classes import Student, Room

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