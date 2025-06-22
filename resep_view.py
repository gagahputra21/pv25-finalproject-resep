from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic


class ResepView(QWidget):
    # Signal: agar bisa dihubungkan ke fungsi di parent window
    editClicked = pyqtSignal()
    exportpdfClicked = pyqtSignal()
    exportcsvClicked = pyqtSignal()
    backClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        
        uic.loadUi("resep_view.ui", self)

        # Scroll area agar semua isi bisa discroll
        self.scroll_area.setWidgetResizable(True)

        # Teks resep
        self.resep_text.setMinimumHeight(300)

        # Tombol-tombol aksi
        self.back_btn.clicked.connect(self.backClicked.emit)
        self.edit_btn.clicked.connect(self.editClicked.emit)
        self.export_pdf_btn.clicked.connect(self.exportpdfClicked.emit)
        self.export_csv_btn.clicked.connect(self.exportcsvClicked.emit)

    def set_resep_text(self, text):
        self.resep_text.setPlainText(text)

    def get_resep_text(self):
        return self.resep_text.toPlainText()

    def clear(self):
        self.resep_text.clear()