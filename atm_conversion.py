#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Authors: Gernot Geppert, Akio Hansen
# (University of Hamburg)

# Load required python modules for calculations
import numpy as np

### universal gas constant in N*m/(K*mol) = J/(K*mol)
R = 8.3144621
### molar masses in kg
molar_mass_co2     = 44.0095 * 10**-3
molar_mass_h2o     = 18.0152 * 10**-3
molar_mass_dry_air = 28.9650 * 10**-3
### specific gas constants in m^2/(s^2*K)
R_co2     = R / molar_mass_co2
R_h2o     = R / molar_mass_h2o
R_dry_air = R / molar_mass_dry_air
### humidity addition for virtual temperature
virt_temp_factor = R_h2o / R_dry_air - 1.0
### 0.622
R_dry_air_to_R_h2o = R_dry_air / R_h2o
## Constants for dewpoint calculation
a = 17.271
b = 237.7 # degC
## Constants for virtual potential temperature
R_cp = 0.286 # Kappa

def calc_vapor_pressure(temp, rho, gas_constant):
    """
    Calculate vapor pressure via gas equation.

    Parameters
    ----------
    temp : array_like
        temperatur in K
    rho : array_like
        density in kg/m^3
    gas_constant: array_like
        specific gas constant in m^2/(s^2*K)

    Returns
    -------
    out : ndarray
        vapor pressure in Pa

    """

    return rho * gas_constant * temp

def calc_density(temp, pressure, gas_constant):
    """
    Calculate density via gas equation.

    Parameters
    ----------
    temp : array_like
        temperatur in K
    pressure : array_like
        (partial) pressure in Pa
    gas_constant: array_like
        specicif gas constant in m^2/(s^2*K)

    Returns
    -------
    out : ndarray
        density in kg/m^3

    """

    return pressure / (temp * gas_constant)

def calc_sat_vapor_pressure(temp):
    """
    Calculate saturation vapor pressure for H2O.

    Uses Magnus formula as in Kraus, 2004: Die AtmosphÃ¤re der Erde.

    Parameters
    ----------
    temp : array_like
        temperature in K

    Returns
    -------
    out : array_like
        saturation vapor pressure in Pa

    """

    return 610.78*np.exp(17.1*(temp-273.15)/(235+temp-273.15))

def calc_density_dry_air(temp, pressure, e_h2o):
    """
    Calculate the density of dry air.

    Parameters
    ----------
    temp : array_like
        temperature in K
    pressure : array_like
        pressure in Pa
    e_h2o: array_like
        partial pressure of H2O

    Returns
    -------
    out : array_like
        density of dry air in kg(dry air)/m^3

    """

    return (pressure - e_h2o) / (R_dry_air * temp)

def calc_sh_from_rh(temp, pressure, rel_hum):
    """
    Calculate specific humidity from relative humidity.

    This uses the approximation as in Kraus 2004, section 8.1.3.

    Parameters
    ----------
    temp : array_like
        temperature in K
    pressure : array_like
        pressure in Pa
    rel_hum: array_like
        relative humidity as fraction of 1, ie. 1 means 100%

    Returns
    -------
    out : array_like
        specific humidity in kg(H2O)/kg(air)

    """

    e_sat_h2o = calc_sat_vapor_pressure(temp)
    return R_dry_air_to_R_h2o * rel_hum * e_sat_h2o / pressure

def calc_sh_from_ah(temp, pressure, abs_hum):
    """
    Calculate specific humidity from absolute humidity.

    Parameters
    ----------
    temp : array_like
        temperatur in K
    pressure : array_like
        pressure in Pa
    abs_hum: array_like
        absolute humidity in kg(H2O)/m^3

    Returns
    -------
    out : array_like
        specific humidity in kg(H2O)/kg(air)

    """

    e_h2o = calc_vapor_pressure(temp, abs_hum, R_h2o)
    rho_dry_air = calc_density_dry_air(temp, pressure, e_h2o)
    return abs_hum / (abs_hum + rho_dry_air)

def calc_ah_from_sh(temp, pressure, spec_hum):
    """
    Calculate absolute humidity from specific humidity.

    Parameters
    ----------
    temp : array_like
        temperatur in K
    pressure : array_like
        pressure in Pa
    spec_hum: array_like
        specific humidity in kg(H2O)/kg(air)

    Returns
    -------
    out : array_like
        absolute humidity in kg(H2O)/m^3

    """

    ### substract H2O partial pressure from air pressure and use gas equation
    ### water vapor and dry air
    return (pressure * spec_hum /
            (temp * ((R_dry_air * (1 - spec_hum)) + (R_h2o * spec_hum))))

def calc_ah_from_rh(temp, pressure, rel_hum):
    """
    Calculate absolute humidity from relative humidity.

    Parameters
    ----------
    temp : array_like
        temperatur in K
    pressure : array_like
        (partial) pressure in Pa
    rel_hum : array_like
        relative humidity as fraction of 1, ie. 1 means 100%

    Returns
    -------
    out : array_like
        absolute humidity in kg(H2O)/m^3

    """

    e_sat_h2o = calc_sat_vapor_pressure(temp)
    e_h2o = rel_hum * e_sat_h2o
    return calc_density(temp, e_h2o, R_h2o)

