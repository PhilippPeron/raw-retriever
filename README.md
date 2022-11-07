# RAW Retriever

RAW Retriever finds NEF-RAW images in a directory and copies them to the JPG location via drag&drop. It is made for photographers.

My personal photography workflow consists of downloading the JPGs and sorting them.
Afterwards I get the RAW images for my best images from the camera. That way I don't have to copy all the RAWs from the beginning.
This is better for my SSD and also faster when sorting images.\
The application helps me in copying the RAW images to the JPG directory.

## Usage:
- Run 'RAW Retriever.exe'
- A directory selection dialog pops up where you can select the directory with the RAW images
- Afterwards you just drag JPGs in the small window.
RAW Retriever tries to find the RAW-counterparts in the selected directory or a first level subdirectory and copies them to the JPG directory.

## EXE generation:
The executable 'RAW Retriever.exe' is generated from 'raw_retriever.py' using pyinstaller. \
The cmd command is: 'pyinstaller .\raw_retriever.py --onefile' \
You can install pyinstaller with pip: 'pip install pyinstaller'

## Other:
The script currently only supports NEF-RAW files.
To change the RAW-file ending to a different one (e.g. ARW or DNG), just change the global variable 'RAW_FILE_ENDING' at the beginning of the script.