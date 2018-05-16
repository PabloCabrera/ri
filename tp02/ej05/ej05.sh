#!/bin/sh

cd "$(dirname "$0")"
CURRENT_DIR=$(pwd)
TERRIER_DIR="$CURRENT_DIR/../terrier-4.0"
CORPUS_DIR="$CURRENT_DIR/../corpus_data/"
TOPICS_FILE="$CURRENT_DIR/topics.txt"
STOP_WORDS_FILE="$CURRENT_DIR/stop_words.txt"
COLLECTION_FILE="$TERRIER_DIR/etc/collection.spec"

echo "\n[Limpiando archivos antiguos]\n"
rm -rf $TERRIER_DIR/var/data
rm -rf $TERRIER_DIR/var/index/*
rm -rf $TERRIER_DIR/var/results/*

echo "\n[Añadiendo archivos al índice]\n"
$TERRIER_DIR/bin/trec_setup.sh "$CORPUS_DIR"

echo "\n[Generando índice]\n"
$TERRIER_DIR/bin/trec_terrier.sh -i -Dtrec.collection.class=SimpleFileCollection

echo "\n[Recuperando]\n"
$TERRIER_DIR/bin/trec_terrier.sh -r -Dtrec.model=BM25 -Dignore.low.idf.terms=false -Dtrec.topics=$TOPICS_FILE
$TERRIER_DIR/bin/trec_terrier.sh -r -Dtrec.model=TF_IDF -Dignore.low.idf.terms=false -Dtrec.topics=$TOPICS_FILE

echo "\n[Generando archivos CSV]\n"
RES_BM25=$TERRIER_DIR/var/results/BM25*.res
RES_TF_IDF=$TERRIER_DIR/var/results/TF_IDF*.res

cat $RES_BM25 | sh ./generar_csv.sh $COLLECTION_FILE > bm25.csv
cat $RES_TF_IDF |  sh ./generar_csv.sh $COLLECTION_FILE > tf_idf.csv