def virtual_temp(temp, spec_hum):
    """
    Calculate virtual temperature.

    Parameters
    ----------
    temp : array_like
        temperatur in K
    spec_hum : array_like
        specific humidity in kg(H2O)/kg(air)

    Returns
    -------
    out : array_like
        virtual temperatur in K

    """

    return temp * (1.0 + virt_temp_factor * spec_hum)

def co2_mass_mr(temp, pressure, co2_conc, abs_hum=None, rel_hum=None,
                spec_hum=None, h2o_conc=None):
    """
    Calculate CO2 mass mixing ratio.

    Needs one atmospheric humidity quantity.

    Parameters
    ----------
    temp : array_like
        temperatur in K
    pressure : array_like
        (partial) pressure in Pa
    co2_conc : array_like
        CO2 concentration in mol/m^3
    abs_hum : array_like, optional
        absolute humidity in kg(H2O)/m^3
    rel_hum : array_like, optional
        relative humidity as fraction of 1, ie. 1 means 100%
    spec_hum : array_like, optional
        specific humidity in kg(H2O)/kg(air)
    h2o_conc : array_like, optional
        H2O concentration in mol/m^3

    Returns
    -------
    out : array_like
        CO2 mass mixing ratio in kg(CO2)/kg(dry air)

    """

    if abs_hum is not None:
        pass
    elif rel_hum is not None:
        abs_hum = calc_ah_from_rh(temp, pressure, rel_hum)
    elif spec_hum is not None:
        abs_hum = calc_ah_from_sh(temp, pressure, spec_hum)
    elif h2o_conc is not None:
        abs_hum = h2o_conc * molar_mass_h2o
    else:
        raise RuntimeError("A measure of atmospheric humidity is required.")

    e_h2o = calc_vapor_pressure(temp, abs_hum, R_h2o)
    dry_air_mass = calc_density_dry_air(temp, pressure, e_h2o) # * 1.0 because it is for 1 m^3
    mass_mr = co2_conc * molar_mass_co2 / dry_air_mass

    ### alternative version via virtual temperature
    # spec_hum = calc_sh_from_ah(temp, pressure, rel_hum)
    # virt_temp = virtual_temp(temp, spec_hum)
    # molar_density_air = pressure / (R * virt_temp)
    # mixing_ratio = co2_conc / (molar_density_air - h2o_conc)
    # mass_mr2 = mixing_ratio * molar_mass_co2 / molar_mass_dry_air

    return mass_mr

def calc_dew_from_rh(temp, rel_hum):
 
    """
    Calculate Dewpoint temperature from relative humidity.

    Parameters
    ----------
    temp : array_like
        temperatur in degree Celsius
    rel_hum : array_like, optional
        relative humidity as fraction of 1, ie. 1 means 100%

    Returns
    -------
    out : array_like
        dew point in degree Celsius

    """

    rel_hum = rel_hum * 100.0

    Td = (b * gamma(temp,rel_hum)) / (a - gamma(temp,rel_hum))
 
    return Td
 
 
def gamma(temp,rel_hum):

    """
    Help function for dewpoint approximation calculation.

    """

    g = (a * temp / (b + temp)) + np.log(rel_hum/100.0)
 
    return g

def calc_rh_from_sh(temp, pressure, spec_hum):
 
    """
    Calculate relative humidity from specific humidity.

    Assumption: Clausius Clapeyron
    Source: https://earthscience.stackexchange.com/questions/2360/how-do-i-convert-specific-humidity-to-relative-humidity

    Parameters
    ----------
    temp : array_like
        temperatur in K
    pressure : array_like
        (partial) pressure in Pa
    spec_hum (q) : array_like, optional
        specific humidity in kg(H2O)/kg(air)

    Returns
    -------
    out : array_like
        relative humidity as fraction of 1, ie. 1 means 100%

    """

    # mass mixing ratios of water vapor at actual conditions
    w = spec_hum

    # Calculate saturation vapor pressure first and
    # second mass mixing ratio of water vapor at saturation
    ws = (0.622 * calc_sat_vapor_pressure(temp)) / pressure

    # Calculate and return relative humidity
    rh = w/ws
 
    return rh

def calc_thtv_from_sh(temp, pressure, spec_hum):
 
    """
    Calculate virtual potential temperature.

    Parameters
    ----------
    temp : array_like
        temperatur in K
    pressure : array_like
        (partial) pressure in Pa
    spec_hum (q) : array_like
        specific humidity in kg(H2O)/kg(air)

    Returns
    -------
    out : array_like
        virtual potential temperature (K)

    """

    # Calculate virtual temperature
    tv = virtual_temp(temp, spec_hum)

    # Calculate virtual potential temperature
    thtv = tv * ((100000.0 / pressure)**R_cp)
 
    return thtv
