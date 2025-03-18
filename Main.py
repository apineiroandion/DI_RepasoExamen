import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Main Window")

        caixa = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        lblSaudo = Gtk.Label(label="Introduce o teu nome")
        txtSaudo = Gtk.Entry()
        txtSaudo.connect("activate", self.on_txtSaudo_activate, lblSaudo)
        caixa.pack_start(txtSaudo, False, False, 5)

        btnSaudo = Gtk.Button()
        btnSaudo.set_label("Saudar ten moito texto para mistrar enton e moi long")
        btnSaudo.connect("clicked", self.on_btnSaudo_clicked, txtSaudo, lblSaudo)
        caixa.pack_start(btnSaudo, False, True, 5)

        self.add(caixa)
        self.connect("delete-event", Gtk.main_quit)

    def on_btnSaudo_clicked(self, btn, txtSaudo, lblSaudo):
        lblSaudo.set_text("Ola " + txtSaudo.get_text())

    def on_txtSaudo_activate(self, txtSaudo, lblSaudo):
        lblSaudo.set_text("Ola " + txtSaudo.get_text())

if __name__ == "__main__":
    win = MainWindow()
    win.show_all()
    Gtk.main()



