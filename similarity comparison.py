import os
from IPython.display import display, clear_output
from time import *
from func_cif import cif
from func_hkl import hkl
import numpy as np

# Read global input from text file.
globalInput = open("global_input.txt")
globalInputLines = globalInput.readlines()
for line in globalInputLines:
    if "cal_mode" in line:
        cal_mode = line.split()[2]
    elif "in_dir" in line:
        in_dir = line.split()[2]
    elif "out_dir" in line:
        out_dir = line.split()[2]
    elif "log_dir" in line:
        log_dir = line.split()[2]
    elif "cif_suffix" in line:
        cif_suffix = line.split()[2]
    elif "hkl_max" in line:
        hklMax = int(line.split()[2])
    elif "2theta_min" in line:
        twoThetaMin = float(line.split()[2])
    elif "2theta_max" in line:
        twoThetaMax = float(line.split()[2])

# Use script func_hkl to generate hkl matrix
print("Generating hkl matrix")
hkl_info = hkl(hklMax)
print("hkl_info done!\n") # This print is usually ignored



cwdir = os.getcwd()
# Count availble CIF files
cif_count = 0
for path, dirs, files in os.walk(in_dir):
    for file in files:
        if file.endswith(cif_suffix):
            cif_count += 1

# Calculate XRD and show progress
cif_cal_count = 0
cif_fail_count = 0
for path, dirs, files in os.walk(in_dir):
    for file1 in files:
        if file.endswith(cif_suffix):
            # Write a log file
            # print("Calculating " + path + ": " + file,)
            # Here combines cwd and subdirectory
            full_dir = "{}/{}".format(cwdir, path)
            # Here record timing
            time_start = time()
            # Here calls main function to calculate XRD and output
            cif_return = cif(full_dir, file, out_dir, hkl_info, twoThetaMin, twoThetaMax, cal_mode)
            # Here record timing
            time_cost = format(time() - time_start, '.3f')
            cif_cal_count += 1
            if type(cif_return) != str:
                cell1 = cif_return
                for file2 in files:
                    if file.endswith(cif_suffix):
                        full_dir = "{}/{}".format(cwdir, path)
                        cif_return = cif(full_dir, file, out_dir, hkl_info, twoThetaMin, twoThetaMax, cal_mode)
                        if type(cif_return) != str:
                            cell2 = cif_return
                            if cell1 == cell2:
                                print("{file1} and {file2} has same cell")


