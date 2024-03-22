import json
import csv
import pandas as pd
import numpy as np
from Project.main import read_cable_characteristics

df = read_cable_characteristics()

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        dtypes = (np.datetime64, np.complexfloating)
        if isinstance(obj, dtypes):
            return str(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            if any([np.issubdtype(obj.dtype, i) for i in dtypes]):
                return obj.astype(str).tolist()
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


# Data to be written

# dictionary = {
# 	"emp_details":[
# 		{
# 			"name": "fatmaayancik",
#
# 			"rollno": 56,
# 			"cgpa": 8.6,
# 			"phonenumber": "9976770500"
# 		},
# 		{	"name": "fatmos",
# 			"rollno": 47,
# 			"cgpa": 9,
# 			"phonenumber": "9976710000"
# 		}
# 	]
# }

# dictionary = {
# 			"name": "fatmaayancik",
# 			"rollno": 56,
# 			"cgpa": 8.6,
# 			"phonenumber": "9976770500"
# }

# with open("sample.json", "w") as outfile:
#     json.dump(dictionary, outfile)
#
# # Opening JSON file
# with open('sample.json', 'r') as openfile:
# 	# Reading from json file
# 	json_object = json.load(openfile)
#
# print(json_object)
# print(type(json_object))
# ---------------------------------------------------------------------------------------------------------------------
# Serial JSON dictionary
# Data to be written
dictionary = {
	"staycable_details": [
		{"Cable_name": df[0],
		 "System_type": df[1],
		 "Number_of_strands": df[3],
		 "Cable_mass": df[4],  # [kg/m]
		 "Inclination": df[5],  # [deg]
		 "Eff_cross_section": df[6],
		 "Length_BP2BP": df[7],
		 "Transition_length_pylon": df[8],
		 "Transition_length_deck": df[9],
		 "Deviator_pylon": df[10],
		 "Deviator_deck": df[11],
		 "Deviator_pos_pylon": df[12],
		 "Deviator_pos_deck": df[13],
		 "Estimated_tension": df[14],
		 "E_modulus": df[15],
		 "Diameter": df[16],
		 "Air_density": df[17]

		 },
		{
		 "Cable_name": df[0],
		 "System_type": df[1],
		 "Number_of_strands": df[3],
		 "Cable_mass": df[4],  # [kg/m]
		 "Inclination": df[5],  # [deg]
		 "Eff_cross_section": df[6],
		 "Length_BP2BP": df[7],
		 "Transition_length_pylon": df[8],
		 "Transition_length_deck": df[9],
		 "Deviator_pylon": df[10],
		 "Deviator_deck": df[11],
		 "Deviator_pos_pylon": df[12],
		 "Deviator_pos_deck": df[13],
		 "Estimated_tension": df[14],
		 "E_modulus": df[15],
		 "Diameter": df[16],
		 "Air_density": df[17]
		}
	]
}
# ---------------------------------------------------------------------------------------------------------------------

# # Serializing json

with open('cable.json', 'w') as f:
	json.dump(dictionary, f, cls=NpEncoder)










# staycable_details = json_object['staycable_details']
# print(json_object)
# print(type(json_object))

# # now we will open a file for writing
# data_file = open('data_file.csv', 'w')
#
# # create the csv writer object
# csv_writer = csv.writer(data_file)
#
# # Counter variable used for writing
# # headers to the CSV file
# count = 0
#
# for emp in emp_details:
# 	if count == 0:
# 		# Writing headers of CSV file
# 		header = emp.keys()
# 		csv_writer.writerow(header)
# 		count += 1
#
# 	# Writing data of CSV file
# 	csv_writer.writerow(emp.values())
#
# data_file.close()

