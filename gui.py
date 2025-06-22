from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow,  QListWidgetItem, QMessageBox, QLabel, QFileDialog
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QIcon

from database import DatabaseManager
from resep_list import RecipeListWidget
from export import export_to_pdf, export_to_csv
from resep_view import ResepView

import os

class ResepApp(QMainWindow):
  def __init__(self):
    super().__init__()
    self.db_manager = DatabaseManager()
    self.current_resep_id = None

    icon_path = os.path.join(os.path.dirname(__file__), "logo.png")
    self.setWindowIcon(QIcon(icon_path))

    self.initUI()
    self.stylesheet()
    

  def initUI(self):
    uic.loadUi("resep.ui", self)
    self.setWindowTitle("Resep")

    self.create_status_bar()
    self.menu_bar()

    self.resep_list_panel()
    self.resep_detail_panel()

    self.resep_view_widget = ResepView()
    self.resep_view_widget.backClicked.connect(self.show_list_page)
    self.resep_view_widget.editClicked.connect(lambda: self.display_resep_detail(self.resep_list_widget.currentItem()))
    self.resep_view_widget.exportpdfClicked.connect(self.export_pdf)
    self.resep_view_widget.exportcsvClicked.connect(self.export_csv)

    self.stackedWidget.addWidget(self.resep_view_widget)

    self.stackedWidget.setCurrentIndex(0)

    self.load_resep_list()

  #Func untuk menambah styles
  def stylesheet(self):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    styleSheet_path = os.path.join(current_dir, 'styles.qss')

    if os.path.exists(styleSheet_path):
      with open(styleSheet_path, "r") as file:
        self.setStyleSheet(file.read())
        print(f"Stylesheet dari '{styleSheet_path}' berhasil dimuat.")
    else:
      QMessageBox.warning(self, "Kesalahan Stylesheet", f"File stylesheet tidak ditemukan: {styleSheet_path}")
      print(f"Kesalahan: File stylesheet tidak ditemukan di {styleSheet_path}")

  #Func untuk menu bar
  def menu_bar(self):
    self.exit_action.setShortcut('Ctrl+Q')
    self.exit_action.triggered.connect(self.close)

    self.export_pdf_action.setStatusTip('Ekspor semua resep ke file PDF')
    self.export_pdf_action.triggered.connect(self.export_pdf)

    self.export_csv_action.setStatusTip('Ekspor semua resep ke file CSV')
    self.export_csv_action.triggered.connect(self.export_csv)

    self.tambah_action.setStatusTip('Tambah resep')
    self.tambah_action.triggered.connect(self.show_new_resep_form)

    self.edit_action.setStatusTip('Edit resep')
    self.edit_action.triggered.connect(lambda: self.display_resep_detail(self.resep_list_widget.currentItem())) #Menggunakan lamda agar bisa mengambil item terpilih dari self.resep_list_widget secara manual

    self.hapus_action.setStatusTip('Hapus resep')
    self.hapus_action.triggered.connect(self.delete_resep)

    self.about_action.setStatusTip('Tantang aplikasi')
    self.about_action.triggered.connect(self.show_about_dialog)

  #Func untuk status bar
  def create_status_bar(self):
    self.statusBar = self.statusBar()
    self.student_name_label = QLabel("Nama: Gagah Putra Lesmana")
    self.student_nim_label = QLabel("NIM F1D021037")

    self.student_name_label.setStyleSheet("padding: 0 8px; color: #555;")
    self.student_nim_label.setStyleSheet("padding: 0 8px; color: #555;")

    self.statusBar.addPermanentWidget(self.student_name_label)
    self.statusBar.addPermanentWidget(self.student_nim_label)

  #Func untuk membuat list resep panel
  def resep_list_panel(self):
    self.list_panel_layout.setContentsMargins(15, 15, 15, 15)
    self.list_panel_layout.setSpacing(10)

    self.list_label.setFont(QFont('Arial', 16, QFont.Bold))

    self.cari_input.textChanged.connect(self.filter_resep_list)

    self.resep_list_widget.setSpacing(10)
    self.resep_list_widget.itemClicked.connect(self.handle_single_click)
    self.resep_list_widget.itemDoubleClicked.connect(self.handle_double_click)

    self.refresh_btn.clicked.connect(self.load_resep_list)
    self.edit_btn.clicked.connect(lambda: self.display_resep_detail(self.resep_list_widget.currentItem()))
    self.tambah_btn.clicked.connect(self.show_new_resep_form)
    self.hapus_btn.clicked.connect(self.delete_resep)

  #Func untuk membuat detail/form list resep panel
  def resep_detail_panel(self):
    self.kategori_input.addItem("Pilih Kategori")
    self.kategori_input.addItems(["Makanan", "Minuman"])

    self.cariGambar_btn.clicked.connect(self.cari_gambar)

    self.kembali_btn.clicked.connect(self.show_list_page)
    self.simpan_btn.clicked.connect(self.save_resep)
    self.bersihkan_btn.clicked.connect(self.clear_detail_panel)

  #Func untuk membuka dialog file untuk memilih gambar
  def cari_gambar(self):
    project_dir = os.path.dirname(os.path.abspath(__file__))

    file_name, _ = QFileDialog.getOpenFileName(self, "Pilih Gambar Resep", project_dir, "Image Files (*.png *.jpg *.gif)")
    if file_name:
      self.gambar_input.setText(file_name)

  #Func untuk menampilkan form resep baru yang ingin ditambah
  def show_new_resep_form(self):
    self.clear_detail_panel_for_new_resep()
    self.stackedWidget.setCurrentIndex(1)

  #Func untuk membersihkan form saat ingin memabah resep baru
  def clear_detail_panel_for_new_resep(self):
    self.clear_detail_panel()
    self.current_resep_id = None
    self.tanggal_input.setText(QDate.currentDate().toString(Qt.ISODate))

  #Func untuk membersihkan form
  def clear_detail_panel(self):
    self.judul_input.clear()
    self.kategori_input.setCurrentIndex(0)
    self.bahan_input.clear()
    self.cara_input.clear()
    self.tanggal_input.clear()
    self.gambar_input.clear()
    self.waktu_input.clear()

    self.resep_list_widget.clearSelection()
    self.current_resep_id = None

  #Func untuk menampilkan halaman list resep
  def show_list_page(self):
    self.stackedWidget.setCurrentIndex(0)
    self.resep_list_widget.clearSelection()
    self.current_resep_id = None

  def load_resep_list(self):
    self.resep_list_widget.clear()
    reseps = self.db_manager.get_all_resep()
    for resep_id, judul, bahan, waktu, porsi, gambar_path in reseps:
      #Membuat ringkasan bahan
      bahan_summary = bahan.split('\n')[0] #Mengambil baris pertama
      if len(bahan_summary) > 70: 
        bahan_summary = bahan_summary[:70] + "..."
      elif '\n' in bahan: #Jika ada baris kedua, tampilkan sebagai indikasi lebih banyak
        bahan_summary += "..."

      list_widget = RecipeListWidget(
        resep_id,
        judul,
        bahan_summary,
        waktu,
        porsi,
        gambar_path
      )

      list_item = QListWidgetItem(self.resep_list_widget)
      list_item.setSizeHint(list_widget.sizeHint())

      list_item.setData(Qt.UserRole, resep_id)
      
      self.resep_list_widget.addItem(list_item)
      self.resep_list_widget.setItemWidget(list_item, list_widget)

  #Func untuk menampilkan resep secara detail pada resep detai panel
  def display_resep_detail(self, item):
    self.current_resep_id = item.data(Qt.UserRole)
    resep_data = self.db_manager.get_resep_detail(self.current_resep_id)
    if resep_data:
      (_, judul, kategori, bahan, cara, tanggal, gambar_path, waktu, porsi) = resep_data

      self.judul_input.setText(judul)
      self.kategori_input.setCurrentText(kategori)
      self.bahan_input.setText(bahan)
      self.cara_input.setText(cara)
      self.tanggal_input.setText(tanggal)
      self.gambar_input.setText(gambar_path if gambar_path else "")
      self.waktu_input.setText(waktu if waktu else "")
      self.porsi_input.setText(porsi if porsi else "")

      self.simpan_btn.setText("Update Resep")
      self.stackedWidget.setCurrentIndex(1)
    else:
      self.clear_detail_panel()
      self.stackedWidget.setCurrentIndex(0)

  #Func untuk menyimpan resep
  def save_resep(self):
    judul = self.judul_input.text().strip()
    kategori = self.kategori_input.currentText()
    bahan = self.bahan_input.toPlainText().strip()
    cara = self.cara_input.toPlainText().strip()
    tanggal = self.tanggal_input.text().strip()
    gambar_path = self.gambar_input.text().strip()
    waktu = self.waktu_input.text().strip()
    porsi = self.porsi_input.text().strip()

    if not judul or not bahan or not cara:
      QMessageBox.warning(self, "Input Tidak lengkap", "Judul, bahan-bahan, dan cara membuat tidak boleh kosong.")
      return
    
    if self.current_resep_id is None: #Memerikasa apakah resep sudah ada
      if self.db_manager.add_resep(judul, kategori, bahan, cara, tanggal, gambar_path, waktu, porsi):
        QMessageBox.information(self, "Sukses", "Resep berhasil ditambahkan!")
        self.load_resep_list()
        self.clear_detail_panel()
        self.show_list_page()

    else: #jika sudah ada resep akan di update
      if self.db_manager.update_resep(self.current_resep_id, judul, kategori, bahan, cara, tanggal, gambar_path, waktu, porsi):
        QMessageBox.information(self, "Sukses", "Resep berhasil diperbarui!")
        self.load_resep_list()
        self.clear_detail_panel()
        self.show_list_page()

  #Func untuk menghapus resep
  def delete_resep(self):
    item = self.resep_list_widget.currentItem()
    if not item:
        QMessageBox.warning(self, "Tidak Ada Resep Terpilih", "Silakan pilih satu resep yang ingin dihapus.")
        return

    resep_id = item.data(Qt.UserRole)
    resep = self.db_manager.get_resep_detail(resep_id)
    if not resep:
        QMessageBox.warning(self, "Resep Tidak Ditemukan", "Resep tidak ditemukan dalam database.")
        return

    judul = resep[1]
    confirm = QMessageBox.question(
        self,
        "Konfirmasi Hapus",
        f"Apakah Anda yakin ingin menghapus resep '{judul}'?",
        QMessageBox.Yes | QMessageBox.No
    )

    if confirm == QMessageBox.Yes:
        if self.db_manager.delete_resep(resep_id):
            QMessageBox.information(self, "Berhasil", f"Resep '{judul}' berhasil dihapus.")
            self.load_resep_list()
            self.clear_detail_panel()
            self.show_list_page()
        else:
            QMessageBox.warning(self, "Gagal", "Resep gagal dihapus.")

  #Func untuk mendeteksi single clik
  def handle_single_click(self, item):
    resep_id = item.data(Qt.UserRole)
    print(f"[Klik 1x] Resep ID: {resep_id}")

  #Func untuk mendeteksi double clik
  def handle_double_click(self, item):
      print(f"[Klik 2x] Menampilkan detail resep...")
      resep_id = item.data(Qt.UserRole)
      self.show_resep_view(resep_id)

  #Func untuk memfilter resep berasarkan judul
  def filter_resep_list(self, text):
    text = text.lower().strip()
    for i in range(self.resep_list_widget.count()):
        item = self.resep_list_widget.item(i)
        widget = self.resep_list_widget.itemWidget(item)

        # Ambil judul dari widget
        judul = widget.judul.lower() if widget and hasattr(widget, "judul") else ""

        # Tampilkan hanya jika mengandung teks pencarian
        item.setHidden(text not in judul)

  #Func untuk ekspor resep ke file PDF
  def export_pdf(self):
    item = self.resep_list_widget.currentItem()
    if not item:
        QMessageBox.warning(self, "Tidak Ada Resep Terpilih", "Silakan pilih satu resep untuk diekspor.")
        return

    resep_id = item.data(Qt.UserRole)
    resep = self.db_manager.get_resep_detail(resep_id)
    if resep:
        export_to_pdf(self, resep)

  #Func untuk ekspor resep ke file CSV
  def export_csv(self):
      item = self.resep_list_widget.currentItem()
      if not item:
          QMessageBox.warning(self, "Tidak Ada Resep Terpilih", "Silakan pilih satu resep untuk diekspor.")
          return

      resep_id = item.data(Qt.UserRole)
      resep = self.db_manager.get_resep_detail(resep_id)
      if resep:
          export_to_csv(self, resep)


  #Func untuk menampilkan dialog 'Tentang'
  def show_about_dialog(self):
    text = (
      "<b>Aplikasi Resep</b><br>"
      "Dibuat dengan PyQt5 dan SQLite.<br><br>"
      "Fitur:<br>"
      "- Melihat dan menambah resep<br>"
      "- Informasi bahan dan cara membuat<br>"
      "- Ekspor ke PDF dan CSV<br><br>"
      "<b>Dibuat oleh Gagah Putra Lesmana (F1D021037)</b><br>"
    )
    QMessageBox.information(self, "Tentang Aplikasi", text)

  #Func untuk menampilkan resep pada ResepWidget
  def show_resep_view(self, resep_id):
    resep_data = self.db_manager.get_resep_detail(resep_id)
    if not resep_data:
        QMessageBox.warning(self, "Kesalahan", "Resep tidak ditemukan.")
        return

    self.current_resep_id = resep_id
    judul, kategori, bahan, cara, tanggal, gambar_path, waktu, porsi = resep_data[1:]

    full_text = f"""Judul: {judul}
Kategori: {kategori}
Tanggal: {tanggal}
Waktu: {waktu}
Porsi: {porsi}

Bahan-bahan:
{bahan}

Cara Membuat:
{cara}
"""
    self.resep_view_widget.set_resep_text(full_text)
    self.stackedWidget.setCurrentWidget(self.resep_view_widget)

  
  def closeEvent(self, event):
    self.db_manager.close()
    event.accept()
  
