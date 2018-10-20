## Ubuntu 16.04.5 LTS (Xenial Xerus) - apenas ref

adicionar repositorio ppa ou nightly
```
apt-add-repository ppa:mutlaqja/ppa
apt-add-repository ppa:mutlaqja/indinightly
```

para reverter para pacotes oficiais
```
apt install ppa-purge

ppa-purge -y ppa:mutlaqja/ppa
rm -f /etc/apt/sources.list.d/mutlaqja-ubuntu-ppa-*

ppa-purge -y ppa:mutlaqja/indinightly
rm -f /etc/apt/sources.list.d/mutlaqja-ubuntu-indinightly-*
```

para remover pacotes oficiais
```
apt purge package
```

efetuar login com usuário que irá executar o pyindi-client
```
pip2  install --user --install-option="--prefix=/usr/local" pyindi-client
```

## Git
```
git clone https://github.com/mmastria/ha.git
cd ha
git config credential.helper store
git config --global user.email "marco@mastria.com.br"
git config --global user.name "mmastria"
git pull
git add *
git commit * -m "release"
git rm xxxx
git commit -m "release"
git push
```
