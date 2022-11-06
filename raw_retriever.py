import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from pathlib import Path
import re

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


def handle_drop_files(file_list):
    file_dict = files_to_dict(file_list)
    copy_files(file_dict)


def copy_files(file_dict, dir_path):
    for _, file_path in file_dict.items():
        # TODO: Check if file exists in RAW directory or first level subdirectory
        # TODO: Copy file from RAW directory to original directory
        # TODO: Make box flash green if successful
        # TODO: Show message box if problem and skip file
        pass


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
