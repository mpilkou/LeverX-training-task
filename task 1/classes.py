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



class Room:
    
    def __init__(self, id, name):
        self._id = id
        self._name = name
        self.students = []

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name