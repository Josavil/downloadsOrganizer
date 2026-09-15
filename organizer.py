#!/usr/bin/env python3
"""
downloads_organizer.py

Organizes files in a Downloads folder into subfolders based on file extension.
"""

import os
import shutil
import argparse
from pathlib import Path

try:
    import tkinter as tk
    from tkinter import messagebox
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

# Default path for Downloads folder (works cross-platform, no hardcoded username)
DEFAULT_RUTA = Path.home() / "Downloads"

# Define folder types and their corresponding extensions
EXTENSIONES = {
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
    ".flac": "08-Audio",
}


def create_folders(ruta: Path, dry_run: bool = False):
    """Create necessary folders if they don't exist."""
    folders = set(EXTENSIONES.values())

    for folder in folders:
        folder_path = ruta / folder
        if not folder_path.exists():
            if dry_run:
                print(f"[DRY RUN] Would create folder: {folder}")
                continue
            try:
                folder_path.mkdir(parents=True, exist_ok=True)
                print(f"Created folder: {folder}")
            except OSError as e:
                print(f"Error creating folder {folder}: {e}")


def unique_destination(destino_path: Path) -> Path:
    """
    If destino_path already exists, append a (1), (2), etc. suffix
    to the filename until a free path is found.
    """
    if not destino_path.exists():
        return destino_path

    stem = destino_path.stem
    suffix = destino_path.suffix
    parent = destino_path.parent
    counter = 1

    while True:
        candidate = parent / f"{stem} ({counter}){suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def organize_files(ruta: Path, dry_run: bool = False, verbose: bool = True):
    """Move files to their corresponding folders based on extension."""
    if not ruta.exists():
        print(f"Downloads folder not found: {ruta}")
        return

    moved_count = 0
    skipped_count = 0

    try:
        for archivo_path in ruta.iterdir():
            archivo = archivo_path.name

            # Skip directories (including the category folders we just made)
            if archivo_path.is_dir():
                continue

            # Skip hidden/dotfiles (e.g. .bashrc, .DS_Store) to avoid
            # splitext treating the whole name as an "extension"
            if archivo.startswith("."):
                continue

            ext = archivo_path.suffix.lower()

            if not ext:
                if verbose:
                    print(f"Skipped (no extension): {archivo}")
                skipped_count += 1
                continue

            if ext not in EXTENSIONES:
                if verbose:
                    print(f"Skipped (unmapped extension {ext}): {archivo}")
                skipped_count += 1
                continue

            destino_folder = EXTENSIONES[ext]
            destino_path = unique_destination(ruta / destino_folder / archivo)

            if dry_run:
                print(f"[DRY RUN] Would move: {archivo} -> {destino_folder}/{destino_path.name}")
                moved_count += 1
                continue

            try:
                shutil.move(str(archivo_path), str(destino_path))
                print(f"Moved: {archivo} -> {destino_folder}/{destino_path.name}")
                moved_count += 1
            except Exception as e:
                print(f"Error moving {archivo}: {e}")

    except Exception as e:
        print(f"Error accessing Downloads folder: {e}")

    print(f"\nTotal files moved: {moved_count}")
    print(f"Total files skipped: {skipped_count}")

    return moved_count, skipped_count


def show_completion_popup(moved_count: int, skipped_count: int, dry_run: bool):
    """Show a small window announcing that the task has finished."""
    if not TKINTER_AVAILABLE:
        print("(tkinter not available, skipping popup notification)")
        return

    title = "Downloads Organizer"
    mode = " (dry run)" if dry_run else ""
    message = (
        f"Organization complete{mode}!\n\n"
        f"Files moved: {moved_count}\n"
        f"Files skipped: {skipped_count}"
    )

    try:
        root = tk.Tk()
        root.withdraw()  # hide the empty root window, only show the messagebox
        root.attributes("-topmost", True)
        messagebox.showinfo(title, message, parent=root)
        root.destroy()
    except tk.TclError as e:
        # Happens if there's no display available (e.g. running over SSH
        # without X forwarding, or in a cron job with no GUI session)
        print(f"(couldn't show popup, no display available: {e})")


def parse_args():
    parser = argparse.ArgumentParser(description="Organize a Downloads folder by file extension.")
    parser.add_argument(
        "--path",
        type=str,
        default=str(DEFAULT_RUTA),
        help=f"Path to the folder to organize (default: {DEFAULT_RUTA})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would happen without moving any files.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only print moves/errors, suppress skip messages.",
    )
    parser.add_argument(
        "--no-notify",
        action="store_true",
        help="Don't show a popup window when the task finishes.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    ruta = Path(args.path).expanduser()

    print("Starting Downloads organizer...")
    print(f"Target directory: {ruta}")
    if args.dry_run:
        print("Mode: DRY RUN (no files will actually be moved)\n")

    create_folders(ruta, dry_run=args.dry_run)
    moved_count, skipped_count = organize_files(ruta, dry_run=args.dry_run, verbose=not args.quiet)

    print("Organization complete!")

    if not args.no_notify:
        show_completion_popup(moved_count, skipped_count, args.dry_run)


if __name__ == "__main__":
    main()
