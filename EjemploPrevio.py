import gi

from gi.repository import Gtk
import sqlite3 as dbapi
from conexionBD import ConexionBD

class FiestraPrincipal (Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Exemplo previo")

        caixaV = Gtk.Box (orientation = Gtk.Orientation.VERTICAL, spacing = 6)
        grid = Gtk.Grid()

        lblNumeroAlbara = Gtk.Label (label="Número albará")
        lblData = Gtk.Label(label="Data")
        lblDataEntrega = Gtk.Label(label="Data entrega")
        lblNumeroCliente = Gtk.Label(label="Número Cliente")
        lblNomeCliente = Gtk.Label(label="Nome Cliente")
        lblApelidosCliente = Gtk.Label (label = "Apelidos Cliente")

        self.cmbNumeroAlbara = Gtk.ComboBox()
        self.txtDataAlbara = Gtk.Entry()
        self.txtDataEntrega = Gtk.Entry()
        self.txtNumeroCliente= Gtk.Entry()
        self.txtNomeCliente = Gtk.Entry()
        self.txtApelidosCliente = Gtk.Entry()

        grid.add(lblNumeroAlbara)
        grid.attach_next_to(self.cmbNumeroAlbara, lblNumeroAlbara,Gtk.PositionType.RIGHT,1,1)
        grid.attach_next_to(lblData, self.cmbNumeroAlbara, Gtk.PositionType.RIGHT, 1,1)
        grid.attach_next_to(self.txtDataAlbara, lblData,  Gtk.PositionType.RIGHT, 1, 1)

        grid.attach_next_to(lblNumeroCliente, lblNumeroAlbara, Gtk.PositionType.BOTTOM, 1,1)
        grid.attach_next_to(self.txtNumeroCliente, lblNumeroCliente, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(lblDataEntrega, self.txtNumeroCliente, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(self.txtDataEntrega, lblDataEntrega, Gtk.PositionType.RIGHT, 1, 1)

        grid.attach_next_to(lblNomeCliente, lblNumeroCliente, Gtk.PositionType.BOTTOM, 1,1)
        grid.attach_next_to(self.txtNomeCliente, lblNomeCliente, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to( lblApelidosCliente ,self.txtNomeCliente, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(self.txtApelidosCliente, lblApelidosCliente , Gtk.PositionType.RIGHT, 1, 1)


        caixaV.pack_start(grid,True, True, 0)

        conBD = ConexionBD("modelosClasicos.dat")
        conBD.conectaBD()
        conBD.creaCursor()
        numerosAlbaras = conBD.consultaSenParametros("Select numeroAlbara from ventas")
        modeloCmbAlbaran = Gtk.ListStore(int)
        for numero in numerosAlbaras:
            modeloCmbAlbaran.append(numero)

        self.cmbNumeroAlbara.set_model(model=modeloCmbAlbaran)
        celda = Gtk.CellRendererText()
        self.cmbNumeroAlbara.pack_start(celda, True)
        self.cmbNumeroAlbara.add_attribute(celda, "text", 0)
        self.cmbNumeroAlbara.set_active(0)
        #self.cmbNumeroAlbara.connect("changed", self.on_cmbNumeroAlbara_changed)

        caixaBotons = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 2)
        self.btnEngadir = Gtk.Button(label="Engadir")
        self.btnEditar = Gtk.Button(label="Editar")
        self.btnBorrar = Gtk.Button(label="Borrar")
        self.btnEngadir.connect("clicked", self.on_btnEngadir_clicked)
        #self.btnEditar.connect("clicked", self.on_btnEditar_clicked)
        #self.btnBorrar.connect("clicked", self.on_btnBorrar_clicked)
        caixaBotons.pack_start(self.btnEngadir, False, False, 2 )
        caixaBotons.pack_start(self.btnEditar, False, False, 2)
        caixaBotons.pack_start(self.btnBorrar, False, False, 2)
        caixaV.pack_start(caixaBotons, False, False, 0)

        self.txtCodigoProduto = Gtk.Entry()
        self.txtCantidade = Gtk.Entry()
        self.txtPrezoUnitario = Gtk.Entry()
        caixaCamposAlbaran = Gtk.Box (orientation = Gtk.Orientation.HORIZONTAL, spacing = 2)
        caixaCamposAlbaran.pack_start(self.txtCodigoProduto, True, False, 2)
        caixaCamposAlbaran.pack_start(self.txtCantidade, True, False, 2)
        caixaCamposAlbaran.pack_start(self.txtPrezoUnitario, True, False, 2)

        caixaV.pack_start(caixaCamposAlbaran, False, False, 0)

        self.trvDetalleAlbara = Gtk.TreeView()
        self.modeloDetalleAlbara = Gtk.ListStore(str, str, int, float)

        punteiro = self.cmbNumeroAlbara.get_active()
        numAlbara = modeloCmbAlbaran [punteiro][0]
        print (numAlbara)
        detalleVentas = conBD.consultaConParametros(
            "Select codigoProduto, cantidade, prezoUnitario from detalleVentas Where numeroAlbaran = ?",
            numAlbara )

        for detalle in detalleVentas:
            nomeProduto = conBD.consultaConParametros ("Select nomeProduto from Produtos Where codigoProduto  = ?",
                                                       detalle[0].strip())
            listaDetalle = list(detalle)
            listaDetalle.insert(1, nomeProduto[0][0])
            print (detalle)
            self.modeloDetalleAlbara.append (listaDetalle)

        self.trvDetalleAlbara.set_model(self.modeloDetalleAlbara)
        #self.seleccion = self.trvDetalleAlbara.SelectionModel()
        caixaV.pack_start(self.trvDetalleAlbara, False, False, 2)
        celda = Gtk.CellRendererText ()
        columna = Gtk.TreeViewColumn("Cod produto", celda, text = 0)
        self.trvDetalleAlbara.append_column(columna)
        celda = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn ("Produto", celda, text = 1)
        self.trvDetalleAlbara.append_column(columna)
        celda = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn("Cantidade", celda, text=2)
        self.trvDetalleAlbara.append_column(columna)
        celda = Gtk.CellRendererText()
        columna = Gtk.TreeViewColumn("Prezo unidade", celda, text=3)
        self.trvDetalleAlbara.append_column(columna)

        caixaBtnAceptar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        self.btnAceptar = Gtk.Button(label="Aceptar")
        self.btnAceptar.connect("clicked", self.on_btnAceptar_clicked)
        caixaBtnAceptar.pack_start(self.btnAceptar, False, False, 2)
        self.btnCancelar = Gtk.Button(label="Cancelar")
        #self.btncancelar.connect("clicked", self.on_btnCancelar_clicked)
        caixaBtnAceptar.pack_start(self.btnCancelar, False, False, 2)
        caixaV.pack_start(caixaBtnAceptar, False, False, 2)

        #caixaV.pack_start (caixaV, True, True, 0)
        self.add(caixaV)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
        self.txtCodigoProduto.set_visible(False)
        self.txtCantidade.set_visible(False)
        self.txtPrezoUnitario.set_visible(False)

        self.operacion = None


    def on_btnEngadir_clicked(self, boton):
        self.operacion = "Engadir"
        self.mostrarControis (True)
        self.bloquearBotons (True)
        self.bloquearBotonsEdicion(False)
        self.limparControis()

    def mostrarControis (self, opcion):

        self.txtCodigoProduto.set_visible(opcion)
        self.txtCantidade.set_visible(opcion)
        self.txtPrezoUnitario.set_visible(opcion)

    def bloquearBotons (self, opcion):
        self.btnAceptar.set_sensitive (opcion)
        self.btnCancelar.set_sensitive(opcion)

    def bloquearBotonsEdicion (self, opcion):
        self.btnEditar.set_sensitive (opcion)
        self.btnEngadir.set_sensitive (opcion)
        self.btnBorrar.set_sensitive(opcion)

    def limparControis (self):

        self.txtCodigoProduto.set_text('')
        self.txtCantidade.set_text('')
        self.txtPrezoUnitario.set_text('')

    def on_btnAceptar_clicked (self, boton):
        if self.operacion == 'Engadir':
            conBD = ConexionBD ('modelosClasicos.dat')
            conBD.conectaBD()
            conBD.creaCursor()
            linhas = conBD.consultaConParametros(
                """Select numeroLinhaAlbaran From detalleVentas Where numeroAlbaran = ?""",
                self.cmbNumeroAlbara.get_model() [self.cmbNumeroAlbara.get_active()][0])
            numLinha = 0
            for linha in linhas:
                if linha[0] > numLinha:
                    numLinha = linha[0]
            numLinha =+ numLinha

            conBD.engadeRexistro("""Insert Into detalleVentas (numeroAlbaran, codigoProduto, cantidade, prezoUnitario, numeroLinhaAlbaran)
                                    Values (?,?,?,?,?)""",
                                 self.cmbNumeroAlbara.get_model() [self.cmbNumeroAlbara.get_active()][0],
                                 self.txtCodigoProduto.get_text(),
                                 int(self.txtCantidade.get_text()),
                                 float(self.txtPrezoUnitario.get_text()),
                                 numLinha)
            nomeProducto = conBD.consultaConParametros ("Select nomeProduto from produtos Where codigoProduto=?",
                                                        self.txtCodigoProduto.get_text())
            conBD.pechaBD()
            self.modeloDetalleAlbara.append([
                self.txtCodigoProduto.get_text(),
                nomeProducto[0][0],
                int(self.txtCantidade.get_text()),
                float(self.txtPrezoUnitario.get_text())])







if __name__ == "__main__":
    FiestraPrincipal()
    Gtk.main()