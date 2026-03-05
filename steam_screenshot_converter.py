import math
import os
import re
import sys
import tkinter
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, simpledialog

from PIL import Image

DPI = (96, 96)
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}

TARGETS_16_9 = [
    (3840, 2160),
    (2560, 1440),
    (1920, 1080),
    (1280, 720),
]

FILENAME_DATE_RE = re.compile(
    r"(\d{4})-(\d{2})-(\d{2})\s*(\d{2})(\d{2})(\d{2})"
)

def get_timestamp(path: Path) -> datetime:
    stat = path.stat()
    try:
        return datetime.fromtimestamp(stat.st_birthtime)
    except AttributeError:
        pass
    
    m = FILENAME_DATE_RE.search(path.stem)
    if m:
        y, mo, d, h, mi, s = map(int, m.groups())
        return datetime(y, mo, d, h, mi, s)
        
    return datetime.fromtimestamp(stat.st_mtime)

def choose_target_size(w: int, h: int):
    diag = math.sqrt(w * w + h * h)
    def dist(t):
        return abs(math.sqrt(t[0]**2 + t[1]**2) - diag)
    return min(TARGETS_16_9, key=dist)

def convert_one(path: Path, out_dir: Path):
    """Returns True if success, False if error."""
    try:
        if not path.exists() or path.suffix.lower() not in IMAGE_EXTS:
            return False

        timestamp = get_timestamp(path)
        base_name = timestamp.strftime('%Y%m%d%H%M%S')
        
        counter = 1
        out_path = out_dir / f"{base_name}_{counter}.jpg"
        
        while out_path.exists():
            counter += 1
            out_path = out_dir / f"{base_name}_{counter}.jpg"

        img = Image.open(path).convert("RGB")
        target_w, target_h = choose_target_size(img.width, img.height)
        
        ir = img.width / img.height
        tr = target_w / target_h
        
        if ir > tr:
            w = target_w
            h = int(w / ir)
        else:
            h = target_h
            w = int(h * ir)
            
        img = img.resize((w, h), Image.LANCZOS)
        canvas = Image.new("RGB", (target_w, target_h), (0, 0, 0))
        canvas.paste(img, ((target_w - w) // 2, (target_h - h) // 2))
        
        canvas.save(out_path, "JPEG", quality=95, subsampling=0, dpi=DPI)
        return True
    except Exception as e:
        print(f"Error processing {path.name}: {e}")
        return False

def get_steam_userdata():
    pf = os.environ.get('ProgramFiles(x86)', r'C:\Program Files (x86)')
    steam_userdata = Path(pf) / "Steam" / "userdata"
    
    if not steam_userdata.exists():
        raise FileNotFoundError("Steam userdata folder not found.")
        
    user_dirs = [d for d in steam_userdata.iterdir() if d.is_dir() and d.name.isdigit()]
    if not user_dirs:
        raise FileNotFoundError("No Steam user folders found.")
        
    return max(user_dirs, key=lambda d: d.stat().st_mtime)

def get_output_folder(appid: str):
    user_folder = get_steam_userdata()
    remote_folder = user_folder / "760" / "remote" / appid / "screenshots"
    remote_folder.mkdir(parents=True, exist_ok=True)
    return remote_folder

def main():
    root = tkinter.Tk()
    root.withdraw()
    args = sys.argv[1:]

    appid = simpledialog.askstring("Steam Screenshot Converter", "Enter Steam AppID:")
    if not appid:
        return

    try:
        output_dir = get_output_folder(appid)
    except Exception as e:
        messagebox.showerror("Critical Error", f"Could not access Steam folder:\n{e}")
        return

    if not args:
        messagebox.showinfo("Info", "Please drag and drop images onto the program icon to convert them.")
        return

    success_count = 0
    fail_count = 0

    for a in args:
        if convert_one(Path(a), output_dir):
            success_count += 1
        else:
            fail_count += 1

    summary_msg = f"Processing complete!\n\nSuccessful: {success_count}"
    if fail_count > 0:
        summary_msg += f"\nErrors: {fail_count}"
    
    summary_msg += f"\n\nFiles saved to:\n{output_dir}"
    
    messagebox.showinfo("Conversion Status", summary_msg)

if __name__ == "__main__":
    main()