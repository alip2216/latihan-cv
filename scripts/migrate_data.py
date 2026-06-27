import sqlite3
import pandas as pd

def migrate():
    conn = sqlite3.connect('cv_data.db')
    cursor = conn.cursor()
    
    # Create sertifikat table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sertifikat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_sertifikat TEXT,
            penerbit TEXT,
            tahun INTEGER,
            deskripsi TEXT,
            gambar TEXT,
            link TEXT
        )
    ''')
    
    xls = pd.ExcelFile('ecv_data.xlsx')
    
    # Migrate Certifications
    cert_df = pd.read_excel(xls, 'Certifications')
    for _, row in cert_df.iterrows():
        title = str(row.get('title', ''))
        issuer = str(row.get('issuer', ''))
        year = int(row.get('year', 2026)) if pd.notna(row.get('year')) else 2026
        desc = str(row.get('description', ''))
        link = str(row.get('link', '')) if pd.notna(row.get('link')) else ''
        
        # check if exists
        cursor.execute("SELECT id FROM sertifikat WHERE nama_sertifikat = ?", (title,))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO sertifikat (nama_sertifikat, penerbit, tahun, deskripsi, gambar, link)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, issuer, year, desc, '', link))
            
    # Migrate Projects
    proj_df = pd.read_excel(xls, 'Projects')
    for _, row in proj_df.iterrows():
        title = str(row.get('title', ''))
        desc = str(row.get('description', ''))
        tools = str(row.get('tools', ''))
        link = str(row.get('link', '')) if pd.notna(row.get('link')) else ''
        
        cursor.execute("SELECT id FROM proyek WHERE nama_proyek = ?", (title,))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO proyek (nama_proyek, deskripsi, gambar, teknologi, link)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, desc, '', tools, link))
            
    conn.commit()
    conn.close()
    print("Migration successful!")

if __name__ == '__main__':
    migrate()
