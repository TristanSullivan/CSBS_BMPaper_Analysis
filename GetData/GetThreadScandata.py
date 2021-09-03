# Code to make Figure 10 

import datetime
import pandas as pd

# data file and fix "dashes"
# --------------------------

filename = 'Analysis/ExtractDataFromES/data/pdf_bmkwg-prod-hepscore-v2.1rc0_46bb2226.pkl'
filename2 = 'Analysis/ExtractDataFromES/data/pdf_bmkwg-prod-hepscore-v2.0_46bb2226.pkl'


pdf0_1 = pd.read_pickle(filename)
pdf0_2 = pd.read_pickle(filename2)
foo = [pdf0_1, pdf0_2]
pdf0 = pd.concat(foo)

pdf0.columns = [i.replace('-', '_') for i in pdf0.columns]

# Print keys
#for x in pdf0.keys():
#    print(x)

# check that atlas bmks exist
pdf1    = pdf0.query('hepscore_status=="success"')
pdf2 = pdf1.query('host_tags_cloud == "HEP-Ironic-scan" or host_tags_cloud == "HEP-Ironic"')

# final set to analyze
pdf     = pdf2


# summarize input file
# --------------------
"""
print()
print("**********************************************************************")
print("\nInitial number of entries in file       = ", len(pdf0))
print("------> require hepscore success        = ", len(pdf1))
print("------> require HEP-Ironic or HEP-Ironic-scan      = ", len(pdf2))
print("-------------------------------------------------")
print("------> Final number for analysis       = ", len(pdf))
print()
print("Unique CPUs = ", len(pdf.host_HW_CPU_CPU_Model.unique()))
print(pdf.groupby(['host_HW_CPU_CPU_Model','host_HW_CPU_CPU_num']).size())
"""
# make a dataframe for each cpuname
# ---------------------------------
cpu_collection = {}
Scores = {}
Benchmarks = []
Benchmarktags = []

Benchmarks.append("hepscore")
Benchmarks.append("hs06")

Benchmarktags.append("hepscore_score")
Benchmarktags.append("hs06_score")

Copies_hepscore = {}
Copies_hs06 = {}

for item in Benchmarks:
    Scores[item] = {}

cpuname = pdf.host_HW_CPU_CPU_Model.unique()

for cpu in cpuname:
    cpu_collection[cpu] = pdf.query('host_HW_CPU_CPU_Model == @cpu')
    Copies_hepscore[cpu] = cpu_collection[cpu]["hepscore_benchmarks_lhcb_gen_sim_bmk_run_info_copies"].array
    Copies_hs06[cpu] = cpu_collection[cpu]["hs06_copies"].array


    for i in range(0, len(Benchmarks)):
        Scores[Benchmarks[i]][cpu] = []
        Scores[Benchmarks[i]][cpu] = cpu_collection[cpu][Benchmarktags[i]].array

for key in Scores:
    print(key)

    for key2 in Scores[key]:
        counter = 0
        print(key2)

        for item in Scores[key][key2]:
            if key == "hs06":
                cores = Copies_hs06[key2][counter]
            else:
                cores = Copies_hepscore[key2][counter]
                
            counter = counter + 1
            if key == "hepscore" or key == "hs06": 
                 print(item, cores)

exit()

