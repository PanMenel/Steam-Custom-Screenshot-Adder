# Steam-Custom-Screenshot-Adder

Converts images to a format that Steam accepts as screenshots and adds them to the according folders.
Simple tool made for convenience for games that can't take screenshots on their own (like FNAF 4).

# How to use
<ol>
  <li>Check your game <strong>App ID</strong> on <strong>steamdb</strong> and copy it.</li>
  <li>Close <strong>Steam</strong>.</li>
  <li><strong>Drag and drop</strong> your screenshot or screenshots onto the program.</li>
  <li><strong>Type in or paste</strong> your App ID and the program will add your already formatted screenshots to your game folder.</li>
  <li>Open <strong>Steam</strong> and your screenshots should be there.</li>
</ol>

# Build
* Put `steam_screenshot_converter.py` and `steam.ico` in the same folder.
* You need **Pillow** and **PyInstaller** for this to work. Install them via pip:
  `pip install Pillow PyInstaller`
* Run the following command to build the executable:
  `py -m PyInstaller --noconsole --onefile --icon=steam.ico steam_screenshot_converter.py`
* After building, your executable will be in the **dist** folder.
