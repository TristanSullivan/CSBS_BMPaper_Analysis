#!/usr/bin/python2

# Code to make Figure 10

from ROOT import TCanvas, TPad, TGraph, gApplication, TLegend, TF1, TH1F, TH2F, TGraphErrors, TLegend

import math

bmresults = {}
bms = ["hepscore", "hs06"]

hists = {}

bmresultsfile = open('./Threadscandata', 'r')
bmresultsstring = bmresultsfile.read()
bmresults_lines = bmresultsstring.split('\n')

cpus = ["Intel(R) Xeon(R) CPU E5-2630 v3 @ 2.40GHz"]

finalgraph_hs06 = TGraphErrors()
finalgraph_hepscore = TGraphErrors()

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

            if float(score) > 0 and float(cores) > 0:
                try:
                    bmresults[currentcpu][currentbm][cores].append(float(score) / float(cores))
                except KeyError:
                    bmresults[currentcpu][currentbm][cores] = []
                    bmresults[currentcpu][currentbm][cores].append(float(score) / float(cores))

            elif float(cores) > 0:
                try:
                    bmresults[currentcpu][currentbm][cores].append(-1)
                except KeyError:
                    bmresults[currentcpu][currentbm][cores] = []
                    bmresults[currentcpu][currentbm][cores].append(-1)
                


limits = {}
limits["hepscore"] = [-5, 95]
limits["hs06"] = [-5, 95]

bins = {}
bins["hepscore"] = 5000
bins["hs06"] = 5000

for cpu in cpus:
    for bm in bms:
        for cores in bmresults[cpu][bm]:
            hists[cpu][bm][cores] = TH1F(cpu + bm + str(cores), "", bins[bm], limits[bm][0], limits[bm][1])
            for item in bmresults[cpu][bm][cores]:
                hists[cpu][bm][cores].Fill(item)

pointcounter = 0

for cpu in cpus:
    for cores in bmresults[cpu]["hs06"]:
        finalgraph_hs06.SetPoint(pointcounter, float(cores), hists[cpu]["hs06"][cores].GetMean() * float(cores) / 16.0 / hists[cpu]["hs06"]["16.0"].GetMean())
        finalgraph_hepscore.SetPoint(pointcounter, float(cores), hists[cpu]["hepscore"][cores].GetMean() * float(cores) / 16.0 / hists[cpu]["hepscore"]["16.0"].GetMean())
        finalgraph_hs06.SetPointError(pointcounter, 0, math.sqrt((hists[cpu]["hs06"][cores].GetStdDev() / hists[cpu]["hs06"][cores].GetMean())**2 + (hists[cpu]["hs06"]["16.0"].GetStdDev() / hists[cpu]["hs06"]["16.0"].GetMean())**2) * hists[cpu]["hs06"][cores].GetMean() * float(cores) / 16.0 / hists[cpu]["hs06"]["16.0"].GetMean())
        finalgraph_hepscore.SetPointError(pointcounter, 0, math.sqrt((hists[cpu]["hepscore"][cores].GetStdDev() / hists[cpu]["hepscore"][cores].GetMean())**2 + (hists[cpu]["hepscore"]["16.0"].GetStdDev() / hists[cpu]["hepscore"]["16.0"].GetMean())**2) * hists[cpu]["hepscore"][cores].GetMean() * float(cores) / 16.0 / hists[cpu]["hepscore"]["16.0"].GetMean())
        pointcounter = pointcounter + 1
        #print(cpu, hists[cpu]["hs06"][cores].GetMean() / (407 / 32.0), hists[cpu]["hepscore"][cores].GetMean() / (355 / 32.0))
        #print(hists[cpu]["hs06"][cores].GetStdDev() / (407 / 32.0), hists[cpu]["hepscore"][cores].GetStdDev() / (355 / 32.0))

c1 = {}
for cpu in cpus:
    counter = 1
    c1[cpu] = TCanvas(cpu, cpu, 1200, 800)
    c1[cpu].Divide(2, 1)
    for bm in bms:
        lesserval = 1000000
        second = 0

        #if (bm == "hepscore" or bm == "hs06") and hists[cpu]["hs06"][cores].Integral(500, 5000) >= 10:
        if (bm == "hepscore" or bm == "hs06"):
            if len(hists[cpu][bm]) == 1:
                c1[cpu].cd(counter)
                counter = counter + 1
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
                    c1[cpu].cd(counter)
                    counter = counter + 1

                    if second == 0:
                        hists[cpu][bm][cores].Draw()
                        hists[cpu][bm][cores].GetXaxis().SetTitle(bm)
                        hists[cpu][bm][cores].SetTitle(cpu)
                        second = 1
                    else:
                        hists[cpu][bm][cores].Draw("same")

c2 = TCanvas("c2", "c2", 1200, 800)
finalgraph_hs06.SetMarkerStyle(20)
finalgraph_hs06.SetMarkerSize(1.5)
finalgraph_hs06.GetXaxis().SetLimits(0, 36)
finalgraph_hs06.GetXaxis().SetNdivisions(9, 0)
finalgraph_hs06.GetXaxis().SetTitle("Threads")
finalgraph_hs06.GetYaxis().SetTitle("Normalized Score")
finalgraph_hs06.Draw("AP")
finalgraph_hepscore.SetMarkerStyle(26)
finalgraph_hepscore.SetMarkerSize(3)
finalgraph_hepscore.SetMarkerColor(4)
finalgraph_hepscore.Draw("P same")

Legend = TLegend(0.15, 0.65, 0.35, 0.85)
Legend.AddEntry(finalgraph_hs06, "HS06_{64bits}", "p")
Legend.AddEntry(finalgraph_hepscore, "HEPscore_{#beta}", "p")
Legend.SetTextSize(0.04)
Legend.SetBorderSize(0)
Legend.Draw()

gApplication.Run()
