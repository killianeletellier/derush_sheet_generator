#!/usr/bin/env python3

# =============================================================================
# CONFIGURATION
# =============================================================================

# Chemins des fichiers
CSV_INPUT = "../derush_sheet.csv"  # Fichier CSV d'entrée
PDF_OUTPUT = "../derush_sheet.pdf"  # Fichier PDF de sortie

# Configuration du PDF
PAGE_SIZE = "A4"  # Format de page (A4, A3, etc.)
ORIENTATION = "landscape"  # Orientation (landscape ou portrait)
MARGINS = {
    "left": 100,
    "right": 100,
    "top": 50,
    "bottom": 50
}

# Configuration des styles
TITLE = "Feuille de dérushage"  # Titre du document
ACCENT_COLOR = "#B45F06"  # Couleur d'accent (format hexadécimal)
FONT_SIZE = {
    "title": 24,
    "header": 10,
    "body": 8
}

# Configuration du tableau
COLUMN_WIDTHS = [65, 59, 59, 50, 150, 150, 150, 45]  # Largeurs des colonnes en points

# =============================================================================
# IMPORTS
# =============================================================================

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import csv
import os

# =============================================================================
# FONCTIONS
# =============================================================================

def create_pdf():
    """Crée le PDF à partir du fichier CSV."""
    # Vérifier si le fichier CSV existe
    if not os.path.exists(CSV_INPUT):
        print(f"Erreur: Le fichier CSV n'existe pas: {CSV_INPUT}")
        return

    # Créer le document PDF avec les marges configurées
    doc = SimpleDocTemplate(
        PDF_OUTPUT,
        pagesize=landscape(A4) if ORIENTATION == "landscape" else A4,
        leftMargin=MARGINS["left"],
        rightMargin=MARGINS["right"],
        topMargin=MARGINS["top"],
        bottomMargin=MARGINS["bottom"]
    )
    elements = []
    
    # Styles personnalisés
    styles = getSampleStyleSheet()
    
    # Style du titre
    title_style = styles['Title']
    title_style.fontSize = FONT_SIZE["title"]
    title_style.textColor = colors.HexColor(ACCENT_COLOR)
    title_style.spaceAfter = 30

    # Style pour les cellules du tableau
    cell_style = ParagraphStyle(
        'CellStyle',
        parent=styles['Normal'],
        fontSize=FONT_SIZE["body"],
        alignment=1,  # 1 = CENTER
        leading=12,
        spaceBefore=6,
        spaceAfter=6,
        wordWrap='CJK'  # Meilleur support pour le retour à la ligne
    )

    # Style pour l'en-tête
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=cell_style,
        fontSize=FONT_SIZE["header"],
        textColor=colors.white,
        spaceBefore=12,
        spaceAfter=12
    )
    
    # Ajouter le titre
    title = Paragraph(TITLE, title_style)
    elements.append(title)
    
    # Lire les données du CSV
    data = []
    with open(CSV_INPUT, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row_index, row in enumerate(reader):
            # Convertir chaque cellule en Paragraph
            formatted_row = []
            for cell in row:
                if row_index == 0:  # Première ligne (en-têtes)
                    formatted_row.append(Paragraph(cell, header_style))
                else:
                    formatted_row.append(Paragraph(cell, cell_style))
            data.append(formatted_row)
    
    # Créer le tableau avec les largeurs définies
    table = Table(data, colWidths=COLUMN_WIDTHS)
    
    # Style du tableau
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(ACCENT_COLOR)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ])
    
    # Appliquer le style au tableau
    table.setStyle(style)
    
    # Ajouter le tableau au document
    elements.append(table)
    
    try:
        # Générer le PDF
        doc.build(elements)
        print(f"Le fichier PDF a été créé avec succès: {PDF_OUTPUT}")
    except Exception as e:
        print(f"Erreur lors de la création du PDF: {e}")

if __name__ == "__main__":
    create_pdf() 