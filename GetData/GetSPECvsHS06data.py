# Code to extract the data for Figure 1 of the 2021 CSBS Paper

import datetime
import pandas as pd
import json

# data file and fix "dashes"
filename = 'es_bmk_2018-06-27.pickle'
pdf0 = pd.read_pickle(filename)

pdf0.columns = [i.replace('-', '_') for i in pdf0.columns]

# Print keys
#for x in pdf0.keys():
#    print(x)

# Cuts from SPEC-CPU2017-Analysis-Include-AMD.ipynb
pdf1 = pdf0.query('cloud != "CERN-wig-project-011"')
pdf2 = pdf1.query('tstart > datetime.date(2018,3,15)')

# For next set of cuts
pdf     = pdf2

pdf['rstart'] = pdf.tstart.apply(lambda x: x.replace(microsecond=0,second=0,minute=0))
pdf['spec2017_bmks_541_leela_r'].head()
pdf_threads_socket = pdf.groupby(['cpuname']).cpunum.quantile(.75).reset_index().rename(columns={'cpunum':'totThreads'}).copy()
npdf = pdf.merge(pdf_threads_socket,how='left',on='cpuname')
npdf.groupby(['cloud','pnode'])[['cpunum','totThreads']].describe()
to_be_excluded = npdf[(npdf.cpunum<npdf.totThreads) & ~(npdf.cloud == 'GridKa')].groupby(['cloud','pnode','totThreads','rstart']).cpunum.agg(['mean','count']).reset_index().query('mean*count<totThreads')
#print(to_be_excluded['pnode'].unique())
#print(to_be_excluded['cloud'].unique())
tmp_pdf = npdf.merge(to_be_excluded,how='left',on=['cloud','pnode','totThreads'],suffixes=('','_y'))
#redefine npdf
fpdf = tmp_pdf[tmp_pdf.rstart_y.isnull()]
vm1 = 'bmk12-slc6-iuogw8ce6s_d7b47da5-b2d1-46e0-b0aa-f5b0adc25b9d'
vm2 = 'bmk12-slc6-o5jvcmjxsm_8b179c55-7967-4979-a4db-470d891c1ba9'
fpdf = fpdf[~(((fpdf.UID==vm1) | (fpdf.UID==vm2)) & (fpdf.hs06_32_avg_core_score>10.7))]
vm1 = 'bmk8-slc6-pvdd93rtag_61dfe509-27cd-44b7-8022-33d804baf902'
vm2 = 'bmk8-slc6-pdv4w02yj5_37c8109e-a34b-41de-939d-43020cebbcac'
vm3 = 'bmk8-slc6-oxddsmf2pl_bc675907-0fd8-4891-bc40-1a67bf138333'

#fpdf = fpdf[~(((fpdf.UID==vm1) | (fpdf.UID==vm2) | (fpdf.UID==vm3)) & (fpdf.hs06_32_avg_core_score>13))]
fpdf = fpdf[~(((fpdf.UID==vm1) | (fpdf.UID==vm2) | (fpdf.UID==vm3)))]

fpdf = fpdf.query('pnode!="p06253971a08885"')

fpdf[fpdf.cpunum<fpdf.totThreads].groupby(['cloud','pnode','totThreads','rstart']).cpunum.agg(['mean','count']).reset_index().query('mean*count<totThreads')
fpdf = fpdf[(fpdf.cloud != 'GridKa') | (fpdf.rstart > '2018-07-02')]

pdf = fpdf

# summarize input file
# --------------------
"""
print()
print("**********************************************************************")
print("\nInitial number of entries in file       = ", len(pdf0))
print("------> remove bad cloud        = ", len(pdf1))
print("------> Time cut        = ", len(pdf2))
print("-------------------------------------------------")
print("------> Final number for analysis       = ", len(pdf))
print()
print("Unique CPUs = ", len(pdf.cpuname))
print(pdf.groupby(['cpuname','cpunum']).size())
print(pdf.groupby(['cpuname','cloud']).size())
"""
# make a dataframe for each cpuname
# ---------------------------------
cpu_collection = {}
cpuname = pdf.cpuname.unique()

