# #Realizo la importaciones que se van a utilizar
from peewee import CharField
from peewee import DateTimeField
from peewee import IntegerField
from peewee import MySQLDatabase
from peewee import Model
from PyQt5 import QtWidgets
import mysql.connector
from agenda_server_vista import Ui_MainWindow
from agenda_server_vista import Ui_menu_modificar
from agenda_server_vista import Ui_Eliminar
from PyQt5.QtWidgets import QMessageBox

# global HOST
global PORT
# #Defino vairables
# #le paso a peewee el nombre de la base de datos
db = MySQLDatabase("db", user="root", password="", host="localhost", port=3306)
# Le paso al ORM (peewee)la clase que contiene el nombre de la base de datos
class BaseModel(Model):
    class Meta:
        database = db


# #Le paso al ORM (peewee),la clase con los nombres de las columnas definidas que contiene la tabla creada por mysql, en este caso para los datops de Agenda
class Agenda(BaseModel):
    id = IntegerField()
    nombre = CharField()
    direccion = CharField()
    telefono = CharField()
    email = CharField()


# #Le paso al ORM (peewee),la clase con los nombres de las columnas definidas que contiene la tabla creada por mysql, en este caso para el LOG
class Log(BaseModel):
    nombre = CharField()
    direccion = CharField()
    telefono = CharField()
    email = CharField()
    datetimes = DateTimeField(primary_key=True)
    ejecucion = CharField()


# #Creo una clase contenedora de los metodos del crud y el enlaze de los botones con los metodos
class Metodos(Ui_MainWindow, Ui_menu_modificar, Ui_Eliminar):
    # #Creo la base de datos(sino existe),tanto la del log como la base de datos propia de la agenda
    # que contiene losd datos de los contactos ,defino sus tablas y sus caracteristicas en lenguaje de MYSQL

    def crearbd(self):
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
        db.connect()
        db.create_tables([Agenda])
        db.create_tables([Log])
        db.close()

    # Estos son los metodos que se usan para el CRUD
    # #Este metodo actualiza la tabla de Agenda-Server obteniendo los datos a travez de peewee
    def actualiza(self):
        try:
            self.tableWidget.setRowCount(0)
            db.connect()
            filas = Agenda.select()
            for fila in filas:
                lista = (
                    "ID: {} ---  Nombre: {} --- Direccion: {} --- Telefono: {} --- Email: {}"
                    "\n".format(
                        fila.id, fila.nombre, fila.direccion, fila.telefono, fila.email
                    )
                )
                rowPosition = self.tableWidget.rowCount()
                self.tableWidget.insertRow(rowPosition)
                self.tableWidget.setItem(
                    rowPosition, 0, QtWidgets.QTableWidgetItem(str(fila.id))
                )
                self.tableWidget.setItem(
                    rowPosition, 1, QtWidgets.QTableWidgetItem(fila.nombre)
                )
                self.tableWidget.setItem(
                    rowPosition, 2, QtWidgets.QTableWidgetItem(fila.direccion)
                )
                self.tableWidget.setItem(
                    rowPosition, 3, QtWidgets.QTableWidgetItem(fila.telefono)
                )
                self.tableWidget.setItem(
                    rowPosition, 4, QtWidgets.QTableWidgetItem(fila.email)
                )
            db.close()

        except:
            msg = QMessageBox()
            msg.setWindowTitle("Agenda-Servidor")
            msg.setText("Algo ocurrio , vuelva a intentarlo.")
            mensaje = msg.exec_()

    # Esta funcion modifica los contactos y guarda los cambios en el servidor a travez del ORM peewee
    def modificar(self):
        try:
            db.connect()
            lista = []
            for datos in (
                self.id_lineEdit,
                self.nombre_lineEdit,
                self.direccion_lineEdit,
                self.telefono_lineEdit,
                self.email_lineEdit,
            ):
                lista.append(datos.text())
            fila = Agenda.get(Agenda.id == str(lista[0]))
            fila.nombre = lista[1]
            fila.direccion = lista[2]
            fila.telefono = lista[3]
            fila.email = lista[4]
            fila.save()
            lista.append("MODIFICADO")
            diclog = {
                "nombre": lista[1],
                "direccion": lista[2],
                "telefono": lista[3],
                "email": lista[4],
                "ejecucion": lista[5],
            }
            Log.create(**diclog)
            db.close()
            msg = QMessageBox()
            msg.setWindowTitle("Agenda-Servidor")
            msg.setText("Contacto modificado.")
            mensaje = msg.exec_()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Agenda-Servidor")
            msg.setText("Algo ocurrio , vuelva a intentarlo.")
            mensaje = msg.exec_()

    # #Lanza el submenu para modificar ejecutando la funcion modificar.
    def abre_modificar(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_menu_modificar()
        self.ui.setupUi(self.window)
        self.window.show()

    # #Lanza el submenu el para eliminar ejecutando la funcion elimina.
    def abre_elimina(self):
        self.window2 = QtWidgets.QMainWindow()
        self.ui = Ui_Eliminar()
        self.ui.setupUi(self.window2)
        self.window2.show()

    # #Esta funcion elimina un contacto que fue seleccionado por su ID
    def elimina(self):
        db.connect()
        listaid = []
        listaid.append(self.lineEdit_id.text())
        int_list = list(map(int, listaid))
        listag = []
        listag.append(Agenda.get(Agenda.id == int_list).nombre)
        listag.append(Agenda.get(Agenda.id == int_list).direccion)
        listag.append(Agenda.get(Agenda.id == int_list).telefono)
        listag.append(Agenda.get(Agenda.id == int_list).email)
        listag.append("BORRADO")
        diclog = {
            "nombre": listag[0],
            "direccion": listag[1],
            "telefono": listag[2],
            "email": listag[3],
            "ejecucion": listag[4],
        }
        Log.create(**diclog)
        Agenda.delete_by_id(int_list)
        db.close()
        msg = QMessageBox()
        msg.setWindowTitle("Agenda-Servidor")
        msg.setText("Contacto borrado.")
        mensaje = msg.exec_()

    # #Esta funcion guarda los contactos nuevos en la base de datos a travez del ORM peewee

    def guarda(self):
        db.connect()
        lista = []
        for datos in (
            self.lineEdit_nombre,
            self.lineEdit_direccion,
            self.lineEdit_telefono,
            self.lineEdit_email,
        ):
            lista.append(datos.text())
        lista.append("GUARDADO")
        dic = {
            "nombre": lista[0],
            "direccion": lista[1],
            "telefono": lista[2],
            "email": lista[3],
        }
        diclog = {
            "nombre": lista[0],
            "direccion": lista[1],
            "telefono": lista[2],
            "email": lista[3],
            "ejecucion": lista[4],
        }
        print(diclog)
        Agenda.create(**dic)
        Log.create(**diclog)
        db.close()
        Metodos.actualiza(self)

    # #Esta funcion cierra la app o submenu que corresponde a eliminar
    def eliminar_cerrar(self):
        Metodos.actualiza(self)

    # #Esta funcion cierra la app o submenu que corresponde a modificar
    def modi_cerrar(self):
        Metodos.actualiza(self)
