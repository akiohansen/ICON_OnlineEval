#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ICON and sounding profile comparison tool
# v0: static and works only for a certain test case with specific sounding
# v1: added dynamical functionality and command line options
# v2: working version with first functionality details
# 15/07/16: Added accumulation of RADOLAN product to generate hourly accumulated precipitation
# v3: added same specific rain colormap, for infos see: http://pyhogs.github.io/colormap-bathymetry.html
# _local : Added support of local RADOLAN files instead of online downloading from SAMD due to OpenID auth
# _5min  : Changed to 5 min plots for ICON and RADOLAN to get comparable movies of rain rates
# v4: Changed from two plots to one subplot with title
# v5: Added check whether date is newer than 2013 then no SAMD RADOLAN data available which will be written at the plot
# _DOMs_ version: Added four panel plot for intercomparison of all three domains with observations

# Load necessary python modules
import sys, subprocess
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from netCDF4 import Dataset
from datetime import datetime
from time import mktime
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Define user inputs - Select stations and variables to be plotted
# available stations - see reference for ICON data on redmine
ICON_filename_DOM01   = sys.argv[1]
ICON_filename_DOM02   = sys.argv[2]
ICON_filename_DOM03   = sys.argv[3]
Unix_time_start       = float(sys.argv[4])
Output_path           = sys.argv[5]
##workdir_path        = sys.argv[6]

# Debug parameters and for developing
#Unix_time_start     = float(1436011200.0)
#ICON_filename_DOM01 = "/work/bm0834/u233139/rain_RADOLAN_DOM01/Extract-Timselmean-Merge-LL-2d_cloud_day_DOM01_ML_20150704T140000Z.nc"
#ICON_filename_DOM02 = "/work/bm0834/u233139/rain_RADOLAN_DOM02/Extract-Timselmean-Merge-LL-2d_cloud_day_DOM02_ML_20150704T140000Z.nc"
#ICON_filename_DOM03 = "/work/bm0834/u233139/rain_RADOLAN_DOM03/Extract-Timselmean-Merge-LL-2d_cloud_day_DOM03_ML_20150704T140000Z.nc"
#Output_path         = "/work/bm0834/u233139/RADO_PLOTS/"

# Creating Custom Colormap
Cmap_arr = np.array([(255,255,255),(238,242,255),(220,228,255),(203,215,255),(186,201,255),(168,188,255),(151,175,255),(134,161,255),
(116,148,255),(99,134,255),(85,123,255),(80,117,255),(75,111,255),(71,105,255),(66,99,255),(61,93,255),(57,87,255),(52,81,255),
(47,75,255),(43,69,255),(45,63,251),(54,56,240),(63,49,230),(73,43,219),(82,36,209),(91,29,198),(100,22,188),(110,15,177),
(119,9,167),(128,2,156),(136,0,142),(143,0,126),(150,0,110),(157,0,95),(164,0,79),(171,0,63),(178,0,47),(185,0,32),(192,0,16),
(199,0,0)])

cmap_rain = mpl.colors.ListedColormap(Cmap_arr/255.0)

# Use custom colormap function from Earle
# def custom_div_cmap(numcolors=256, name='custom_div_cmap',
#                     mincol='white', midcol='blue', maxcol='red'):
#     """ Create a custom diverging colormap with three colors
    
#     Default is blue to white to red with 11 colors.  Colors can be specified
#     in any way understandable by matplotlib.colors.ColorConverter.to_rgb()
#     """

#     from matplotlib.colors import LinearSegmentedColormap 
    
#     cmap = LinearSegmentedColormap.from_list(name=name, 
#                                              colors =[mincol, midcol, maxcol],
#                                              N=numcolors)
#     return cmap

