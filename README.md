# Outils de Dérushage

Ce projet contient un ensemble d'outils pour faciliter le processus de dérushage de fichiers vidéo MXF. Il permet de :
1. Générer automatiquement une feuille de dérushage au format CSV
2. Convertir cette feuille en PDF pour une meilleure lisibilité

## Prérequis

### Installation de FFmpeg

Le script nécessite FFmpeg (et plus particulièrement ffprobe) pour fonctionner. Voici comment l'installer selon votre système d'exploitation :

#### Windows
1. Téléchargez FFmpeg depuis le site officiel : https://ffmpeg.org/download.html
2. Choisissez la version "Windows builds from gyan.dev"
3. Téléchargez la version "essentials"
4. Extrayez l'archive
5. Ajoutez le chemin du dossier `bin` à votre variable d'environnement PATH

#### macOS
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

### Installation de Python

Le script nécessite Python 3.6 ou supérieur.

#### Windows
1. Téléchargez Python depuis https://www.python.org/downloads/
2. Lors de l'installation, cochez "Add Python to PATH"

#### macOS
```bash
brew install python3
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3
```

### Installation des dépendances Python

```bash
pip install reportlab
```

## Structure des dossiers

Le projet s'attend à trouver les fichiers dans la structure suivante :
```
votre_projet/
├── SCRIPTS/
│   ├── derush_sheet.py    # Script de génération du CSV
│   ├── csv_to_pdf.py      # Script de conversion en PDF
│   └── README.md
├── VIDEO/
│   ├── fichier1.MXF
│   ├── fichier2.MXF
│   └── ...
├── derush_sheet.csv       # Généré par derush_sheet.py
└── derush_sheet.pdf       # Généré par csv_to_pdf.py
```

## Processus de dérushage

### 1. Génération de la feuille de dérushage (CSV)

Le script `derush_sheet.py` analyse tous les fichiers MXF du dossier VIDEO et génère un fichier CSV contenant :
- Les noms des fichiers
- Les timecodes de début et de fin
- La durée de chaque fichier
- Des colonnes vides pour le contenu image, le contenu son, les observations et le choix

#### Configuration
Vous pouvez modifier les paramètres suivants au début du script :
```python
# Chemins des dossiers
VIDEO_DIR = "../VIDEO"  # Dossier contenant les fichiers vidéo MXF
CSV_OUTPUT = "../derush_sheet.csv"  # Fichier CSV de sortie

# Configuration des timecodes
FPS = 25  # Images par seconde
```

#### Utilisation
```bash
cd SCRIPTS
python derush_sheet.py
```

### 2. Conversion en PDF

Le script `csv_to_pdf.py` convertit le fichier CSV en un PDF formaté et facile à lire.

#### Configuration
Vous pouvez personnaliser l'apparence du PDF en modifiant ces paramètres :
```python
# Chemins des fichiers
CSV_INPUT = "../derush_sheet.csv"
PDF_OUTPUT = "../derush_sheet.pdf"

# Configuration du PDF
PAGE_SIZE = "A4"
ORIENTATION = "landscape"
MARGINS = {
    "left": 100,
    "right": 100,
    "top": 50,
    "bottom": 50
}

# Styles
TITLE = "Feuille de dérushage"
ACCENT_COLOR = "#B45F06"
FONT_SIZE = {
    "title": 24,
    "header": 10,
    "body": 8
}
```

#### Utilisation
```bash
cd SCRIPTS
python csv_to_pdf.py
```

## Workflow complet

1. Placez vos fichiers MXF dans le dossier VIDEO
2. Exécutez `derush_sheet.py` pour générer le CSV
3. Remplissez manuellement les colonnes du CSV :
   - CONTENU IMAGE : Description de ce que l'on voit
   - CONTENU SON : Description de ce que l'on entend
   - OBSERVATIONS : Notes supplémentaires
   - CHOIX : "Validé" ou "Rejeté"
4. Exécutez `csv_to_pdf.py` pour générer le PDF final

## Dépannage

### Le script ne trouve pas ffprobe
- Vérifiez que FFmpeg est correctement installé
- Sur Windows, vérifiez que le dossier bin de FFmpeg est dans votre PATH
- Essayez de redémarrer votre terminal

### Le script ne trouve pas les fichiers vidéo
- Vérifiez que la structure des dossiers est correcte
- Vérifiez que les fichiers sont bien au format .MXF
- Vérifiez les permissions des dossiers

### Le script plante
- Vérifiez que vous avez les permissions d'écriture dans le dossier parent
- Vérifiez que les fichiers MXF ne sont pas corrompus
- Vérifiez que vous avez assez d'espace disque

### Problèmes avec le PDF
- Vérifiez que reportlab est correctement installé
- Vérifiez que vous avez les permissions d'écriture pour le fichier PDF
- Ajustez les marges ou la taille des polices si le contenu ne tient pas sur la page 