import tomllib
import shutil
import subprocess
from io import StringIO, BytesIO

def makefig(lines):
	meta = tomllib.load(BytesIO(''.join(lines).encode()))

	subprocess.run(['pandoc', f"src/figures/{meta['name']}.md", '-o', 'tmp/caption.tex'])
	
	with open('tmp/caption.tex') as fid:
		caption = fid.read().strip()

	shutil.copyfile(f"src/figures/{meta['name']}.pdf", f"tex/input/{meta['name']}.pdf")

	wstr = f"width={meta['width']}" if 'width' in meta else ""
	hstr = f"height={meta['height']}" if 'height' in meta else ""
	shapestr = ','.join([_ for _ in [wstr, hstr] if _])	

	return f"""\\begin{{figure}}[{meta['position']}]
\\center
\\includegraphics[{shapestr}]{{input/{meta['name']}}}
\\caption{{
{caption}
}}
\\label{{{meta['label']}}}
\\end{{figure}}
"""

with open('src/body.md') as fid:
	lines = fid.readlines()

while True:
	for k,l in enumerate(lines):
		if l.startswith('%%% figure'):
			kstart = k
		elif l.startswith('%%% end-figure'):
			kstop = k
			break
	else:
		break
	lines = lines[:kstart] + [makefig(lines[kstart+1:kstop])] + lines[kstop+1:]

with open('tmp/body_withfloats.md', 'w') as fid:
	fid.write(''.join(lines))