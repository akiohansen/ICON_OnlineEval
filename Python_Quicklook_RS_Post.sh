#!/bin/bash
# Bash Script to start 1D meteogram quicklook generation
# ./Python_Quicklook_v0.sh

echo 'Start processing of 1D ICON-LEM meteogram output...'

# Go to evaluation toolbox
cd /mnt/lustre02/work/bm0834/u233139/eval_toolbox/

# Generate commands
# 20130420
mkdir /mnt/lustre02/work/bm0834/u233139/eval_toolbox/PLOTS_20130420/
python ICON_RS_DWD_quicklook_v6.py /mnt/lustre02/work/bm0834/k203095/OUTPUT/20130420-default/DATA/1d_vars_DOM03_20130420T000000Z_20130421T000000Z.nc 1366408800 1366495200 /mnt/lustre02/work/bm0834/u233139/eval_toolbox/PLOTS_20130420/

## 20130424
mkdir /mnt/lustre02/work/bm0834/u233139/eval_toolbox/PLOTS_20130424/
python ICON_RS_DWD_quicklook_v6.py /mnt/lustre02/work/bm0834/k203095/OUTPUT/20130424-default/DATA/1d_vars_DOM03_20130424T000000Z_20130425T000000Z.nc 1366754400 1366840800 /mnt/lustre02/work/bm0834/u233139/eval_toolbox/PLOTS_20130424/

## 20130425
mkdir /mnt/lustre02/work/bm0834/u233139/eval_toolbox/PLOTS_20130425/
python ICON_RS_DWD_quicklook_v6.py /mnt/lustre02/work/bm0834/k203095/OUTPUT/20130425-default/DATA/1d_vars_DOM03_20130425T000000Z_20130425T060000Z.nc 1366840800 1366862400 /mnt/lustre02/work/bm0834/u233139/eval_toolbox/PLOTS_20130425/
python ICON_RS_DWD_quicklook_v6.py /mnt/lustre02/work/bm0834/k203095/OUTPUT/20130425-default/DATA/1d_vars_DOM03_20130425T060000Z_20130425T110000Z.nc 1366862400 1366880400 /mnt/lustre02/work/bm0834/u233139/eval_toolbox/PLOTS_20130425/
python ICON_RS_DWD_quicklook_v6.py /mnt/lustre02/work/bm0834/k203095/OUTPUT/20130425-default/DATA/1d_vars_DOM03_20130425T220000Z_20130426T000000Z.nc 1366920000 1366927200 /mnt/lustre02/work/bm0834/u233139/eval_toolbox/PLOTS_20130425/

## 20130426
mkdir /mnt/lustre02/work/bm0834/u233139/eval_toolbox/PLOTS_20130426/
python ICON_RS_DWD_quicklook_v6.py /mnt/lustre02/work/bm0834/k203095/OUTPUT/20130426-default/DATA/1d_vars_DOM03_20130426T000000Z_20130427T000000Z.nc 1366927200 1367013600 /mnt/lustre02/work/bm0834/u233139/eval_toolbox/PLOTS_20130426/

## 20130502
mkdir /mnt/lustre02/work/bm0834/u233139/eval_toolbox/PLOTS_20130502/
python ICON_RS_DWD_quicklook_v6.py /mnt/lustre02/work/bm0834/k203095/OUTPUT/20130502-default/DATA/1d_vars_DOM03_20130502T000000Z_20130503T000000Z.nc 1367445600 1367532000 /mnt/lustre02/work/bm0834/u233139/eval_toolbox/PLOTS_20130502/

## 20130505
mkdir /mnt/lustre02/work/bm0834/u233139/eval_toolbox/PLOTS_20130505/
python ICON_RS_DWD_quicklook_v6.py /mnt/lustre02/work/bm0834/k203095/OUTPUT/20130505-default/DATA/1d_vars_DOM03_20130505T000000Z_20130506T000000Z.nc 1367704800 1367791200 /mnt/lustre02/work/bm0834/u233139/eval_toolbox/PLOTS_20130505/

## 20130511
mkdir /mnt/lustre02/work/bm0834/u233139/eval_toolbox/PLOTS_20130511/
python ICON_RS_DWD_quicklook_v6.py /mnt/lustre02/work/bm0834/k203095/OUTPUT/20130511-default/DATA/1d_vars_DOM03_20130511T000000Z_20130512T000000Z.nc 1368223200 1368309600 /mnt/lustre02/work/bm0834/u233139/eval_toolbox/PLOTS_20130511/

echo 'All meteogram plots are finished...'
