#!/bin/bash
# Unix script to check for new files to read
# Works for 1D meteograms and 2D fields
# ./

### BEGIN OF USER INPUT SECTION ###
INPUT_DIR=/mnt/lustre01/scratch/u/u233139/INPUT_ICON
SCRIPT_DIR=/mnt/lustre01/scratch/u/u233139/FILES
PLOT_DIR=/mnt/lustre01/scratch/u/u233139/plots/
WORK_DIR=/mnt/lustre01/scratch/u/u233139/workdir/
### END OF USER INPUT SECTION #####

# Create ICON 2D working folder, if it not existing
mkdir -p $SCRIPT_DIR'/ICON_2D'
TEMP_DIR_2D=$SCRIPT_DIR'/ICON_2D'

# Special Product Fileprefix
MODIS_PREFIX=$SCRIPT_DIR'/ICON_2D/EMLL-CloudCover-IWV-'
RADOLAN_PREFIX=$SCRIPT_DIR'/ICON_2D/EMLL-RainRate-'

# Basic variables
len_INPUT=${#INPUT_DIR}

# Generate Filelists, if not yet existing
if [ -e $INPUT_DIR/2d_cloud_*DOM03_ML_*.nc ]; then
  echo '' > $SCRIPT_DIR/filelist2D_last
fi
if [ -e $INPUT_DIR/1d_vars_DOM03_*.nc ]; then
  echo '' > $SCRIPT_DIR/filelist1D_last
fi

# Create new filelist
if [ -e $INPUT_DIR/2d_cloud_*DOM03_ML_*.nc ]; then
    ls $INPUT_DIR/2d_cloud_*DOM03_ML_*.nc > $SCRIPT_DIR/filelist2D_new 
    # Check for new files and in case of new files, start processing
    grep -Fxvf $SCRIPT_DIR/filelist2D_last $SCRIPT_DIR/filelist2D_new > $SCRIPT_DIR/files2D_diff
    mv filelist2D_new filelist2D_last
fi
# Create new filelist
if [ -e $INPUT_DIR/1d_vars_DOM03_*.nc ]; then
    ls $INPUT_DIR/1d_vars_DOM03_*.nc > $SCRIPT_DIR/filelist1D_new
    # Check for new files and in case of new files, start processing
    grep -Fxvf $SCRIPT_DIR/filelist1D_last $SCRIPT_DIR/filelist1D_new > $SCRIPT_DIR/files1D_diff
    mv filelist1D_new filelist1D_last
fi

## 2D file part
# Calculate date position in string
date_start=`expr $len_INPUT + 24`  
date_end=`expr $len_INPUT + 38`

# Loop through all 2 dimensional files and start processing them
if [ -e $SCRIPT_DIR/files2D_diff ]; then
    while read i_file; do
      in_file=$(echo $i_file | cut -c$date_start-$date_end)
      #echo $in_file
      rfc_form="${in_file:0:4}-${in_file:4:2}-${in_file:6:2} ${in_file:9:2}:${in_file:11:2}:${in_file:13:2} +0200"
      #echo $rfc_form
      epoch_time=$(date -d "$rfc_form" +%s)
      #echo $epoch_time
      #echo `date -d @$epoch_time`

      # Get filename only
      INPUT_FILENAME=$(basename $i_file)
      echo $INPUT_FILENAME

      # Call python and shell script
      echo "Start processing file... " $i_file
      $SCRIPT_DIR/convert_ICON_2d.sh $i_file $TEMP_DIR_2D
      python $SCRIPT_DIR/ICON_MODIS_quicklook_v1.py $MODIS_PREFIX$INPUT_FILENAME $epoch_time $PLOT_DIR
      python $SCRIPT_DIR/ICON_RADOLAN_quicklook_v3.py $RADOLAN_PREFIX$INPUT_FILENAME $epoch_time $PLOT_DIR $WORK_DIR

    done <files2D_diff
fi
# Finished

## 1D meteogram output part
# Calculate stop date position in string of 1D meteogram output
date_1d_start=`expr $len_INPUT + 16`  
date_1d_start_end=`expr $len_INPUT + 30`
date_1d_stop=`expr $len_INPUT + 33`  
date_1d_stop_end=`expr $len_INPUT + 47`

# Loop through all 1 dimensional files and start processing them
if [ -e $SCRIPT_DIR/files1D_diff ]; then
    while read i_file; do
      in_file_start=$(echo $i_file | cut -c$date_1d_start-$date_1d_start_end)
      in_file_stop=$(echo $i_file | cut -c$date_1d_stop-$date_1d_stop_end)
      #echo $in_file
      rfc_form_start="${in_file_start:0:4}-${in_file_start:4:2}-${in_file_start:6:2} ${in_file_start:9:2}:${in_file_start:11:2}:${in_file_start:13:2} +0200"
      rfc_form_stop="${in_file_stop:0:4}-${in_file_stop:4:2}-${in_file_stop:6:2} ${in_file_stop:9:2}:${in_file_stop:11:2}:${in_file_stop:13:2} +0200"
      #echo $rfc_form
      epoch_time_start=$(date -d "$rfc_form_start" +%s)
      epoch_time_stop=$(date -d "$rfc_form_stop" +%s)
      #echo $epoch_time
      #echo `date -d @$epoch_time`

      # Get filename only
      INPUT_FILENAME=$(basename $i_file)
      echo $INPUT_FILENAME

      # Call python and shell script
      echo "Start processing file... " $i_file
      #echo $INPUT_FILENAME $epoch_time_start $epoch_time_stop $PLOT_DIR
      python $SCRIPT_DIR/ICON_RS_DWD_quicklook_v4.py $i_file $epoch_time_start $epoch_time_stop $PLOT_DIR

    done <files1D_diff
fi
# Finished

# Cleaning temporary directories
rm -r -f $TEMP_DIR_2D

echo "Waiting for new files, all files successfully processed so far."
