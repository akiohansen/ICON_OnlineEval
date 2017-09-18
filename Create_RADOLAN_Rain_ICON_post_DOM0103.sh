#!/bin/bash
# Rain RADOLAN processing script for python script for all three domains
# ./Create_RADOLAN_Rain_ICON_post_DOM01_03.sh

echo 'Start postprocessing ICON and RADOLAN files to Python plot routine...'

# User settings
outpath=/mnt/lustre01/work/um0203/u233139/RADOLAN_PLOTS_DOM01/

for file in /mnt/lustre02/work/bm0834/u233139/rain_RADOLAN_DOM01/Extract-Timselmean-Merge-LL-2d_cloud_*_DOM01_ML_*.nc
#for file in /mnt/lustre02/work/bm0834/u233139/rain_RADOLAN/Extract-Timselmean-Merge-LL-2d_cloud_day_DOM03_ML_20130502T100000Z.nc
do
    echo "Start processing of file: $file"

    # Get Filename only
    INPUT_FILE="${file##*/}"
    #echo "$INPUT_FILE"

    # Create unix timestamp
    in=`echo $file | cut -d_ -f8`
    #echo $in
    rfc_form="${in:0:4}-${in:4:2}-${in:6:2} ${in:9:2}:${in:11:2}:${in:13:2}"
    #echo $rfc_form    
    time_unix=$(date -d "$rfc_form" +%s)

    # Start python plotting routine
    #echo $file $time_unix $outpath
    python /mnt/lustre02/work/bm0834/u233139/eval_toolbox/ICON_RADOLAN_quicklook_5min_v5_local.py $file $time_unix $outpath 

done

# Finish script
echo 'Finished generating all plots! Have fun!'

echo 'mistralpp5'
