from pathlib import Path
import re
import shutil
import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QMessageBox

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
        global RAW_DIRECTORY
        RAW_DIRECTORY = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        _ = raw_directory_to_path()
        print(f"Selected RAW directory: '{RAW_DIRECTORY}'")
        print("-----------------------")


def raw_directory_to_path():
    raw_dir_path = Path(RAW_DIRECTORY)
    if not RAW_DIRECTORY or not raw_dir_path.exists():
        print(f"Chosen directory: '{RAW_DIRECTORY}' does not exist. Exit Program.")
        exit()
        sys.exit(app.exec_())
    return raw_dir_path


def handle_drop_files(file_list):
    raw_dir_path = raw_directory_to_path()
    file_dict = files_to_dict(file_list)
    copy_files(file_dict, raw_dir_path)
    print("---------------------")


def copy_files(file_dict, raw_dir_path):
    """Go through dropped files and copy RAW equivalent from RAW directory"""
    files_copied = []
    for file_stem, file_path in file_dict.items():

        try:
            raw_file_path = get_raw_file_path(raw_dir_path, file_stem)
        except FileNotFoundError:
            continue
        except ValueError:
            continue
        dst_path = file_path.parent / raw_file_path.name
        if dst_path.exists():
            print(f"RAW file already in destination directory. File Skipped: '{file_stem}'")
            continue
        try:
            shutil.copy(raw_file_path, dst_path)
        except Exception:
            show_critical_messagebox(
                "Copy Problem",
                f"There has been a problem when copying '{raw_file_path}'"
            )
            continue
        files_copied.append(file_stem)
    # TODO: Make box flash green if successful
    print(f"Copied {str(files_copied)} successfully")


def get_raw_file_path(raw_dir_path, file_stem):
    """Find raw file in RAW directory and return its path"""
    subdirectories = [name for name in os.listdir(raw_dir_path) if
                      os.path.isdir(os.path.join(raw_dir_path, name))]
    search_directories = [raw_dir_path / sub_dir for sub_dir in subdirectories]
    search_directories.append(raw_dir_path)
    valid_raw_file_paths = []
    for dir_path in search_directories:
        raw_file_path = dir_path / f"{file_stem}.{RAW_FILE_ENDING}"
        if raw_file_path.exists():
            valid_raw_file_paths.append(raw_file_path)
    if len(valid_raw_file_paths) <= 0:
        print(
            f"! Could not find RAW version of {file_stem} in '{RAW_DIRECTORY}. Skipped file.'")
        raise FileNotFoundError
    elif len(valid_raw_file_paths) > 1:
        print(
            f"! {len(valid_raw_file_paths)} RAW files with name {file_stem}.{RAW_FILE_ENDING}."
            f"Skipped file. ({valid_raw_file_paths})"
        )
        raise ValueError
    else:
        return valid_raw_file_paths[0]


def files_to_dict(file_list):
    file_dict = {}  # Key:file-stem Value:Path(file)
    for file in file_list:
        file_path = Path(file)
        # Check file existence
        if not file_path.exists():
            show_critical_messagebox(
                "File does not exist",
                f"{file_path.name} does not exist and was skipped"
            )
        file_name = file_path.name
        if not check_regex(file_name=file_name):
            show_critical_messagebox(
                "Invalid file name",
                f"Invalid jp(e)g file name. File Skipped: '{file_name}' "
            )
            continue
        file_dict[file_path.stem] = file_path
    return file_dict


def check_regex(file_name):
    """Check if file name has jp(e)g ending"""
    regex = r"(?i)\w*\.(\bjpg\b|\bjpeg\b)"
    match = re.compile(regex).match(file_name)
    return bool(match)


def show_critical_messagebox(title, text):
    print(text)
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(text)
    msg.setWindowTitle(title)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setWindowFlags(Qt.WindowStaysOnTopHint)
    retval = msg.exec_()


class RAWRetriever(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("RAW Retriever")
        self.setAcceptDrops(True)
        self.resize(320, 100)
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
