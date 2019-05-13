from app import db_handler
from jsonpickle import encode
import app.ctdcore.loading_RESM

class JobSite:
    def __init__

class Resource:
    def __init__(self, resource_id):
        self.id = resource_id
        self.keys = self.retrieve_keys(resource_id)
        self.abbrev = ""

    def serialize(self):
        return encode(self)

    def retrieve_keys(self, resource_id):
        return db_handler.get_resource_keys(resource_id)

    def update_keys(self, mod_keys):
        db_handler.update_resource_keys(mod_keys)
        self.keys = mod_keys
    
    def map(self, vacancy_id):
        return


class Vacancy:
    def __init__(self, vacancy_id):
        self.id = vacancy_id


class Mapping:
    def __inti__(self, mapping_id, resource_id, vacancy_id):
        self.id = mapping_id
        self.vacancy = Vacancy(vananct_id)
        self.resource = Resoucre(resource_id) 