# Read ICON model data function
def get_ICON_Model_data(ICON_file):
	"This function reads ICON rain rate data and calculates 1hour sum."

	# Open NetCDF connection to file in read-only mode
	fh_ICON = Dataset(ICON_file, mode='r')

	# Read time vector
	ICON_time = fh_ICON.variables['time'][:]

	# Read variables to workspace
	rain_gsp_rate_ICON = fh_ICON.variables['rain_gsp_rate'][:]
	# dimensions: 
	# Convert from kg m2 / s to mm/hr
	rain_gsp_rate_ICON = rain_gsp_rate_ICON*3600.0

	# Get information about grid and preprocess them for Basemap
	ICON_X = fh_ICON.variables['lon']
	ICON_Y = fh_ICON.variables['lat']
	ICON_X_mesh, ICON_Y_mesh = np.meshgrid(ICON_X, ICON_Y)

	# Close NetCDF file connection
	fh_ICON.close()

	# Create ICON dictonary with all available data
	ICON_data_dict = {"ICON_X_mesh" : ICON_X_mesh, "ICON_Y_mesh" : ICON_Y_mesh, "rain_gsp_rate_ICON" : rain_gsp_rate_ICON, "ICON_time" : ICON_time}

	return ICON_data_dict


# Read OBS (RADOLAN) data function
def get_RADOLAN_Data(unix_time_in):
	"This function downloads RADOLAN data from HDCP2 database and process data."

	# Create filename strings
	date_in = datetime.fromtimestamp( unix_time_in )

	# Check whether requested date is within 2013, otherwise set placeholder file
	#if (unix_time_in < 1388530800.0):
	RADOLAN_file = '/mnt/lustre01/work/um0203/u233139/RADOLAN/hdfd_miub_drnet00_l3_rr_v00_'+date_in.strftime('%Y%m%d')+'000000.nc'
	#else:
	#	RADOLAN_file = '/mnt/lustre01/work/um0203/u233139/RADOLAN/hdfd_miub_drnet00_l3_rr_v00_'+'20130502'+'000000.nc'

    # OLD online HD(CP)2 database option, TODO: Update to new SAMD archive OpenID login
	# RADOLAN_link  = 'http://data.hdcp2.uni-koeln.de/thredds/fileServer/hdcp2/drnet/00/rr/l3/hdfd/miub/'+date_in.strftime('%Y')+'/hdfd_miub_drnet00_l3_rr_v00_'+date_in.strftime('%Y%m%d')+'000000.nc'
	# RADOLAN_file  = workdir_path+'hdfd_miub_drnet00_l3_rr_v00_'+date_in.strftime('%Y%m%d')+'000000.nc'
	# subprocess.call(['wget', '--user', 'hdcp2user', '--password', 'jetStream6:9', '-O', RADOLAN_file, RADOLAN_link])

	# Read RADOLAN file
	fh_RADOLAN        = Dataset(RADOLAN_file, mode='r')
	# Read environment variables
	RADOLAN_time      = fh_RADOLAN.variables['time'][:] - 7200.0 # Conversion to UTC
	RADOLAN_lon       = fh_RADOLAN.variables['lon'][0,:]
	RADOLAN_lat       = fh_RADOLAN.variables['lat'][:,0]
	# Read rain rate values
	RADOLAN_rain_rate = fh_RADOLAN.variables['rr'][:]

	# Finding indices of unix_in for 5 minutes instantaneous rain rates (mm/hr)
	#if (unix_time_in < 1388530800.0):
	precip_idx = np.where((RADOLAN_time >= (unix_time_in-30)) & (RADOLAN_time <= (unix_time_in+30)))
	#else:
	#	precip_idx = np.zeros((1,1))
	#dt_intv         = RADOLAN_time[hour_precip_idx][1] - RADOLAN_time[hour_precip_idx][0]

	# Convert unit from m/s to mm/hr
	RADOLAN_rain_rate = RADOLAN_rain_rate*1000*3600.0       # Convert from m/s to mm/hr
	RADOLAN_rain_5min = RADOLAN_rain_rate[precip_idx[0][0]].squeeze()

	### Plot section of RADOLAN data
	RADOLAN_X_mesh, RADOLAN_Y_mesh = np.meshgrid(RADOLAN_lon, RADOLAN_lat)


	# Create RADOLAN dictonary with all available data
	RADOLAN_data_dict = {"RADOLAN_X_mesh" : RADOLAN_X_mesh, "RADOLAN_Y_mesh" : RADOLAN_Y_mesh,
	   "RADOLAN_rain_5min" : RADOLAN_rain_5min}

	return RADOLAN_data_dict


