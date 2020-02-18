#!/usr/bin/python3

import json
import typing
import mysql.connector
from classes import Student, Room
from controllers import FilesController, DBController
from models import Model


if __name__ == "__main__":
    # check input
    import sys

    if len(sys.argv) < 3:
        print('give 3 arguments - path to students.json, path to rooms.json, output_path path (<name>.json,xml)')
        exit()

    # init controller
    file_controll = FilesController(students_path = sys.argv[1], rooms_path = sys.argv[2])

    # students to rooms & file export
    file_controll.concatinate_students_to_rooms_from_json()

    if sys.argv[3][-3:] == 'xml':
        file_controll.export_xml(output_path = sys.argv[3])
    else:
        file_controll.export_json(output_path = sys.argv[3])


    db_controll = DBController(students_path = sys.argv[1], rooms_path = sys.argv[2])
    # db import
    db_controll.import_to_db()

    # selects
    db_controll.show_all_selects()