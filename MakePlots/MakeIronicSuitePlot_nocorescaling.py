#!/usr/bin/python2

# Code to make Figure 9
# I couldn't figure out how to make the stat boxes pretty using Python
# I had to resort to C++ (see MakeIronicSuitePlot_nocorescaling_fromhists.C)
# In addition to making the plot badly, this script also writes out the histograms
# Output file is ProcurementHists.root

from ROOT import TCanvas, TPad, TGraph, gApplication, TLegend, TF1, TH1F, TH2F, TGraphErrors, TLegend, gStyle, TFile

import math

bmresults = {}
bms = ["hepscore", "hs06"]

hists = {}

bmresultsfile = open('./IronicSuitedata', 'r')
bmresultsstring = bmresultsfile.read()
bmresults_lines = bmresultsstring.split('\n')

cpus = ["Intel(R) Xeon(R) Platinum 8360Y CPU @ 2.40GHz", "AMD EPYC 7302 16-Core Processor"]

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
                    bmresults[currentcpu][currentbm][cores].append(float(score))
                except KeyError:
                    bmresults[currentcpu][currentbm][cores] = []
                    bmresults[currentcpu][currentbm][cores].append(float(score))

            elif float(cores) > 0:
                try:
                    bmresults[currentcpu][currentbm][cores].append(-1)
                except KeyError:
                    bmresults[currentcpu][currentbm][cores] = []
                    bmresults[currentcpu][currentbm][cores].append(-1)

limits = {}
limits["hepscore"] = [3.0575, 3.2075]
limits["hs06"] = [2.98, 3.13]

bins = {}
bins["hepscore"] = 64
bins["hs06"] = 20

ref = {}
ref["hs06"] = 407.6
ref["hepscore"] = 355.7

for cpu in cpus:
    for bm in bms:
        for cores in bmresults[cpu][bm]:
            hists[cpu][bm][cores] = TH1F(cpu + bm + str(cores), "", bins[bm], limits[bm][0], limits[bm][1])
            for item in bmresults[cpu][bm][cores]:
                hists[cpu][bm][cores].Fill(item / ref[bm])

c1 = {}
for cpu in cpus:
    counter = 1
    c1[cpu] = TCanvas(cpu, cpu, 800, 800)
    c1[cpu].Divide(1, 2)
    for bm in bms:
        lesserval = 1000000
        second = 0

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
                    c1[cpu].cd(counter)
                    counter = counter + 1

                    if second == 0:
                        hists[cpu][bm][cores].Draw()
                        hists[cpu][bm][cores].GetXaxis().SetTitle(bm)
                        hists[cpu][bm][cores].SetTitle(cpu)
                        second = 1
                    else:
                        hists[cpu][bm][cores].Draw("same")


            
            for cores in hists[cpu][bm]:
                c1[cpu].cd(counter)
                counter = counter + 1
                if second == 0:
                    hists[cpu][bm][cores].Draw()
                    hists[cpu][bm][cores].GetXaxis().SetTitle(bm)
                    hists[cpu][bm][cores].SetTitle(cpu)
                    second = 1
                else:
                    hists[cpu][bm][cores].SetLineColor(2)
                    hists[cpu][bm][cores].Draw("same")

gStyle.SetFitFormat(".5g")
gStyle.SetOptStat(0)
gStyle.SetStatX(0.89)
gStyle.SetStatY(0.89)
gStyle.SetStatW(0.2)
gStyle.SetStatBorderSize(0)
gStyle.SetOptTitle(0)
gStyle.SetOptFit(111)

# Necessary because of fixing fit paramater (see below)
fit_hepscore = TF1("fit_hepscore", "gaus", 3.06, 3.21)
fit_hepscore.SetLineColor(4)
fit_hepscore.SetNpx(1000)
fit_hepscore.SetParName(1, "\mu")
fit_hepscore.SetParName(2, "\sigma")
fit_hepscore.SetParameter(0, hists["AMD EPYC 7302 16-Core Processor"]["hepscore"]["64.0"].GetBinContent(hists["AMD EPYC 7302 16-Core Processor"]["hepscore"]["64.0"].GetMaximumBin()))
fit_hepscore.SetParameter(1, hists["AMD EPYC 7302 16-Core Processor"]["hepscore"]["64.0"].GetMean())
fit_hepscore.SetParameter(2, hists["AMD EPYC 7302 16-Core Processor"]["hepscore"]["64.0"].GetStdDev())

