import streamlit as st
import sqlite3
import base64
import os

def get_image_src(image_path):
    if not image_path:
        return ""
    if image_path.startswith("http://") or image_path.startswith("https://") or image_path.startswith("data:"):
        return image_path
    try:
        with open(image_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            ext = os.path.splitext(image_path)[1][1:].lower()
            if ext == "jpg": ext = "jpeg"
            return f"data:image/{ext};base64,{b64}"
    except Exception:
        return ""

import admin_dashboard

# Ensure database tables exist
admin_dashboard.inisialisasi_db()



# --- 3. CUSTOM STYLING (CSS) ---
st.markdown("""
<style>
/* Import Google Fonts & FontAwesome */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

/* Apply font to text elements only, avoiding overriding material icons */
html, body, p, h1, h2, h3, h4, h5, h6, label, a, li, button, input, textarea {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Glassmorphic Profile Sidebar & Custom Container */
[data-testid="stSidebar"] {
    background-color: var(--secondary-background-color);
    border-right: 1px solid rgba(128, 128, 128, 0.1);
}

/* Custom cards */
.custom-card {
    background-color: var(--secondary-background-color);
    border: 1px solid rgba(128, 128, 128, 0.15);
    border-radius: 12px;
    padding: 22px;
    margin-bottom: 16px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    display: flex;
    flex-direction: column;
    height: 100%;
}
.card-img {
    width: 100%;
    height: 180px;
    object-fit: cover;
    border-radius: 8px;
    margin-bottom: 16px;
}
.card-tech-badge {
    display: inline-block;
    background-color: rgba(128, 128, 128, 0.1);
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-right: 6px;
    margin-bottom: 10px;
}
.card-btn {
    display: inline-block;
    background-color: var(--primary-color);
    color: white !important;
    text-decoration: none !important;
    padding: 8px 16px;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-top: auto;
    text-align: center;
    transition: background-color 0.2s ease;
}
.card-btn:hover {
    background-color: #1d4ed8;
}
.custom-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    border-color: var(--primary-color);
}

/* Featured Card for Klinik Afsan */
.featured-card {
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.08) 0%, rgba(147, 51, 234, 0.08) 100%);
    border: 2px solid var(--primary-color);
    border-radius: 16px;
    padding: 26px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 10px 20px -5px rgba(37, 99, 235, 0.15);
    transition: all 0.3s ease;
}
.featured-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 25px -5px rgba(37, 99, 235, 0.25);
}
.featured-badge {
    position: absolute;
    top: 12px;
    right: 12px;
    background-color: var(--primary-color);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* Tech Pill Style */
.tech-pill {
    display: inline-block;
    background-color: rgba(37, 99, 235, 0.08);
    color: var(--primary-color);
    padding: 6px 14px;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-right: 8px;
    margin-bottom: 8px;
    border: 1px solid rgba(37, 99, 235, 0.15);
    transition: all 0.2s ease;
}
.tech-pill:hover {
    background-color: var(--primary-color);
    color: white;
    transform: scale(1.05);
}

/* Modern Hoverable Contact Info Badge */
.contact-item {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
    font-size: 0.95rem;
    padding: 10px 15px;
    border-radius: 8px;
    background-color: rgba(128, 128, 128, 0.05);
    border: 1px solid rgba(128, 128, 128, 0.1);
    transition: all 0.2s ease;
}
.contact-item:hover {
    border-color: var(--primary-color);
    background-color: rgba(37, 99, 235, 0.05);
    transform: translateX(4px);
}
.contact-icon {
    font-size: 1.25rem;
}
.contact-link {
    color: var(--text-color) !important;
    text-decoration: none !important;
    font-weight: 600 !important;
    flex-grow: 1;
    transition: color 0.2s ease;
}
.contact-item:hover .contact-link {
    color: var(--primary-color) !important;
}

/* Gradient text for headers */
.gradient-text {
    background: linear-gradient(90deg, var(--primary-color) 0%, #a855f7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)


# --- 4. SIDEBAR PANEL (IDENTITAS & NAVIGASI) ---
# Tampilkan Foto Profil jika ada
try:
    st.sidebar.image("profile.png", use_container_width=True)
except Exception:
    # Tampilkan avatar inisial jika gambar tidak termuat
    st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 1.5rem; margin-top: 1rem;">
        <div style="width: 130px; height: 130px; border-radius: 50%; background-color: var(--primary-color); color: white; display: inline-flex; align-items: center; justify-content: center; font-size: 2.8rem; font-weight: bold; margin: 0 auto;">
            AA
        </div>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("<h3 style='text-align: center; margin-bottom: 2px;'>Alif Amunawwar</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; font-style: italic; color: gray; margin-top: 0px; margin-bottom: 20px;'>Fullstack Developer</p>", unsafe_allow_html=True)

st.sidebar.divider()

# Check for admin parameter in URL
is_admin_mode = st.query_params.get("admin") == "true"

if is_admin_mode:
    st.sidebar.markdown("<p style='font-size: 0.85rem; font-weight: 600; color: gray; margin-bottom: 8px;'>NAVIGASI UTAMA</p>", unsafe_allow_html=True)
    menu = st.sidebar.radio("Pilih Halaman:", ["CV & Portofolio (Publik)", "Admin Panel (Privat)"], label_visibility="collapsed")
else:
    menu = "CV & Portofolio (Publik)"


# --- 5. HALAMAN PUBLIK ---
if menu == "CV & Portofolio (Publik)":
    # Hero Section
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2.5rem; margin-top: 1.5rem;">
        <div style="background-color: rgba(37, 99, 235, 0.1); display: inline-block; padding: 6px 16px; border-radius: 20px; color: var(--primary-color); font-weight: 700; margin-bottom: 15px; font-size: 0.9rem; border: 1px solid rgba(37, 99, 235, 0.2);">
            <i class="fas fa-rocket" style="margin-right: 6px;"></i> SISTECH Portfolio Expo 2026
        </div>
        <h1 style="font-size: 3rem; font-weight: 800; margin-bottom: 0.5rem; line-height: 1.2;">
            <span class="gradient-text">Alif Amunawwar</span>
        </h1>
        <p style="font-size: 1.25rem; font-weight: 600; color: gray; letter-spacing: 0.5px; margin-bottom: 5px;">
            Information Systems Student & Fullstack Developer
        </p>
        <p style="font-size: 1.05rem; font-style: italic; color: var(--primary-color); font-weight: 500;">
            "Empowering Future Digital Professionals"
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_dl1, col_dl2, col_dl3 = st.columns([1, 1, 1])
    with col_dl2:
        try:
            with open("cv_alif_amunawwar.pdf", "rb") as pdf_file:
                st.download_button(
                    label="📄 Download CV PDF",
                    data=pdf_file,
                    file_name="cv_alif_amunawwar.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        except FileNotFoundError:
            pass
            
    st.markdown("<div style='margin-bottom: 2.5rem;'></div>", unsafe_allow_html=True)
    
    # About Me Section
    st.markdown("""
    <div class="custom-card" style="margin-bottom: 2.5rem;">
        <h3 style="margin-top: 0; color: var(--primary-color); font-weight: 700; margin-bottom: 10px;">👨‍💻 About Me</h3>
        <p style="font-size: 1rem; line-height: 1.6; margin-bottom: 0; opacity: 0.95;">
            Saya adalah mahasiswa Sistem Informasi semester 4 yang fokus pada pengembangan backend 
            menggunakan framework Laravel dan Python, serta memiliki minat mendalam pada optimasi database. 
            Saya berdedikasi untuk menciptakan arsitektur kode yang bersih, aman, dan efisien untuk mendukung performa sistem terbaik.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Grid 2 Kolom untuk Kontak & Tech Stack
    col_profile, col_tech = st.columns([1, 1], gap="medium")
    
    with col_profile:
        st.subheader("📌 Kontak & Sosial Media")
        st.markdown("""
        <div class="custom-card" style="height: calc(100% - 20px);">
            <div class="contact-item">
                <span class="contact-icon"><i class="fab fa-whatsapp"></i></span>
                <a href="https://wa.me/62881011515321" target="_blank" class="contact-link">0881-0115-15321</a>
            </div>
            <div class="contact-item">
                <span class="contact-icon"><i class="fas fa-envelope"></i></span>
                <a href="mailto:alifamunawwar16@gmail.com" class="contact-link">alifamunawwar16@gmail.com</a>
            </div>
            <div class="contact-item">
                <span class="contact-icon"><i class="fab fa-github"></i></span>
                <a href="https://github.com/alip2216" target="_blank" class="contact-link">alip2216</a>
            </div>
            <div class="contact-item">
                <span class="contact-icon"><i class="fab fa-instagram"></i></span>
                <a href="https://instagram.com/alfanwwar_" target="_blank" class="contact-link">@alfanwwar_</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_tech:
        st.subheader("🛠️ Tech Stack & Keahlian")
        st.markdown("""
        <div class="custom-card" style="height: calc(100% - 20px);">
            <p style="font-size: 0.9rem; font-weight: 600; margin-bottom: 15px; color: gray;">
                Teknologi yang biasa saya gunakan dalam pengembangan software:
            </p>
            <div style="display: flex; flex-wrap: wrap;">
                <span class="tech-pill">Laravel 12</span>
                <span class="tech-pill">Python</span>
                <span class="tech-pill">Streamlit</span>
                <span class="tech-pill">MySQL</span>
                <span class="tech-pill">SQLite</span>
                <span class="tech-pill">AJAX</span>
                <span class="tech-pill">SweetAlert2</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.divider()
    
    # Proyek Utama (Featured Project)
    st.subheader("🔥 Proyek Utama")
    st.markdown("""
    <div class="featured-card">
        <span class="featured-badge">PROYEK UTAMA</span>
        <h3 style="margin-top: 5px; color: var(--primary-color); font-weight: 800; font-size: 1.6rem; margin-bottom: 4px;">Klinik Afsan</h3>
        <p style="font-weight: 600; font-size: 1.05rem; margin-bottom: 12px; color: var(--text-color); opacity: 0.8;">Sistem ERP & Antrean Klinik Real-time berbasis Laravel 12</p>
        <p style="font-size: 0.95rem; line-height: 1.6; color: var(--text-color); opacity: 0.95;">
            Klinik Afsan adalah sistem Enterprise Resource Planning (ERP) klinik komprehensif yang dirancang untuk mengotomatisasi
            seluruh alur kerja operasional klinik medis. Dilengkapi fitur manajemen antrean pasien secara real-time,
            rekam medis digital (EMR), manajemen inventaris obat terintegrasi, dan laporan analitik keuangan klinik yang dinamis.
        </p>
        <div style="margin-top: 18px; display: flex; flex-wrap: wrap; gap: 8px;">
            <span style="background-color: var(--primary-color); color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.75rem; font-weight:600;">Laravel 12</span>
            <span style="background-color: var(--primary-color); color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.75rem; font-weight:600;">MySQL</span>
            <span style="background-color: var(--primary-color); color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.75rem; font-weight:600;">AJAX & Realtime</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Portofolio Proyek (Dinamis dari Database)
    st.subheader("🗂️ Portofolio Proyek Lainnya")
    daftar_proyek = admin_dashboard.get_semua_proyek()
    
    if not daftar_proyek:
        st.info("Belum ada proyek lain di portofolio.")
    else:
        # Tampilkan dalam grid 2 kolom
        for i in range(0, len(daftar_proyek), 2):
            col1, col2 = st.columns(2, gap="medium")
            
            # Kolom 1
            if i < len(daftar_proyek):
                p_id, p_nama, p_deskripsi, p_gambar, p_teknologi, p_link = daftar_proyek[i]
                with col1:
                    src_url = get_image_src(p_gambar)
                    gambar_html = f'<img src="{src_url}" class="card-img">' if src_url else ''
                    tech_html = ''.join([f'<span class="card-tech-badge">{t.strip()}</span>' for t in p_teknologi.split(',') if t.strip()]) if p_teknologi else ''
                    link_html = f'<a href="{p_link}" target="_blank" class="card-btn">Lihat Proyek <i class="fas fa-external-link-alt" style="margin-left:5px;"></i></a>' if p_link else ''
                    
                    st.markdown(f"""
                    <div class="custom-card">
                        {gambar_html}
                        <h4 style="margin-top: 0; color: var(--primary-color); font-weight: 700; margin-bottom: 8px;">{p_nama}</h4>
                        <div style="margin-bottom: 12px;">{tech_html}</div>
                        <p style="font-size: 0.9rem; line-height: 1.5; margin-bottom: 15px; opacity: 0.95; flex-grow: 1;">{p_deskripsi}</p>
                        <div style="margin-top: auto;">{link_html}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Kolom 2
            if i + 1 < len(daftar_proyek):
                p_id, p_nama, p_deskripsi, p_gambar, p_teknologi, p_link = daftar_proyek[i+1]
                with col2:
                    src_url = get_image_src(p_gambar)
                    gambar_html = f'<img src="{src_url}" class="card-img">' if src_url else ''
                    tech_html = ''.join([f'<span class="card-tech-badge">{t.strip()}</span>' for t in p_teknologi.split(',') if t.strip()]) if p_teknologi else ''
                    link_html = f'<a href="{p_link}" target="_blank" class="card-btn">Lihat Proyek <i class="fas fa-external-link-alt" style="margin-left:5px;"></i></a>' if p_link else ''
                    
                    st.markdown(f"""
                    <div class="custom-card">
                        {gambar_html}
                        <h4 style="margin-top: 0; color: var(--primary-color); font-weight: 700; margin-bottom: 8px;">{p_nama}</h4>
                        <div style="margin-bottom: 12px;">{tech_html}</div>
                        <p style="font-size: 0.9rem; line-height: 1.5; margin-bottom: 15px; opacity: 0.95; flex-grow: 1;">{p_deskripsi}</p>
                        <div style="margin-top: auto;">{link_html}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
    st.divider()
    
    # Sertifikasi (Dinamis dari Database)
    st.subheader("📜 Lisensi & Sertifikasi")
    daftar_sertifikat = admin_dashboard.get_semua_sertifikat()
    
    if not daftar_sertifikat:
        st.info("Belum ada sertifikasi.")
    else:
        for i in range(0, len(daftar_sertifikat), 2):
            col1, col2 = st.columns(2, gap="medium")
            
            if i < len(daftar_sertifikat):
                s_id, s_nama, s_penerbit, s_tahun, s_desc, s_gambar, s_link = daftar_sertifikat[i]
                with col1:
                    src_url = get_image_src(s_gambar) if s_gambar else ""
                    img_html = f'<img src="{src_url}" class="card-img" style="height: 140px;">' if src_url else ''
                    link_html = f'<a href="{s_link}" target="_blank" class="card-btn" style="background-color: #0f172a;">Lihat Sertifikat <i class="fas fa-certificate" style="margin-left:5px;"></i></a>' if s_link else ''
                    
                    st.markdown(f"""
                    <div class="custom-card" style="border-top: 4px solid var(--primary-color);">
                        {img_html}
                        <h4 style="margin-top: 0; color: var(--text-color); font-weight: 700; margin-bottom: 4px;">{s_nama}</h4>
                        <p style="font-weight: 600; font-size: 0.9rem; color: var(--primary-color); margin-bottom: 12px;">{s_penerbit} • {s_tahun}</p>
                        <p style="font-size: 0.9rem; line-height: 1.5; margin-bottom: 15px; opacity: 0.95; flex-grow: 1;">{s_desc}</p>
                        <div style="margin-top: auto;">{link_html}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
            if i + 1 < len(daftar_sertifikat):
                s_id, s_nama, s_penerbit, s_tahun, s_desc, s_gambar, s_link = daftar_sertifikat[i+1]
                with col2:
                    src_url = get_image_src(s_gambar) if s_gambar else ""
                    img_html = f'<img src="{src_url}" class="card-img" style="height: 140px;">' if src_url else ''
                    link_html = f'<a href="{s_link}" target="_blank" class="card-btn" style="background-color: #0f172a;">Lihat Sertifikat <i class="fas fa-certificate" style="margin-left:5px;"></i></a>' if s_link else ''
                    
                    st.markdown(f"""
                    <div class="custom-card" style="border-top: 4px solid var(--primary-color);">
                        {img_html}
                        <h4 style="margin-top: 0; color: var(--text-color); font-weight: 700; margin-bottom: 4px;">{s_nama}</h4>
                        <p style="font-weight: 600; font-size: 0.9rem; color: var(--primary-color); margin-bottom: 12px;">{s_penerbit} • {s_tahun}</p>
                        <p style="font-size: 0.9rem; line-height: 1.5; margin-bottom: 15px; opacity: 0.95; flex-grow: 1;">{s_desc}</p>
                        <div style="margin-top: auto;">{link_html}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # Footer Section (Value-Sell Backend CMS)
    st.markdown("""
    <div style="text-align: center; margin-top: 3.5rem; margin-bottom: 1.5rem; padding: 15px; border-radius: 8px; background-color: rgba(128, 128, 128, 0.05); border: 1px dashed rgba(128, 128, 128, 0.2);">
        <p style="font-size: 0.85rem; color: gray; margin: 0; line-height: 1.5;">
            💻 <b>Developer Insights:</b> Website portofolio ini bersifat <b>dinamis</b>. Dibangun secara mandiri menggunakan 
            <b>Python, Streamlit, dan SQLite</b>, lengkap dengan sistem manajemen konten (CMS) di balik <b>Admin Panel</b> 
            untuk pengelolaan data proyek secara real-time.
        </p>
    </div>
    """, unsafe_allow_html=True)


# --- 6. HALAMAN ADMIN (PRIVAT) ---
elif menu == "Admin Panel (Privat)":
    admin_dashboard.show_admin_panel()
