#!/usr/bin/env python3
import os
import shutil

# Base path for Downloads folder
ruta = "/home/USERNAME/Downloads/"

# Define folder types and their corresponding extensions
extensiones = {
    ".mp4": "07-Videos",
    ".avi": "07-Videos",
    ".mkv": "07-Videos",
    ".mov": "07-Videos",
    ".jpg": "06-Imagenes",
    ".jpeg": "06-Imagenes",
    ".png": "06-Imagenes",
    ".gif": "06-Imagenes",
    ".bmp": "06-Imagenes",
    ".docx": "04-Word",
    ".doc": "04-Word",
    ".xlsx": "05-Excel",
    ".xls": "05-Excel",
    ".txt": "01-txt",
    ".zip": "00-Zip",
    ".rar": "00-Zip",
    ".7z": "00-Zip",
    ".pdf": "02-PDFs",
    ".sql": "10-SQL",
    ".js": "11-JavaScript",
    ".py": "09-Python",
    ".ppt": "03-PowerPoint",
    ".pptx": "03-PowerPoint",
    ".mp3": "08-Audio",
    ".wav": "08-Audio",
    ".flac": "08-Audio"
}

def create_folders():
    """Create necessary folders if they don't exist"""
    folders = set(extensiones.values())

    for folder in folders:
        folder_path = os.path.join(ruta, folder)
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
                print(f"Created folder: {folder}")
            except OSError as e:
                print(f"Error creating folder {folder}: {e}")

def organize_files():
    """Move files to their corresponding folders based on extension"""
    if not os.path.exists(ruta):
        print(f"Downloads folder not found: {ruta}")
        return

    moved_count = 0

    try:
        for archivo in os.listdir(ruta):
            archivo_path = os.path.join(ruta, archivo)

            # Skip if it's a directory
            if os.path.isdir(archivo_path):
                continue

            # Get file extension
            nombre, ext = os.path.splitext(archivo)
            ext = ext.lower()

            # Check if extension is in our mapping
            if ext in extensiones:
                destino_folder = extensiones[ext]
                destino_path = os.path.join(ruta, destino_folder, archivo)

                try:
                    # Check if destination file already exists
                    if os.path.exists(destino_path):
                        print(f"File already exists: {destino_path}")
                        continue

                    shutil.move(archivo_path, destino_path)
                    print(f"Moved: {archivo} -> {destino_folder}/")
                    moved_count += 1

                except Exception as e:
                    print(f"Error moving {archivo}: {e}")
            else:
                print(f"Unknown extension: {ext} for file {archivo}")

    except Exception as e:
        print(f"Error accessing Downloads folder: {e}")

    print(f"Total files moved: {moved_count}")

def main():
    """Main function to organize downloads"""
    print("Starting Downloads organizer...")
    print(f"Target directory: {ruta}")

    # Create folders first
    create_folders()

    # Then organize files
    organize_files()

    print("Organization complete!")

if __name__ == "__main__":
    main()
