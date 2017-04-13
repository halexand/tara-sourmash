#!/bin/bash
#PBS -l walltime=24:00:00,nodes=1:ppn=8
#PBS -l mem=32gb
#PBS -A ged
#PBS -m abe
#PBS -M harriet.xander@gmail.com
#export MKL_NUM_THREADS=8
#export OMP_NUM_THREADS=8

module load powertools
#activate the environment for khmer and sourmash

source activate py3.tara

WD=/mnt/scratch/alexa503/tara/PRJEB1787_prok_shotgun

cd $WD

#manipulate forward and reverse names as well as output file names
fname=XXERRName
echo $fname
fname2=${fname/_1/_2}
output=${fname/_1.*/}.paired.fq.gz
output2=${fname/_1.*/}.paired.trimmed.fq

#interleave the reads and do abundance trimming at k=31
interleave-reads.py ${fname} ${fname2} --gzip -o $output

trim-low-abund.py $output -M 16e9 -k 31 --gzip -o $output2

