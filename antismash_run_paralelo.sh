#!/bin/bash
GENOMA=$1
OUTDIR=$2

#Se já processado, pula
if [ -d "$OUTDIR" ]; then
    echo "Já processado: $OUTDIR"
    exit 0
fi

echo "Rodando antiSMASH em $GENOMA"
antismash --output-dir "$OUTDIR" "$GENOMA" #colocar linha de comando completa já testada na outra função

