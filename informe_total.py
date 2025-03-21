import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, SimpleDocTemplate, Image

def generar_informe(output_filename, lista):
    doc = SimpleDocTemplate(output_filename, pagesize=A4)

    tables = []

    for item in lista:
        numero = item[0]
        nome = item[1]
        apellido = item[2]
        telefono = item[3]
        direccion = item[4]
        cidade = item[5]
        provincia = item[6]
        codigoPostal = item[7]
        pais = item[8]
        axente = item[9]

        print (numero, nome, apellido, telefono, direccion, cidade, pais, axente)
        fichaClientelbl = "Ficha Cliente"
        numerolbl = "Número"

        nomelbl = "Nome"

        direccionlbl = "Direccion"

        cidadelbl = "Cidade"

        provincialbl = "Provincia"

        codigoPostallbl = "Codigo Postal"

        paislbl = "Pais"

        axentelbl = "Axente"

        telefonolbl = "Telefono"

        tabla_datos = Table([
            [fichaClientelbl, "", numerolbl, numero],
            [nomelbl, nome, "" , ""],
            [direccionlbl, direccion, "", ""],
            [cidadelbl, provincialbl, codigoPostallbl, paislbl],
            [cidade, provincia, codigoPostal, pais],
            [axentelbl, axente, telefonolbl, telefono],
            []
        ], colWidths=[120, 100])

        tabla_datos.setStyle(TableStyle([
            # Cabecera
            ('BACKGROUND', (0, 1), (-4, 1), HexColor("#8ebbe4")),
            ('BACKGROUND', (0, 2), (-4, 2), HexColor("#8ebbe4")),
            ('BACKGROUND', (0, 3), (-1, 3), HexColor("#8ebbe4")),
            ('BACKGROUND', (0, 5), (-4, 5), HexColor("#8ebbe4")),
            ('BACKGROUND', (2, 5), (-2, 5), HexColor("#8ebbe4")),

            ('GRID', (0, 0), (-1, -1), 1, colors.white),

        ]))

        tables.append(tabla_datos)

    doc.build(tables)

