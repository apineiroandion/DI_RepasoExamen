import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class FiestraPrincipal (Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Exemplo con GTK TreeView")

        # Creación do modelo de datos
        columnas = ["Nome", "Apelidos", "NUmero de telefono"]
        # Datos da axenda telefónica
        axendaTelefonica = [["Antonio", "Pérez", "981234567"],
                             ["María", "López", "982345678"],
                             ["Manuel", "García", "983456789"],
                             ["Ana", "Martínez", "984567890"]]

        # Creación do modelo de datos
        listin = Gtk.ListStore(str, str, str)
        # Engadir os rexistros
        for rexistro in axendaTelefonica:
            listin.append(rexistro)

        # Creación da vista do modelo
        caixaV = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        # Creación do TreeView
        vista = Gtk.TreeView(model=listin)

        # Creación das columnas
        for i in range (len(columnas)):
            celda = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(columnas[i], celda, text=i)
            vista.append_column(columna)

        caixaV.pack_start(vista, True, True, 0)

        self.add(caixaV)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()


if __name__ == "__main__":
    FiestraPrincipal()
    Gtk.main()
