import gi

from conexionBD import ConexionBD

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class MainWindor(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Main Window")

        caixaV = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        grid = Gtk.Grid()

        lblNumeroAlbaran = Gtk.Label(label="Número de albarán")
        lblData = Gtk.Label(label="Data")
        lblEntrega = Gtk.Label(label="Entrega")
        lblNumeroCliente = Gtk.Label(label="Número de cliente")
        lblApelidosCliente = Gtk.Label(label="Apelidos do cliente")
        lblNomeCliente = Gtk.Label(label="Nome do cliente")

        self.cmbNumeroAlbaran = Gtk.ComboBox()
        self.txtDataAlbaran = Gtk.Entry()
        self.txtDataEntrega = Gtk.Entry()
        self.txtNumeroCliente = Gtk.Entry()
        self.txtApelidosCliente = Gtk.Entry()
        self.txtNomeCliente = Gtk.Entry()

        # Añadimos los elementos al grid
        grid.add(lblNumeroAlbaran)
        #attach (elemento, columna, fila, ancho, alto) es decir, el elemento, la columna, la fila, el ancho y el alto
        #el next_to es para que se ponga a la derecha del elemento anterior
        grid.attach_next_to(self.cmbNumeroAlbaran, lblNumeroAlbaran, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(lblData, lblNumeroAlbaran, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.txtDataAlbaran, lblData, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(lblEntrega, lblData, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.txtDataEntrega, lblEntrega, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(lblNumeroCliente, self.cmbNumeroAlbaran, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(self.txtNumeroCliente, lblNumeroCliente, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(lblApelidosCliente, lblNumeroCliente, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.txtApelidosCliente, lblApelidosCliente, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(lblNomeCliente, lblApelidosCliente, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.txtNomeCliente, lblNomeCliente, Gtk.PositionType.RIGHT, 1, 1)


        # Añadimos el grid a la caja vertical parametros: widget, expandir, rellenar, margen
        caixaV.pack_start(grid, True, True, 0)


        conBD = ConexionBD("modelosClasicos.dat")
        conBD.conectaBD()
        conBD.creaCursor()
        numerosAlbaran = conBD.consultaSenParametros("SELECT numeroAlbara FROM ventas")
        modeloCmbAlbaran = Gtk.ListStore(int)
        for numero in numerosAlbaran:
            modeloCmbAlbaran.append(numero)

        self.cmbNumeroAlbaran.set_model(model = modeloCmbAlbaran)
        celda = Gtk.CellRendererText()
        self.cmbNumeroAlbaran.pack_start(celda, True)
        self.cmbNumeroAlbaran.add_attribute(celda, "text", 0)
        #self.cmbNumeroAlbaran.connect("changed", self.on_cmbNumeroAlbaran_changed)

        caixa_botons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        self.boton_engadir = Gtk.Button(label="Engadir")
        self.boton_editar = Gtk.Button(label="Editar")
        self.boton_borrar = Gtk.Button(label="Borrar")

        self.boton_engadir.connect("clicked", self.on_boton_engadir_clicked)
        self.boton_editar.connect("clicked", self.on_boton_editar_clicked)
        self.boton_borrar.connect("clicked", self.on_boton_borrar_clicked)

        caixa_botons.pack_start(self.boton_engadir, True, True, 0)
        caixa_botons.pack_start(self.boton_editar, True, True, 0)
        caixa_botons.pack_start(self.boton_borrar, True, True, 0)

        caixaV.pack_start(caixa_botons, False, False, 0)


        self.txtCodigoProducto = Gtk.Entry()
        self.txtCantidade = Gtk.Entry()
        self.txtPrezoUnitario = Gtk.Entry()
        caixa_campos_albaran = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        caixa_campos_albaran.pack_start(self.txtCodigoProducto, True, True, 2)
        caixa_campos_albaran.pack_start(self.txtCantidade, True, True, 2)
        caixa_campos_albaran.pack_start(self.txtPrezoUnitario, True, True, 2)

        self.txtCodigoProducto.set_visible(False)
        self.txtCantidade.set_visible(False)
        self.txtPrezoUnitario.set_visible(False)

        self.operacion = None

        caixaV.pack_start(caixa_campos_albaran, False, False, 0)



        self.tryDetalleAlbaran = Gtk.TreeView()
        self.modelDetalleAlbaran = Gtk.ListStore(int, str, int, float)


        numero_albaran = self.cmbNumeroAlbaran.get_active()

        detalle_ventas = conBD.consultaConParametros("SELECT codigoProduto, cantidade, prezoUnitario FROM detalleVentas WHERE numeroAlbaran = ?", numero_albaran)

        for detalle in detalle_ventas:
            nomeProducto = conBD.consultaConParametros("SELECT nomeProduto FROM produtos WHERE codigoProduto = ?", detalle[0].strip()) #strip() elimina los espacios en blanco

            listaDetalle = list(detalle)
            listaDetalle.insert(1, nomeProducto[0][0])
            print(listaDetalle)
            self.modelDetalleAlbaran.append(listaDetalle)


        self.tryDetalleAlbaran.set_model(self.modelDetalleAlbaran)
        self.selection = self.tryDetalleAlbaran.get_selection()

        caixaV.pack_start(self.tryDetalleAlbaran, True, True, 0)

        # Creación das columnas
        for i in range(4):
            celda = Gtk.CellRendererText()
            nombresColumnas = ["Código Produto", "Nome Produto", "Cantidade", "Prezo Unitario"]
            columna = Gtk.TreeViewColumn(nombresColumnas[i], celda, text=i) #text=i indica la posición de la lista que se mostrará en la columna
            self.tryDetalleAlbaran.append_column(columna)



        caixa_boton_aceptar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        self.boton_aceptar = Gtk.Button(label="Aceptar")
        self.boton_aceptar.connect("clicked", self.on_boton_aceptar_clicked)

        self.boton_cancelar = Gtk.Button(label="Cancelar")
        self.boton_cancelar.connect("clicked", self.on_boton_cancelar_clicked)
        caixa_boton_aceptar.pack_start(self.boton_aceptar, True, True, 2)
        caixa_boton_aceptar.pack_start(self.boton_cancelar, True, True, 2)

        caixaV.pack_start(caixa_boton_aceptar, False, False, 0)

        self.add(caixaV)
        self.connect("delete-event", Gtk.main_quit)

    def on_boton_engadir_clicked(self, widget):
        self.operacion = "engadir"
        self.mostrar_controis(True)
        self.bloquear_botons(False)
        self.bloquearBotonsEdicion(False)
        self.limpiar_controis()

    def mostrar_controis(self, opcion):
        self.txtCodigoProducto.set_visible(opcion)
        self.txtCantidade.set_visible(opcion)
        self.txtPrezoUnitario.set_visible(opcion)

    def bloquear_botons(self, opcion):
        self.boton_aceptar.setEnabled(opcion)
        self.boton_cancelar.setEnabled(opcion)

    def bloquearBotonsEdicion(self, opcion):
        self.boton_engadir.setEnabled(opcion)
        self.boton_editar.setEnabled(opcion)
        self.boton_borrar.setEnabled(opcion)

    def limpiar_controis(self):
        self.txtCodigoProducto.set_text("")
        self.txtCantidade.set_text("")
        self.txtPrezoUnitario.set_text("")

    def on_boton_editar_clicked(self, widget):
        print("Botón Editar clicado")

    def on_boton_borrar_clicked(self, widget):
        print("Botón Borrar clicado")

    def on_boton_aceptar_clicked(self, widget):
        if self.operacion == "engadir":
            conxBD = ConexionBD("modelosClasicos.dat")
            conxBD.conectaBD()
            conxBD.creaCursor()
            linhas = conxBD.consultaConParametros(
                "SELECT * FROM detalleVentas WHERE numeroAlbaran = ?",
                self.cmbNumeroAlbaran.get_active())
            numLinha = 0
            for linha in linhas:
                if linha[0] > numLinha:
                    numLinha = linha[0]
            numLinha += 1
            conxBD.engadirFila("""Insert into detalleVentas (numeroAlbaran, codigoProduto, cantidade, prezoUnitario), values (?, ?, ?, ?)""",
                               (self.cmbNumeroAlbaran.get_active(), self.txtCodigoProducto.get_text(), self.txtCantidade.get_text(), self.txtPrezoUnitario.get_text()))



    def on_boton_cancelar_clicked(self, widget):
        print("Botón Cancelar clicado")



if __name__ == "__main__":
    win = MainWindor()
    win.show_all()
    Gtk.main()