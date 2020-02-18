import typing
import mysql.connector
from classes import Student, Room

class Model:
    def __init__(self, **kwargs):
        self.connection = mysql.connector.connect(
                                user =      kwargs.get('user') or 'root', 
                                password=   kwargs.get('root') or 'root',
                                host =      kwargs.get('host') or '127.0.0.1',
                                database =  kwargs.get('database') or 'leverx_task4_db',
                                auth_plugin=kwargs.get('auth_plugin') or 'mysql_native_password')

    def insert_rooms(self, rooms: typing.Iterable[Room]) -> None:
        my_cursor = self.connection.cursor()
        sql = "INSERT INTO Rooms (id, name) VALUES (%s, %s)"
        val = [
            (room.id, room.name) for room in rooms
            ]
        my_cursor.executemany(sql, val)
        self.connection.commit()

    def insert_students(self, students: typing.Iterable[Student]) -> None:
        my_cursor = self.connection.cursor()
        sql = "INSERT INTO Students (id, name, sex, birthday, room_id) VALUES (%s, %s, %s, %s, %s)"
        val = [
            (s.id, s.name, s.sex, s.birthday, s.room) for s in students
            ]
        my_cursor.executemany(sql, val)
        self.connection.commit()


    def select_rooms_with_count_students(self) -> typing.Iterable[typing.Tuple[str,int]]:
        my_cursor = self.connection.cursor()
        sql = "SELECT R.name, count(S.id) as students_in_room \
                FROM Students as S \
                    INNER JOIN Rooms as R \
                        ON S.room_id = R.id \
                GROUP BY R.id"
        
        my_cursor.execute(sql)
        return my_cursor.fetchall()
    
    def select_rooms_with_smalles_date_arg(self) -> typing.Iterable[(str)]:
        my_cursor = self.connection.cursor()
        sql = "SELECT R.name \
            FROM Students as S \
                INNER JOIN Rooms as R ON S.room_id = R.id \
            GROUP BY R.id \
            ORDER BY avg(S.birthday) ASC \
            LIMIT 5"
        
        my_cursor.execute(sql)
        return my_cursor.fetchall()

    def select_rooms_with_largest_date_differense(self) -> typing.Iterable[str]:
        my_cursor = self.connection.cursor()
        sql = "SELECT R.name \
            FROM Students as S \
                INNER JOIN Rooms as R ON S.room_id = R.id \
            GROUP BY R.id \
            ORDER BY (MAX(S.birthday)-MIN(S.birthday)) ASC \
            LIMIT 5"
        
        my_cursor.execute(sql)
        return my_cursor.fetchall()

    def select_rooms_there_living_with_different_sex(self) -> typing.Iterable[str]:
        my_cursor = self.connection.cursor()
        sql = "SELECT R.name \
            FROM Rooms as R \
            WHERE (\
                    SELECT count(*) \
                    FROM Students as S1 \
                    WHERE S1.sex = 'M' and S1.room_id = R.id \
                    Group BY S1.room_id) \
                         < \
                    (SELECT count(*) \
                    FROM Students as S2 \
                    WHERE S2.room_id = R.id \
                    Group BY S2.room_id)"
        
        my_cursor.execute(sql)
        return my_cursor.fetchall()
    

    def __del__(self):
        self.connection.close()