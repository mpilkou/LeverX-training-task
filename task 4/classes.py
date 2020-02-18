import typing

class Student:
    
    def __init__(self, **kwargs):
        self._id = kwargs['id']
        self._name = kwargs['name']
        self._room = kwargs['room']
        self._birthday = kwargs['birthday']
        self._sex = kwargs['sex']

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def room(self):
        return self._room

    @property
    def birthday(self):
        return self._birthday

    @property
    def sex(self):
        return self._sex


    def to_json(self) -> dict:
        return {'id': self._id, 'name':self._name}

    def to_xml(self) -> str:
        return '\t\t<student id=\"{s_id}\"> {s_name} </student>\n'.format(s_id = self.id ,s_name = self.name)

class Room:
    
    def __init__(self, **kwargs):
        self._id = kwargs['id']
        self._name = kwargs['name']
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

    def addStudent(self, student) -> None:
        self._students.append(student)

    def to_json(self) -> dict:
        return {'id': self._id, 'name':self._name, 'students': [s.to_json() for s in self._students]}

    def to_xml(self) -> typing.Iterable[str]:
        yield '<room id=\"{r_id}\"> \n<name>{r_name}</name> \n\t<students>\n'.format(r_id = self.id, r_name = self.name)
        for s in self.students:
            yield s.to_xml()
        yield '\t</students> \n</room>\n'
