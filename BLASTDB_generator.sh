#!/bin/bash

default_root="./Influenza A virus M gene"
fr=""
cnt=0

read -p "Enter name of the name of FASTA root directory (default $default_root): " fr

STARTTIME=$(date +%s)

if [ -z "$fr" ]; then

	echo "No input received. Use default fasta root directory instead..."
	fr="$default_root"
	echo "FASTA root directory:	$fr"

fi

if [ ! -d "$fr" ]; then

	echo "The FASTA root directory doesn't exist. The script will end here."
	exit 1

fi

cd "$fr"
echo ">>> Entering $fr"

if [ -d "Human" ]; then

	echo "A directory named Human was found."

	cd Human
	for d in */ ; do

		cd "$d"

		find . -type f -name '*.nhr' -delete
		find . -type f -name '*.nin' -delete
		find . -type f -name '*.nsg' -delete

		d=${d::-1}

		for fa in *.fasta ; do
			makeblastdb -in "$fa" -input_type fasta -dbtype nucl -out "${fa%.*}"
			cnt=$((cnt+1))
		done

		cd ..
	done

fi

if [ -d "Animal" ]; then

	echo "A directory named Animal was found."

	for d in */ ; do

		cd $d

		find . -type f -name '*.nhr' -delete
		find . -type f -name '*.nin' -delete
		find . -type f -name '*.nsg' -delete

		d=${d::-1}

		for fa in *.fasta ; do
			makeblastdb -in "$fa" -input_type fasta -dbtype nucl -out "${fa%.*}"
			cnt=$((cnt+1))
		done

		cd ..

	done

fi

if [ -d "Both" ]; then

	echo "A directory named Both was found."

	for d in */ ; do

		cd $d

		find . -type f -name '*.nhr' -delete
		find . -type f -name '*.nin' -delete
		find . -type f -name '*.nsg' -delete

		d=${d::-1}

		for fa in *.fasta ; do
			makeblastdb -in "$fa" -input_type fasta -dbtype nucl -out "${fa%.*}"
			cnt=$((cnt+1))
		done

		cd ..

	done

fi

cd ..
echo ">>> Exiting $fr"

ENDTIME=$(date +%s)



echo ""
echo ""
echo ""
echo ""
echo "Number of BLAST database created ::	$cnt"
echo "Time used in seconds ::	$(($ENDTIME-$STARTTIME))"
