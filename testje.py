import jsonpickle

class C:
    def __init__(self):
        self.name = 'hans'
        self.age = 31
        self.keys = [{"id": 1 , "value" : 9, "desc": "db2"}, {"id": 2 , "value" : 0, "desc": "Flask"}, {"id": 3 , "value" : 9, "desc": "Boe"}]

c  = C()

pickled = jsonpickle.encode(c)
print(pickled)

b = jsonpickle.decode(pickled)
print(b.keys)