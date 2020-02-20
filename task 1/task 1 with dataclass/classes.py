import typing
from dataclasses import dataclass

@dataclass
class Student:
    id: int
    name: str
    room: str

    def to_json(self) -> dict:
        return {'id': self.id, 'name':self.name}
    
    def to_xml(self) -> str:
        return '\t\t<student id=\"{s_id}\"> {s_name} </student>\n'.format(s_id = self.id ,s_name = self.name)

@dataclass
class Room:
    
    id : int
    name : str
    students = []

    def addStudent(self, student) -> None:
        self.students.append(student)

    def to_json(self) -> dict:
        print('exp')
        print(self.id)
        return {'id': self.id, 'name':self.name, 'students': [s.to_json() for s in self.students]}

    def to_xml(self) -> typing.Iterable[str]:
        print('xml')
        print(self.id)
        yield '<room id=\"{r_id}\"> \n<name>{r_name}</name> \n\t<students>\n'.format(r_id = self.id, r_name = self.name)
        for s in self.students:
            yield s.to_xml()
        yield '\t</students> \n</room>\n'
