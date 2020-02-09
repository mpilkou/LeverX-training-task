#!/usr/bin/python3
if __name__ == "__main__":
    from classes import Controller

    controll = Controller(students = 'students.jsona', rooms = 'students.jsona')

    controll2 = Controller('students.jsona', 'students.jsona')

    print(controll)