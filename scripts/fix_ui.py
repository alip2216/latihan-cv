import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Tech Stack Title
content = content.replace(
    '<div style="text-align: center; margin-bottom: 15px;">',
    '<div style="text-align: center; margin-bottom: 35px; padding-top: 20px;">'
)

# 2. About Me Title
content = content.replace(
    '<h3 style="margin-top: 0; color: var(--primary-color); font-weight: 700; margin-bottom: 10px;">👨‍💻 About Me</h3>',
    '<h3 style="margin-top: 0; padding-top: 20px; color: var(--primary-color); font-weight: 700; margin-bottom: 30px;">👨‍💻 About Me</h3>'
)

# 3. Portofolio Proyek Lainnya
content = content.replace(
    'st.subheader("🗂️ Portofolio Proyek Lainnya")',
    'st.markdown("<h3 style=\'padding-top: 20px; margin-bottom: 30px; font-weight: 700; color: var(--primary-color);\'>🗂️ Portofolio Proyek Lainnya</h3>", unsafe_allow_html=True)'
)

# 4. Lisensi & Sertifikasi
content = content.replace(
    'st.subheader("📜 Lisensi & Sertifikasi")',
    'st.markdown("<h3 style=\'padding-top: 20px; margin-bottom: 30px; font-weight: 700; color: var(--primary-color);\'>📜 Lisensi & Sertifikasi</h3>", unsafe_allow_html=True)'
)

# 5. Deskripsi Proyek Color (make it brighter for accessibility)
# <p style="font-size: 0.9rem; line-height: 1.5; margin-bottom: 15px; opacity: 0.95; flex-grow: 1;">{p_deskripsi}</p>
content = content.replace(
    '<p style="font-size: 0.9rem; line-height: 1.5; margin-bottom: 15px; opacity: 0.95; flex-grow: 1;">{p_deskripsi}</p>',
    '<p style="font-size: 0.9rem; line-height: 1.5; margin-bottom: 15px; color: #f1f5f9; flex-grow: 1;">{p_deskripsi}</p>'
)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
