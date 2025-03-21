import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
import sqlite3 as dbapi
from conexionBD import ConexionBD
from informe_total import generar_informe


class FiestraPrincipal(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Exame21032025_GrupoA")

        caixaV = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        marco = Gtk.Frame (label = "Cliente")
        caixaV.pack_start (marco, True, True, 3)
        grid = Gtk.Grid()
        marco.add(grid)

        lblNumeroCliente = Gtk.Label(label ="Número Cliente")
        lblNomeCliente = Gtk.Label(label ="Nome")
        lblApelidosCliente = Gtk.Label(label ="Apelidos")
        lblDirección = Gtk.Label(label ="Dirección")
        lblCidade = Gtk.Label(label ="Cidade")
        lblProvinciaEstado = Gtk.Label(label ="Provincia")
        lblCodigoPostal = Gtk.Label(label ="Código postal")
        lblTelefono = Gtk.Label(label ="Teléfono")
        lblPais = Gtk.Label(label ="País")
        lblAxenteComercial = Gtk.Label(label ="AxenteComercial")
        self.txtNumeroCliente = Gtk.Entry()
        self.txtNomeCliente = Gtk.Entry()
        self.txtApelidosCliente = Gtk.Entry()
        self.txtDireccion = Gtk.Entry()
        self.txtCidade = Gtk.Entry()
        self.txtProvinciaEstado = Gtk.Entry()
        self.txtCodigoPostal = Gtk.Entry()
        self.txtTelefono = Gtk.Entry()
        self.txtPais = Gtk.Entry()
        self.txtAxenteComercial = Gtk.Entry()

        grid.attach(lblNumeroCliente, 0, 0, 1, 1)
        grid.attach(self.txtNumeroCliente, 1, 0, 1, 1)
        grid.attach(lblNomeCliente, 2, 0, 1, 1)
        grid.attach(self.txtNomeCliente, 3, 0, 1, 1)
        grid.attach(lblApelidosCliente, 0, 1, 1, 1)
        grid.attach(self.txtApelidosCliente, 1, 1, 3, 1)
        grid.attach(lblDirección, 0, 3, 1, 1)
        grid.attach(self.txtDireccion, 1, 3, 3, 1)
        grid.attach(lblCidade, 0, 4, 1, 1)
        grid.attach(self.txtCidade, 1, 4, 1, 1)
        grid.attach(lblProvinciaEstado, 2, 4, 1, 1)
        grid.attach(self.txtProvinciaEstado, 3, 4, 1, 1)
        grid.attach(lblCodigoPostal, 0, 5, 1, 1)
        grid.attach(self.txtCodigoPostal, 1, 5, 1, 1)
        grid.attach(lblTelefono, 2, 5, 1, 1)
        grid.attach(self.txtTelefono, 3, 5, 1, 1)
        grid.attach(lblPais, 0, 6, 1, 1)
        grid.attach(self.txtPais, 1, 6, 1, 1)
        grid.attach(lblAxenteComercial, 2, 6, 1, 1)
        grid.attach(self.txtAxenteComercial, 3, 6, 1, 1)

        caixaHTaboa = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 2)


        self.trvClientes = Gtk.TreeView()
        caixaHTaboa.pack_start (self.trvClientes, True, True, 2)
        self.btnEngadir = Gtk.Button(label ="Engadir")
        self.btnEngadir.connect('clicked', self.on_btnEngadir_clicked)

        self.btnEditar = Gtk.Button(label ="Editar")
        self.btnEditar.connect('clicked', self.on_btnEditar_clicked)

        self.btnBorrar = Gtk.Button(label ="Borrar")
        self.btnBorrar.connect('clicked', self.on_btnBorrar_clicked)

        self.btnInforme = Gtk.Button(label="Informe")
        self.btnInforme.connect('clicked', self.on_btnInforme_clicked)
        

        caixaBotonsEdicion = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 2)
        caixaBotonsEdicion.pack_start(self.btnEngadir, False, False, 0)
        caixaBotonsEdicion.pack_start(self.btnEditar, False, False, 0)
        caixaBotonsEdicion.pack_start(self.btnBorrar, False, False, 0)
        caixaBotonsEdicion.pack_start(self.btnInforme, False, False, 0)

        #TABLA

        conxBD = ConexionBD("modelosClasicos.dat")
        conxBD.conectaBD()
        conxBD.creaCursor()

        clientes = conxBD.consultaSenParametros("Select * from clientes")
        conxBD.pechaBD()

        self.modelo = Gtk.ListStore(int, str, str, str, str, str, str, str, str, int)
        for rexistro in clientes:
            self.modelo.append(rexistro)

        vista = Gtk.TreeView(model=self.modelo)

        columnas = ["Número Cliente", "Nome", "Apelidos", "Dirección", "Cidade", "Provincia", "Código Postal", "Teléfono", "País", "Axente"]

        for i in range(10):
            celda = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(columnas[i], celda, text=i)
            vista.append_column(columna)

        #######

        caixaHTaboa.pack_start(vista, True, True, 2)
        caixaHTaboa.pack_start(caixaBotonsEdicion, True, True, 2)
        caixaV.pack_start (caixaHTaboa, True, True, 2)



        caixaBtnAceptar = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        self.btnAceptar = Gtk.Button(label="Aceptar")
        self.btnAceptar.connect('clicked', self.on_btnAceptar_clicked)
        self.btnCancelar = Gtk.Button (label = "Cancelar")
        self.btnCancelar.connect('clicked', self.on_btnCancelar_clicked)
        caixaBtnAceptar.pack_end (self.btnCancelar, False, False, 2)
        caixaBtnAceptar.pack_end(self.btnAceptar, False, False, 2)
        caixaV.pack_start (caixaBtnAceptar, False, False, 2)

        self.add(caixaV)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

        self.estado_inicial()


    def on_btnEngadir_clicked(self, boton):
        print("pulso btn engadir")
        self.estado_editando()


    def on_btnEditar_clicked(self, boton):
        print("pulso btn editar")
        self.estado_editando()

    def on_btnBorrar_clicked(self, boton):
        print("pulso btn borrar")
        self.estado_editando()

    def on_btnInforme_clicked(self, boton):
        print("Informe")
        self.generar_informe_total()

    def on_btnAceptar_clicked(self, boton):
        print("pulso btn aceptar")
        self.introducir_registro()
        self.estado_inicial()

    def on_btnCancelar_clicked(self, boton):
        print("pulso btn cancelar")
        self.estado_inicial()

    def bloquearDesbloquearBotons(self, opcion):
        self.btnAceptar.set_sensitive(opcion)
        self.btnCancelar.set_sensitive(opcion)

    def bloquearDesbloquearBotonsEdicion(self, opcion):
        self.btnEditar.set_sensitive(opcion)
        self.btnEngadir.set_sensitive(opcion)
        self.btnBorrar.set_sensitive(opcion)
        self.btnInforme.set_sensitive(opcion)

    def bloquearDesbloquearCadrosTexto (self, opcion):
        self.txtNumeroCliente.set_sensitive(opcion)
        self.txtNomeCliente.set_sensitive(opcion)
        self.txtApelidosCliente.set_sensitive(opcion)
        self.txtDireccion.set_sensitive(opcion)
        self.txtCidade.set_sensitive(opcion)
        self.txtProvinciaEstado.set_sensitive(opcion)
        self.txtCodigoPostal.set_sensitive(opcion)
        self.txtTelefono.set_sensitive(opcion)
        self.txtPais.set_sensitive(opcion)
        self.txtAxenteComercial.set_sensitive(opcion)

    def limparControis(self):
        self.txtNumeroCliente.set_text('')
        self.txtNomeCliente.set_text('')
        self.txtApelidosCliente.set_text('')
        self.txtDireccion.set_text('')
        self.txtCidade.set_text('')
        self.txtProvinciaEstado.set_text('')
        self.txtCodigoPostal.set_text('')
        self.txtTelefono.set_text('')
        self.txtPais.set_text('')
        self.txtAxenteComercial.set_text('')

    def estado_inicial(self):
        self.bloquearDesbloquearCadrosTexto(False)
        self.bloquearDesbloquearBotons(False)
        self.bloquearDesbloquearBotonsEdicion(True)
        self.limparControis()

    def estado_editando(self):
        self.bloquearDesbloquearCadrosTexto(True)
        self.bloquearDesbloquearBotons(True)
        self.bloquearDesbloquearBotonsEdicion(False)

    def introducir_registro(self):
        conBD = ConexionBD('modelosClasicos.dat')
        conBD.conectaBD()
        conBD.creaCursor()

        conBD.engadeRexistro("""Insert Into clientes (numeroCliente, nomeCliente, apelidosCliente, telefono, direccion, cidade, provinciaEstado, codigoPostal, pais, axenteComercial)
                                            Values (?,?,?,?,?,?,?,?,?,?)""",
                            int(self.txtNumeroCliente.get_text()),
                            self.txtNomeCliente.get_text(),
                            self.txtApelidosCliente.get_text(),
                            self.txtDireccion.get_text(),
                            self.txtCidade.get_text(),
                            self.txtProvinciaEstado.get_text(),
                            self.txtCodigoPostal.get_text(),
                            self.txtTelefono.get_text(),
                            self.txtPais.get_text(),
                            int(self.txtAxenteComercial.get_text())
                             )
        list = conBD.consultaConParametros("SELECT * FROM clientes WHERE numeroCliente = ?", int(self.txtNumeroCliente.get_text()))

        for i in list:
            print(i)
            self.modelo.append(i)

        conBD.pechaBD()

    def generar_informe_total(self):
        generar_informe("informe_total.pdf", self.modelo)


if __name__ == "__main__":
    FiestraPrincipal()
    Gtk.main()