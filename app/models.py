from app import db_handler
from jsonpickle import encode

class Resource:
    def __init__(self, resource_id):
        self.id = resource_id
        self.keys = self.retrieve_keys(resource_id)

    def serialize(self):
        return encode(self)

    def retrieve_keys(self, resource_id):
        return db_handler.get_resource_keys(resource_id)

    def update_keys(self, mod_keys):
        db_handler.update_resource_keys(mod_keys)
        self.keys = mod_keys


class Vacancy:
    def __init__(self, vacancy_id):
        self.id = vacancy_id


