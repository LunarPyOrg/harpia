PREFIX ?= ${HOME}/.local

all:
	@mkdir -p ${DESTDIR}${PREFIX}/bin
	@cp -p harpia.py ${DESTDIR}${PREFIX}/bin/harpia
	@mkdir -p ${HOME}/.config/harpia/
	@cp token_sample.ini ${HOME}/.config/harpia/token.ini
