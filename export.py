from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QTextDocument
from PyQt5.QtPrintSupport import QPrinter
import csv
import os

def export_to_pdf(parent, resep_data):
    file_name, _ = QFileDialog.getSaveFileName(parent, "Ekspor Resep ke PDF", "", "PDF Files (*.pdf)")
    if not file_name:
        return

    judul, kategori, bahan, cara, tanggal, gambar_path, waktu, porsi = resep_data[1:]

    if gambar_path and os.path.exists(gambar_path):
        absolute_path = os.path.abspath(gambar_path)
        img_html = f'<p><img src="file:///{absolute_path.replace("\\", "/")}" width="200"></p>'

    doc = QTextDocument()
    html_content = f"""
<html>
  <head>
    <style>
      body {{
        font-family: Arial, sans-serif;
        margin: 30px;
        font-size: 12pt;
        line-height: 1.5;
      }}
      h1 {{
        font-size: 20pt;
        margin-bottom: 10px;
      }}
      img {{
        max-width: 300px;
        margin-bottom: 15px;
      }}
      .meta {{
        margin-bottom: 15px;
      }}
      .meta p {{
        margin: 3px 0;
      }}
      .section-title {{
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 5px;
      }}
      .content-box {{
        white-space: pre-wrap;
      }}
    </style>
  </head>
  <body>
    <h1>{judul}</h1>
    {img_html if gambar_path else ''}
    <div class="meta">
      <p><b>Kategori:</b> {kategori or '-'}</p>
      <p><b>Tanggal:</b> {tanggal or '-'}</p>
      <p><b>Waktu:</b> {waktu or '-'}</p>
      <p><b>Porsi:</b> {porsi or '-'}</p>
    </div>

    <div>
      <div class="section-title">Bahan:</div>
      <div class="content-box">{bahan}</div>

      <div class="section-title">Cara Membuat:</div>
      <div class="content-box">{cara}</div>
    </div>
  </body>
</html>
"""
    doc.setHtml(html_content)

    printer = QPrinter()
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setOutputFileName(file_name)
    doc.print_(printer)

    QMessageBox.information(parent, "Berhasil", f"Data resep berhasil diekspor ke PDF:\n{file_name}")


def export_to_csv(parent, resep_data):
    file_name, _ = QFileDialog.getSaveFileName(parent, "Ekspor Resep ke CSV", "", "CSV Files (*.csv)")
    if not file_name:
        return

    try:
        with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            writer.writerow(['ID', 'Judul', 'Kategori', 'Bahan', 'Cara', 'Tanggal', 'Gambar', 'Waktu', 'Porsi'])
            writer.writerow(resep_data)
        QMessageBox.information(parent, "Berhasil", f"Data resep berhasil diekspor ke CSV:\n{file_name}")
    except Exception as e:
        QMessageBox.critical(parent, "Gagal", f"Ekspor CSV gagal: {e}")
