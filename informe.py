import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, SimpleDocTemplate, Image

def generar_informe(output_filename):
    doc = SimpleDocTemplate(output_filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    #Componentes
    #Labels

    fichaClientelbl = "Ficha Cliente"
    numerolbl = "Número"
    numero = 1

    nomelbl = "Nome"
    nome = "Ana Perez Diz"

    direccionlbl = "Direccion"
    direccion = "Garcia Barbón 3"

    cidadelbl = "Cidade"
    cidade = "Vigo"

    provincialbl = "Provincia"
    provincia = "Pontevedra"

    codigoPostallbl = "Codigo Postal"
    codigoPostal = "362016"

    paislbl = "Pais"
    pais = "España"

    axentelbl = "Axente"
    axente = "1"

    telefonolbl = "Telefono"
    telefono = "986 201 322"

    tabla_datos = Table([
        [fichaClientelbl, "", numerolbl, numero],
        [nomelbl, nome, "" , ""],
        [direccionlbl, direccion, "", ""],
        [cidadelbl, provincialbl, codigoPostallbl, paislbl],
        [cidade, provincia, codigoPostal, pais],
        [axentelbl, axente, telefonolbl, telefono],
    ])

    tabla_datos.setStyle(TableStyle([
        # Cabecera
        ('BACKGROUND', (0, 1), (-4, 1), HexColor("#8ebbe4")),
        ('BACKGROUND', (0, 2), (-4, 2), HexColor("#8ebbe4")),
        ('BACKGROUND', (0, 3), (-1, 3), HexColor("#8ebbe4")),
        ('BACKGROUND', (0, 5), (-4, 5), HexColor("#8ebbe4")),
        ('BACKGROUND', (2, 5), (-2, 5), HexColor("#8ebbe4")),

        ('GRID', (0, 0), (-1, -1), 1, colors.white),

    ]))

    elements.append(tabla_datos)

    doc.build(elements)



if __name__ == '__main__':
    generar_informe("informe.pdf")