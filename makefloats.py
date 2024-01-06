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

	position = meta['position'] if 'position' in meta else ''

	if 'sidecaption' not in meta:
		return f"""\\begin{{figure}}[{position}]
\\center
\\includegraphics[{shapestr}]{{input/{meta['name']}}}\\\\
\\caption{{
{caption}
}}
\\label{{{meta['label']}}}
\\end{{figure}}
"""
	else:
		sidecaptionwidth = float(meta['sidecaptionwidth']) if 'sidecaptionwidth' in meta else 0.5
		if meta['sidecaption'] in ['right', 'r']:
			return f"""\\begin{{figure}}[{position}]
\\begin{{minipage}}{{{0.95-sidecaptionwidth}\\textwidth}}
\\includegraphics[{shapestr}]{{input/{meta['name']}}}
\\end{{minipage}}
\\hfill
\\begin{{minipage}}{{{sidecaptionwidth}\\textwidth}}
\\caption{{
{caption}
}}
\\label{{{meta['label']}}}
\\end{{minipage}}
\\end{{figure}}
"""
		elif meta['sidecaption'] in ['left', 'l']:
			return f"""\\begin{{figure}}[{position}]
\\begin{{minipage}}{{{sidecaptionwidth}\\textwidth}}
\\caption{{
{caption}
}}
\\label{{{meta['label']}}}
\\end{{minipage}}
\\hfill
\\begin{{minipage}}{{{0.95-sidecaptionwidth}\\textwidth}}
\\includegraphics[{shapestr}]{{input/{meta['name']}}}
\\end{{minipage}}
\\end{{figure}}
"""
	raise Error(f"Failed to make figure \"{meta['name']}\".")

def maketable(lines):
	meta = tomllib.load(BytesIO(''.join(lines).encode()))

	subprocess.run(['pandoc', f"src/tables/{meta['name']}.md", '-o', 'tmp/caption.tex'])
	
	with open('tmp/caption.tex') as fid:
		caption = fid.read().strip()

	try:
		shutil.copyfile(f"src/tables/{meta['name']}.pdf", f"tex/input/{meta['name']}.pdf")

		wstr = f"width={meta['width']}" if 'width' in meta else ""
		hstr = f"height={meta['height']}" if 'height' in meta else ""
		shapestr = ','.join([_ for _ in [wstr, hstr] if _])

		return f"""\\begin{{table}}[{meta['position']}]
\\center
\\includegraphics[{shapestr}]{{input/{meta['name']}}}\\\\
\\caption{{
{caption}
}}
\\label{{{meta['label']}}}
\\end{{table}}
"""

	except FileNotFoundError:
		with open(f"src/tables/{meta['name']}.tex") as fid:
			latextable = fid.read().strip()

		fontsize = meta['fontsize'] if 'fontsize' in meta else 'small'
		
		return f"""\\begin{{table}}[{meta['position']}]
\\center
\\{fontsize}
{latextable}
\\caption{{
{caption}
}}
\\label{{{meta['label']}}}
\\end{{table}}
"""
		

	return ""
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

while True:
	for k,l in enumerate(lines):
		if l.startswith('%%% table'):
			kstart = k
		elif l.startswith('%%% end-table'):
			kstop = k
			break
	else:
		break
	lines = lines[:kstart] + [maketable(lines[kstart+1:kstop])] + lines[kstop+1:]

out = ''.join(lines)

with open('src/substitutions.txt') as fid:
	substitutions = [_.strip().split('\t') for _ in fid.readlines()]
for s in substitutions:
	out = out.replace(*s)

with open('tmp/body_withfloats.md', 'w') as fid:
	fid.write(out)