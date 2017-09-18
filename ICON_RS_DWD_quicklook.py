#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ICON and sounding profile comparison tool
# v0: static and works only for a certain test case with specific sounding
# v1: added dynamical functionality and command line options
# v2: working version with first functionality details
# v3: cleaned code of not necessary functions and corrected %y bug
# v4: Added possibility that 1D files could contain several timesteps
# v5: Corrected bug of index 0 for ICON and 1 as first for observations
# v6: Added support of windspeed profiles

# Load necessary python modules
import sys
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from datetime import datetime
from time import mktime
import pickle # Python module to save/load external files

# Define user inputs - Select stations and variables to be plotted
# available stations - see reference for ICON data on redmine
unix_time_in_start = float(sys.argv[2])
unix_time_in_stop  = float(sys.argv[3])
ICON_filename      = sys.argv[1]
station_list       = [2,6,8,9,10,11,12,13,15,16,17,31,32,33,34,35]
variables_list     = ["temp","spec_hum"]
output_path        = sys.argv[4]


# Read ICON model date function
def get_ICON_Model_time(ICON_file, unix_time_in):
	"This function gets ICON dates and convert it to unix timestamp array."

	print unix_time_in

	# Open NetCDF connection to file in read-only mode
	fh_ICON = Dataset(ICON_file, mode='r')

	# Read time variable of NetCDF file
	dates_ICON = fh_ICON.variables['date']

	#### Read available dates ####
	# Initialize Numpy NaN array with length of timestamps included in ICON file
	dates_ICON_Unix = np.ones(dates_ICON.shape[0])
	time_fmt_ICON   = '%Y%m%dT%H%M%S'

	for i in range(0, dates_ICON.shape[0]):
		sdate              = ''.join(dates_ICON[i,0:15])
		dates_ICON_Unix[i] = mktime(datetime.strptime(sdate[0:], time_fmt_ICON).timetuple())
		del sdate

	fh_ICON.close()

	# Search for corresponding unix timestamp, for which the plots should be generated
	time_idx_ICON = np.where( (dates_ICON_Unix == unix_time_in) | ( dates_ICON_Unix == (unix_time_in+9) ) | ( dates_ICON_Unix == (unix_time_in-9) ) ) [0][0]

	# Return time index of ICON data back
	return time_idx_ICON


# Read ICON model data function
def get_ICON_Model_data(ICON_file, time_idx_ICON):
	"This function reads ICON data."

	# Open NetCDF connection to file in read-only mode
	fh_ICON = Dataset(ICON_file, mode='r')

	# Read variables to workspace
	ICON_values        = fh_ICON.variables['values'][:]
	# dimensions: time (2000), height (151), nvars (33), nstations (36)
	ICON_station_hsurf = fh_ICON.variables['station_hsurf'][:]
	# dimensions: nstations (36)
	ICON_heights       = fh_ICON.variables['heights'][:]
	# dimensions: height (151), nvars (33) - always the same, nstations (36)

	# Close NetCDF file connection
	fh_ICON.close()

	# Create ICON dictonary with all available data
	ICON_data_dict = {"ICON_values" : ICON_values, "ICON_station_hsurf" : ICON_station_hsurf, "ICON_heights" : ICON_heights}

	return ICON_data_dict


# Read OBS (sounding and AMDAR) data function
def get_OBS_Data(stat_id, unix_time_in):
	"This function reads sounding and AMDAR data."
	from math import floor

	# Create station name and timestamp
	station_name  = 'c' + str(stat_id)
	# Round time to full hour
	unix_time_str = str(int( (floor(unix_time_in / 3600) * 3600) ))

	# Read observational data from pickle file
	obs_data_file = pickle.load( open( "/mnt/lustre01/work/bm0834/u233139/icon_eval/obs_data_v11082017.p", "rb" ) )

	# Check, if data is available for specific station and timestep
	if unix_time_str in obs_data_file[station_name]:
		# Create OBS dictonary with all available data
		OBS_data_dict = {"Height" : obs_data_file[station_name][unix_time_str]["Height"] ,
	   		"Temperature" : obs_data_file[station_name][unix_time_str]["Temperature"] ,
	   		"SpecHumidity" : obs_data_file[station_name][unix_time_str]["SpecHumidity"],
	   		"WindSpd" : obs_data_file[station_name][unix_time_str]["WindSpd"]}
	else:
		OBS_data_dict = 9999.0

	return OBS_data_dict


