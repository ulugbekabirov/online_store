from enum import Enum
import os 
import json
from dotenv import load_dotenv
load_dotenv()

token_name = os.getenv("TOKEN_NAME")

admin_list = json.loads(os.getenv("ADMIN_LIST"))

port_number = os.getenv("REDIS_PORTNUMBER")
host_name = os.getenv("REDIS_HOSTNAME")
db_number = os.getenv("REDIS_DBNUMBER")

class States(Enum):
	State_One = "1"
	State_Two = "2"
	State_Three = "3"
	State_Four = "4"
	State_Five = "5"
	State_Six = "6"