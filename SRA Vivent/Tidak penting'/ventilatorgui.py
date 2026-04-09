from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# File output PDF
output_path = "/mnt/data/absensi.pdf"

# Buat dokumen
doc = SimpleDocTemplate(output_path, pagesize=A4)
elements = []
styles = getSampleStyleSheet()
style_normal = styles["Normal"]
style_title = styles["Title"]

# Judul
elements.append(Paragraph("DAFTAR HADIR", style_title))
elements.append(Paragraph("Mata Kuliah: _______________________", style_normal))
elements.append(Paragraph("Kelas: ____________________________", style_normal))
elements.append(Paragraph("Dosen: ____________________________", style_normal))
elements.append(Paragraph("Tanggal: __________________________", style_normal))
elements.append(Spacer(1, 12))

# Data tabel (header + baris kosong)
data = [
    ["No", "NIM", "Nama Mahasiswa", "Paraf"]
]

# Tambahkan 20 baris kosong
for i in range(1, 21):
    data.append([str(i), "", "", ""])

# Buat tabel
table = Table(data, colWidths=[30, 100, 250, 100])
table.setStyle(TableStyle([
    ("GRID", (0,0), (-1,-1), 1, colors.black),
    ("ALIGN", (0,0), (0,-1), "CENTER"),
    ("ALIGN", (3,0), (3,-1), "CENTER"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
]))

elements.append(table)

# Build dokumen
doc.build(elements)

output_path