# Combine model and OBS data, preprocess for plotting function
def combine_ICON_OBS(stat_id, ICON_data_dict, time_idx_ICON, OBS_data_dict):
	"This function combines and matches ICON and OBS data."

	# Read ICON values for specific station
	st_ICON_height     = ICON_data_dict["ICON_heights"][:,0,stat_id-1]   # Save height levels 
	st_ICON_height[-1] = ICON_data_dict["ICON_station_hsurf"][stat_id-1] # Add surface height for lowest level
	# Temperature
	st_ICON_temperature      = ICON_data_dict["ICON_values"][time_idx_ICON,:,1,stat_id-1]-273.15 # Temperature 
	st_ICON_temperature[150] = np.nan                                                            # Remove last line because sfc
	# Specific Humidity
	st_ICON_spechum      = ICON_data_dict["ICON_values"][time_idx_ICON,:,8,stat_id-1] * 1000.0 # Specific humidity 
	st_ICON_spechum[150] = np.nan     
	# Wind Speed
	st_ICON_wind_U       = ICON_data_dict["ICON_values"][time_idx_ICON,:,5,stat_id-1]       # Wind speed - U-component
	st_ICON_wind_V       = ICON_data_dict["ICON_values"][time_idx_ICON,:,6,stat_id-1]       # Wind speed - V-component
	st_ICON_windspd      = np.sqrt((st_ICON_wind_U**2) + (st_ICON_wind_V**2))               # Wind speed 
	st_ICON_windspd[150] = np.nan                                                           # Remove last line because sfc

	# Read OBS data for specific station
	st_OBS_height      = OBS_data_dict["Height"]
	st_OBS_temperature = OBS_data_dict["Temperature"]
	st_OBS_spechum     = OBS_data_dict["SpecHumidity"]
	st_OBS_windspd     = OBS_data_dict["WindSpd"]

	# Create ICON - OBS dictonary for plotting
	ICON_OBS_dict_plot = {"stat_id":stat_id , "st_ICON_height":st_ICON_height , "st_ICON_temperature":st_ICON_temperature , "st_ICON_spechum":st_ICON_spechum, "st_ICON_windspd":st_ICON_windspd ,
		"st_OBS_height":st_OBS_height, "st_OBS_temperature":st_OBS_temperature, "st_OBS_spechum":st_OBS_spechum, "st_OBS_windspd":st_OBS_windspd}

	# Return back Python dictonary with Numpy arrays of all necessary data
	return ICON_OBS_dict_plot


