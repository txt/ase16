BEGIN { RS="\0" 
        getline header < "etc/header"
        RS="\n"
}
In      { print } 
/^#/    { if (!In) print header "\n" $0
          In = 1 }