# Define python plot function function
def plot_synergy_precip(ICON_data_dict_DOM01, ICON_data_dict_DOM02, ICON_data_dict_DOM03, RADOLAN_data_dict, time_idx, unix_time_in):
	"This function gets ICON and RADOLAN data and plot them together."

	# Import map data for plotting
	from mpl_toolkits.basemap import Basemap
	from math import ceil

	# Create well formatted time_string
	time_string = datetime.fromtimestamp(int(unix_time_in)).strftime('%Y-%m-%d-%H-%M')

	# Calculate scaling min and max values
	#scale_max = np.max(ICON_data_dict["rain_gsp_rate_ICON_sum"])
	scale_max   = int(20)
	scale_range = np.linspace(0.0, scale_max, 41)  # create colorbar vector

	# Next idea for two subplots
	fig = plt.figure(num=None, figsize=(10, 6), dpi=150, facecolor='w', edgecolor='k')

	plt.suptitle("Rain at: "+time_string, fontweight="bold", size=20)

	ax1 = fig.add_subplot(221)
	ax1.set_title("RADOLAN Rain Rate")
	first = ax1.contourf(RADOLAN_data_dict["RADOLAN_X_mesh"], RADOLAN_data_dict["RADOLAN_Y_mesh"], RADOLAN_data_dict["RADOLAN_rain_5min"], scale_range, interpolation='none', cmap=cmap_rain)
	map = Basemap(llcrnrlon=4.0,llcrnrlat=47.0,urcrnrlon=15.0,urcrnrlat=55.0,
	             resolution='i')
	map.drawcoastlines()
	map.drawcountries()
	lat_ticks = [55.0,53.0,51.0,49.0,47.0]
	map.drawparallels(lat_ticks, labels=[1,0,0,0], linewidth=0.0)
	lon_ticks = [4.0,6.0,8.0,10.0,12.0,14.0]
	map.drawmeridians(lon_ticks, labels=[0,0,0,1], linewidth=0.0)
	# If data is not within 2013 and thus no SAMD data available write text to plot
	#if (unix_time_in > 1388530800.0):
	#	ax1.text(6.0, 51.0, 'No RADOLAN in SAMD!', style='italic', bbox={'facecolor':'red', 'alpha':0.5, 'pad':8})

    # ICON DOM01
	ax2 = fig.add_subplot(222)
	ax2.set_title("ICON DOM01 Rain Rate")
	second = ax2.contourf(ICON_data_dict_DOM01["ICON_X_mesh"], ICON_data_dict_DOM01["ICON_Y_mesh"], ICON_data_dict_DOM01["rain_gsp_rate_ICON"][time_idx,:,:], scale_range, interpolation='none', cmap=cmap_rain)
	map = Basemap(llcrnrlon=4.0,llcrnrlat=47.0,urcrnrlon=15.0,urcrnrlat=55.0,
	             resolution='i')
	map.drawcoastlines()
	map.drawcountries()
	lat_ticks = [55.0,53.0,51.0,49.0,47.0]
	map.drawparallels(lat_ticks, labels=[1,0,0,0], linewidth=0.0)
	lon_ticks = [4.0,6.0,8.0,10.0,12.0,14.0]
	map.drawmeridians(lon_ticks, labels=[0,0,0,1], linewidth=0.0)

	# ICON DOM02
	ax3 = fig.add_subplot(223)
	ax3.set_title("ICON DOM02 Rain Rate")
	second = ax3.contourf(ICON_data_dict_DOM02["ICON_X_mesh"], ICON_data_dict_DOM02["ICON_Y_mesh"], ICON_data_dict_DOM02["rain_gsp_rate_ICON"][time_idx,:,:], scale_range, interpolation='none', cmap=cmap_rain)
	map = Basemap(llcrnrlon=4.0,llcrnrlat=47.0,urcrnrlon=15.0,urcrnrlat=55.0,
	             resolution='i')
	map.drawcoastlines()
	map.drawcountries()
	lat_ticks = [55.0,53.0,51.0,49.0,47.0]
	map.drawparallels(lat_ticks, labels=[1,0,0,0], linewidth=0.0)
	lon_ticks = [4.0,6.0,8.0,10.0,12.0,14.0]
	map.drawmeridians(lon_ticks, labels=[0,0,0,1], linewidth=0.0)

	# ICON DOM03
	ax4 = fig.add_subplot(224)
	ax4.set_title("ICON DOM03 Rain Rate")
	second = ax4.contourf(ICON_data_dict_DOM03["ICON_X_mesh"], ICON_data_dict_DOM03["ICON_Y_mesh"], ICON_data_dict_DOM03["rain_gsp_rate_ICON"][time_idx,:,:], scale_range, interpolation='none', cmap=cmap_rain)
	map = Basemap(llcrnrlon=4.0,llcrnrlat=47.0,urcrnrlon=15.0,urcrnrlat=55.0,
	             resolution='i')
	map.drawcoastlines()
	map.drawcountries()
	lat_ticks = [55.0,53.0,51.0,49.0,47.0]
	map.drawparallels(lat_ticks, labels=[1,0,0,0], linewidth=0.0)
	lon_ticks = [4.0,6.0,8.0,10.0,12.0,14.0]
	map.drawmeridians(lon_ticks, labels=[0,0,0,1], linewidth=0.0)

	axlist = [ax1,ax2,ax3,ax4]
	cbar = fig.colorbar(first, ax=axlist, orientation='vertical')
	cbar.set_label('Rain rate (mm/hr)')

	# Save plot to file
	plt.savefig(Output_path + 'ICON_DOM123_RADOLAN_5min_precip_'+ time_string + '.png', dpi=300, format='png')
	plt.close()
	#plt.show()

	return 0


