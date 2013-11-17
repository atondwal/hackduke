#!/bin/zsh
for a in `cat`; do
        V=$(((($RANDOM) % 100) - 50))
        echo -n "<prosody pitch=\"+$V\">$a</prosody> " |
        sed 's/+-/-/'
done | espeak -ven+f3 -m --stdout -p 60 -s 180 |  lame -  $1
