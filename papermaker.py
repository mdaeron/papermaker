import shutil
import os
import pathlib
import sys
import tomllib
import subprocess
import io
import hashlib

def maketitle(
	toml_file = 'src/metadata.toml',
	tex_file = 'work/input/maketitle.tex',
	):

	with open(toml_file, 'rb') as fid:
		meta = tomllib.load(fid)

	for author in meta['author']:
		if 'affiliations' in author and isinstance(author['affiliations'], str):
			author['affiliations'] = [author['affiliations']]

	affiliationlist = []
	for author in meta['author']:
		for affiliation in author['affiliations']:
			if affiliation not in affiliationlist:
				if affiliation not in meta['affiliations']:
					raise KeyError(f'"{affiliation}" is not defined in [affiliations].')
				affiliationlist.append(affiliation)

	affiliationmarkers = {v: (k+1) for k,v in enumerate(affiliationlist)}
	
	with open(tex_file, 'w') as fid:
		fid.write(f"""{{
			\\raggedright
			\\sffamily
			{{\\huge\\bfseries
			{meta['title']}\\\\\\mbox{{}}
			}}\\\\
			\\vspace{{4mm}}""")

		authorlist = []
		for author in meta['author']:
			authorlist.append(author['name'])

			if 'corresponding' in author and author['corresponding']:
				authorlist[-1] += "\\,*"

			if 'affiliations' in author:

				authorlist[-1] += "\\textsuperscript{\\,("
				
				authorlist[-1] += '\\mbox{,}'.join([
					f"{affiliationmarkers[affiliation]}"
					for affiliation in author['affiliations']
					])

				authorlist[-1] += ")}"

			if 'orcid' in author:
				authorlist[-1] += f'\\,{{\\raisebox{{-0.07ex}}{{\\href{{https://orcid.org/{author["orcid"]}}}{{\\color{{white!67!black}}{{\\faOrcid}}}}}}}}'

			if 'email' in author:
				authorlist[-1] += f'\\,\\raisebox{{0ex}}{{\\href{{mailto:{author["email"]}}}{{\\color{{white!67!black}}{{\\faEnvelopeOpenText}}}}}}'


		authorstr = '\\,, '.join(authorlist)

		fid.write(f"""
			{{\\large
			{authorstr}
			}}\\\\
			\\vspace{{10mm}}
			""")

		if len([author for author in meta['author'] if 'corresponding' in author and author['corresponding']]) == 1:
			fid.write("""{\\footnotesize
				*{\\itshape corresponding author}\\\\\\vspace{1ex}""")

		elif len([author for author in meta['author'] if 'corresponding' in author and author['corresponding']]) > 1:
			fid.write("""{\\footnotesize
				*{\\itshape corresponding authors}\\\\\\vspace{1ex}""")

		for affiliation in affiliationmarkers:
			fid.write(f"""
				({affiliationmarkers[affiliation]}) {meta['affiliations'][affiliation]}\\\\""")


		fid.write("}")

		fid.write(f"\n}}")


def makefig(lines):
	meta = tomllib.load(io.BytesIO(''.join(lines).encode()))
	
	print(f'-> Make figure {meta["name"]}')

	subprocess.run(['pandoc', f"src/figures/{meta['name']}.md", '-o', 'work/caption.tex'])
	
	with open('work/caption.tex') as fid:
		caption = fid.read().strip()

	shutil.copyfile(f"src/figures/{meta['name']}.pdf", f"work/input/{meta['name']}.pdf")

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
	meta = tomllib.load(io.BytesIO(''.join(lines).encode()))

	print(f'-> Make table {meta["name"]}')

	subprocess.run(['pandoc', f"src/tables/{meta['name']}.md", '-o', 'work/caption.tex'])
	
	with open('work/caption.tex') as fid:
		caption = fid.read().strip()

	try:
		shutil.copyfile(f"src/tables/{meta['name']}.pdf", f"work/input/{meta['name']}.pdf")

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

def makefloats():
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

	print('-> Apply substitutions')

	with open('src/substitutions.txt') as fid:
		substitutions = [_.strip().split('\t') for _ in fid.readlines()]
	for s in substitutions:
		out = out.replace(*s)

	with open('work/body_withfloats.md', 'w') as fid:
		fid.write(out)


try:
	print('-> Delete old work dir')
	shutil.rmtree('work', ignore_errors = True)
except:
	sys.exit('Error: Could not delete old work dir.')

try:
	print('-> Create new work dir')
	os.mkdir('work')
	os.mkdir('work/input')
except:
	sys.exit('Error: Could not create new work dir.')

try:
	for g in pathlib.Path('./tex').glob('*.tex'):
		print(f'-> Copy {g} to work/{g.name}')
		shutil.copy(g, 'work')
except:
	sys.exit('Error: Could not copy tex template files.')

try:
	for g in pathlib.Path('./src').glob('*.tex'):
		print(f'-> Copy {g} to work/input/{g.name}')
		shutil.copy(g, 'work/input')
except:
	sys.exit('Error: Could not copy src/*.tex files.')

try:
	print('-> Copy src/refs.bib to work/input/refs.bib')
	shutil.copy('src/refs.bib', 'work/input/refs.bib')
except:
	sys.exit('Error: Could not copy refs.bib file.')

try:
	print('-> Create work/input/maketitle.tex')
	maketitle()
except:
	sys.exit('Error: Could not create maketitle.tex.')

try:
	print('-> Make floats')
	makefloats()
except:
	sys.exit('Error: Could not make floats.')

try:
	print('-> Convert body')
	subprocess.run(['pandoc', 'work/body_withfloats.md', '-o', 'work/input/body.tex'])
except:
	sys.exit('Error: Could not convert body.')

for content in [
	'contributions',
	'abstract',
	'reproducibility',
	'acknowledgements',
	]:
	try:
		if pathlib.Path(f'src/{content}.md').is_file():
			print(f'-> Convert {content}')
			subprocess.run(['pandoc', f'src/{content}.md', '-o', f'work/input/{content}.tex'])
	except:
		sys.exit(f'Error: Could not convert {content}.')

try:
	print('-> Run latexmk')
	subprocess.run(['latexmk', '-xelatex', '-quiet', 'article'], cwd = 'work')
except:
	sys.exit('Error: latexmk did not run successfully.')

try:
	print(f'-> Copy work/article.pdf to build/paper.pdf')
	shutil.copy('work/article.pdf', 'build/paper.pdf')
except:
	sys.exit('Error: Could not copy final output.')
