curl -L $1|gunzip|head -4000000 > ${1##*/}_head.fq