fit_hs06 = TF1("fit_hs06", "gaus", 2.95, 3.15)
fit_hs06.SetLineColor(4)
fit_hs06.SetNpx(1000)
fit_hs06.SetParName(1, "\mu")
fit_hs06.SetParName(2, "\sigma")
fit_hs06.SetParameter(0, hists["AMD EPYC 7302 16-Core Processor"]["hs06"]["64.0"].GetBinContent(hists["AMD EPYC 7302 16-Core Processor"]["hs06"]["64.0"].GetMaximumBin()))
fit_hs06.SetParameter(1, hists["AMD EPYC 7302 16-Core Processor"]["hs06"]["64.0"].GetMean())
fit_hs06.SetParameter(2, hists["AMD EPYC 7302 16-Core Processor"]["hs06"]["64.0"].GetStdDev())

c1["AMD EPYC 7302 16-Core Processor"].cd(1)
hists["AMD EPYC 7302 16-Core Processor"]["hs06"]["64.0"].SetLineColor(1)
hists["AMD EPYC 7302 16-Core Processor"]["hs06"]["64.0"].SetFillColor(18)
hists["AMD EPYC 7302 16-Core Processor"]["hs06"]["64.0"].GetXaxis().SetTitleSize(0.05)
hists["AMD EPYC 7302 16-Core Processor"]["hs06"]["64.0"].GetYaxis().SetTitleSize(0.05)
hists["AMD EPYC 7302 16-Core Processor"]["hs06"]["64.0"].GetXaxis().SetTitleOffset(0.9)
hists["AMD EPYC 7302 16-Core Processor"]["hs06"]["64.0"].GetXaxis().SetLabelOffset(0.01)
hists["AMD EPYC 7302 16-Core Processor"]["hs06"]["64.0"].GetXaxis().SetTitle("HS06_{64bits}")
hists["AMD EPYC 7302 16-Core Processor"]["hs06"]["64.0"].GetYaxis().SetTitle("Entries")
#hists["AMD EPYC 7302 16-Core Processor"]["hs06"]["64.0"].SetStats(0)
hists["AMD EPYC 7302 16-Core Processor"]["hs06"]["64.0"].SetTitle("")
hists["AMD EPYC 7302 16-Core Processor"]["hs06"]["64.0"].Fit("fit_hs06", "RB")

# Fix amplitude parameter to keep it out of the stat box
fit_hs06.FixParameter(0, fit_hs06.GetParameter(0))
hists["AMD EPYC 7302 16-Core Processor"]["hs06"]["64.0"].Fit("fit_hs06", "RB")
hists["AMD EPYC 7302 16-Core Processor"]["hs06"]["64.0"].Draw("E")

c1["AMD EPYC 7302 16-Core Processor"].cd(2)
hists["AMD EPYC 7302 16-Core Processor"]["hepscore"]["64.0"].SetLineColor(1)
hists["AMD EPYC 7302 16-Core Processor"]["hepscore"]["64.0"].SetFillColor(18)
hists["AMD EPYC 7302 16-Core Processor"]["hepscore"]["64.0"].GetXaxis().SetTitleSize(0.05)
hists["AMD EPYC 7302 16-Core Processor"]["hepscore"]["64.0"].GetYaxis().SetTitleSize(0.05)
hists["AMD EPYC 7302 16-Core Processor"]["hepscore"]["64.0"].GetXaxis().SetLabelOffset(0.01)
hists["AMD EPYC 7302 16-Core Processor"]["hepscore"]["64.0"].GetXaxis().SetTitle("HEPscore_{#beta}")
hists["AMD EPYC 7302 16-Core Processor"]["hepscore"]["64.0"].GetXaxis().SetTitleOffset(0.9)
hists["AMD EPYC 7302 16-Core Processor"]["hepscore"]["64.0"].GetYaxis().SetTitle("Entries")
hists["AMD EPYC 7302 16-Core Processor"]["hepscore"]["64.0"].SetTitle("")
#hists["AMD EPYC 7302 16-Core Processor"]["hepscore"]["64.0"].SetStats(0)
hists["AMD EPYC 7302 16-Core Processor"]["hepscore"]["64.0"].Fit("fit_hepscore", "RB")

fit_hepscore.FixParameter(0, fit_hepscore.GetParameter(0))
fit_hepscore.SetParLimits(2, 0, 0.01)
hists["AMD EPYC 7302 16-Core Processor"]["hepscore"]["64.0"].Fit("fit_hepscore", "RB")
hists["AMD EPYC 7302 16-Core Processor"]["hepscore"]["64.0"].Draw("E")

outfile = TFile("ProcurementHists.root", "RECREATE")
hists["AMD EPYC 7302 16-Core Processor"]["hepscore"]["64.0"].SetName("HEPscore")
hists["AMD EPYC 7302 16-Core Processor"]["hepscore"]["64.0"].Write()
hists["AMD EPYC 7302 16-Core Processor"]["hs06"]["64.0"].SetName("HS06")
hists["AMD EPYC 7302 16-Core Processor"]["hs06"]["64.0"].Write()
outfile.Close()


gApplication.Run()
