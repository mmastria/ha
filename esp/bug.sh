#!/bin/bash

echo .
echo ............................
echo . alterar em cada projeto:
echo . \[common\]
echo . lib_deps =
echo .     AsyncTCP@\<1.1.0
echo ............................

find . -type d -name AsyncTCP_ID1826|grep -v \/lib|xargs -n 1 rm -rf

for i in $(find ./config -type f -maxdepth 2 -name platformio.ini)
do
[ $(grep 'AsyncTCP@<1.1.0' ${i} |wc -l) = 0 ] && \
sed -i -e '/lib_deps =/ a\'$'\n''\ \ \ \ AsyncTCP@<1.1.0'$'\n''' ${i}
done

find . -name platformio.ini-e -exec rm {} \;

[ $(grep 'partitions' config/.gitignore|wc -l) = 0 ] && \
echo '**/partitions.csv' >> config/.gitignore
