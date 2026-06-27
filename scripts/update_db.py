import sqlite3
conn = sqlite3.connect('cv_data.db')
cursor = conn.cursor()
cursor.execute("UPDATE proyek SET gambar = 'sikahil_bootcamp.png' WHERE nama_proyek = 'Sikahil Bootcamp'")
conn.commit()
conn.close()
print("Updated!")
