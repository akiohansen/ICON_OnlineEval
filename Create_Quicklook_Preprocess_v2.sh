#!/bin/bash
# Bash Script to preprocess ICON files for 5 minutes data on lat lon for precipitation
# Idea is to compare these files with RADOLAN files and create precip movies as well as daily sums
# ./Create_Quicklook_Preprocess.sh

echo 'Start preprocessing ICON files...'

#for file in /work/bm0834/k203095/OUTPUT/*/DATA/2d_cloud*DOM*
for file in /work/bm0834/k203095/OUTPUT/20130424/DATA/2d_cloud_*_DOM*_ML_20130424T*
#for file in /work/bm0834/k203095/OUTPUT/20130420/DATA/2d_cloud_day_DOM01_ML_20130420T150000Z.nc
do
    echo "$file"

    # Get Filename only
    INPUT_FILE="${file##*/}"
    echo "$INPUT_FILE"

    # Get number of timesteps to do right time averaging for 5 minutes
    numtim=`cdo ntime $file`
    #numtim="360"
    echo "$numtim"

    if [ "$numtim" == "360" ]
        then
            timint=30
            echo "10 seconds data"
    elif [ "$numtim" == "60" ]
        then
            timint=5
            echo "1 minute data"
    elif [ "$numtim" == "12" ]
        then
            timint=1
            echo "already 5 minute data"
    elif [ "$numtim" == "1" ]
        then
            timint=1
            echo "only last time step"
    else
        timint=1
        echo "Error, please check for inconsistency!"
    fi

    # Check which domain and which grid file has to be used according to predfined data
    if [[ $INPUT_FILE == *"DOM01_ML_20130420T"* ]] || [[ $INPUT_FILE == *"DOM01_ML_20130421T"* ]] || [[ $INPUT_FILE == *"DOM01_ML_20130424T"* ]] || [[ $INPUT_FILE == *"DOM01_ML_20130425T"* ]] || [[ $INPUT_FILE == *"DOM01_ML_20130426T"* ]] || [[ $INPUT_FILE == *"DOM01_ML_20130427T"* ]]; then
    	griddes="/mnt/lustre01/scratch/u/u233139/griddes/dom01_GRID_3d_fine_DOM01_ML_20130424T000000Z"
    	gridfile="/work/bm0834/k203095/OUTPUT/hdcp2_final_1dom/GRIDS/GRID_3d_fine_DOM01_ML_20130424T000000Z.nc"
    	outputdir="/mnt/lustre02/work/bm0834/u233139/rain_RADOLAN_DOM01/"
  		#echo "Use grid: "$griddes" with "$gridfile
    elif [[ $INPUT_FILE == *"DOM01_ML_20130502T"* ]] || [[ $INPUT_FILE == *"DOM01_ML_20130503T"* ]] || [[ $INPUT_FILE == *"DOM01_ML_20130505T"* ]] || [[ $INPUT_FILE == *"DOM01_ML_20130506T"* ]] || [[ $INPUT_FILE == *"DOM01_ML_20130511T"* ]] || [[ $INPUT_FILE == *"DOM01_ML_20130512T"* ]] || [[ $INPUT_FILE == *"DOM01_ML_20130528T"* ]] || [[ $INPUT_FILE == *"DOM01_ML_20130529T"* ]]; then
    	griddes="/mnt/lustre01/scratch/u/u233139/griddes/dom01_GRID_3d_fine_DOM01_ML_20130502T000000Z"
    	gridfile="/work/bm0834/k203095/OUTPUT/20130502/GRID/GRID_3d_fine_DOM01_ML_20130502T000000Z.nc"
    	outputdir="/mnt/lustre02/work/bm0834/u233139/rain_RADOLAN_DOM01/"
  		#echo "Use grid: "$griddes" with "$gridfile
    elif [[ $INPUT_FILE == *"DOM01_ML_20150704T"* ]] || [[ $INPUT_FILE == *"DOM01_ML_20150705T"* ]] || [[ $INPUT_FILE == *"DOM01_ML_20150706T"* ]]; then
    	griddes="/mnt/lustre01/scratch/u/u233139/griddes/dom01_hdcp2_de_shift_R0625m"
    	gridfile="/work/bm0834/k203095/icon-hdcp2-icon-lem/icon-lem/experiments/hdcp2_de_shift/hdcp2_de_shift_R0625m.nc"
    	outputdir="/mnt/lustre02/work/bm0834/u233139/rain_RADOLAN_DOM01/"
  		#echo "Use grid: "$griddes" with "$gridfile
    elif [[ $INPUT_FILE == *"DOM02_ML_20130420T"* ]] || [[ $INPUT_FILE == *"DOM02_ML_20130421T"* ]] || [[ $INPUT_FILE == *"DOM02_ML_20130424T"* ]] || [[ $INPUT_FILE == *"DOM02_ML_20130425T"* ]] || [[ $INPUT_FILE == *"DOM02_ML_20130426T"* ]] || [[ $INPUT_FILE == *"DOM02_ML_20130427T"* ]]; then
    	griddes="/mnt/lustre01/scratch/u/u233139/griddes/dom02_GRID_3d_fine_DOM02_ML"
    	gridfile="/work/bm0834/k203095/OUTPUT/hdcp2_final_2dom/GRIDS/GRID_3d_fine_DOM02_ML.nc"
    	outputdir="/mnt/lustre02/work/bm0834/u233139/rain_RADOLAN_DOM02/"
  		#echo "Use grid: "$griddes" with "$gridfile
    elif [[ $INPUT_FILE == *"DOM02_ML_20130502T"* ]] || [[ $INPUT_FILE == *"DOM02_ML_20130503T"* ]] || [[ $INPUT_FILE == *"DOM02_ML_20130505T"* ]] || [[ $INPUT_FILE == *"DOM02_ML_20130506T"* ]] || [[ $INPUT_FILE == *"DOM02_ML_20130511T"* ]] || [[ $INPUT_FILE == *"DOM02_ML_20130512T"* ]] || [[ $INPUT_FILE == *"DOM02_ML_20130528T"* ]] || [[ $INPUT_FILE == *"DOM02_ML_20130529T"* ]]; then
    	griddes="/mnt/lustre01/scratch/u/u233139/griddes/dom02_GRID_3d_fine_DOM02_ML_20130502T000000Z"
    	gridfile="/work/bm0834/k203095/OUTPUT/20130502/GRID/GRID_3d_fine_DOM02_ML_20130502T000000Z.nc"
    	outputdir="/mnt/lustre02/work/bm0834/u233139/rain_RADOLAN_DOM02/"
  		#echo "Use grid: "$griddes" with "$gridfile
    elif [[ $INPUT_FILE == *"DOM02_ML_20150704T"* ]] || [[ $INPUT_FILE == *"DOM02_ML_20150705T"* ]] || [[ $INPUT_FILE == *"DOM02_ML_20150706T"* ]]; then
    	griddes="/mnt/lustre01/scratch/u/u233139/griddes/dom02_hdcp2_de_shift_nest_R0312m"
    	gridfile="/work/bm0834/k203095/icon-hdcp2-icon-lem/icon-lem/experiments/hdcp2_de_shift/hdcp2_de_shift_nest_R0312m.nc"
    	outputdir="/mnt/lustre02/work/bm0834/u233139/rain_RADOLAN_DOM02/"
  		#echo "Use grid: "$griddes" with "$gridfile
    elif [[ $INPUT_FILE == *"DOM03_ML_20130420T"* ]] || [[ $INPUT_FILE == *"DOM03_ML_20130421T"* ]] || [[ $INPUT_FILE == *"DOM03_ML_20130424T"* ]] || [[ $INPUT_FILE == *"DOM03_ML_20130425T"* ]] || [[ $INPUT_FILE == *"DOM03_ML_20130426T"* ]] || [[ $INPUT_FILE == *"DOM03_ML_20130427T"* ]]; then
    	griddes="/mnt/lustre01/scratch/u/u233139/griddes/dom03_GRID_3d_fine_DOM03_ML"
    	gridfile="/work/bm0834/k203095/OUTPUT/GRIDS/GRID_3d_fine_DOM03_ML.nc"
    	outputdir="/mnt/lustre02/work/bm0834/u233139/rain_RADOLAN_DOM03/"
  		#echo "Use grid: "$griddes" with "$gridfile
    elif [[ $INPUT_FILE == *"DOM03_ML_20130502T"* ]] || [[ $INPUT_FILE == *"DOM03_ML_20130503T"* ]] || [[ $INPUT_FILE == *"DOM03_ML_20130505T"* ]] || [[ $INPUT_FILE == *"DOM03_ML_20130506T"* ]] || [[ $INPUT_FILE == *"DOM03_ML_20130511T"* ]] || [[ $INPUT_FILE == *"DOM03_ML_20130512T"* ]] || [[ $INPUT_FILE == *"DOM03_ML_20130528T"* ]] || [[ $INPUT_FILE == *"DOM03_ML_20130529T"* ]]; then
    	griddes="/mnt/lustre01/scratch/u/u233139/griddes/dom03_GRID_3d_fine_DOM03_ML_20130502T000000Z"
    	gridfile="/work/bm0834/k203095/OUTPUT/20130502/GRID/GRID_3d_fine_DOM03_ML_20130502T000000Z.nc"
    	outputdir="/mnt/lustre02/work/bm0834/u233139/rain_RADOLAN_DOM03/"
  		#echo "Use grid: "$griddes" with "$gridfile
    elif [[ $INPUT_FILE == *"DOM03_ML_20150704T"* ]] || [[ $INPUT_FILE == *"DOM03_ML_20150705T"* ]] || [[ $INPUT_FILE == *"DOM03_ML_20150706T"* ]]; then
    	griddes="/mnt/lustre01/scratch/u/u233139/griddes/dom03_hdcp2_de_shift_nest_R0156m"
    	gridfile="/work/bm0834/k203095/icon-hdcp2-icon-lem/icon-lem/experiments/hdcp2_de_shift/hdcp2_de_shift_nest_R0156m.nc"
    	outputdir="/mnt/lustre02/work/bm0834/u233139/rain_RADOLAN_DOM03/"
  		#echo "Use grid: "$griddes" with "$gridfile
	else
		echo "Error finding the correct grid. STOP!"  	
	fi

    # Extract rain variable and do 5 minute averaging with temporary file
    cdo -timselmean,"$timint" -selvar,rain_gsp_rate "$file" "/mnt/lustre02/work/bm0834/u233139/rain_RADOLAN/temp/Extract-Timselmean-"$INPUT_FILE

    # Merge grid with the file for later regridding
    cdo -P 20 -setgrid,$gridfile "/mnt/lustre02/work/bm0834/u233139/rain_RADOLAN/temp/Extract-Timselmean-"$INPUT_FILE "/mnt/lustre02/work/bm0834/u233139/rain_RADOLAN/temp/Extract-Timselmean-Merge-"$INPUT_FILE

    # Remap to latlon grid for final file
    cdo -P 12 -remapdis,$griddes "/mnt/lustre02/work/bm0834/u233139/rain_RADOLAN/temp/Extract-Timselmean-Merge-"$INPUT_FILE $outputdir"Extract-Timselmean-Merge-LL-"$INPUT_FILE

    # Delete temporary files
    rm -f /mnt/lustre02/work/bm0834/u233139/rain_RADOLAN/temp/*


done

# Finish script
echo 'Finished processing all files'


# # DOM01
# 20130420T, 20130421T: /work/bm0834/k203095/OUTPUT/hdcp2_final_1dom/GRIDS/GRID_3d_fine_DOM01_ML_20130424T000000Z.nc
# 20130424T, 20130425T: ""
# 20130425T, 20130426T: ""
# 20130426T, 20130427T: ""

# 20130502T, 20130503T: /work/bm0834/k203095/OUTPUT/20130502/GRID/GRID_3d_fine_DOM01_ML_20130502T000000Z.nc
# 20130505T, 20130506T: ""
# 20130511T, 20130512T: ""
# 20130528T, 20130529T: ""
# 20150704T, 20150705T, 20150706T: /work/bm0834/k203095/icon-hdcp2-icon-lem/icon-lem/experiments/hdcp2_de_shift/hdcp2_de_shift_R0625m.nc

# # DOM02
# 20130420T, 20130421T: /work/bm0834/k203095/OUTPUT/hdcp2_final_2dom/GRIDS/GRID_3d_fine_DOM02_ML.nc
# 20130424T, 20130425T: ""
# 20130425T, 20130426T: ""
# 20130426T, 20130427T: ""

# 20130502T, 20130503T: /work/bm0834/k203095/OUTPUT/20130502/GRID/GRID_3d_fine_DOM02_ML_20130502T000000Z.nc
# 20130505T, 20130506T: ""
# 20130511T, 20130512T: ""
# 20130528T, 20130529T: ""
# 20150704T, 20150705T, 20150706T: /work/bm0834/k203095/icon-hdcp2-icon-lem/icon-lem/experiments/hdcp2_de_shift/hdcp2_de_shift_nest_R0312m.nc

# # DOM03
# 20130420T, 20130421T: /work/bm0834/k203095/OUTPUT/GRIDS/GRID_3d_fine_DOM03_ML.nc
# 20130424T, 20130425T: ""
# 20130425T, 20130426T: ""
# 20130426T, 20130427T: ""

# 20130502T, 20130503T: /work/bm0834/k203095/OUTPUT/20130502/GRID/GRID_3d_fine_DOM03_ML_20130502T000000Z.nc
# 20130505T, 20130506T: ""
# 20130511T, 20130512T: ""
# 20130528T, 20130529T: ""
# 20150704T, 20150705T, 20150706T: /work/bm0834/k203095/icon-hdcp2-icon-lem/icon-lem/experiments/hdcp2_de_shift/hdcp2_de_shift_nest_R0156m.nc


