from pymongo import MongoClient
import certifi
from config import Config

# Se inicializa la conexión a MongoDB una sola vez
client = MongoClient(
    Config.MONGO_URI,
    tlsCAFile=certifi.where()
)

db = client['proyecto_cv']

usuarios_collection = db['usuarios']
documentos_collection = db['documentos']