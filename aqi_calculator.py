import pandas as pd

molecule_list = []

class Molecule:
    def __init__(self, name, molar_mass):
        self.name = name
        self.molar_mass = molar_mass # Molar Mass is in grams per molecule
        self.concentration = 0
        molecule_list.append(self) 

"""
OpenWeatherMap provides ozone data on the 1-hour scale rather than the 8-hour scale.
Therefore, the 8-hour ozone row will be ommitted.
"""

# EPA standard table for determining AQI for individual pollutants

data = {
    "I_low-I_high": ["0-50", "51-100", "101-150", "151-200", "201-300", "301-400", "401-500"],
    # "Ozone (8-hour)": ["0.0-0.054", "0.055-0.070", "0.071-0.085", "0.086-0.105", "0.106-0.2", "-", "-"],
    "Ozone": ["-", "-", "0.125-0.164", "0.165-0.204", "0.205-0.404", "0.405-0.504", "0.505-0.604"], # 1-hour
    "Fine Particulate Matter": ["0.0-12.0", "12.1-35.4", "35.5-55.4", "55.5-150.4", "150.5-250.4", "250.5-350.4", "350.5-500.4"],
    "Coarse Particulate Matter": ["0-54", "55-154", "155-254", "255-354", "355-424", "425-504", "505-604"],
    "Carbon Monoxide": ["0.0-4.4", "4.5-9.4", "9.5-12.4", "12.5-15.4", "15.5-30.4", "30.5-40.4", "40.5-50.4"],
    "Sulfur Dioxide": ["0-35", "36-75", "76-185", "186-304", "305-604", "605-804", "805-1004"],
    "Nitrogen Dioxide": ["0-53", "54-100", "101-360", "361-649", "650-1249", "1250-1649", "1650-2049"]
}

df = pd.DataFrame(data)

# Instantiating molecules
o3 = Molecule('Ozone', 48)
no2 = Molecule('Nitrogen Dioxide', 46.0055)
so2 = Molecule('Sulfur Dioxide', 64.066)
co = Molecule('Carbon Monoxide', 28.01)
pm2_5 = Molecule('Fine Particulate Matter', None)
pm10 = Molecule('Coarse Particulate Matter', None)

air_molar_volume = 24.45 # molar volume of air in liters at NTP conditions (25°C and 760 torr)

"""
c_p = the truncated concentration of pollutant p
bp_hi = the concentration breakpoint that is greater than or equal to c_p
bp_low = the concentration breakpoint that is less than or equal to c_p
i_hi = the AQI value corresponding to bp_high
i_low = the AQI value corresponding to bp_low

"""

# Formula for calculating the AQI of an individual pollutant
def aqi_formula(c_p, bp_hi, bp_low, i_hi, i_low):
    return round((((i_hi - i_low)/(bp_hi - bp_low)) * (c_p - bp_low)) + i_low)

# Calculate which pollutant has the highest AQI score
def calculate_aqi(pollutant_data):
    # Converts molecule concentrations to appropriate units of measurement and changes the instance varaibles accordingly
    for molecule in molecule_list:
        if (molecule.name == 'Ozone'):
            molecule.concentration = mg_per_m3_to_ppm(molecule, pollutant_data.get('o3', 0))
        elif (molecule.name == 'Carbon Monoxide'):
            molecule.concentration = mg_per_m3_to_ppm(molecule, pollutant_data.get('co', 0))
        elif (molecule.name == 'Nitrogen Dioxide'):
            molecule.concentration = mg_per_m3_to_ppb(molecule, pollutant_data.get('no2', 0))
        elif (molecule.name == 'Sulfur Dioxide'):
            molecule.concentration = mg_per_m3_to_ppb(molecule, pollutant_data.get('so2', 0))

    pm2_5.concentration = pollutant_data.get('pm2_5', 0)
    pm10.concentration = pollutant_data.get('pm10', 0)

    # Truncating values in accordance to EPA standards
    o3.concentration = truncate(o3.concentration, 3)
    no2.concentration = truncate(no2.concentration, 0)
    so2.concentration = truncate(so2.concentration, 0)
    co.concentration = truncate(co.concentration, 1)
    pm2_5.concentration = truncate(pm2_5.concentration, 1)
    pm10.concentration = truncate(pm10.concentration, 0)

    aqi_scores = []

    for molecule in molecule_list:
        aqi_scores.append(calculate_individual_aqi(molecule))

    # The official AQI score is represented by the pollutant which has the highest individual AQI score
    return max(aqi_scores)

def calculate_individual_aqi(pollutant):
    # Grab table data given the type of pollutant
    pollutant_data = data[pollutant.name]
    c_p = pollutant.concentration
    
    # 1-hour ozone levels less than 0.125 do not define AQI
    if (pollutant.name == 'Ozone') and (c_p < 0.125):
        return 0.0

    # Determine AQI breakpoint
    def find_index(data, number):
        for index, range_str in enumerate(data):
            if (range_str == '-'):
                continue
            lower, upper = map(float, range_str.split('-'))
            if lower <= number <= upper:
                return index
        return -1
    
    index = find_index(pollutant_data, c_p)
    
    # Find corresponding table data
    if index != -1:
        aqi_range = data["I_low-I_high"][index]
    else:
        # This would happen if a pollutant has an AQI score so large that its corresponding table value is not present
        return 500

    lower_str, upper_str = aqi_range.split('-')

    # Converting the string values to integers
    i_hi = int(upper_str)
    i_low = int(lower_str)
    
    bp_low, bp_hi = pollutant_data[index].split('-')

    aqi_score = aqi_formula(float(c_p), float(bp_hi), float(bp_low), float(i_hi), float(i_low)) 
    return aqi_score  

def truncate(number, decimal_points):
    if decimal_points < 0:
        raise ValueError("Decimal points must be a non-negative integer.")

    factor = 10 ** decimal_points
    return int(number * factor) / factor

# The conversion of a microgram of a molecule per meter^3 to parts per million (PPM)
def mg_per_m3_to_ppm(molecule, concentration):
    molecule.concentration = mg_per_m3_to_ppb(molecule, concentration) / 1000
    return molecule.concentration

# The conversion of a microgram of a molecule per meter^3 to parts per billion (PPB)
def mg_per_m3_to_ppb(molecule, concentration):
    molecule.concentration = 24.45 * concentration / molecule.molar_mass
    return molecule.concentration