# Loop to write out benchmark scores
for cpu in cpuname:
    #print(cpu)
        
    cpu_collection[cpu] = pdf.query('cpuname == @cpu')

    cpunum = cpu_collection[cpu].cpunum.unique()

    # This if else block is here because the E5-2630 v4 was profiled in two different ways, and the data need to be separated
    if cpu == "Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz":
        clouds = cpu_collection[cpu].cloud.unique()
        print(cpu, end = '')

        for cloud in clouds:
            print(cloud)
            cpu_collection_cloud = cpu_collection[cpu].query('cloud == @cloud')
            num = 20
            print(num)

   	    # Different options for error bars
            print(cpu_collection_cloud['hs06_32_score'].mean() / float(num))
            print(cpu_collection_cloud['hs06_32_score'].std() / float(num))
            #print(cpu_collection_cloud['hs06_32_score'].quantile(0.75) / float(num) - cpu_collection_cloud['hs06_32_score'].quantile(0.25) / float(num))
            #print(cpu_collection_cloud['hs06_32_score'].quantile(0.95) / float(num) - cpu_collection_cloud['hs06_32_score'].quantile(0.05) / float(num))
            print(cpu_collection_cloud['hs06_64_score'].mean() / float(num))
            print(cpu_collection_cloud['hs06_64_score'].std() / float(num))
            #print(cpu_collection_cloud['hs06_64_score'].quantile(0.75) / float(num) - cpu_collection_cloud['hs06_64_score'].quantile(0.25) / float(num))
            #print(cpu_collection_cloud['hs06_64_score'].quantile(0.95) / float(num) - cpu_collection_cloud['hs06_64_score'].quantile(0.05) / float(num))
            print(cpu_collection_cloud['spec2017_score'].mean() / float(num))
            print(cpu_collection_cloud['spec2017_score'].std() / float(num))
            #print(cpu_collection_cloud['spec2017_score'].quantile(0.75) / float(num) - cpu_collection_cloud['spec2017_score'].quantile(0.25) / float(num))
            #print(cpu_collection_cloud['spec2017_score'].quantile(0.95) / float(num) - cpu_collection_cloud['spec2017_score'].quantile(0.05) / float(num))
    else:
        print(cpu)

        for num in cpunum:
            print(num)
    
            cpu_collection_num = cpu_collection[cpu].query('cpunum == @num')

	    # Different options for error bars
            print(cpu_collection_num['hs06_32_score'].mean() / float(num))
            print(cpu_collection_num['hs06_32_score'].std() / float(num))
            #print(cpu_collection_num['hs06_32_score'].quantile(0.75) / float(num) - cpu_collection_num['hs06_32_score'].quantile(0.25) / float(num))
            #print(cpu_collection_num['hs06_32_score'].quantile(0.95) / float(num) - cpu_collection_num['hs06_32_score'].quantile(0.05) / float(num))
            print(cpu_collection_num['hs06_64_score'].mean() / float(num))
            print(cpu_collection_num['hs06_64_score'].std() / float(num))
            #print(cpu_collection_num['hs06_64_score'].quantile(0.75) / float(num) - cpu_collection_num['hs06_64_score'].quantile(0.25) / float(num))
            #print(cpu_collection_num['hs06_64_score'].quantile(0.95) / float(num) - cpu_collection_num['hs06_64_score'].quantile(0.05) / float(num))
            print(cpu_collection_num['spec2017_score'].mean() / float(num))
            print(cpu_collection_num['spec2017_score'].std() / float(num))
            #print(cpu_collection_num['spec2017_score'].quantile(0.75) / float(num) - cpu_collection_num['spec2017_score'].quantile(0.25) / float(num))
            #print(cpu_collection_num['spec2017_score'].quantile(0.95) / float(num) - cpu_collection_num['spec2017_score'].quantile(0.05) / float(num))

exit()

