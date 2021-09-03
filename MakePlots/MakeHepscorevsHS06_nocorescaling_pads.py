#!/usr/bin/python2

# Make Figure 8
# Bisector, horizontal line, and correlation factor need to be added manually
# I used ROOT interactively for this
# This script also plots the HEPscore and HS06 histograms for each CPU

import math
from ROOT import TCanvas, TPad, TGraph, gApplication, TLegend, TF1, TH1F, TH2F, TGraphErrors, TMultiGraph

bmresults = {}
bms = ["hepscore", "belle2_gen_sim_reco", "lhcb_gen_sim", "atlas_gen", "cms_gen_sim", "cms_digi", "cms_reco", "hs06"]

refs = {}
hists = {}

bmresultsfile = open('./HepscorevsHS06data', 'r')
bmresultsstring = bmresultsfile.read()
bmresults_lines = bmresultsstring.split('\n')

cpus = ["AMD EPYC 7302 16-Core Processor", "Intel(R) Xeon(R) Gold 6338 CPU @ 2.00GHz", "AMD EPYC 7763 64-Core Processor", "Intel(R) Xeon(R) Platinum 8380 CPU @ 2.30GHz", "Intel(R) Xeon(R) Platinum 8360H CPU @ 3.00GHz", "AMD EPYC 7742 64-Core Processor", "Intel(R) Xeon(R) Platinum 8268 CPU @ 2.90GHz", "Intel(R) Xeon(R) Platinum 8168 CPU @ 2.70GHz", "Intel(R) Xeon(R) CPU E5-2680 v4 @ 2.40GHz", "Intel(R) Xeon(R) CPU E5-2630 v3 @ 2.40GHz", "Intel(R) Xeon(R) CPU E5-2650 v4 @ 2.20GHz", "Intel(R) Xeon(R) Gold 6130 CPU @ 2.10GHz", "Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz", "Intel(R) Xeon(R) Platinum 8358 CPU @ 2.60GHz", "Intel(R) Xeon(R) Silver 4216 CPU @ 2.10GHz"]

finalhist = TH2F("finalhist", "", 250, 0, 2.5, 250, 0, 2.5)
finalgraph = TGraphErrors()
finalgraph_hton = TGraphErrors()
finalgraph_htoff = TGraphErrors()
residuals = TGraphErrors()
residuals_hton = TGraphErrors()
residuals_htoff = TGraphErrors()

for cpu in cpus:
    bmresults[cpu] = {}
    hists[cpu] = {}

    for bm in bms:
        hists[cpu][bm] = {}
        bmresults[cpu][bm] = {}

for line in bmresults_lines:
    if line in bms:
        currentbm = line
        #print(currentbm)

    elif line in cpus:
        currentcpu = str(line)
        #if currentbm == "hepscore":
            #print(currentcpu)
        
    else:
        if len(line.split()) == 2:
            score = str(line.split()[0])
            cores = str(line.split()[1])
            #if currentbm == "hs06":
                #print(score, cores)

            if float(score) > 0 and float(cores) > 0:
                try:
                    #bmresults[currentcpu][currentbm][cores].append(float(score) / float(cores))
                    bmresults[currentcpu][currentbm][cores].append(float(score))
                except KeyError:
                    bmresults[currentcpu][currentbm][cores] = []
                    #bmresults[currentcpu][currentbm][cores].append(float(score) / float(cores))
                    bmresults[currentcpu][currentbm][cores].append(float(score))

            elif float(cores) > 0:
                try:
                    bmresults[currentcpu][currentbm][cores].append(-1)
                except KeyError:
                    bmresults[currentcpu][currentbm][cores] = []
                    bmresults[currentcpu][currentbm][cores].append(-1)
                


limits = {}
limits["hepscore"] = [0, 5000]
limits["belle2_gen_sim_reco"] = [0, 500]
limits["lhcb_gen_sim"] = [0, 5000]
limits["atlas_gen"] = [0, 30000]
limits["cms_gen_sim"] = [0, 1000]
limits["cms_digi"] = [0, 500]
limits["cms_reco"] = [0, 2000]
limits["hs06"] = [0, 5000]

bins = {}
bins["hepscore"] = 5000
bins["belle2_gen_sim_reco"] = 500
bins["lhcb_gen_sim"] = 2000 
bins["atlas_gen"] = 3000
bins["cms_gen_sim"] = 1000
bins["cms_digi"] = 1000
bins["cms_reco"] = 400
bins["hs06"] = 5000

