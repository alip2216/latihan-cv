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
        st.markdown("### 🗃️ Database Editor")
        st.caption("Klik dua kali pada sel untuk mengubah data. Anda juga dapat menambah atau menghapus baris di bagian bawah tabel.")
        
        all_dfs = load_data()
        if all_dfs:
            tabs = st.tabs(list(all_dfs.keys()))
            edited_dfs = {}
            
            for i, (sheet_name, df) in enumerate(all_dfs.items()):
                with tabs[i]:
                    st.markdown(f"**Manajemen Sheet:** `{sheet_name}`")
                    # data_editor returns a new dataframe with the edits applied
                    edited_dfs[sheet_name] = st.data_editor(
                        df, 
                        num_rows="dynamic",
                        use_container_width=True,
                        key=f"editor_{sheet_name}",
                        height=400
                    )
            
            st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
            if st.button("💾 Simpan Semua Perubahan", type="primary", use_container_width=True):
                save_data(edited_dfs)
