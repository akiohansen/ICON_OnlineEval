#!/bin/bash
# Unix script to convert and select variables of ICON 2D output
# ./

# Command line arguments
INPUT_FILE_PATH=$1
OUTPUT_DIR=$2

# Static links
GRID_FILE='/mnt/lustre01/scratch/u/u233139/grids/dom03_griddes'
# Get Filename only
INPUT_FILE="${INPUT_FILE_PATH##*/}"
echo $ INPUT_FILE

# MODIS and GPS IWV cdo preprocessing script
# EMLL - Extract, Merged, LatLon
cdo -seltimestep,1 -selvar,clt,prw $INPUT_FILE_PATH Extract-$INPUT_FILE
/work/bm0834/anurag/CDO/cdo_new -s -P 24 -merge /work/bm0834/k203095/OUTPUT/GRIDS/horizontal_grid_DOM03.nc Extract-$INPUT_FILE Extract-Merge-$INPUT_FILE
cdo -P 24 -remapdis,$GRID_FILE Extract-Merge-$INPUT_FILE $OUTPUT_DIR/EMLL-CloudCover-IWV-$INPUT_FILE
# Delete temporary files
rm -f Extract-$INPUT_FILE Extract-Merge-$INPUT_FILE

# RADOLAN cdo preprocessing script
# EMLL - Extract, Merged, LatLon
cdo -selvar,rain_gsp_rate $INPUT_FILE_PATH Extract-$INPUT_FILE
/work/bm0834/anurag/CDO/cdo_new -s -P 12 -merge /work/bm0834/k203095/OUTPUT/GRIDS/horizontal_grid_DOM03.nc Extract-$INPUT_FILE Extract-Merge-$INPUT_FILE
cdo -P 24 -timsum, Extract-Merge-$INPUT_FILE Extract-Merge-Time-$INPUT_FILE
cdo -P 24 -remapdis,$GRID_FILE Extract-Merge-Time-$INPUT_FILE $OUTPUT_DIR/EMLL-RainRate-$INPUT_FILE

# Delete temporary files
rm -f Extract-$INPUT_FILE Extract-Merge-$INPUT_FILE Extract-Merge-Time-$INPUT_FILE

echo "All files preprocessed and ready for python quicklook generation!"

# FinishedEMLL-CloudCover-IWV-
