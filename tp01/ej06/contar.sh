#!/bin/bash

ARCHIVO_TERMINOS=../ej05/terminos.txt
ARCHIVO_ESTADISTICAS=../ej05/estadisticas.txt

T5=$(grep " CF:5 " $ARCHIVO_TERMINOS|wc -l)
T4=$(grep " CF:4 " $ARCHIVO_TERMINOS|wc -l)
T3=$(grep " CF:3 " $ARCHIVO_TERMINOS|wc -l)
T2=$(grep " CF:2 " $ARCHIVO_TERMINOS|wc -l)
T1=$(grep " CF:1 " $ARCHIVO_TERMINOS|wc -l)
SUMA=$(($T5 + $T4 + $T3 + $T2 + $T1))
TOTAL=$(egrep '^Terminos extraidos' $ARCHIVO_ESTADISTICAS | sed 's/.*: //')

echo "Cantidad total de terminos en corpus: $TOTAL"
echo "Cantidad de términos con frecuencia igual o menor a 5: $SUMA"
echo "  $T1 terminos de aparicion única"
echo "  $T2 terminos aparecen 2 veces"
echo "  $T3 terminos aparecen 3 veces"
echo "  $T4 terminos aparecen 4 veces"
echo "  $T5 terminos aparecen 5 veces"
echo ""
echo "Proporcion: "$((($SUMA*100)/$TOTAL))"%"


