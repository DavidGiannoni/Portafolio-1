import sys
from agenda_cliente_vista import Ui_MainWindow
from PyQt5 import QtWidgets
from agenda_cliente_modelo import theproc

# #Inicia la App principal Agenda-Cliente
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("PROGRAMA CERRADO.")
        if theproc != "servidor.py":
            theproc.kill()
