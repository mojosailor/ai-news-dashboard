import re
from pathlib import Path

INDEX_PATH = Path('html/index.html')
REPORT_PATH = Path('scripts/new_report_block.txt')

html = INDEX_PATH.read_text(encoding='utf-8')
new_report_text = REPORT_PATH.read_text(encoding='utf-8')

pattern = re.compile(r'const REPORT = \{.*?\n\};\n', re.DOTALL)
matches = pattern.findall(html)
assert len(matches) == 1, f'expected 1 REPORT block, found {len(matches)}'
assert 'TAG_META' not in matches[0], 'pattern over-matched into TAG_META'

new_html = html.replace(matches[0], new_report_text, 1)
INDEX_PATH.write_text(new_html, encoding='utf-8')
print('REPORT block swapped successfully')
