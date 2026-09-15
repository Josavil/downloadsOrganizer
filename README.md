# downloadsOrganizer

A simple Python script that organizes your Downloads folder by moving files into subfolders based on their extension — keeps things tidy without any manual sorting.

The main script is `organizer.py`.

## What it does

- Scans your Downloads folder (or any folder you point it to)
- Creates category subfolders (Images, Videos, PDFs, Word, Excel, PowerPoint, Audio, Python, JavaScript, SQL, Zip, txt) if they don't already exist
- Moves each file into the folder matching its extension
- Renames files automatically if a file with the same name already exists in the destination, so nothing gets overwritten
- Shows a popup window when it's done, with a summary of how many files were moved and skipped

## Requirements

- Python 3.7+
- `tkinter` (used only for the completion popup)
  - Included by default on Windows and macOS Python installs
  - On Linux, if it's missing, install it with:
    ```bash
    sudo apt install python3-tk        # Debian/Ubuntu
    sudo dnf install python3-tkinter   # Fedora
    sudo pacman -S tk                  # Arch/Manjaro
    ```
  - If `tkinter` isn't available, the script still runs fine — it just skips the popup and prints a summary to the terminal instead.

## Usage

Clone the repo and run the script directly:

```bash
git clone https://github.com/Josavil/downloadsOrganizer.git
cd downloadsOrganizer
python3 organizer.py
```

By default it organizes `~/Downloads`. You can point it at a different folder:

```bash
python3 organizer.py --path /path/to/folder
```

### Options

| Flag          | Description                                                        |
|---------------|----------------------------------------------------------------------|
| `--path PATH` | Folder to organize (default: your Downloads folder)                |
| `--dry-run`   | Preview what would happen without actually moving any files        |
| `--quiet`     | Only print moves and errors, suppress "skipped" messages           |
| `--no-notify` | Don't show the popup window when the task finishes                 |

**Tip:** run with `--dry-run` first to see what the script *would* do before letting it touch your real files.

```bash
python3 organizer.py --dry-run
```

## File type mapping

| Folder          | Extensions                          |
|------------------|--------------------------------------|
| `00-Zip`         | `.zip` `.rar` `.7z`                  |
| `01-txt`         | `.txt`                               |
| `02-PDFs`        | `.pdf`                               |
| `03-PowerPoint`  | `.ppt` `.pptx`                       |
| `04-Word`        | `.doc` `.docx`                       |
| `05-Excel`       | `.xls` `.xlsx`                       |
| `06-Imagenes`    | `.jpg` `.jpeg` `.png` `.gif` `.bmp`  |
| `07-Videos`      | `.mp4` `.avi` `.mkv` `.mov`          |
| `08-Audio`       | `.mp3` `.wav` `.flac`                |
| `09-Python`      | `.py`                                |
| `10-SQL`         | `.sql`                               |
| `11-JavaScript`  | `.js`                                |

Files with an extension not listed here are left alone and reported as "skipped." Hidden files (dotfiles like `.bashrc`) are also ignored.

## Notes

- The script only moves files sitting directly in the target folder — it doesn't touch files inside subfolders (including the category folders it creates).
- Running it multiple times is safe: existing category folders won't be recreated, and naming collisions are handled by appending `(1)`, `(2)`, etc. to the new file instead of overwriting.

## License

MIT 
