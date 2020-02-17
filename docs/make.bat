call make-docs.bat html

cd _build/html
tar cf docs.tar *
bzip2 docs.tar

move docs.tar.bz2 ../../
