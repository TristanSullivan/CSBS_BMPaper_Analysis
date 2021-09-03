# Code to get the data for Figure 9

import json
import pandas as pd

# Aug. 10, include procurement data
filename = 'Analysis/ExtractDataFromES/data/pdf_bmk-prod-hepscore-v2.1_19cd09aa.pkl'
filename2 = 'Analysis/ExtractDataFromES/data/pdf_bmk-prod-hepscore-v2.0_19cd09aa.pkl'

pdf0_1 = pd.read_pickle(filename)
pdf0_2 = pd.read_pickle(filename2)
foo = [pdf0_1, pdf0_2]
pdf0 = pd.concat(foo)

# Print keys
#for x in pdf0.keys():
#    print(x)

# Replace dashes with underscores
pdf0.columns = [i.replace('-', '_') for i in pdf0.columns]

# Replicating cuts in HS06-HEPWL-dataset_v2.0.ipynb from hep-benchmarks/private-tools repository
pdf1    = pdf0.query('host_tags_cloud==\"IronicSuitev2\"')

hepscore_reject_hash_json = "Analysis/Notebooks/data/hepscore_reject_hash.json"
with open(hepscore_reject_hash_json) as f:
    hepscore_reject_hash_list = json.loads(f.read())
    f.close()

#print("\nRejected hash list\n", hepscore_reject_hash_list)
# NB the pdf.hepscore_hash.isna() is needed to include the HS06 results!!! do not remove


pdf2 = pdf1[~(pdf1.hepscore_app_info_config_hash.isin(hepscore_reject_hash_list)) | pdf1.hepscore_app_info_config_hash.isna()] 
pdf3 = pdf2.query('hs06_hash == \"d4526aa8d1a97f5c8dfeac384d37e0b2\"')
pdf4 = pdf3.query('host_HW_CPU_CPU_num > 4')

# final set to analyze
pdf     = pdf4

# summarize input file
# --------------------
"""
print()
print("**********************************************************************")
print("\nInitial number of entries in file       = ", len(pdf0))
print("------> require IronicSuitev2    = ", len(pdf1))
print("------> remove bad HEPscore hash values    = ", len(pdf2))
print("------> remove bad HS06 hash values    = ", len(pdf3))
print("------> remove 4 core    = ", len(pdf4))
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
Benchmarks.append("belle2_gen_sim_reco")
Benchmarks.append("lhcb_gen_sim")
Benchmarks.append("atlas_gen")
Benchmarks.append("cms_gen_sim")
Benchmarks.append("cms_digi")
Benchmarks.append("cms_reco")
Benchmarks.append("hs06")

Benchmarktags.append("hepscore_score")
Benchmarktags.append("hepscore_wl_scores_belle2_gen_sim_reco_bmk_gen_sim_reco")
Benchmarktags.append("hepscore_wl_scores_lhcb_gen_sim_bmk_gen_sim")
Benchmarktags.append("hepscore_wl_scores_atlas_gen_bmk_gen")
Benchmarktags.append("hepscore_wl_scores_cms_gen_sim_bmk_gen_sim")
Benchmarktags.append("hepscore_wl_scores_cms_digi_bmk_digi")
Benchmarktags.append("hepscore_wl_scores_cms_reco_bmk_reco")
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
            print(item, cores)
exit()

