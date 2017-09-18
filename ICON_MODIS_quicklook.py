#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ICON and MeteoSat comparison tool
# v1: first testing version

# Load necessary python modules
import sys, subprocess
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from datetime import datetime
from time import mktime


# Define user inputs - Select stations and variables to be plotted
# available stations - see reference for ICON data on redmine
unix_time_in   = float(sys.argv[2])
ICON_filename  = sys.argv[1]
output_path    = sys.argv[3]


# Read ICON model data function
def get_ICON_Model_data(ICON_file):
	"This function reads ICON cloud cover data."

	# Open NetCDF connection to file in read-only mode
	fh_ICON = Dataset(ICON_file, mode='r')

	# Read total cloud cover variable to workspace
	ICON_clt        = fh_ICON.variables['clt'][0,:,:]
	# dimensions: lat (7779), lon (6668)

	# Read grid information and create python meshgrids for plots
	ICON_X = fh_ICON.variables['lon']
	ICON_Y = fh_ICON.variables['lat']
	ICON_X_mesh, ICON_Y_mesh = np.meshgrid(ICON_X, ICON_Y)

	# Close NetCDF file connection
	fh_ICON.close()

	# Create ICON dictonary with all available data
	ICON_data_dict = {"ICON_clt" : ICON_clt, "ICON_X_mesh" : ICON_X_mesh, "ICON_Y_mesh" : ICON_Y_mesh}

	return ICON_data_dict


# Read OBS (sounding and AMDAR) data function
def get_Sat_Data(unix_time_in):
	"This function downloads TROPOS airmass and satellite data."

	# Create filename strings
	date_in = datetime.fromtimestamp( unix_time_in )

	daynat_link  = 'http://sat.tropos.de/hope/images/'+date_in.strftime('%Y/%m/%d')+'/msevi-'+date_in.strftime('%Y%m%dT%H%MZ')+'-daynat-rss-de.jpg'
	airmass_link = 'http://sat.tropos.de/hope/images/'+date_in.strftime('%Y/%m/%d')+'/msevi-'+date_in.strftime('%Y%m%dT%H%MZ')+'-airmass-rss-de.jpg'
	daynat_file  = output_path+'msevi-'+date_in.strftime('%Y%m%dT%H%MZ')+'-daynat-rss-de.jpg'
	airmass_file = output_path+'msevi-'+date_in.strftime('%Y%m%dT%H%MZ')+'-airmass-rss-de.jpg'

	# day natural color satellite picture
	subprocess.call(['wget', '--user', 'hope', '--password', 'sat4hope', '-O', daynat_file, daynat_link])
	# day/night airmass picture
	subprocess.call(['wget', '--user', 'hope', '--password', 'sat4hope', '-O', airmass_file, airmass_link])

	return 0


# Define python plot function function for total cloud cover
def plot_ICON_clt(ICON_data_dict):
	"This function gets ICON data and plots corresponding satellite pictures."

	# Import and create basemap for plotting countries and coastlines
	from mpl_toolkits.basemap import Basemap

	# Create well formatted time_string
	time_string = datetime.fromtimestamp(int(unix_time_in)).strftime('%Y-%m-%d-%H-%M')

	# Plotting temperature data
	plt.figure()
	# Plot contourf plot with lat/lon regridded ICON data
	cmap_cloud   = plt.cm.gray
	levels_cloud = np.arange(0,101,10)
	plt.contourf(ICON_data_dict["ICON_X_mesh"], ICON_data_dict["ICON_Y_mesh"], ICON_data_dict["ICON_clt"], levels=levels_cloud, cmap=cmap_cloud)
	plt.colorbar()
	# Plot map data
	map = Basemap(llcrnrlon=4.0,llcrnrlat=47.0,urcrnrlon=15.0,urcrnrlat=55.0,
	             resolution='i')
	map.drawcoastlines()
	map.drawcountries()
	lat_ticks = [55.0,53.0,51.0,49.0,47.0]
	map.drawparallels(lat_ticks, labels=[1,0,0,0], linewidth=0.0)
	lon_ticks = [4.0,6.0,8.0,10.0,12.0,14.0]
	map.drawmeridians(lon_ticks, labels=[0,0,0,1], linewidth=0.0)
	# Save plot and show it
	plt.savefig(output_path + 'TotalCloudCover_' + time_string + '.png')
	#plt.show()


# Main control function
def main():
	# Define parameters
	#stat_id = 11
	print "Starting satellite quicklook generation..."
	print ICON_filename
	print unix_time_in

	# Read ICON file and create dictonary for the data
	ICON_data_dict = get_ICON_Model_data(ICON_filename)

	# Create total cloud cover plot
	plot_ICON_clt(ICON_data_dict)
	del ICON_data_dict

	# Download and save corresponding Meteosat satellite pictures
	sat_status = get_Sat_Data(unix_time_in)
	if(sat_status != 0):
		print("Error downloading satellite pictures!")


# Call main routine
main()
print "Finished program"