for cpu in cpus:
    for bm in bms:
        for cores in bmresults[cpu][bm]:
            hists[cpu][bm][cores] = TH1F(cpu + bm + str(cores), "", bins[bm], limits[bm][0], limits[bm][1])
            for item in bmresults[cpu][bm][cores]:

                # Fill histograms but remove a few bad data points
                if cpu == "AMD EPYC 7763 64-Core Processor":
                    if bm == "hepscore" and item < 3200:
                        hists[cpu][bm][cores].Fill(item)
                    elif bm == "hs06" and item < 3300:
                        hists[cpu][bm][cores].Fill(item)
                    elif bm != "hs06" and bm != "hepscore":
                        hists[cpu][bm][cores].Fill(item)
                elif cpu == "Intel(R) Xeon(R) Gold 6130 CPU @ 2.10GHz":
                    if bm == "hepscore" and item > 200:
                        hists[cpu][bm][cores].Fill(item)
                    elif bm != "hepscore":
                        hists[cpu][bm][cores].Fill(item)
                elif cpu == "Intel(R) Xeon(R) Platinum 8358 CPU @ 2.60GHz":
                    if bm == "hepscore" and item > 1200:
                        hists[cpu][bm][cores].Fill(item)
                    elif bm != "hepscore":
                        hists[cpu][bm][cores].Fill(item)
                else:
                    hists[cpu][bm][cores].Fill(item)


goodcpus = []

for cpu in cpus:
    for cores in bmresults[cpu]["hs06"]:
        if hists[cpu]["hs06"][cores].Integral() > 0 and cpu not in goodcpus:
            goodcpus.append(cpu)
            #print("Good!", cpu)

        print(cpu, cores, hists[cpu]["hepscore"][cores].Integral())



ht = {}
for cpu in cpus:
    ht[cpu] = {}
    
    for cores in bmresults[cpu]["hs06"]:
        if hists[cpu]["hs06"][cores].GetMean() / (float(cores) / 32) / 407.6 > 1.7:
            ht[cpu][cores] = 0
            print(cpu, cores, ht[cpu][cores])
        else:
            ht[cpu][cores] = 1
            print(cpu, cores, ht[cpu][cores])

pointcounter = 0
pointcounter_hton = 0
pointcounter_htoff = 0

for cpu in cpus:
    for cores in bmresults[cpu]["hs06"]:
        if cpu in goodcpus:
            finalhist.Fill(hists[cpu]["hs06"][cores].GetMean() / 407.6, hists[cpu]["hepscore"][cores].GetMean() / 355.7)
            finalgraph.SetPoint(pointcounter, hists[cpu]["hs06"][cores].GetMean() / 407.6, hists[cpu]["hepscore"][cores].GetMean() / 355.7)
            finalgraph.SetPointError(pointcounter, hists[cpu]["hs06"][cores].GetStdDev() / 407.6, hists[cpu]["hepscore"][cores].GetStdDev() / 355.7)
            pointcounter = pointcounter + 1
            print(cpu, hists[cpu]["hs06"][cores].GetMean() / 407.6, hists[cpu]["hepscore"][cores].GetMean() / 355.7, hists[cpu]["hs06"][cores].GetStdDev() / 407.6, hists[cpu]["hepscore"][cores].GetStdDev() / 355.7)

            if ht[cpu][cores]:
                finalgraph_hton.SetPoint(pointcounter_hton, hists[cpu]["hs06"][cores].GetMean() / 407.6, hists[cpu]["hepscore"][cores].GetMean() / 355.7)
                finalgraph_hton.SetPointError(pointcounter_hton, hists[cpu]["hs06"][cores].GetStdDev() / 407.6, hists[cpu]["hepscore"][cores].GetStdDev() / 355.7)
                pointcounter_hton = pointcounter_hton + 1
            else:
                finalgraph_htoff.SetPoint(pointcounter_htoff, hists[cpu]["hs06"][cores].GetMean() / 407.6, hists[cpu]["hepscore"][cores].GetMean() / 355.7)
                finalgraph_htoff.SetPointError(pointcounter_htoff, hists[cpu]["hs06"][cores].GetStdDev() / 407.6, hists[cpu]["hepscore"][cores].GetStdDev() / 355.7)
                pointcounter_htoff = pointcounter_htoff + 1
c1 = {}
for cpu in cpus:
    if cpu not in goodcpus:
        continue

    counter = 1
    c1[cpu] = TCanvas(cpu, cpu, 1200, 800)
    c1[cpu].Divide(2, 1)
    for bm in bms:
        lesserval = 1000000
        second = 0

        if (bm == "hepscore" or bm == "hs06"):
            c1[cpu].cd(counter)
            counter = counter + 1
            if len(hists[cpu][bm]) == 1:
                for cores in hists[cpu][bm]:
                    hists[cpu][bm][cores].Draw()
                    hists[cpu][bm][cores].GetXaxis().SetTitle(bm)
                    hists[cpu][bm][cores].SetTitle(cpu)
            else:
                for cores in hists[cpu][bm]:
                    if float(cores) < lesserval:
                        lesserval = float(cores)

                for cores in hists[cpu][bm]:
                    if float(cores) != lesserval:
                        hists[cpu][bm][cores].SetLineColor(2)

                for cores in hists[cpu][bm]:
                    if second == 0:
                        hists[cpu][bm][cores].Draw()
                        hists[cpu][bm][cores].GetXaxis().SetTitle(bm)
                        hists[cpu][bm][cores].SetTitle(cpu)
                        second = 1
                    else:
                        hists[cpu][bm][cores].Draw("same")

