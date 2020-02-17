. ./make-docs.sh html

cd _build/html
tar cf docs.tar *
bzip2 docs.tar

mv docs.tar.bz2 ../../
