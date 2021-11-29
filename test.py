import os
cwdir = os.getcwd()
print(cwdir)
for path, dirs, files in os.walk("archive_cif/cod_archive/1"):
    for file1 in files:
        if file1.endswith(".cif"):
            print(path)
