import pickle
import json
import cv2
import numpy as np
import os

material_absorpition_coeffcieint = "/fs/nexus-scratch/jeran/GWA/tools/material_absorption.pickle"
material_file = pickle.load(open(material_absorpition_coeffcieint, "rb"))
in_folder_path = "/fs/nexus-scratch/jeran/image/test-seen/"
brain_folder_path1 = "/scratch1/anton/Soundspaces/test-seen_full/test-seen_material/"
brain_folder_path2 = "/scratch1/anton/Soundspaces/test-seen_full/test-seen_segment/"

file_list = os.listdir(in_folder_path)

material_name = "/fs/nexus-scratch/jeran/image/material_name.pickle"
name_file = pickle.load(open(material_name, "rb"))

for folds in file_list:
	# print("folds ",folds)
	fold_list = os.listdir(in_folder_path+folds)
	for files in fold_list:
		print("files ",files)

		if(files.endswith("json")):
			file_name_json = in_folder_path + folds +"/" + files
			brain_name_json1 = brain_folder_path1 + folds +"/" + files
			brain_name_json2 = brain_folder_path2 + folds +"/" + files

			file_name_png = file_name_json.replace("_label.json",".png")
			file_name_absorption = brain_name_json1.replace("_label.json",".png")
			file_name_segment_png = brain_name_json2.replace("_label.json","_segment.png")
			print("file_name ",file_name_json)
			f = open(file_name_json)
			data = json.load(f)
			image = cv2.imread(file_name_png)
			shape = image.shape
			new_image_2 = 128 * np.ones(shape, dtype=int)

			num_materials = len(data['mask'])

			for j in range(1,num_materials):
				x1 = int(data['mask'][1]['box'][0])
				y1 = int(data['mask'][1]['box'][1])
				x2 = int(data['mask'][1]['box'][2])
				y2 = int(data['mask'][1]['box'][3])
				material = data['mask'][1]['label']
				material_num = int(name_file[material] //len(list(name_file.keys())) *255)
				color = np.array([material_num, material_num, material_num])
				
				absorption= material_file[material]
				absorption_new=np.array([int(absorption[1]*16)+(int(absorption[2]*16)*16),int(absorption[3]*16)+(int(absorption[4]*16)*16),int(absorption[5]*16)+(int(absorption[6]*16)*16)])


				new_image_2[y1:y2,x1:x2,:]= absorption_new #absorption

			cv2.imwrite(file_name_absorption,new_image_2)



