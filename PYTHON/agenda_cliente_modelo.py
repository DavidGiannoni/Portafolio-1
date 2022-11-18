# #Aca importo todos los modulos que utilizo
from pathlib import Path
import subprocess
import sys
import os
import threading
from PyQt5.QtWidgets import QMessageBox
from peewee import CharField
from peewee import DateTimeField
from peewee import MySQLDatabase
from peewee import Model
from PyQt5 import QtWidgets
from peewee import IntegerField
import mysql.connector

# #defino algunas variables globales para el path
theproc = "servidor.py"
theproc2 = "cliente.py"
# Creo la base de datos con sus 3 tablas con el lenguaje de MySQL.
db = MySQLDatabase("db", user="root", password="", host="localhost", port=3306)
mibase_a = mysql.connector.connect(host="localhost", user="root", passwd="")
micursor_a = mibase_a.cursor()
micursor_a.execute("CREATE DATABASE IF NOT EXISTS db")
mibase_agenda = mysql.connector.connect(
    host="localhost", user="root", passwd="", database="db"
)
micursor_agenda = mibase_agenda.cursor()
micursor_agenda.execute(
    "CREATE TABLE IF NOT EXISTS `agenda` (`id` INT(10) NOT NULL AUTO_INCREMENT , `nombre` VARCHAR(128) CHARACTER SET utf8 COLLATE utf8_spanish2_ci NOT NULL , `telefono` INT(30) NOT NULL , `direccion` VARCHAR(128) CHARACTER SET utf8 COLLATE utf8_spanish2_ci NOT NULL , `email` VARCHAR(128) CHARACTER SET utf8 COLLATE utf8_spanish2_ci NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;"
)
mibase_log = mysql.connector.connect(
    host="localhost", user="root", passwd="", database="db"
)
micursor_log = mibase_log.cursor()
micursor_log.execute(
    "CREATE TABLE IF NOT EXISTS `log` (`nombre` VARCHAR(128) CHARACTER SET utf8 COLLATE utf8_spanish2_ci NOT NULL ,`direccion` VARCHAR(128) CHARACTER SET utf8 COLLATE utf8_spanish2_ci NOT NULL, `telefono` INT(10) NOT NULL , `email` VARCHAR(128) CHARACTER SET utf8 COLLATE utf8_spanish2_ci NOT NULL , `ejecucion` VARCHAR(128) CHARACTER SET utf8 COLLATE utf8_spanish2_ci NOT NULL ,`datetimes` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ) ENGINE = InnoDB;"
)
mibase_peticiones = mysql.connector.connect(
    host="localhost", user="root", passwd="", database="db"
)
micursor_peticiones = mibase_peticiones.cursor()
micursor_peticiones.execute(
    "CREATE TABLE IF NOT EXISTS `peticiones` ( `id` INT(10) NOT NULL AUTO_INCREMENT , `autorizaciones` VARCHAR(128) CHARACTER SET utf8 COLLATE utf8_spanish2_ci NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;"
)

# clase que utiliza el ORM para manejar la base de datos
class BaseModel(Model):
    class Meta:
        database = db


# Clase que utiliza el ORM  para manejar la tabla agenda
class Agenda(BaseModel):
    id = IntegerField()
    nombre = CharField()
    direccion = CharField()
    telefono = CharField()
    email = CharField()


# Clase que utiliza el ORM para manejar la tabla log.
class Log(BaseModel):
    nombre = CharField()
    direccion = CharField()
    telefono = CharField()
    email = CharField()
    datetimes = DateTimeField(primary_key=True)
    ejecucion = CharField()


# clase que utiliza el ORM para manejar la tabla Peticiones.
class Peticiones(BaseModel):
    id = IntegerField(primary_key=True)
    autorizaciones = CharField()


# Conexion del ORM , genera su configuracion.
db.connect()
db.create_tables([Agenda])
db.create_tables([Log])
db.close()


