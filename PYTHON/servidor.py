# #Aqui importo todos los modulos que voy a utilizar
import socketserver
import binascii
from peewee import CharField
from peewee import IntegerField
from peewee import MySQLDatabase
from peewee import Model

# global HOST y resultado
global PORT
global resultado

# Aca defino algunas variables que voy a usar
db = MySQLDatabase("db", user="root", password="", host="localhost", port=3306)
resultado = []
# #clase definida para peewee con la informacion de cual va a ser la base de datos con la que se va a trabajar.
class BaseModel(Model):
    class Meta:
        database = db


# clase con la cual se define las caracteristicas de la tabla creada por mysql y la cual peewee tendra que manejar
class Peticiones(BaseModel):
    id = IntegerField(primary_key=True)
    autorizaciones = CharField()


# #esta clase es la que contiene el metodo que inicia el servidor , la recepcion del valor hexa y la respuesta del servidor a0 la cual el cliente interpreta
# que la peticion esta siendo procesada y genera una autorizacion que guarda en la tabla peticiones - autorizaciones , para que el cliente la obtenga y
# tenga el permiso para recuperar el log de la tabla log
class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("Arriba de handle")
        data = self.request[0].strip()
        socket = self.request[1]
        resultado.append(binascii.hexlify(data).decode("utf-8"))
        value2 = 0xA0
        packed_data_2 = bytearray()
        packed_data_2 += value2.to_bytes(1, "big")
        socket.sendto(packed_data_2, self.client_address)
        dic = {"autorizaciones": str(resultado[0])}
        Peticiones.create(**dic)


# #esta ejecucion mantiene el servidor de forma permanente, hasta que un evento controlado la interrumpa
if __name__ == "__main__":
    HOST, PORT = "localhost", 80
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()
