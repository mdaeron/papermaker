import tomllib

with open('src/metadata.toml', 'rb') as fid:
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


with open('tex/input/maketitle.tex', 'w') as fid:
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
  \\vspace{{10mm}}""")

	if len([author for author in meta['author'] if 'corresponding' in author and author['corresponding']]) == 1:
		fid.write("""
  {\\footnotesize
    *{\\itshape corresponding author}\\\\\\vspace{1ex}""")

	elif len([author for author in meta['author'] if 'corresponding' in author and author['corresponding']]) > 1:
		fid.write("""
  {\\small
    *{\\itshape corresponding authors}\\\\\\vspace{1ex}""")

	for affiliation in affiliationmarkers:
		fid.write(f"""
    ({affiliationmarkers[affiliation]}) {meta['affiliations'][affiliation]}\\\\""")


	fid.write("""
  }""")
	fid.write(f"\n}}")