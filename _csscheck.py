import sys, re
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

html = Path(r'C:\Users\max\Desktop\сайт\index.html').read_text(encoding='utf-8')
print("style tags:", html.count('<style'))
print("rel=stylesheet count:", html.count('rel="stylesheet"'))
css_hrefs = re.findall(r'<link[^>]*stylesheet[^>]*href="([^"]+)"', html)
print("CSS hrefs:")
for h in css_hrefs:
    print("  ", h)
