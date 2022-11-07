import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog
from pathlib import Path
import re
import shutil

RAW_DIRECTORY = ""
RAW_FILE_ENDING = "NEF"


class Label(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop JPGs Here \n\n')
        self.setStyleSheet("""
             QLabel{
                 border: 3px dashed #aaa
             }
         """)
        RAW_DIRECTORY = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        _ = raw_directory_to_path()
        print(f"Selected RAW directory: '{RAW_DIRECTORY}'")
        print("-----------------------")


def raw_directory_to_path():
    raw_dir_path = Path(RAW_DIRECTORY)
    if not RAW_DIRECTORY or not raw_dir_path.exists():
        print(f"Chosen directory: '{RAW_DIRECTORY}' does ont exist. Exit Program.")
        exit()
        sys.exit(app.exec_())
    return raw_dir_path


def handle_drop_files(file_list):
    raw_dir_path = raw_directory_to_path()
    file_dict = files_to_dict(file_list)
    copy_files(file_dict, raw_dir_path)


def copy_files(file_dict, raw_dir_path):
    """Go through dropped files and copy RAW equivalent from RAW directory"""
    for file_stem, file_path in file_dict.items():

        try:
            raw_file_path = get_raw_path(raw_dir_path, file_stem)
        except FileNotFoundError:
            print(f"! Could not find RAW version of {file_stem} in '{RAW_DIRECTORY}. Skipped file.'")
            continue
        dst_path = file_path.parent / raw_file_path.name
        try:
            shutil.copy(raw_file_path, dst_path)
        except Exception:  # TODO: Make exception type more precise
            # TODO: Show message box if problem and skip file
            continue
        # TODO: Make box flash green if successful


def get_raw_path(raw_dir_path, file_stem):
    """Find raw file in RAW directory and return its path"""
    # TODO: Check if file exists in RAW directory or first level subdirectory, raise FileNotFound error
    return raw_file_path


def get_dst_path(file_path, raw_file_path):
    dst_path = file_path.parent / raw_file_path.name
    return dst_path


def files_to_dict(file_list):
    file_dict = {}  # Key:file-stem Value:Path(file)
    for file in file_list:
        file_path = Path(file)
        # Check file existence
        if not file_path.exists():
            print(f"{file_path.name} does not exist and was skipped")
        file_name = file_path.name
        if not check_regex(file_name=file_name):
            print(f"Problem: '{file_name}' is not a valid jp(e)g file name. File Skipped!")
            continue
        file_dict[file_path.stem] = file_path
    return file_dict


def check_regex(file_name):
    """Check if file name has jpg ending"""
    regex = r"(?i)\w*\.(\bjpg\b|\bjpeg\b)"
    match = re.compile(regex).match(file_name)
    return bool(match)


class RAWRetriever(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setAcceptDrops(True)
        self.resize(300, 100)
        main_layout = QVBoxLayout()
        self.photoViewer = Label()
        main_layout.addWidget(self.photoViewer)

        self.setLayout(main_layout)

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            urls = event.mimeData().urls()
            file_list = [url.toLocalFile() for url in urls]
            handle_drop_files(file_list=file_list)
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = RAWRetriever()
    # TODO: ask for RAW directory
    demo.show()
    sys.exit(app.exec_())
