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
    st.markdown("<h2 style='color: var(--primary-color);'>🔐 Admin Panel (Excel Editor)</h2>", unsafe_allow_html=True)
    st.info("Halaman ini bersifat privat. Anda memiliki kontrol penuh terhadap file ecv_data.xlsx di sini.")
    
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
        st.markdown("### 🗃️ Enterprise Database Editor")
        st.caption("Kelola seluruh portofolio Anda melalui antarmuka profesional di bawah ini.")
        
        all_dfs = load_data()
        if all_dfs:
            sheet_names = list(all_dfs.keys())
            
            # Membagi layar menjadi 2 kolom (Sidebar Kustom & Ruang Kerja)
            col_nav, col_workspace = st.columns([1, 4], gap="large")
            
            with col_nav:
                st.markdown("""
                <div style="background-color: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 15px; margin-bottom: 20px;">
                    <h4 style="margin-top: 0; color: #38bdf8; font-size: 1.1rem;">🛠️ Navigasi Sheet</h4>
                    <p style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 10px;">Pilih tabel untuk diedit</p>
                </div>
                """, unsafe_allow_html=True)
                
                selected_sheet = st.radio("Pilih Sheet:", sheet_names, label_visibility="collapsed")
            
            with col_workspace:
                st.markdown(f"<h3 style='margin-top: 0; color: white;'>📄 Lembar Kerja: <span style='color: #a855f7;'>{selected_sheet}</span></h3>", unsafe_allow_html=True)
                st.caption("💡 Klik dua kali (double-click) pada sel tabel untuk mengubah data. Tekan tanda + di bawah tabel untuk menambah baris baru.")
                
                edited_df = st.data_editor(
                    all_dfs[selected_sheet], 
                    num_rows="dynamic",
                    use_container_width=True,
                    key=f"editor_{selected_sheet}",
                    height=450
                )
                
                st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                if st.button(f"💾 Simpan Perubahan pada '{selected_sheet}'", type="primary", use_container_width=True):
                    # Update only the edited sheet in the dictionary
                    all_dfs[selected_sheet] = edited_df
                    save_data(all_dfs)
