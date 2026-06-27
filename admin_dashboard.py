import streamlit as st
import pandas as pd
import os

EXCEL_FILE = "ecv_data.xlsx"

def load_data():
    try:
        return pd.read_excel(EXCEL_FILE, sheet_name=None)
    except Exception as e:
        st.error(f"Gagal memuat {EXCEL_FILE}: {e}")
        return None

def save_data(all_dfs):
    try:
        with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl") as writer:
            for sheet_name, df in all_dfs.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        st.success("Semua perubahan berhasil disimpan ke Excel secara permanen!")
    except Exception as e:
        st.error(f"Gagal menyimpan ke {EXCEL_FILE}: {e}")

def inisialisasi_db():
    # Deprecated: SQLite no longer used
    pass

def show_admin_panel():
    st.markdown("""
    <style>
    /* Styling khusus untuk Radio Button agar seperti menu sidebar vertikal modern */
    [data-testid="stRadio"] > div {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    [data-testid="stRadio"] label {
        background-color: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 12px 16px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    [data-testid="stRadio"] label:hover {
        background-color: rgba(56, 189, 248, 0.1);
        border-color: rgba(56, 189, 248, 0.3);
        transform: translateX(4px);
    }
    
    /* Login Box Container */
    .login-container {
        max-width: 400px;
        margin: 40px auto;
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    if "admin_logged_in" not in st.session_state:
        st.session_state["admin_logged_in"] = False
        
    if not st.session_state["admin_logged_in"]:
        st.markdown("<h2 style='text-align: center; margin-bottom: 5px; color: white;'>🔐 Portal Admin</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94a3b8; margin-bottom: 20px;'>Masuk untuk mengelola portofolio</p>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Masuk Sekarang", use_container_width=True)
                
                if submitted:
                    if username == "admin" and password == "rahasia123":
                        st.session_state["admin_logged_in"] = True
                        st.rerun()
                    else:
                        st.error("Kredensial tidak valid!")
    else:
        # Header Admin Terlogin
        col_header1, col_header2 = st.columns([4, 1])
        with col_header1:
            st.markdown("<h2 style='margin: 0; color: white;'>⚡ Enterprise Workspace</h2>", unsafe_allow_html=True)
            st.caption("Kelola seluruh data portofolio (CRUD) secara dinamis.")
        with col_header2:
            if st.button("🚪 Keluar", use_container_width=True):
                st.session_state["admin_logged_in"] = False
                st.rerun()
            
        st.divider()
        
        all_dfs = load_data()
        if all_dfs:
            sheet_names = list(all_dfs.keys())
            
            # Membagi layar menjadi 2 kolom (Sidebar Kustom & Ruang Kerja)
            col_nav, col_workspace = st.columns([1, 3.5], gap="large")
            
            with col_nav:
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba(56,189,248,0.1) 0%, rgba(168,85,247,0.1) 100%); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 15px; margin-bottom: 20px;">
                    <h4 style="margin: 0; color: #f8fafc; font-size: 1.1rem; display: flex; align-items: center; gap: 8px;">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
                        Navigasi Data
                    </h4>
                </div>
                """, unsafe_allow_html=True)
                
                selected_sheet = st.radio("Pilih Sheet:", sheet_names, label_visibility="collapsed")
            
            with col_workspace:
                st.markdown(f"""
                <div style="display: flex; align-items: baseline; gap: 10px; margin-bottom: 10px;">
                    <h3 style='margin: 0; color: white;'>📄 Lembar Kerja:</h3>
                    <h3 style='margin: 0; color: #a855f7;'>{selected_sheet}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                st.info("💡 **Tips:** Klik dua kali pada sel tabel untuk mengubah data. Tekan baris kosong di bagian bawah tabel untuk menambah data baru. Seleksi baris lalu tekan tombol `Delete` pada keyboard untuk menghapus (CRUD).")
                
                # Container berbayang untuk tabel
                edited_df = st.data_editor(
                    all_dfs[selected_sheet], 
                    num_rows="dynamic",
                    use_container_width=True,
                    key=f"editor_{selected_sheet}",
                    height=500
                )
                
                st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                if st.button(f"💾 Simpan Perubahan ke Database ({selected_sheet})", type="primary", use_container_width=True):
                    # Update only the edited sheet in the dictionary
                    all_dfs[selected_sheet] = edited_df
                    save_data(all_dfs)
