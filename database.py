import sqlite3
from PyQt5.QtWidgets import QMessageBox
import sys

class DatabaseManager:
  def __init__(self, db_name="resep.db"):
    self.db_name = db_name
    self.conn = None
    self.cursor = None
    self.connect()
    self.create_table()
  
  def connect(self):
    try:
      self.conn = sqlite3.connect(self.db_name)
      self.cursor = self.conn.cursor()
      print(f"Terhubung ke database: {self.db_name}")
    except sqlite3.Error as e:
      QMessageBox.critical(None, "Kesalahan Database", f"Gagal terhubung ke database: {e}")
      sys.exit(1)

  def create_table(self):
    try:
      self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS resep (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          judul TEXT NOT NULL,
          kategori TEXT,
          bahan TEXT,
          cara TEXT,
          tanggal TEXT,
          gambar_path TEXT,
          waktu TEXT,
          porsi TEXT
        )
      """)
      self.conn.commit()
      print("Tabel 'resep' berhasil dibuat atau sudah ada.")
    except sqlite3.Error as e:
      QMessageBox.critical(None, "Kesalahan Database", f"Gagal membuat tabel: {e}")

  
  def add_resep(self, judul, kategori, bahan, cara, tanggal, gambar_path, waktu, porsi):
    try:
      self.cursor.execute("""
        INSERT INTO resep (judul, kategori, bahan, cara, tanggal, gambar_path, waktu, porsi) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (judul, kategori, bahan, cara, tanggal, gambar_path, waktu, porsi))
      self.conn.commit()
      return True
    except sqlite3.Error as e:
      QMessageBox.critical(None, "Kesalahana Database", f"Gagal menambahkan resep: {e}")
      return False
    
  def get_all_resep(self):
    try:
        self.cursor.execute("SELECT id, judul, bahan, waktu, porsi, gambar_path FROM resep ORDER BY judul ASC")
        return self.cursor.fetchall()
    except sqlite3.Error as e:
        QMessageBox.critical(None, "Kesalahan Database", f"Gagal mengambil resep: {e}")
        return []
  
  def get_resep_detail(self, resep_id):
    try:
        self.cursor.execute("SELECT * FROM resep WHERE id = ?", (resep_id,))
        return self.cursor.fetchone()
    except sqlite3.Error as e:
        QMessageBox.critical(None, "Kesalahan Database", f"Gagal mengambil detail resep: {e}")
        return None
    
  def update_resep(self, resep_id, judul, kategori, bahan, cara, tanggal, gambar_path, waktu, porsi):
    try:
      self.cursor.execute("""
          UPDATE resep SET judul = ?, kategori = ?, bahan = ?, cara = ?, tanggal = ?, gambar_path = ?, waktu = ?, porsi = ?
          WHERE id = ?
      """, (judul, kategori, bahan, cara, tanggal, gambar_path, waktu, porsi, resep_id))
      self.conn.commit()
      return True
    except sqlite3.Error as e:
        QMessageBox.critical(None, "Kesalahan Database", f"Gagal memperbarui resep: {e}")
        return False
    
  def delete_resep(self, resep_id):
    try:
        self.cursor.execute("DELETE FROM resep WHERE id = ?", (resep_id,))
        self.conn.commit()
        return True
    except sqlite3.Error as e:
        QMessageBox.critical(None, "Kesalahan Database", f"Gagal menghapus resep: {e}")
        return False
    
  def close(self):
     if self.conn:
        self.conn.close()
        print("Koneksi database ditutup")