# Define python plot function function
def plot_synergy(ICON_OBS_dict_plot, unix_time_in):
	"This function gets ICON and OBS data and plot them together."

	# Station name dictonary
	st_name_plot = ['Empty','JOYCE','KITCube','LACROS','RAO','Cabauw','ETGB Bergen',
		'De Bilt','Essen','Greifswald','Idar-Oberstein','Kuemmersbruck',
		'Lindenberg','Meiningen','Muenchen-Oberschleissheim','Norderney',
		'Schleswig','Stuttgart','Bayreuth','Nordholz','Ziegendorf','HOPE_c21',
		'HOPE_c22','HOPE_c23','HOPE_c24','HOPE_c25','HOPE_c26','HOPE_c27','HOPE_c28',
		'HOPE_c29','HOPE_c30','EDDF Frankfurt','EDDM Muenchen','EDDL Duesseldorf',
		'EDDH Hamburg','EDDT Berlin','LACORS Leipzig']

	# Create well formatted time_string
	time_string = datetime.fromtimestamp(int(unix_time_in)).strftime('%Y-%m-%d-%H-%M')

	# Plotting temperature data
	plt.figure()
	plot_temp = plt.plot(ICON_OBS_dict_plot["st_ICON_temperature"],ICON_OBS_dict_plot["st_ICON_height"], color='blue')
	plot_temp = plt.plot(ICON_OBS_dict_plot["st_OBS_temperature"],ICON_OBS_dict_plot["st_OBS_height"], color='k')
	plt.ylim(0, 10000)
	plt.ylabel('Height (m)')
	plt.xlabel('Temperature (C)')
	plt.xlim(-60, 30)
	plt.legend( ('ICON', 'OBS'), 'upper right')
	plt.title("Station: " + st_name_plot[ICON_OBS_dict_plot["stat_id"]] + " - " + time_string)
	plt.grid('on')

	plt.savefig(output_path + 'Temp_profile_c'+ str(ICON_OBS_dict_plot["stat_id"]) + '_' + time_string + '.png')
	plt.close()
	#plt.show()

	# Plotting specific humidity data
	plt.figure()
	plot_spechum = plt.plot(ICON_OBS_dict_plot["st_ICON_spechum"],ICON_OBS_dict_plot["st_ICON_height"], color='blue')
	plot_spechum = plt.plot(ICON_OBS_dict_plot["st_OBS_spechum"],ICON_OBS_dict_plot["st_OBS_height"], color='k')
	plt.ylim(0, 10000)
	plt.ylabel('Height (m)')
	plt.xlabel('Specific Humidity (g/kg)')
	plt.xlim(0, 10)
	plt.legend( ('ICON', 'OBS'), 'upper right')
	plt.title("Station: " + st_name_plot[ICON_OBS_dict_plot["stat_id"]] + " - " + time_string)
	plt.grid('on')

	plt.savefig(output_path + 'SpecHum_profile_c'+ str(ICON_OBS_dict_plot["stat_id"]) + '_' + time_string + '.png')
	plt.close()
	#plt.show()

	# Plotting wind speed profile data
	plt.figure()
	plot_windspd = plt.plot(ICON_OBS_dict_plot["st_ICON_windspd"],ICON_OBS_dict_plot["st_ICON_height"], color='blue')
	plot_windspd = plt.plot(ICON_OBS_dict_plot["st_OBS_windspd"],ICON_OBS_dict_plot["st_OBS_height"], color='k')
	plt.ylim(0, 10000)
	plt.ylabel('Height (m)')
	plt.xlabel('Wind speed (m/s)')
	plt.xlim(0, 50)
	plt.legend( ('ICON', 'OBS'), 'upper right')
	plt.title("Station: " + st_name_plot[ICON_OBS_dict_plot["stat_id"]] + " - " + time_string)
	plt.grid('on')

	plt.savefig(output_path + 'WindSpd_profile_c'+ str(ICON_OBS_dict_plot["stat_id"]) + '_' + time_string + '.png')
	plt.close()
	#plt.show()


# Main control function
def main():
	# Define parameters
	#stat_id = 11
	print "Starting quicklook generation..."
	print "filename: ",sys.argv[1]
	print "start: ",sys.argv[2]
	print "stop: ",sys.argv[3]
	print "plot: ",sys.argv[4]

	# Calculate time steps containing 1D meteogram file
	t_steps = int(round((unix_time_in_stop - unix_time_in_start)/60/60))+1
	# Generate unix time stamp
	unix_time_in = unix_time_in_start

	for i_step in range(0,t_steps):

		# Debugging
		print "First iteration"
	
		# Search for time idx in ICON file
		time_idx_ICON = get_ICON_Model_time(ICON_filename, unix_time_in)

		# Read ICON file and create dictonary for the data
		ICON_data_dict = get_ICON_Model_data(ICON_filename, time_idx_ICON)

		# Loop over all stations, which were selected in the user input
		for stat_id in station_list:
			# Read corresponding observational data
			OBS_data_dict = get_OBS_Data(stat_id, unix_time_in)
			# If there are no observations available, skip plotting
			if (OBS_data_dict == 9999.0):
				continue

			# Combine ICON and OBS data to one dictonary for postprocessing
			ICON_OBS_dict_plot = combine_ICON_OBS(stat_id, ICON_data_dict, time_idx_ICON, OBS_data_dict)

			# Print plots for selected variables and timestamps
			plot_synergy(ICON_OBS_dict_plot, unix_time_in)
			del ICON_OBS_dict_plot

		# Generate unix time stamp
		unix_time_in = unix_time_in + 3600.0

# End of main()

# Call main routine
main()
print "Finished program"
