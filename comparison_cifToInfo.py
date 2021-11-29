cifInfo = open("archive_log/cell_log_archive_cif_cod_archive_1_mode_similarity_comparision_v2.txt")
cifInfoLines = cifInfo.readlines()

cal_log = open("archive_log/cifToInfo_v2.txt", "a")

size = len(cifInfoLines)

for i in range (0, size):
    print(i)
    for j in range (i+1, size):
        if cifInfoLines[i].split()[1:] == cifInfoLines[j].split()[1:]:
            print(cifInfoLines[i].split()[0], cifInfoLines[j].split()[0], file = cal_log)

cal_log.close()
