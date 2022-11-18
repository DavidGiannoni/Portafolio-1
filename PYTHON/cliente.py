# #Aca importo los modulos que voy a utilizar
import socket
import sys
import binascii

# #el siguiente script ejecuta la funcion del cliente , enviar una peticion al servidor el cual respondera con un valor para confirmar la recepcion
# de la peticion y posteriormente envia un diccionario con los registros de log
HOST, PORT = "localhost", 80
data = " ".join(sys.argv[1:])
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mi_valor = 0x00003EF5
print(type(mi_valor))
packed_data = bytearray()
packed_data += mi_valor.to_bytes(4, "big")
mensaje = packed_data
sock.sendto(mensaje, (HOST, PORT))
print("ESTADO DEL CLIENTE: PETICION ENVIADA." "\n")
received = sock.recvfrom(1024)
# ===== ENVIO Y RECEPCIÓN DE DATOS =================
print(
    "ESTADO DEL CLIENTE - DATOS ENVIADOS:",
    binascii.hexlify(mensaje).decode("utf-8"),
    "\n",
)
print(
    "ESTADO DEL CLIENTE - DATOS RECIBIDOS DEL SERVIDOR:",
    binascii.hexlify(received[0]).decode("utf-8"),
    "\n",
)
print("LISTA DE LOG RECIBIDA:" "\n")
