#!/usr/bin/python3
if __name__ == "__main__":
    from classes import Controller

    

    controll = Controller(students_path = 'students.json', rooms_path = 'rooms.json')

    print(controll.add_rooms_from_json())

    controll.export_json()

    controll2 = Controller('students.jsona', 'students.jsona')



    print(controll)