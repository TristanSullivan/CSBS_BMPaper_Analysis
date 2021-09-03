# Code to extract B2 data for Figure 3
# For other workloads, see GetReferenceMachinedata.py

import datetime
import pandas as pd

# data file and fix "dashes"
filename = 'Analysis/ExtractDataFromES/data/pdf_bmkwg-prod-hepscore-v2.0-dev0_a9d9701c.pkl'
pdf0 = pd.read_pickle(filename)

# Print keys
#for x in pdf0.keys():
#    print(x)

pdf0.columns = [i.replace('-', '_') for i in pdf0.columns]
# Select reference machine
pdf1    = pdf0.query('host_HW_CPU_CPU_Model == "Intel(R) Xeon(R) CPU E5-2630 v3 @ 2.40GHz"' )


# final set to analyze
pdf     = pdf1

# summarize input file
# --------------------
"""
print()
print("**********************************************************************")
print("\nInitial number of entries in file       = ", len(pdf0))
print("------> Select reference machine CPU   = ", len(pdf1))
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

Benchmarks.append("belle2_gen_sim_reco")

Benchmarktags.append("hepscore_wl_scores_belle2_gen_sim_reco_bmk_gen_sim_reco")

Copies_hepscore = {}

for item in Benchmarks:
    Scores[item] = {}

cpuname = pdf.host_HW_CPU_CPU_Model.unique()

for cpu in cpuname:
    cpu_collection[cpu] = pdf.query('host_HW_CPU_CPU_Model == @cpu')
    Copies_hepscore[cpu] = cpu_collection[cpu]["hepscore_benchmarks_belle2_gen_sim_reco_bmk_run_info_copies"].array


    for i in range(0, len(Benchmarks)):
        Scores[Benchmarks[i]][cpu] = []
        Scores[Benchmarks[i]][cpu] = cpu_collection[cpu][Benchmarktags[i]].array

for key in Scores:
    print(key)

    for key2 in Scores[key]:
        counter = 0
        print(key2)

        for item in Scores[key][key2]:
            cores = Copies_hepscore[key2][counter]

            counter = counter + 1
            print(item, cores)
exit()

