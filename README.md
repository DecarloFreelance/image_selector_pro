# Image Selector – Mark & Delete GUI

A Python GUI tool to browse random images from a directory, mark unwanted ones, and optionally delete them. Built with `tkinter` and `Pillow`.

## Features

- **Select any directory** via text entry or file browser.
- **Choose sample size** (ALL, 10, 100, 500, 1000 images).
- **Mark images for deletion** with one click – automatically advances to the next image.
- **Unmark** by clicking the same button again (stays on current image).
- **Navigate** with Previous / Next buttons.
- **Final actions**:
  - Delete all marked images permanently.
  - Save list of marked image paths to a text file without deleting.
- Count of marked images shown at all times.

## Requirements

- Python 3.6+
- `Pillow` (Python Imaging Library)
- `tkinter` (usually included with Python, but may need separate install on Linux)

## Installation

### Option 1: Virtual Environment (recommended)

Avoids system package conflicts on modern Linux distributions (Debian/Ubuntu 23.04+).

```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Pillow
pip install Pillow
```

### Option 2: System Package (no pip conflicts)

Install Pillow via your system package manager – pip is not needed.

```bash
# Debian/Ubuntu
sudo apt install python3-pil python3-pil.imagetk
```
```bash
# Fedora
sudo dnf install python3-pillow python3-tkinter
```
```bash
# Arch Linux
sudo pacman -S python-pillow tk
```

Additional Tkinter (if missing)
On some Linux installations, tkinter is not bundled. Install it:

```bash
sudo apt install python3-tk   # Debian/Ubuntu
```

### Usage
Run the script:
```bash
python3 image_selector_pro.py
```
### Follow the dialogs:

Choose a directory – type the path or click "Browse".

Select sample size – how many random images to load (ALL may be slow for huge folders).

Review images:

Mark & Next → marks current image and moves to next.

Unmark → click again on the same image to remove from deletion list (stays on image).

Previous / Next → navigate without marking.

At the end (or by clicking "Delete Marked & Exit") you can:

Delete all marked images (permanent).

Save list of marked paths to marked_for_deletion.txt.

Exit without action if you only want to browse.

Notes
Deletions are permanent (no recycle bin). Use the "Save Marked List" option if unsure.

For folders with tens of thousands of images, sampling 100–1000 is recommended for performance.

Supported image formats: .jpg, .jpeg, .png, .gif, .bmp, .tiff.

License
MIT
