import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class NombreApellidoApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Formulario GTK")

        # Layout principal
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # Entrada de Nombre
        hbox_nombre = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.nombre_entry = Gtk.Entry() # Campo de texto
        hbox_nombre.pack_start(Gtk.Label(label="Nombre:"), False, False, 0) # Etiqueta param: texto, expandir, rellenar, margen
        hbox_nombre.pack_start(self.nombre_entry, True, True, 0) # Campo de texto param: expandir, rellenar, margen
        vbox.pack_start(hbox_nombre, False, False, 0) # Caja de texto param: expandir, rellenar, margen

        # Entrada de Apellido
        hbox_apellido = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.apellido_entry = Gtk.Entry()
        hbox_apellido.pack_start(Gtk.Label(label="Apellido:"), False, False, 0)
        hbox_apellido.pack_start(self.apellido_entry, True, True, 0)
        vbox.pack_start(hbox_apellido, False, False, 0)

        # Botón para agregar a la tabla
        self.boton_agregar = Gtk.Button(label="Agregar")
        self.boton_agregar.connect("clicked", self.on_agregar_clicked)
        vbox.pack_start(self.boton_agregar, False, False, 0)

        # Vista de la tabla
        self.store = Gtk.ListStore(str, str)
        self.treeview = Gtk.TreeView(model=self.store)

        # Columnas de la tabla
        for i, titulo in enumerate(["Nombre", "Apellido"]):
            renderer = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(titulo, renderer, text=i)
            self.treeview.append_column(columna)

        vbox.pack_start(self.treeview, True, True, 0)

    def on_agregar_clicked(self, widget):
        nombre = self.nombre_entry.get_text().strip()
        apellido = self.apellido_entry.get_text().strip()
        if nombre and apellido:
            self.store.append([nombre, apellido])
            self.nombre_entry.set_text("")
            self.apellido_entry.set_text("")

# Ejecutar la aplicación
if __name__ == "__main__":
    win = NombreApellidoApp()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()