# Main control function
def main():
	# Define parameters
	#stat_id = 11
	print "Starting RADOLAN 5 minutes quicklook generation..."
	print ICON_filename_DOM01, '\n', ICON_filename_DOM02, '\n', ICON_filename_DOM03, '\n'
	print Unix_time_start

	# Debugging
	print "Start generating 5 minutes Rain movies..."

	# Get start unix time
	unix_time_in = Unix_time_start

	# Get ICON model data dictonaries
	ICON_data_dict_DOM01 = get_ICON_Model_data(ICON_filename_DOM01)
	ICON_data_dict_DOM02 = get_ICON_Model_data(ICON_filename_DOM02)
	ICON_data_dict_DOM03 = get_ICON_Model_data(ICON_filename_DOM03)

	# Check for minimal number of timesteps of all three ICON files
	ICON_num_tsteps = np.min([ICON_data_dict_DOM01["ICON_time"].size, ICON_data_dict_DOM02["ICON_time"].size, ICON_data_dict_DOM03["ICON_time"].size])
	# Check whether only one time step or 12 time steps are included in ICON input file
	if (ICON_num_tsteps == 12):
		end_idx = 12
		#print "Time steps are: "+str(end_idx)
	elif (ICON_num_tsteps == 1):
		end_idx = 1
		#print "Time steps are: "+str(end_idx)
	else:
		print "Error at time steps in ICON"

	# Loop for 1 hour with 5 minutes interval
	for time_idx in range(0,end_idx):
		# Read RADOLAN OBS rain rate file and create dictonary for the data
		RADOLAN_data_dict = get_RADOLAN_Data(unix_time_in)

		# Print plots for selected variables and timestamps
		print "Generate next plot for time_idx: "+str(time_idx)+" and Unix: "+str(unix_time_in)
		plot_synergy_precip(ICON_data_dict_DOM01, ICON_data_dict_DOM02, ICON_data_dict_DOM03, RADOLAN_data_dict, time_idx, unix_time_in)
		del RADOLAN_data_dict

		# Calculate new unix time_stamp for RADOLAN data
		unix_time_in += 300.0 # added 5 minutes

	# End of main

# Call main routine
main()
print "Finished program"