# #Esta clase contiene todos las funciones que engloban la accion determinada por el usuario mediantes los botones de la app Agenda_cliente
class ClienteMetodo:
    # #Incorporo las rutas al archivo del servidor.py y cliente.py , para vincularlos con los metodos
    def __init__(
        self,
    ):
        pass
        self.raiz = Path(__file__).resolve().parent
        self.ruta_server = os.path.join(self.raiz, "servidor.py")
        self.ruta_cliente = os.path.join(self.raiz, "cliente.py")

    # #Este metodo destruye el servidor y llama al metodo lanzar_servidor atravez de hilos
    def intenta_conectar(self):
        if theproc != "servidor.py":
            theproc.kill()
            threading.Thread(
                target=self.m.lanza_servidor, args=(True,), daemon=True
            ).start()
        else:
            threading.Thread(
                target=self.m.lanza_servidor, args=(True,), daemon=True
            ).start()

    # #Este metodo lanza el servidor.
    def lanza_servidor(self, var):
        the_path = self.ruta_server
        if var == True:
            global theproc
            theproc = subprocess.Popen([sys.executable, the_path])
            print("ESTADO DEL SERVIDOR: ENCENDIDO.")
            theproc.communicate()

    # #Este metodo detiene el servidor cuando se presiona salir
    def desconectando(self):
        global theproc
        if theproc != "servidor.py":
            theproc.kill()
        msg = QMessageBox()
        msg.setWindowTitle("Agenda-Cliente")
        msg.setText("ESTADO DEL SERVIDOR:APAGADO.")
        mensaje = msg.exec_()

    # #Este metodo ejecuta el modulo cliente.py para iniciar el proceso de recupero de registro de log
    def recuperando(self):
        the_path2 = self.ruta_cliente
        theproc2 = subprocess.Popen([sys.executable, the_path2])
        theproc2.communicate()
        print("Recuperando datos...")
        peti = Peticiones.select()
        for fila in peti:
            lista = "ID: {} ---  Autorizacion: {}" "\n".format(
                fila.id, fila.autorizaciones
            )
        if fila.autorizaciones == "00003ef5":
            print("Autorizacion obtenida del servidor...")
            self.tableWidget.setRowCount(0)
            obtengolog = Log.select()
            for fila in obtengolog:
                logobtenido = "Nombre:{} --- Direccion:{} --- Telefono:{} --- Email:{} --- Operacion:{} --- Fecha:{}" "\n".format(
                    fila.nombre,
                    fila.direccion,
                    fila.telefono,
                    fila.email,
                    fila.ejecucion,
                    fila.datetimes,
                )
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)
                self.tableWidget.setItem(
                    rowPosition, 0, QtWidgets.QTableWidgetItem(fila.nombre)
                )
                self.tableWidget.setItem(
                    rowPosition,
                    1,
                    QtWidgets.QTableWidgetItem(fila.direccion),
                )
                self.tableWidget.setItem(
                    rowPosition, 2, QtWidgets.QTableWidgetItem(fila.telefono)
                )
                self.tableWidget.setItem(
                    rowPosition, 3, QtWidgets.QTableWidgetItem(fila.email)
                )
                self.tableWidget.setItem(
                    rowPosition,
                    4,
                    QtWidgets.QTableWidgetItem(fila.ejecucion),
                )
                self.tableWidget.setItem(
                    rowPosition,
                    5,
                    QtWidgets.QTableWidgetItem(str(fila.datetimes)),
                )
            msg = QMessageBox()
            msg.setWindowTitle("Agenda-Cliente")
            msg.setText("Datos recuperados.")
            mensaje = msg.exec_()
        else:
            print("No hay autorizacion")

    # #Este metodo detiene el servidor y cierra la app cuando se presiona salir
    def saliendo(self):
        if theproc == True:
            theproc.kill()
        sys.exit()
