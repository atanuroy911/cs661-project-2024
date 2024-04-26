import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QComboBox
)
from PyQt5.QtGui import QImage, QColor
import zlib

ALLOWED = 'abcdefghijklmnopqrstuvwxyz0123456789\''

def clean_lyrics(dirty_lyrics):
    lyrics = dirty_lyrics.lower()
    ret = []
    current = ''
    for c in lyrics:
        if c in ALLOWED:
            current += c
        else:
            if current != '':
                ret.append(current)
            current = ''
    if current != '':
        ret.append(current)
    print(ret)
    return ret

def clean_lyrics_to_SSMatrix(lyrics):
    return [[word_1 == word_2 for word_1 in lyrics] for word_2 in lyrics]

def color_array(ssmatrix, color_match, color_mismatch):
    return [color_match if x else color_mismatch for row in ssmatrix for x in row]

def save_png(ssmatrix, file_name, colors=((240, 194, 14), (30, 15, 30))):
    assert file_name.endswith('.png'), "file_name must end with <.png>"
    im = QImage(len(ssmatrix), len(ssmatrix), QImage.Format_RGB32)
    for i, color in enumerate(color_array(ssmatrix, colors[0], colors[1])):
        row = i // len(ssmatrix)
        col = i % len(ssmatrix)
        im.setPixelColor(col, row, QColor(*color))
    im.save(file_name)

def lyrics_to_entrypy(words):
    data_in = ' '.join(words).encode('utf-8')
    data_out = zlib.compress(data_in, level=9)
    return (len(data_out) / len(data_in)) if data_in != 0 else 0

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Self-Similarity Matrix Generator')
        self.setMinimumSize(500, 250)

        self.text_edit = QTextEdit()
        self.text_edit.setFocus()
        self.generate_btn = QPushButton('Generate (^Ret)')
        self.clear_btn = QPushButton('Clear text area (^L)')
        self.combo_box = QComboBox()
        self.combo_box.addItems(['Green on black', 'Poziomka', 'Złoty'])
        self.combo_box.setCurrentText('Poziomka')
        self.entropy_label = QLabel('Entropy of input: unknown')

        self.generate_btn.clicked.connect(self.generate)
        self.clear_btn.clicked.connect(self.clear_screen)

        central_widget = QWidget()
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        text_layout = QVBoxLayout()
        text_layout.addWidget(self.text_edit)
        text_layout.addWidget(self.generate_btn)
        text_layout.addWidget(self.clear_btn)
        main_layout.addLayout(text_layout)

        btn_layout = QVBoxLayout()
        btn_layout.addWidget(self.combo_box)
        btn_layout.addWidget(self.entropy_label)
        main_layout.addLayout(btn_layout)

    def generate(self):
        ls = self.text_edit.toPlainText()
        lyrics = clean_lyrics(ls)
        save_png(clean_lyrics_to_SSMatrix(lyrics), 'hello.png', self.color_schemes[self.combo_box.currentText()])
        entropy = lyrics_to_entrypy(lyrics)
        self.entropy_label.setText('Entropy of input: {:0.2f}%'.format(entropy * 100))

    def clear_screen(self):
        self.text_edit.clear()

    color_schemes = {
        'Green on black': ((32, 194, 14), (0, 0, 0)),
        'Poziomka': ((240, 57, 87), (30, 15, 30)),
        'Złoty': ((197, 179, 88), (30, 30, 30)),
    }

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
