#!/usr/bin/env python3
"""
downloads_organizer.py

Organizes files in a Downloads folder into subfolders based on file extension.
"""

import os
import shutil
import argparse
from pathlib import Path
from collections import defaultdict

try:
    import tkinter as tk
    from tkinter import messagebox
    from tkinter import ttk
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
        return {}, 0

    moved_count = 0
    skipped_count = 0
    folder_stats = defaultdict(int)  # Track files per folder

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
                folder_stats[destino_folder] += 1
                moved_count += 1
                continue

            try:
                shutil.move(str(archivo_path), str(destino_path))
                print(f"Moved: {archivo} -> {destino_folder}/{destino_path.name}")
                folder_stats[destino_folder] += 1
                moved_count += 1
            except Exception as e:
                print(f"Error moving {archivo}: {e}")

    except Exception as e:
        print(f"Error accessing Downloads folder: {e}")

    print(f"\nTotal files moved: {moved_count}")
    print(f"Total files skipped: {skipped_count}")

    return dict(folder_stats), skipped_count


def show_completion_popup(moved_count, skipped_count, dry_run, folder_stats):
    try:
        root = tk.Tk()
        title_suffix = " (Dry Run)" if dry_run else ""
        root.title(f"Downloads Organizer{title_suffix}")
        root.geometry("450x350")
        root.minsize(400, 300)

        # Apply a modern cross-platform theme ('clam')
        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")

        # Custom styling for a clean, flat look
        style.configure(".", font=("Segoe UI", 10))
        style.configure("Heading.TLabel", font=("Segoe UI", 12, "bold"))
        style.configure("Treeview", rowheight=26, fieldbackground="#ffffff", background="#ffffff")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#f1f3f5")
        style.configure("TButton", padding=6)

        # Main container with comfortable padding
        main_frame = ttk.Frame(root, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Summary header label
        status_text = f"Successfully organized {moved_count} file(s)."
        if dry_run:
            status_text = f"[DRY RUN] Would organize {moved_count} file(s)."
        
        header_label = ttk.Label(main_frame, text=status_text, style="Heading.TLabel")
        header_label.pack(anchor=tk.W, pady=(0, 10))

        # Treeview with Scrollbar inside a clean container
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        tree = ttk.Treeview(tree_frame, columns=("count",), show="headings", selectmode="none")
        tree_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.config(yscrollcommand=tree_scroll.set)

        # Configure columns and headings
        tree.heading("#1", text="Folder", anchor=tk.W)
        tree.heading("count", text="Files Moved", anchor=tk.CENTER)
        
        # Give proportions to columns (Treeview columns use identifiers)
        tree.column("#1", width=280, anchor=tk.W)
        tree.column("count", width=90, anchor=tk.CENTER)

        # Add folder data to tree
        if folder_stats:
            for folder_name in sorted(folder_stats.keys()):
                count = folder_stats[folder_name]
                tree.insert("", tk.END, values=(folder_name, count))
        else:
            tree.insert("", tk.END, values=("No files moved", "—"))

        # Pack tree and scrollbar neatly
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Close button container
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        close_button = ttk.Button(button_frame, text="Close", command=root.destroy)
        close_button.pack(side=tk.RIGHT)

        root.mainloop()

    except tk.TclError as e:
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
    folder_stats, skipped_count = organize_files(ruta, dry_run=args.dry_run, verbose=not args.quiet)

    # Extract moved_count from folder_stats
    moved_count = sum(folder_stats.values())

    print("Organization complete!")

    if not args.no_notify:
        show_completion_popup(moved_count, skipped_count, args.dry_run, folder_stats)


if __name__ == "__main__":
    main()
