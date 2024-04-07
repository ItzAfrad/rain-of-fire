import sys
from cx_Freeze import setup, Executable

# Dependencies
build_exe_options = {
    "packages": ["pygame"],
    "include_files": ["player.png", "enemy.png", "bg.png", "bg_music.mp3", "high_score.txt"]
}

# Executable
executables = [
    Executable("rain of fire.py", base=None)
]

# Setup
setup(
    name="Rain of Fire",  # Change this to your game's name
    version="1.0",  # Change this to your game's version
    description="A simple game using pygame",
    options={"build_exe": build_exe_options},
    executables=executables
)
