referenceScript=base-error-abundtrim.sh



#Now, let's take in all the files and work on them one-by-one
for file in $(ls ../PRJEB1787_prok_shotgun/*_1.fastq.gz)
do
#Manipulate the string with a bit of bash-foo
        strip=${file/*\//}
        fname=${strip/_*/}
        scriptName=${fname}.errtrim.qsub
        cp $referenceScript $scriptName
        sed "s@XXERRName@$strip@g" $scriptName > tmp
        mv tmp $scriptName

done
exit 0

