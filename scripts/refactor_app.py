import sys

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if line.startswith('    daftar_proyek = ambil_semua_proyek()'):
        new_lines.append('    daftar_proyek = admin_dashboard.get_semua_proyek()\n')
    elif line.startswith('# --- 6. HALAMAN ADMIN (PRIVAT) ---'):
        skip = True
        new_lines.append('# --- 6. HALAMAN ADMIN (PRIVAT) ---\n')
        new_lines.append('elif menu == "Admin Panel (Privat)":\n')
        new_lines.append('    admin_dashboard.show_admin_panel()\n')
        break
    else:
        new_lines.append(line)

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("app.py refactored successfully.")
