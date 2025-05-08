# Derush Sheet Generator

Ce script Python permet de générer automatiquement une feuille de dérushage à partir de fichiers vidéo MXF. Il extrait les timecodes et la durée de chaque fichier et crée un fichier CSV prêt à être utilisé.

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

## Structure des dossiers

Le script s'attend à trouver les fichiers dans la structure suivante :
```
votre_projet/
├── SCRIPTS/
│   ├── derush_sheet.py
│   └── README.md
├── VIDEO/
│   ├── fichier1.MXF
│   ├── fichier2.MXF
│   └── ...
└── derush_sheet.csv (sera créé ici)
```

## Configuration

Vous pouvez modifier les paramètres suivants au début du script `derush_sheet.py` :

```python
# Chemins des dossiers (relatifs au dossier SCRIPTS)
VIDEO_DIR = "../VIDEO"  # Dossier contenant les fichiers vidéo MXF
CSV_OUTPUT = "../derush_sheet.csv"  # Fichier CSV de sortie

# Configuration de la barre de progression
PROGRESS_BAR_LENGTH = 50  # Longueur de la barre de progression

# Configuration des timecodes
FPS = 25
```

## Utilisation

1. Ouvrez un terminal
2. Naviguez vers le dossier SCRIPTS :
   ```bash
   cd chemin/vers/votre_projet/SCRIPTS
   ```
3. Rendez le script exécutable (Unix/macOS) :
   ```bash
   chmod +x derush_sheet.py
   ```
4. Exécutez le script :
   ```bash
   # Sur Unix/macOS
   ./derush_sheet.py
   
   # Sur Windows
   python derush_sheet.py
   ```

## Sortie

Le script génère un fichier CSV avec les colonnes suivantes :
- FICHIER : Nom du fichier MXF
- TC IN : Timecode de début
- TC OUT : Timecode de fin
- DURÉE : Durée du fichier
- CONTENU IMAGE : À remplir manuellement
- CONTENU SON : À remplir manuellement
- OBSERVATIONS : À remplir manuellement
- CHOIX : À remplir manuellement

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