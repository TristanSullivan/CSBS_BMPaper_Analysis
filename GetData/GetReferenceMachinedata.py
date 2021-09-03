# Code to get the data for Figure 3
# The files used here don't include B2 data; see GetB2RefData.py

import datetime
import pandas as pd


# data file and fix "dashes"
# --------------------------

filename = 'pdf_bmkwg-prod-hepscore-v01_dc78745b.pkl'
filename2 = 'pdf_bmkwg-prod-hepscore-v1.8_dc78745b.pkl'
filename3 = 'pdf_bmkwg-prod-hepscore-v2.1-dev_dc78745b.pkl'

pdf0_1 = pd.read_pickle(filename)
pdf0_2 = pd.read_pickle(filename2)
pdf0_3 = pd.read_pickle(filename3)
foo = [pdf0_1, pdf0_2, pdf0_3]
pdf0 = pd.concat(foo)

# Print keys
#for x in pdf0.keys():
#    print(x)

pdf0.columns = [i.replace('-', '_') for i in pdf0.columns]

# Online selection
pdf1    = pdf0.query('host_VO == "hepscore-determine-refval" and  hepscore_hash == "891496727e3e1b0b2fdbd70303cc53758300ac73c498679e15c4b7952d69c443"' )


# This is in the online notebook, but doesn't seem to remove any reference machine data. Left it in anyway.
bmks = {"atlas_gen", "atlas_sim", "atlas_digi_reco", "cms_gen_sim", "cms_digi", "cms_reco", "lhcb_gen_sim"}

pdfs = []
counter = 0
pdfs.append(pdf1)
for i in range(0, 3):
    for bmk in bmks:
        if bmk != "atlas_digi_reco":
            querystring = "hepscore_benchmarks_" + bmk + "_bmk_run" + str(i) + "_report_log != \"ERROR\""
            pdfs.append(pdfs[counter].query(querystring))
            counter = counter + 1
            pdf = pdfs[counter]
        else:
            querystring = "hepscore_benchmarks_" + bmk + "_bmk_run" + str(i) + "_duration > 1000"
            pdfs.append(pdfs[counter].query(querystring))
            counter = counter + 1
            pdf = pdfs[counter]


# summarize input file
# --------------------
"""
print()
print("**********************************************************************")
print("\nInitial number of entries in file       = ", len(pdf0))
print("------> Select reference machine data   = ", len(pdf1))
print("-------------------------------------------------")
print("------> Final number for analysis       = ", len(pdf))
print()
print("Unique CPUs = ", len(pdf.host_cpuname.unique()))
print(pdf.groupby(['host_cpuname','host_cpunum']).size())
"""
# make a dataframe for each cpuname
# ---------------------------------
MinEntries = 10
cpu_collection = {}
Scores = {}
Benchmarks = []
Benchmarktags = []

Benchmarks.append("hepscore")
Benchmarks.append("atlas_gen")
Benchmarks.append("atlas_sim")
Benchmarks.append("cms_gen_sim")
Benchmarks.append("cms_digi")
Benchmarks.append("cms_reco")
Benchmarks.append("lhcb_gen_sim")


Benchmarktags.append("hepscore_score")
Benchmarktags.append("hepscore_wl_scores_atlas_gen_bmk_gen")
Benchmarktags.append("hepscore_wl_scores_atlas_sim_bmk_sim")
Benchmarktags.append("hepscore_wl_scores_cms_gen_sim_bmk_gen_sim")
Benchmarktags.append("hepscore_wl_scores_cms_digi_bmk_digi")
Benchmarktags.append("hepscore_wl_scores_cms_reco_bmk_reco")
Benchmarktags.append("hepscore_wl_scores_lhcb_gen_sim_bmk_gen_sim")

Copies_hepscore = {}

for item in Benchmarks:
    Scores[item] = {}

cpuname = pdf.host_cpuname.unique()

for cpu in cpuname:
    cpu_collection[cpu] = pdf.query('host_cpuname == @cpu')
    Copies_hepscore[cpu] = cpu_collection[cpu]["hepscore_benchmarks_lhcb_gen_sim_bmk_run0_report_copies"].array

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

