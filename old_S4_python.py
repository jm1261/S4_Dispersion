import os
from organisation_functions import *
from sharexplot import doublesharex
import numpy as np
from scipy import interpolate
import decimal
import shutil

main_dir = plat_form()
sub_dir = main_dir + "/150219_to_010319/VASE"
dispersion_dir = sub_dir + "/Dispersions"
l_script = "S4_lua.lua"

harmonics = 225
period = range(460, 521, 30)
radius = range(60, 101, 5)
dose = np.linspace(1, 1.8, 5)
mat1 = ["Air", 1.00027717, 0, 0] ## matn = ["name", n, k, thickness] ##
mat2_thick = range(110, 131, 10) ## nm ##
mat3 = ["Silica", 1.4649, 0.0017953, 0] ## matn = ["name", n, k, thickness] ##

for a in range(len(period)):
	for b in range(len(radius)):
		for c in range(len(mat2_thick)):
			file_string = "aSiH_"
			data_files = datafiles(dirname=dispersion_dir, filestring=file_string)
			print(data_files)
			
			for d in range(len(data_files)):
				selected_file = data_files[d]
				H_Conc = selected_file.split("_")[1]
				file_name = dispersion_dir + "/" + selected_file
				xy = np.loadtxt(file_name, skiprows=2)
				
				for e in range(len(dose)):
					hole_radius = radius[b] * dose[e]
				
					def n(x):
						x_points = xy[:,0]
						y_points = xy[:,1]
						xyz = interpolate.splrep(x_points, y_points)
						return interpolate.splev(x, xyz)
					def k(x):
						x_points = xy[:,0]
						y_points = xy[:,2]
						abc = interpolate.splrep(x_points, y_points)
						return interpolate.splev(x, abc)
					def drange(y, z, jump):
						while y < z:
							yield float(y)
							y += decimal.Decimal(jump)
							
					txt_file = file_string +str(H_Conc) +"_" +str(harmonics) +"_" +str(period[a]) +"_" +str(mat2_thick[c]) +"_" + str(hole_radius) +"_" +str(mat1[0]) +".txt"
					output = " >> " +txt_file
					
					for x in drange(600, 900, 1):
						args = "harmonics = "+str(harmonics) +"; period = "+str(period[a]) +"; hole_radius = "+str(hole_radius) +"; wavelength = "+str(x) +"; mat1 = "+str(mat1[0]) +"; mat1_n = "+str(mat1[1]) +"; mat1_k = "+str(mat1[2]) +"; mat1_thick = "+str(mat1[3]) +"; mat2 = "+(str(file_string)+str(H_Conc)) +"; mat2_n = "+str(n(x)) +"; mat2_k = "+str(k(x)) +"; mat2_thick = "+str(mat2_thick[c]) +"; mat3 = "+str(mat3[0]) +"; mat3_n = "+str(mat3[1]) +"; mat3_k = "+str(mat3[2]) +"; mat3_thick = "+str(mat3[3])
						print(args)
						os.system('S4 -a ' +"\""+ args +"\" "+ l_script + output)
						
					ab = np.loadtxt(txt_file)
					wavelength = ab[:,0]
					transmission = ab[:,1]
					reflection = ab[:,2]
					
					graph_file = txt_file[0:-4] +".png"
					graph_dir = sub_dir +"/" +file_string +H_Conc
					txt_dir = graph_dir + "_Txt"
					
					graph_name = file_string +H_Conc +" Period " +str(period[a]) +" Thickness " +str(mat2_thick[c]) +" Hole Radius " +str(hole_radius) +" Top Layer " +str(mat1[0])
					
					doublesharex(x1=wavelength, x2=wavelength, y1=transmission, y2=reflection, fx=10, fy=7, lc1='b', lc2='orange', lw1=2, lw2=2, ln1="Transmission", ln2="Reflection", grid1=True, legend=True, frame=True, numcol=2, xlabel="Wavelength [nm]", xsize=14, ylabel1="Transmission", ysize1=14, ylabel2="Reflection", ysize2=14, ymin1=0, ymin2=0, ymax1=1, ymax2=1, title=graph_name, titlesize=18, plotshow=False, plotsave=True, graphname=graph_file)
					
					shutil.copy(graph_file, graph_dir)
					os.remove(graph_file)
					shutil.copy(txt_file, txt_dir)
					os.remove(txt_file)
