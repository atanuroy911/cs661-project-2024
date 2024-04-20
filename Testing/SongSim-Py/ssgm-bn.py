import os
import sys
import zlib
import string
from PyQt5.QtWidgets import (
    QApplication,
    QMessageBox,
    QMainWindow,
    QTextEdit,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QComboBox,
    QFileDialog,
    QSizePolicy
)
from PyQt5.QtGui import QImage, QColor, QFont
import docx

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


# Define the Unicode range for Bengali characters
ALLOWED_BENGALI = ""


def clean_lyrics(dirty_lyrics):
    ALLOWED_BENGALI = set(
        "অ আ ই ঈ উ ঊ ঋ এ ঐ ও ঔ ক খ গ ঘ ঙ চ ছ জ ঝ ঞ ট ঠ ড ঢ ণ ত থ দ ধ ন প ফ ব ভ ম য র ল শ ষ স হ ় া ি ী ু ূ ৃ ে ৈ ো ৌ ্ ৎ ৗ ড় ঢ় য় ৠ ৣ ০ ১ ২ ৩ ৪ ৫ ৬ ৭ ৮ ৯"
    )
    lyrics = dirty_lyrics.lower()
    ret = []
    current = ""
    for c in lyrics:
        if c == " " or c == "\n":
            if current.strip() != "":
                ret.append(current.strip())
            current = ""
        elif c in ALLOWED_BENGALI:
            current += c
        elif c not in string.punctuation:
            current += c
    if current.strip() != "":
        ret.append(current.strip())
    # print(ret)
    return ret


def clean_lyrics_to_SSMatrix(lyrics):
    return [[word_1 == word_2 for word_1 in lyrics] for word_2 in lyrics]


def color_array(ssmatrix, color_match, color_mismatch):
    return [color_match if x else color_mismatch for row in ssmatrix for x in row]


def save_png(ssmatrix, file_name, colors=((240, 194, 14), (30, 15, 30))):
    assert file_name.endswith(".png"), "file_name must end with <.png>"
    im = QImage(len(ssmatrix), len(ssmatrix), QImage.Format_RGB32)
    for i, color in enumerate(color_array(ssmatrix, colors[0], colors[1])):
        row = i // len(ssmatrix)
        col = i % len(ssmatrix)
        im.setPixelColor(col, row, QColor(*color))
    im.save(file_name)