finalgraph_hton.SetMarkerColor(4)
#finalgraph_hton.SetMarkerStyle(20)
#finalgraph_htoff.SetMarkerStyle(20)
finalgraph_hton.SetMarkerStyle(22)
finalgraph_hton.SetMarkerSize(1.2)
finalgraph_htoff.SetMarkerStyle(20)
mg = TMultiGraph()
mg.Add(finalgraph_hton)
mg.Add(finalgraph_htoff)

fit = TF1("fit", "pol1", 0, 10)
fit.SetLineColor(1)
c2 = TCanvas("c2", "c2", 675, 900)
pad1 = TPad("pad1", "", 0, 0.33, 1.0, 1.0)
pad2 = TPad("pad2", "", 0, 0.0, 1.0, 0.33)
pad1.Draw()
pad2.Draw()
pad1.cd()
mg.GetXaxis().SetTitle("HS06_{64bits} Score")
mg.GetYaxis().SetTitle("HEPScore_{#beta} Score")
mg.GetXaxis().SetLimits(0, 10)
mg.GetYaxis().SetRangeUser(0, 10)
mg.Draw("AP")
print(finalgraph.GetCorrelationFactor())
#mg.Fit("fit", "R")

pad2.cd()
pad2.SetBottomMargin(0.15)

x = finalgraph_hton.GetX()
y = finalgraph_hton.GetY()
xerr = finalgraph_hton.GetEX()
yerr = finalgraph_hton.GetEY()
for i in range(0, finalgraph_hton.GetN()):
    res = y[i] - x[i]
    deltares = math.sqrt(xerr[i]**2 + yerr[i]**2)
    resnorm = res / x[i]
    delta = resnorm * math.sqrt((deltares / res)**2 + (xerr[i] / x[i])**2)
    residuals_hton.SetPoint(i, x[i], resnorm)
    residuals_hton.SetPointError(i, 0, delta)

x = finalgraph_htoff.GetX()
y = finalgraph_htoff.GetY()
xerr = finalgraph_htoff.GetEX()
yerr = finalgraph_htoff.GetEY()
for i in range(0, finalgraph_htoff.GetN()):
    res = y[i] - x[i]
    deltares = math.sqrt(xerr[i]**2 + yerr[i]**2)
    resnorm = res / x[i]
    delta = resnorm * math.sqrt((deltares / res)**2 + (xerr[i] / x[i])**2)
    residuals_htoff.SetPoint(i, x[i], res / x[i])
    residuals_htoff.SetPointError(i, 0, delta)

residuals_hton.SetMarkerColor(4)
#residuals_hton.SetMarkerStyle(20)
#residuals_htoff.SetMarkerStyle(20)
residuals_hton.SetMarkerStyle(22)
residuals_hton.SetMarkerSize(1.2)
residuals_htoff.SetMarkerStyle(20)
mg_res = TMultiGraph()
mg_res.Add(residuals_hton)
mg_res.Add(residuals_htoff)

mg_res.GetXaxis().SetLabelSize(0.05)
mg_res.GetYaxis().SetLabelSize(0.05)
mg_res.GetXaxis().SetTitleSize(0.06)
mg_res.GetYaxis().SetTitleSize(0.06)
mg_res.GetXaxis().SetTitleOffset(0.8)
mg_res.GetYaxis().SetTitleOffset(0.6)
mg_res.GetXaxis().SetLimits(0, 10)
mg_res.GetYaxis().SetRangeUser(-0.5, 0.5)
mg_res.GetXaxis().SetTitle("HS06_{64bits} Score")
mg_res.GetYaxis().SetTitle("HEPscore_{#beta} / HS06_{64bits} - 1")
mg_res.Draw("AP")

"""
finalgraph.SetMarkerStyle(20)
finalgraph.GetXaxis().SetTitle("HS06_{64bits} Score")
finalgraph.GetYaxis().SetTitle("HEPScore")
finalgraph.GetXaxis().SetLimits(0, 10)
finalgraph.GetYaxis().SetRangeUser(0, 10)
finalgraph.Draw("AP")
finalgraph.Fit("fit", "R")


for i in range(0, finalgraph.GetN()):
    x = finalgraph.GetX()
    y = finalgraph.GetY()
    res = fit.Eval(x[i]) - y[i]
    residuals.SetPoint(i, x[i], res / y[i])

c2.cd(2)
residuals.SetMarkerStyle(20)
residuals.GetXaxis().SetLimits(0, 10)
residuals.GetXaxis().SetTitle("HS06_{64bits} Score")
residuals.GetYaxis().SetTitle("(Fit - Data) / Data")
residuals.Draw("AP")
"""

gApplication.Run()
