import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

site = Path(r'C:\Users\max\Desktop\сайт')
FILES = ['index.html','briquettes.html','about.html','contacts.html','production.html']

FIX = """<style>/* fix top offset vs original */
.M63kCb, .p9b27 { top: 0px !important; }
</style>
</head>"""

for f in FILES:
    p = site / f
    html = p.read_text(encoding='utf-8')
    if '.M63kCb' in html and 'top: 0px !important' not in html:
        # insert before </head>
        if '</head>' in html:
            html = html.replace('</head>', FIX, 1)
            p.write_text(html, encoding='utf-8')
            print(f"FIXED: {f}")
        else:
            print(f"NO </head> in {f}")
    else:
        print(f"SKIP (already or no M63kCb): {f}")
