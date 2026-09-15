1| # downloadsOrganizer
2| 
3| A simple Python script that organizes your Downloads folder by moving files into subfolders based on their extension — keeps things tidy without any manual sorting.
4| 
5| The main script is `organizer.py`.
6| 
7| ## What it does
8| 
9| - Scans your Downloads folder (or any folder you point it to)
10| - Creates category subfolders (Images, Videos, PDFs, Word, Excel, PowerPoint, Audio, Python, JavaScript, SQL, Zip, txt) if they don't already exist
11| - Moves each file into the folder matching its extension
12| - Renames files automatically if a file with the same name already exists in the destination, so nothing gets overwritten
13| - Shows a popup window when it's done, with a summary of how many files were moved and skipped
14| 
15| ## Requirements
16| 
17| - Python 3.7+
18| - `tkinter` (used only for the completion popup)
19|   - Included by default on Windows and macOS Python installs
20|   - On Linux, if it's missing, install it with:
21|     ```bash
22|     sudo apt install python3-tk        # Debian/Ubuntu
23|     sudo dnf install python3-tkinter   # Fedora
24|     sudo pacman -S tk                  # Arch/Manjaro
25|     ```
26|   - If `tkinter` isn't available, the script still runs fine — it just skips the popup and prints a summary to the terminal instead.
27| 
28| ## Usage
29| 
30| Clone the repo and run the script directly:
31| 
32| ```bash
33| git clone https://github.com/Josavil/downloadsOrganizer.git
34| cd downloadsOrganizer
35| python3 organizer.py
36| ```
37| 
38| By default it organizes `~/Downloads`. You can point it at a different folder:
39| 
40| ```bash
41| python3 organizer.py --path /path/to/folder
42| ```
43| 
44| ### Options
45| 
46| | Flag          | Description                                                        |
47| |---------------|----------------------------------------------------------------------|
48| | `--path PATH` | Folder to organize (default: your Downloads folder)                |
49| | `--dry-run`   | Preview what would happen without actually moving any files        |
50| | `--quiet`     | Only print moves and errors, suppress "skipped" messages           |
51| | `--no-notify` | Don't show the popup window when the task finishes                 |
52| 
53| **Tip:** run with `--dry-run` first to see what the script *would* do before letting it touch your real files.
54| 
55| ```bash
56| python3 organizer.py --dry-run
57| ```
58| 
59| ## File type mapping
60| 
61| | Folder          | Extensions                          |
62| |------------------|--------------------------------------|
63| | `00-Zip`         | `.zip` `.rar` `.7z`                  |
64| | `01-txt`         | `.txt`                               |
65| | `02-PDFs`        | `.pdf`                               |
66| | `03-PowerPoint`  | `.ppt` `.pptx`                       |
67| | `04-Word`        | `.doc` `.docx`                       |
68| | `05-Excel`       | `.xls` `.xlsx`                       |
69| | `06-Imagenes`    | `.jpg` `.jpeg` `.png` `.gif` `.bmp`  |
70| | `07-Videos`      | `.mp4` `.avi` `.mkv` `.mov`          |
71| | `08-Audio`       | `.mp3` `.wav` `.flac`                |
72| | `09-Python`      | `.py`                                |
73| | `10-SQL`         | `.sql`                                |
74| | `11-JavaScript`  | `.js`                                |
75| 
76| Files with an extension not listed here are left alone and reported as "skipped." Hidden files (dotfiles like `.bashrc`) are also ignored.
77| 
78| ## Notes
79| 
80| - The script only moves files sitting directly in the target folder — it doesn't touch files inside subfolders (including the category folders it creates).
81| - Running it multiple times is safe: existing category folders won't be recreated, and naming collisions are handled by appending `(1)`, `(2)`, etc. to the new file instead of overwriting.
82| - Multi-part extensions (e.g. `.tar.gz`, `.tar.bz2`) are treated using the final suffix only (so `file.tar.gz` is seen as `.gz`).
83|   If you want `.tar.gz` files grouped with other archives, either add an entry for `.gz` mapping to `00-Zip` in `organizer.py` or modify the script to detect these endings explicitly.
84| 
85| ## License
86| 
87| MIT 
