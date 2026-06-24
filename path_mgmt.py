import os


font_path = "fonts/Pixeltype.ttf"
pacman_path = "assets/pacman.png"
blue_path = "assets/blueG.png"
orange_path = "assets/orangeG.png"
pink_path = "assets/pinkG.png"
red_path = "assets/redG.png"
vul_path = "assets/vulnerable.png"

if not os.path.exists(font_path):
    font_path = "_internal/fonts/Pixeltype.ttf"
if not os.path.exists(pacman_path):
    pacman_path = "_internal/assets/pacman.png"
if not os.path.exists(blue_path):
    blue_path = "_internal/assets/blueG.png"
if not os.path.exists(orange_path):
    orange_path = "_internal/assets/orangeG.png"
if not os.path.exists(pink_path):
    pink_path = "_internal/assets/pinkG.png"
if not os.path.exists(red_path):
    red_path = "_internal/assets/redG.png"
if not os.path.exists(vul_path):
    vul_path = "_internal/assets/vulnerable.png"
