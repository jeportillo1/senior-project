cd ..

#|| goto :batch_part
 python3.10 $*
exit

:batch_part
 py -3.10 %*