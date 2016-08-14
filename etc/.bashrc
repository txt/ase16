make1() {
    if [ -f Makefile ]; then
	/usr/bin/make $*
	return 0
    fi
    if [ -f make.mk ]; then
	/usr/bin/make -f make.mk $*
	return 0
    fi	    
    echo "nothing to do"
}

make() {
  root=$(git rev-parse --show-toplevel)
  if [ -n "$root" ]; then
    ( cd $root; make1 $*)
  else
    /usr/bin/make $*
  fi
}
