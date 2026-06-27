import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace multiple spaces before HTML tags
content = re.sub(r'^[ \t]+(<div)', r'\1', content, flags=re.MULTILINE)
content = re.sub(r'^[ \t]+(<h4)', r'\1', content, flags=re.MULTILINE)
content = re.sub(r'^[ \t]+(<p)', r'\1', content, flags=re.MULTILINE)
content = re.sub(r'^[ \t]+({)', r'\1', content, flags=re.MULTILINE)
content = re.sub(r'^[ \t]+(</div)', r'\1', content, flags=re.MULTILINE)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Indentation fixed!")