def lyrics_to_entrypy(words):
    data_in = " ".join(words).encode("utf-8")
    data_out = zlib.compress(data_in, level=9)
    return (len(data_out) / len(data_in)) if data_in != 0 else 0


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.dataset_folder = None

        self.setWindowTitle("Self-Similarity Matrix Generator")
        self.setMinimumSize(500, 250)

        self.text_edit = QTextEdit()
        self.text_edit.setFocus()
        self.generate_btn = QPushButton("Generate from File")
        self.generate_btn_txt = QPushButton("Generate from text")
        self.clear_btn = QPushButton("Clear text area ")
        self.combo_box = QComboBox()
        self.combo_box.addItems(["Green on black", "Poziomka", "Złoty"])
        self.combo_box.setCurrentText("Poziomka")
        self.entropy_label = QLabel("Entropy of input: unknown")
        
        # Initialize QLabel to display the image
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(300, 300)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setScaledContents(True)

        self.generate_btn.clicked.connect(self.generate)
        self.generate_btn_txt.clicked.connect(self.generate_txt)
        self.clear_btn.clicked.connect(self.clear_screen)

        central_widget = QWidget()
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        text_layout = QVBoxLayout()
        text_layout.addWidget(self.text_edit)
        text_layout.addWidget(self.generate_btn)
        text_layout.addWidget(self.generate_btn_txt)
        text_layout.addWidget(self.clear_btn)
        main_layout.addLayout(text_layout)

        btn_layout = QVBoxLayout()
        btn_layout.addWidget(self.combo_box)
        btn_layout.addWidget(self.entropy_label)

        # Add combo boxes for selecting lyricists and songs
        self.lyricists_combo = QComboBox()
        self.songs_combo = QComboBox()
        btn_layout.addWidget(self.lyricists_combo)
        btn_layout.addWidget(self.songs_combo)

        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.image_label)


        # Set the font for Bengali text
        font = QFont()
        font.setFamily("kalpurush.ttf")
        self.text_edit.setFont(font)

        # Connect the lyricists_combo to populate_lyricists_combo function
        self.lyricists_combo.activated.connect(self.populate_songs_combo)

        self.select_dataset_folder()

    # Function to select the dataset folder
    def select_dataset_folder(self):
        self.dataset_folder = QFileDialog.getExistingDirectory(
            self, "Select Dataset Folder"
        )
        if self.dataset_folder:
            self.populate_lyricists_combo()

    # Function to populate the combo box with the lyricists from the dataset folder
    def populate_lyricists_combo(self):
        if self.dataset_folder:
            lyricists = [
                name
                for name in os.listdir(self.dataset_folder)
                if os.path.isdir(os.path.join(self.dataset_folder, name))
            ]
            self.lyricists_combo.clear()
            self.lyricists_combo.addItems(lyricists)

    # Function to populate the songs combo box based on the selected lyricist
    def populate_songs_combo(self):
        if self.dataset_folder:
            lyricist = self.lyricists_combo.currentText()
            songs_folder = os.path.join(self.dataset_folder, lyricist)
            songs = [
                name for name in os.listdir(songs_folder) if name.endswith(".docx")
            ]
            self.songs_combo.clear()
            self.songs_combo.addItems(songs)

    # Generate function to create the self-similarity matrix
    
    # Update the image displayed on the QLabel
    def update_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setFixedHeight(300)
        self.image_label.setFixedWidth(300)


    def generate(self):
        if self.dataset_folder:
            lyricist = self.lyricists_combo.currentText()
            song = self.songs_combo.currentText()
            try:
                song_path = os.path.join(self.dataset_folder, lyricist, song)
                doc = docx.Document(song_path)
                text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                lyrics = clean_lyrics(text)
                self.text_edit.setText("\n".join(lyrics))
                save_png(
                    clean_lyrics_to_SSMatrix(lyrics),
                    "hello.png",
                    self.color_schemes[self.combo_box.currentText()],
                )
                entropy = lyrics_to_entrypy(lyrics)
                self.entropy_label.setText(
                    "Entropy of input: {:0.2f}%".format(entropy * 100)
                )
                self.update_image("hello.png")  # Update the displayed image
            except FileNotFoundError:
                if self.text_edit.toPlainText():
                    text = self.text_edit.toPlainText()
                    lyrics = clean_lyrics(text)
                    save_png(
                        clean_lyrics_to_SSMatrix(lyrics),
                        "hello.png",
                        self.color_schemes[self.combo_box.currentText()],
                    )
                    entropy = lyrics_to_entrypy(lyrics)
                    self.entropy_label.setText(
                        "Entropy of input: {:0.2f}%".format(entropy * 100)
                    )
                    self.update_image("hello.png")  # Update the displayed image
                else:
                    QMessageBox.critical(
                        self, "Error", "File not found and no text entered."
                    )
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
                
    def generate_txt(self):
        try:
            if self.text_edit.toPlainText():
                text = self.text_edit.toPlainText()
                lyrics = clean_lyrics(text)
                save_png(
                    clean_lyrics_to_SSMatrix(lyrics),
                    "hello.png",
                    self.color_schemes[self.combo_box.currentText()],
                )
                entropy = lyrics_to_entrypy(lyrics)
                self.entropy_label.setText(
                    "Entropy of input: {:0.2f}%".format(entropy * 100)
                )
                self.update_image("hello.png")  # Update the displayed image
            else:
                QMessageBox.critical(
                    self, "Error", "No text entered."
                )
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # Function to clear the text area
    def clear_screen(self):
        self.text_edit.clear()

    # Color schemes for self-similarity matrix
    color_schemes = {
        "Green on black": ((32, 194, 14), (0, 0, 0)),
        "Poziomka": ((240, 57, 87), (30, 15, 30)),
        "Złoty": ((197, 179, 88), (30, 30, 30)),
    }


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
