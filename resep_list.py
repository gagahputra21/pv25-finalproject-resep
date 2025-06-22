from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

import os

class RecipeListWidget(QWidget):
  def __init__(self, resep_id, judul, bahan_summary, waktu, porsi, gambar_path, parent=None):
    super().__init__(parent)
    self.resep_id = resep_id
    self.judul = judul
    self.bahan_summary = bahan_summary
    self.waktu = waktu
    self.porsi = porsi
    self.gambar_path = gambar_path

    self.initUI()

  
  def initUI(self):

    self.gambar_label = QLabel()
    self.gambar_label.setFixedSize(100, 100)

    if self.gambar_path and os.path.exists(self.gambar_path):
        pixmap = QPixmap(self.gambar_path)
        self.gambar_label.setPixmap(pixmap.scaled(self.gambar_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
    else:
        self.gambar_label.setText("No Image")

    self.judul_label = QLabel(self.judul)
    self.bahan_label = QLabel(self.bahan_summary)

    self.waktu_icon = QLabel("⏰")
    self.waktu_label = QLabel(self.waktu)

    self.porsi_icon = QLabel("👨‍👩‍👧‍👦")
    self.porsi_label = QLabel(self.porsi)

    # Layout serve (waktu dan porsi)
    serve_layout = QHBoxLayout()
    serve_layout.addWidget(self.waktu_icon)
    serve_layout.addWidget(self.waktu_label)
    serve_layout.addWidget(self.porsi_icon)
    serve_layout.addWidget(self.porsi_label)

    # Layout teks
    text_layout = QVBoxLayout()
    text_layout.addWidget(self.judul_label)
    text_layout.addWidget(self.bahan_label)
    text_layout.addLayout(serve_layout)

    # Layout utama
    main_layout = QHBoxLayout(self)
    main_layout.addWidget(self.gambar_label)
    main_layout.addLayout(text_layout)

    self.setLayout(main_layout)
