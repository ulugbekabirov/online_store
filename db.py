import redis
import json


class RedisStates():
    def __init__(self, host, port, db):
        self.db = redis.Redis(host=host, port=port,
                              db=db, decode_responses=True)
        self.data = {
            'state': 1,
            'selects': {

                "density": "",  # средняя максимальная
                "material": "",  # жаккард синтетика
                "image_id": "",
                "size": "",  # односпальные двуспальные полуторные
                "dimentions": "",  # размеры
            }
        }

    def getState(self, user_id):
        if self.db.get(user_id) == None:
            self.db.set(user_id, json.dumps(self.data))
            return self.data['state']
        else:
            json_data = self.db.get(user_id)
            parced_data = json.loads(json_data)
            return parced_data['state']
 

    def setState(self, user_id, state):
        if self.db.get(user_id) == None:
            self.db.set(user_id, json.dumps(self.data))
        json_data = self.db.get(user_id)
        parced_data = json.loads(json_data)
        parced_data['state'] = state
        self.db.set(user_id, json.dumps(parced_data))


    def getDensity(self, user_id):
        json_data = self.db.get(user_id)
        parced_data = json.loads(json_data)
        return parced_data['selects']["density"]

                
    def setDensity(self, user_id, density):
        json_data = self.db.get(user_id)
        parced_data = json.loads(json_data)
        parced_data['selects']['density'] = density
        self.db.set(user_id, json.dumps(parced_data))


    def getMaterial(self, user_id):
        json_data = self.db.get(user_id)
        parced_data = json.loads(json_data)
        return parced_data['selects']["material"]

                
    def setMaterial(self, user_id, material):
        json_data = self.db.get(user_id)
        parced_data = json.loads(json_data)
        parced_data['selects']['material'] = material
        self.db.set(user_id, json.dumps(parced_data))


    def getSize(self, user_id):
        json_data = self.db.get(user_id)
        parced_data = json.loads(json_data)
        return parced_data['selects']["size"]

                
    def setSize(self, user_id, size):
        json_data = self.db.get(user_id)
        parced_data = json.loads(json_data)
        parced_data['selects']['size'] = size
        self.db.set(user_id, json.dumps(parced_data))


    def getDimentions(self, user_id):
        json_data = self.db.get(user_id)
        parced_data = json.loads(json_data)
        return parced_data['selects']["dimentions"]

                
    def setDimentions(self, user_id, dimentions):
        json_data = self.db.get(user_id)
        parced_data = json.loads(json_data)
        parced_data['selects']['dimentions'] = dimentions
        self.db.set(user_id, json.dumps(parced_data))


    def getImage(self, user_id):
        json_data = self.db.get(user_id)
        parced_data = json.loads(json_data)
        return parced_data['selects']["image_id"]


    def setImage(self,user_id,image_id):
        json_data = self.db.get(user_id)
        parced_data = json.loads(json_data)
        parced_data['selects']['image_id'] = image_id
        self.db.set(user_id, json.dumps(parced_data))
