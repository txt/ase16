F=$(shell find . -name '*.md')

typo:  ready
	@- git status
	@- git commit -am "saving"
	@- git push origin master

commit:  ready
	@- git status
	@- git commit -a
	@- git push origin master

update:; @- git pull origin master
status:; @- git status

ready: gitting prep

gitting:
	@git config --global credential.helper cache
	@git config credential.helper 'cache --timeout=3600'
	@git config --global user.email tim.menzies@gmail.com

timm:
	@git config --global user.name "Tim Menzies"

prep:
	@$(foreach f,$F, if [ "etc/header" -nt "$f" ]; then echo "# updating $f ... "; gawk -f etc/headers.awk $f > .tmp; mv .tmp $f; fi; )

prepping:
	@$(foreach f,$F, echo "# updating $f ... "; gawk -f etc/headers.awk $f > .tmp; mv .tmp $f;  )
