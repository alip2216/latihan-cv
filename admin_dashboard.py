import streamlit as st
import sqlite3
import pandas as pd

def inisialisasi_db():
    conn = sqlite3.connect("cv_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proyek (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_proyek TEXT,
            deskripsi TEXT,
            gambar TEXT,
            teknologi TEXT,
            link TEXT
        )
    ''')
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
    conn.commit()
    conn.close()

# --- Fungsi CRUD Proyek ---
def get_semua_proyek():
    conn = sqlite3.connect("cv_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nama_proyek, deskripsi, gambar, teknologi, link FROM proyek")
    data = cursor.fetchall()
    conn.close()
    return data

def tambah_proyek(nama, deskripsi, gambar, teknologi, link):
    conn = sqlite3.connect("cv_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO proyek (nama_proyek, deskripsi, gambar, teknologi, link) VALUES (?, ?, ?, ?, ?)", 
                   (nama, deskripsi, gambar, teknologi, link))
    conn.commit()
    conn.close()

def hapus_proyek(id_proyek):
    conn = sqlite3.connect("cv_data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM proyek WHERE id = ?", (id_proyek,))
    conn.commit()
    conn.close()
    
def update_proyek(id_proyek, nama, deskripsi, gambar, teknologi, link):
    conn = sqlite3.connect("cv_data.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE proyek SET nama_proyek=?, deskripsi=?, gambar=?, teknologi=?, link=? WHERE id=?", 
                   (nama, deskripsi, gambar, teknologi, link, id_proyek))
    conn.commit()
    conn.close()

# --- Fungsi CRUD Sertifikat ---
def get_semua_sertifikat():
    conn = sqlite3.connect("cv_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nama_sertifikat, penerbit, tahun, deskripsi, gambar, link FROM sertifikat")
    data = cursor.fetchall()
    conn.close()
    return data

def tambah_sertifikat(nama, penerbit, tahun, deskripsi, gambar, link):
    conn = sqlite3.connect("cv_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sertifikat (nama_sertifikat, penerbit, tahun, deskripsi, gambar, link) VALUES (?, ?, ?, ?, ?, ?)", 
                   (nama, penerbit, tahun, deskripsi, gambar, link))
    conn.commit()
    conn.close()

def hapus_sertifikat(id_sertifikat):
    conn = sqlite3.connect("cv_data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sertifikat WHERE id = ?", (id_sertifikat,))
    conn.commit()
    conn.close()

def update_sertifikat(id_sertifikat, nama, penerbit, tahun, deskripsi, gambar, link):
    conn = sqlite3.connect("cv_data.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE sertifikat SET nama_sertifikat=?, penerbit=?, tahun=?, deskripsi=?, gambar=?, link=? WHERE id=?", 
                   (nama, penerbit, tahun, deskripsi, gambar, link, id_sertifikat))
    conn.commit()
    conn.close()


def show_admin_panel():
    st.markdown("<h2 style='color: var(--primary-color);'>🔐 Admin Panel</h2>", unsafe_allow_html=True)
    st.info("Halaman ini bersifat privat. Hanya pemilik eCV yang dapat mengedit konten.")
    
    if "admin_logged_in" not in st.session_state:
        st.session_state["admin_logged_in"] = False
        
    if not st.session_state["admin_logged_in"]:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            
            if submitted:
                if username == "admin" and password == "rahasia123":
                    st.session_state["admin_logged_in"] = True
                    st.rerun()
                else:
                    st.error("Username atau password salah!")
    else:
        st.success("Login berhasil!")
        if st.button("Logout"):
            st.session_state["admin_logged_in"] = False
            st.rerun()
            
        st.divider()
        
        tab1, tab2 = st.tabs(["Manajemen Proyek", "Manajemen Sertifikasi"])
        
        # --- TAB PROYEK ---
        with tab1:
            st.subheader("Data Proyek Portofolio")
            daftar_proyek = get_semua_proyek()
            
            # Tambah Proyek Baru
            with st.expander("➕ Tambah Proyek Baru"):
                with st.form("form_tambah_proyek"):
                    nama_baru = st.text_input("Nama Proyek")
                    desc_baru = st.text_area("Deskripsi")
                    gambar_baru = st.text_input("Nama File Gambar / URL", placeholder="Contoh: afsan_mobile.png")
                    tech_baru = st.text_input("Teknologi (pisahkan dengan koma)", placeholder="Contoh: Python, Streamlit")
                    link_baru = st.text_input("Link Proyek", placeholder="URL Github / Website")
                    submit_baru = st.form_submit_button("Simpan Proyek")
                    
                    if submit_baru:
                        if nama_baru:
                            tambah_proyek(nama_baru, desc_baru, gambar_baru, tech_baru, link_baru)
                            st.success("Proyek berhasil ditambahkan!")
                            st.rerun()
                        else:
                            st.error("Nama proyek wajib diisi!")
            
            # List Proyek untuk Edit / Hapus
            st.markdown("#### Daftar Proyek Saat Ini")
            for p in daftar_proyek:
                p_id, p_nama, p_deskripsi, p_gambar, p_teknologi, p_link = p
                with st.container():
                    st.markdown(f"**{p_nama}**")
                    col_edit, col_del = st.columns([1, 1])
                    
                    with col_edit:
                        with st.expander(f"✏️ Edit '{p_nama}'"):
                            with st.form(f"form_edit_{p_id}"):
                                edit_nama = st.text_input("Nama Proyek", value=p_nama)
                                edit_desc = st.text_area("Deskripsi", value=p_deskripsi)
                                edit_gambar = st.text_input("Gambar/URL", value=p_gambar)
                                edit_tech = st.text_input("Teknologi", value=p_teknologi)
                                edit_link = st.text_input("Link", value=p_link)
                                submit_edit = st.form_submit_button("Update Proyek")
                                
                                if submit_edit:
                                    update_proyek(p_id, edit_nama, edit_desc, edit_gambar, edit_tech, edit_link)
                                    st.success("Diupdate!")
                                    st.rerun()
                                    
                    with col_del:
                        if st.button(f"🗑️ Hapus '{p_nama}'", key=f"del_p_{p_id}"):
                            hapus_proyek(p_id)
                            st.rerun()
                    st.divider()
                    
        # --- TAB SERTIFIKAT ---
        with tab2:
            st.subheader("Data Sertifikasi")
            daftar_sertifikat = get_semua_sertifikat()
            
            with st.expander("➕ Tambah Sertifikat Baru"):
                with st.form("form_tambah_sert"):
                    s_nama = st.text_input("Nama Sertifikat")
                    s_penerbit = st.text_input("Penerbit (Issuer)")
                    s_tahun = st.number_input("Tahun", min_value=1990, max_value=2050, value=2026, step=1)
                    s_desc = st.text_area("Deskripsi Singkat")
                    s_gambar = st.text_input("Nama File Gambar / URL (Opsional)")
                    s_link = st.text_input("Link Sertifikat / Bukti")
                    s_submit = st.form_submit_button("Simpan Sertifikat")
                    
                    if s_submit:
                        if s_nama:
                            tambah_sertifikat(s_nama, s_penerbit, s_tahun, s_desc, s_gambar, s_link)
                            st.success("Sertifikat ditambahkan!")
                            st.rerun()
                        else:
                            st.error("Nama sertifikat wajib diisi!")
                            
            st.markdown("#### Daftar Sertifikat Saat Ini")
            for s in daftar_sertifikat:
                s_id, s_nama, s_penerbit, s_tahun, s_desc, s_gambar, s_link = s
                with st.container():
                    st.markdown(f"**{s_nama} ({s_tahun})** - {s_penerbit}")
                    c_edit, c_del = st.columns([1, 1])
                    
                    with c_edit:
                        with st.expander(f"✏️ Edit '{s_nama}'"):
                            with st.form(f"form_edit_s_{s_id}"):
                                e_nama = st.text_input("Nama Sertifikat", value=s_nama)
                                e_penerbit = st.text_input("Penerbit", value=s_penerbit)
                                e_tahun = st.number_input("Tahun", value=s_tahun)
                                e_desc = st.text_area("Deskripsi", value=s_desc)
                                e_gambar = st.text_input("Gambar", value=s_gambar)
                                e_link = st.text_input("Link", value=s_link)
                                e_submit = st.form_submit_button("Update Sertifikat")
                                
                                if e_submit:
                                    update_sertifikat(s_id, e_nama, e_penerbit, e_tahun, e_desc, e_gambar, e_link)
                                    st.success("Diupdate!")
                                    st.rerun()
                                    
                    with c_del:
                        if st.button(f"🗑️ Hapus '{s_nama}'", key=f"del_s_{s_id}"):
                            hapus_sertifikat(s_id)
                            st.rerun()
                    st.divider()

if __name__ == '__main__':
    inisialisasi_db()
