#!/usr/bin/python3.6

import json
import typing

from classes import Student, Room

class Controller:

    def __init__(self, students_path : str, rooms_path : str):
        
        # chech files existens
        if self.check_file_not_exists(students_path) and self.check_file_not_exists(rooms_path):
            exit()

        self.students_path = students_path
        self.rooms_path = rooms_path
        self.rooms = {}
        self.export = None

    # add students to rooms
    def concatinate_students_to_rooms_from_json(self) -> None:
        
        # add rooms
        for room in self.import_rooms_from_json():
            self.rooms[room.id] = room
        
        # add students to rooms
        for student in self.import_students_from_json():
            self.rooms[student.room].addStudent(student)

        self.export = ExporterToFile(self.rooms)
    
    def import_rooms_from_json(self) -> typing.Iterable[Room]:
        with open(self.rooms_path, 'r') as rooms_file: 
            for room in json.load(rooms_file):
                yield Room(**room)

    def import_students_from_json(self) -> typing.Iterable[Student]:
        with open(self.students_path, 'r') as students_file:
            for student in json.load(students_file):
                yield Student(**student)

    # check files existense
    def check_file_not_exists(self, path : str) -> bool:
        try:
            open(path, "r")
            return False
        except FileNotFoundError:
            print("File " + path + " not exist")
            return True


    def export_xml(self, output_path : str) -> None:
        self.export.export_xml(output_path)

    def export_json(self, output_path : str) -> None:
        self.export.export_json(output_path)
    

class ExporterToFile:

    def __init__(self, data : dict):
        self.data = data

    def export_json(self, output_path : str) -> None:
        with open(output_path, 'w') as outfile:
            json.dump(self.data, outfile, indent=2, default=self.my_jsonEncoder)
    
    def export_xml(self, output_path : str) -> None:
        with open(output_path, 'w') as outfile:
            for r in self.data.values():
                # generator of students in rooms write
                for i in r.to_xml():
                    outfile.write(i)

    @staticmethod
    def my_jsonEncoder(obj: object):
        return obj.to_json()

if __name__ == "__main__":

    # check input
    import argparse

    parser = argparse.ArgumentParser(description='give 3 arguments - path to students.json, path to rooms.json, output_path path (<name>.json,xml)')

    parser.add_argument('students', metavar='[path to students.json]', type=str, help='path to students.json file')
    parser.add_argument('rooms', metavar='[path to rooms.json]', type=str, help='path to rooms.json file')
    parser.add_argument('output_file', metavar='[output file (xml or json)]', type=str, help='output file ( xml or json) file')

    args = parser.parse_args()



    # init controller
    file_controll = Controller(students_path = args.students, rooms_path = args.rooms)

    # students to rooms & file export
    file_controll.concatinate_students_to_rooms_from_json()

    if args.output_file[3][-3:] == 'xml':
        file_controll.export_xml(output_path = args.output_file)
    else:
        file_controll.export_json(output_path = args.output_file)
        