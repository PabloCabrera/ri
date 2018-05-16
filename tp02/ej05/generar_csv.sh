#!/bin/sh

COLLECTION_FILE=$1

echo "QUERY_ID,RANK,DOC_NAME,SCORE"
while read QUERY_ID IGNORE DOC_ID RANK SCORE METHOD ; do
	DOC_NAME=$(egrep -v '^#' "$COLLECTION_FILE" | head -n $DOC_ID | tail -n 1| sed 's/.*\///')
	echo "$QUERY_ID,$RANK,$DOC_NAME,$SCORE"
done
