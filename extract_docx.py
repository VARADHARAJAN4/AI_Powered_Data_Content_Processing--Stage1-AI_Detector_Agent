from zipfile import ZipFile
from xml.etree import ElementTree as ET
from pathlib import Path

path = Path('complete flow.docx')
with ZipFile(path) as z:
    root = ET.fromstring(z.read('word/document.xml'))
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
texts = [t.text or '' for t in root.findall('.//w:t', ns)]
print('\n'.join(texts))
