#!/usr/bin/python3

import json
import typing
from classes import Student, Room
from controllers import FilesController, DBController
from models import Model


if __name__ == "__main__":
    # check input
    import argparse

    parser = argparse.ArgumentParser(description='give 3 arguments - path to students.json, path to rooms.json, output_path path (<name>.json,xml)')

    parser.add_argument('students', metavar='[path to students.json]', type=str, help='path to students.json file')
    parser.add_argument('rooms', metavar='[path to rooms.json]', type=str, help='path to rooms.json file')
    parser.add_argument('output_file', metavar='[output file (xml or json)]', type=str, help='output file ( xml or json) file')

    args = parser.parse_args()



    # init controller
    file_controll = FilesController(students_path = args.students, rooms_path = args.rooms)

    # students to rooms & file export
    file_controll.concatinate_students_to_rooms_from_json()

    if args.output_file[3][-3:] == 'xml':
        file_controll.export_xml(output_path = args.output_file[3][-3:])
    else:
        file_controll.export_json(output_path = args.output_file[3][-3:])


    db_controll = DBController(students_path = args.students, rooms_path = args.rooms)
    # db import
    db_controll.import_to_db()

    # selects
    db_controll.show_all_selects()