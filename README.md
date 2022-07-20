# Harpia Project

Harpia é um instalador feito em python
Foca principalmente em repositórios do Github

![Python Ver](https://img.shields.io/badge/Python-3.10-blue?style=flat-square)


## Importante
É necessário utilizar um token do github dentro de token.ini (com acesso à repositórios livres) para que o harpia funcione.
Caso faça o executável, seria interessante copiar o `token.ini` para `~/.config/harpia/token.ini`


### Uso
> utilizando python diretamente
```sh
$ python3 harpia.py <search ou install> package
```


### Uso com executável
> criação do executável
```sh
$ pyinstaller harpia.py --onefile
$ cd dist/
$ ./harpia <search ou install> package
```
