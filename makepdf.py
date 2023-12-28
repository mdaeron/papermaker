import shutil, subprocess, hashlib

newstate = '0'
oldstate = '1'

with open('hash.log', 'w') as logid:
	while newstate != oldstate:
		subprocess.run(['xelatex', 'main', '-halt-on-error'])
		subprocess.run(['biber', 'main'])
		hasher = hashlib.md5()
		with open('main.out', 'rb') as fid:
			hasher.update(fid.read())
		oldstate = newstate
		newstate = hasher.hexdigest()
		logid.write(newstate + '\n')
