#!/usr/bin/env python3

# =============================================================================
# CONFIGURATION
# =============================================================================

# Chemins des dossiers (relatifs au dossier SCRIPTS)
VIDEO_DIR = "../VIDEO"  # Dossier contenant les fichiers vidéo MXF
CSV_OUTPUT = "../derush_sheet.csv"  # Fichier CSV de sortie

# Configuration de la barre de progression
PROGRESS_BAR_LENGTH = 50  # Longueur de la barre de progression

# Configuration des timecodes
FPS = 25

# =============================================================================
# IMPORTS
# =============================================================================

import os
import subprocess
import csv
from datetime import timedelta
import sys

# =============================================================================
# FONCTIONS
# =============================================================================

def check_ffprobe():
    """Vérifie si ffprobe est installé."""
    try:
        subprocess.run(['ffprobe', '-version'], capture_output=True, check=True)
        print("ffprobe est correctement installé.")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("ffprobe n'est pas installé. Veuillez l'installer avec la commande appropriée pour votre système d'exploitation.")
        print("Windows: https://ffmpeg.org/download.html")
        print("macOS: brew install ffmpeg")
        print("Linux: sudo apt-get install ffmpeg")
        exit(1)

def tc_to_frames(tc):
    """Convertit un timecode en nombre total de frames."""
    hh, mm, ss, ff = map(int, tc.split(':'))
    return (hh * 3600 + mm * 60 + ss) * FPS + ff

def frames_to_tc(total_frames):
    """Convertit le nombre total de frames en timecode."""
    frames = total_frames % FPS
    total_seconds = total_frames // FPS
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{frames:02d}"

def get_video_info(file_path):
    """Obtient les informations de timecode et de durée d'un fichier vidéo."""
    try:
        # Obtenir le timecode
        tc_in = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format_tags=timecode',
             '-of', 'default=noprint_wrappers=1:nokey=1', file_path],
            capture_output=True, text=True, check=True
        ).stdout.strip()

        # Obtenir la durée
        duration = float(subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', file_path],
            capture_output=True, text=True, check=True
        ).stdout.strip())

        # Calculer le timecode out
        if tc_in:
            tc_in_frames = tc_to_frames(tc_in)
            duration_frames = round(duration * FPS)
            tc_out_frames = tc_in_frames + duration_frames - 1
            tc_out = frames_to_tc(tc_out_frames)
        else:
            tc_in = "00:00:00:00"
            tc_out = "00:00:00:00"

        # Formater la durée
        duration_td = timedelta(seconds=round(duration))
        hours = duration_td.seconds // 3600
        minutes = (duration_td.seconds % 3600) // 60
        seconds = duration_td.seconds % 60
        formatted_duration = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        return tc_in, tc_out, formatted_duration

    except subprocess.SubprocessError as e:
        print(f"\nErreur lors de l'analyse du fichier {file_path}: {e}")
        return "00:00:00:00", "00:00:00:00", "00:00:00"

def print_progress(current, total, filename):
    """Affiche une barre de progression."""
    filled_length = int(round(PROGRESS_BAR_LENGTH * current / float(total)))
    percents = round(100.0 * current / float(total), 1)
    bar = '=' * filled_length + '-' * (PROGRESS_BAR_LENGTH - filled_length)
    sys.stdout.write(f'\r[{bar}] {percents}% - {filename}')
    sys.stdout.flush()

def main():
    # Vérifier ffprobe
    check_ffprobe()

    # Obtenir les chemins absolus
    script_dir = os.path.dirname(os.path.abspath(__file__))
    video_dir = os.path.join(script_dir, VIDEO_DIR)
    csv_path = os.path.join(script_dir, CSV_OUTPUT)

    print(f"Recherche des fichiers dans: {video_dir}")
    print(f"Fichier CSV de sortie: {csv_path}")

    # Vérifier si le répertoire VIDEO existe
    if not os.path.exists(video_dir):
        print(f"Erreur: Le répertoire VIDEO n'existe pas: {video_dir}")
        exit(1)

    # Créer le fichier CSV avec l'en-tête
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['FICHIER', 'TC IN', 'TC OUT', 'DURÉE', 'CONTENU IMAGE', 'CONTENU SON', 'OBSERVATIONS', 'CHOIX'])
        csvfile.flush()

        # Parcourir tous les fichiers .MXF dans le répertoire VIDEO
        mxf_files = [f for f in os.listdir(video_dir) if f.endswith('.MXF')]
        total_files = len(mxf_files)
        print(f"Nombre de fichiers MXF trouvés: {total_files}")

        for index, filename in enumerate(mxf_files, 1):
            file_path = os.path.join(video_dir, filename)
            if os.path.isfile(file_path):
                print_progress(index, total_files, filename)
                tc_in, tc_out, duration = get_video_info(file_path)
                writer.writerow([filename, tc_in, tc_out, duration, '', '', ''])
                csvfile.flush()

    print("\n\nLe fichier derush_sheet.csv a été créé avec succès.")

if __name__ == '__main__':
    main()
