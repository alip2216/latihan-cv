from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Arial bold 24
        self.set_font('helvetica', 'B', 24)
        # Title
        self.cell(0, 10, 'ALIF AMUNAWWAR', 0, 1, 'C')
        # Subtitle
        self.set_font('helvetica', 'I', 12)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, 'Information Systems Student & Fullstack Developer', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_cv():
    pdf = PDF()
    pdf.add_page()
    
    # Contact Info
    pdf.set_font('helvetica', '', 10)
    pdf.set_text_color(0, 0, 0)
    contact_info = (
        "Phone: 0881-0115-15321 | Email: alifamunawwar16@gmail.com\n"
        "GitHub: github.com/alip2216 | Instagram: @alfanwwar_"
    )
    pdf.multi_cell(0, 6, contact_info, 0, 'C')
    pdf.ln(10)
    
    # About Me Section
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(37, 99, 235) # Blue color for headers
    pdf.cell(0, 8, 'ABOUT ME', 0, 1, 'L')
    pdf.set_draw_color(200, 200, 200)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(50, 50, 50)
    about_text = (
        "Saya adalah mahasiswa Sistem Informasi semester 4 yang fokus pada pengembangan backend "
        "menggunakan framework Laravel dan Python, serta memiliki minat mendalam pada optimasi database. "
        "Saya berdedikasi untuk menciptakan arsitektur kode yang bersih, aman, dan efisien untuk mendukung "
        "performa sistem terbaik."
    )
    pdf.multi_cell(0, 6, about_text)
    pdf.ln(8)
    
    # Tech Stack
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(0, 8, 'TECH STACK & SKILLS', 0, 1, 'L')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 6, "Laravel 12, Python, Streamlit, MySQL, SQLite, AJAX, SweetAlert2, Dart, Flutter, PHP, Bootstrap")
    pdf.ln(8)
    
    # Projects
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(0, 8, 'KEY PROJECTS', 0, 1, 'L')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    projects = [
        {
            "name": "Klinik Afsan",
            "tech": "Laravel 12, MySQL, AJAX & Realtime",
            "desc": "Sistem Enterprise Resource Planning (ERP) klinik komprehensif yang dirancang untuk mengotomatisasi seluruh alur kerja operasional klinik medis. Dilengkapi fitur manajemen antrean pasien secara real-time, rekam medis digital (EMR), manajemen inventaris obat terintegrasi, dan laporan analitik keuangan klinik yang dinamis."
        },
        {
            "name": "Afsan Mobile",
            "tech": "Dart, Flutter",
            "desc": "Aplikasi mobile yang terintegrasi dengan sistem Klinik Afsan untuk memudahkan pasien melakukan reservasi dan memantau antrean secara real-time."
        },
        {
            "name": "Sikahil Bootcamp",
            "tech": "PHP, Bootstrap, MySQL",
            "desc": "Platform pembelajaran web interaktif berbasis PHP. Menyediakan materi pemrograman dan sistem manajemen kelas untuk peserta secara terstruktur."
        }
    ]
    
    for proj in projects:
        pdf.set_font('helvetica', 'B', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 6, proj["name"], 0, 1, 'L')
        
        pdf.set_font('helvetica', 'I', 10)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 6, f'Tech: {proj["tech"]}', 0, 1, 'L')
        
        pdf.set_font('helvetica', '', 11)
        pdf.set_text_color(50, 50, 50)
        pdf.multi_cell(0, 6, proj["desc"])
        pdf.ln(4)
        
    pdf.output('cv_alif_amunawwar.pdf')

if __name__ == '__main__':
    create_cv()
