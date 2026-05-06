from pathlib import Path

path = Path('html/archive/2026-05-06.html')
html = path.read_text(encoding='utf-8')

# 1) Brand span suffix
html = html.replace('Prevwind · Project Flux</span>', 'Prevwind · Project Flux · Archived</span>')

# 2) Header right-nav: replace Archive button with Latest + Archive
html = html.replace(
    '<a class="archive-link" href="archive/" title="Browse archive">',
    '<a class="archive-link" href="../" title="Back to latest">\n'
    '      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/></svg>\n'
    '      Latest\n'
    '    </a>\n'
    '    <a class="archive-link" href="index.html" title="Browse archive">'
)

# 3) Insert archive banner immediately after </header>
banner = (
    '\n<div class="archive-banner">\n'
    '  Viewing archived report. <a href="../" style="color:var(--both)">Go to today\'s dashboard</a> '
    'or <a href="index.html" style="color:var(--both)">browse all archives</a>.\n'
    '</div>\n'
)
if '</header>' in html and 'archive-banner' not in html:
    html = html.replace('</header>\n', '</header>\n' + banner, 1)

# 4) Add .archive-banner CSS rule before #report-date
css_rule = (
    '  .archive-banner {\n'
    '    max-width: 1100px;\n'
    '    margin: -8px auto 20px;\n'
    '    padding: 10px 14px;\n'
    '    background: var(--surface);\n'
    '    border: 1px solid var(--border);\n'
    '    border-left: 3px solid var(--bonus);\n'
    '    border-radius: 6px;\n'
    '    color: var(--muted);\n'
    '    font-size: 12px;\n'
    '  }\n'
)
marker = '  #report-date {'
if marker in html and '.archive-banner' not in html:
    html = html.replace(marker, css_rule + marker, 1)

path.write_text(html, encoding='utf-8')
print('archive adjustments applied')
