# #Llamo las importaciones necesarias para la correcta ejecucion del modulo
import sys
from agenda_server_modelo import Ui_MainWindow
from PyQt5 import QtWidgets
from agenda_server_modelo import Metodos

# #Inicia la App principal Agenda-Servidor
if __name__ == "__main__":
    Metodos.crearbd(Ui_MainWindow)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
