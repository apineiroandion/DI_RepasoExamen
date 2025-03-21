import gi

from gi.repository import Gtk
import sqlite3 as dbapi
from conexionBD import ConexionBD

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.connect("destroy", Gtk.main_quit)
        self.set_title("Exemplo previo")

        conBD = ConexionBD("modelosClasicos.dat")
        conBD.conectaBD()
        conBD.creaCursor()

        caixaV = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        lista = conBD.consultaSenParametros("SELECT nomeCLiente, apelidosCliente FROM clientes")

        modelo = Gtk.ListStore(str, str)
        for rexistro in lista:
            modelo.append(rexistro)

        vista = Gtk.TreeView(model=modelo)

        for i in range(2):
            celda = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn("Columna " + str(i), celda, text=i)
            vista.append_column(columna)

        caixaV.pack_start(vista, True, True, 0)
        self.add(caixaV)
        self.show_all()




if __name__ == "__main__":
    ventana = MainWindow()
    ventana.show_all()
    Gtk.main()