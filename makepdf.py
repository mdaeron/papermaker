import shutil, subprocess, hashlib

newstate = '0'
oldstate = '1'

with open('hash.log', 'w') as logid:
	while newstate != oldstate:
		subprocess.run(['xelatex', 'article'])
# 		subprocess.run(['xelatex', '--interaction=batchmode', 'article', '2>&1', '>', 'xelatex.log'])
		subprocess.run(['biber', 'article', '--onlylog'])
		hasher = hashlib.md5()
		with open('article.out', 'rb') as fid:
			hasher.update(fid.read())
		oldstate = newstate
		newstate = hasher.hexdigest()
		logid.write(newstate + '\n')
