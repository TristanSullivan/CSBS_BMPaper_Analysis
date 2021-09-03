#!/usr/bin/python2

# Code to make Figure 3
# I couldn't figure out how to make the stat boxes pretty using Python
# I had to resort to C++ (see MakeRefMachinePlot_fromhists.C)
# In addition to making the plot badly, this script also writes out the histograms
# Output file is RefMachineHists.root

from ROOT import TCanvas, TPad, TGraph, gApplication, TLegend, TF1, TH1F, gStyle, TStyle, gPad, TFile

bmresults = {}
bms = ["atlas_gen", "atlas_sim", "belle2_gen_sim_reco", "cms_gen_sim", "cms_digi", "cms_reco", "lhcb_gen_sim"]

refs = {}
hists = {}
hists_coarse = {}

bmresultsfile = open('./RealReferenceMachineData_withatlassim', 'r')
bmresultsstring = bmresultsfile.read()
bmresults_lines = bmresultsstring.split('\n')

cpus = ["Intel(R) Xeon(R) CPU E5-2630 v3 @ 2.40GHz"]

for cpu in cpus:
    bmresults[cpu] = {}
    hists[cpu] = {}
    hists_coarse[cpu] = {}

    for bm in bms:
        hists[cpu][bm] = {}
        hists_coarse[cpu][bm] = {}
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
limits["belle2_gen_sim_reco"] = [5.4, 5.5]
limits["lhcb_gen_sim"] = [89.4, 91.4]
limits["atlas_gen"] = [370, 420]
limits["atlas_sim"] = [0.0635, 0.0651]
limits["cms_gen_sim"] = [0.71, 0.75]
limits["cms_digi"] = [3.5, 3.7]
limits["cms_reco"] = [2.16, 2.25]

bins = {}
bins["belle2_gen_sim_reco"] = 100
bins["lhcb_gen_sim"] = 150
bins["atlas_gen"] = 100
bins["atlas_sim"] = 75
bins["cms_gen_sim"] = 150
bins["cms_digi"] = 125
bins["cms_reco"] = 200

for cpu in cpus:
    for bm in bms:
        for cores in bmresults[cpu][bm]:
            hists[cpu][bm][cores] = TH1F(cpu + bm + str(cores), "", bins[bm], limits[bm][0], limits[bm][1])
            hists_coarse[cpu][bm][cores] = TH1F(cpu + bm + str(cores) + "_coarse", "", bins[bm] / 5, limits[bm][0], limits[bm][1])
            for item in bmresults[cpu][bm][cores]:
                hists[cpu][bm][cores].Fill(item)
                hists_coarse[cpu][bm][cores].Fill(item)
                if (bm == "atlas_sim"):
                    print(item)

bmtitles = {"lhcb_gen_sim": "LHCb GEN-SIM", "atlas_gen": "ATLAS GEN", "atlas_sim": "ATLAS SIM", "cms_gen_sim": "CMS GEN-SIM", "cms_digi": "CMS DIGI", "cms_reco": "CMS RECO", "belle2_gen_sim_reco": "Belle II GEN-SIM-RECO"}

gStyle.SetOptFit(111)
gStyle.SetStatX(0.89)
gStyle.SetStatY(0.89)
gStyle.SetStatW(0.22)
gStyle.SetFitFormat(".5g")
gStyle.SetStatBorderSize(0)
gStyle.SetOptStat(0)
gStyle.SetStatFontSize(0.06)

fits = []
fits_coarse = []
fits_coarse_draw = []
c1 = {}
c2 = {}

for cpu in cpus:
    counter = 0
    c1[cpu] = TCanvas("c1", "c1", 800, 1200)
    c1[cpu].Divide(2, 4)
    for bm in bms:
        c1[cpu].cd(counter + 1)

        hists[cpu][bm]["32.0"].GetXaxis().SetTitle(bm)
        hists[cpu][bm]["32.0"].GetYaxis().SetTitle("Counts")
        hists[cpu][bm]["32.0"].SetTitle("")
        hists[cpu][bm]["32.0"].Draw("E")

        fitname = bm
        low = hists[cpu][bm]["32.0"].GetMean() - 2 * hists[cpu][bm]["32.0"].GetStdDev()
        high = hists[cpu][bm]["32.0"].GetMean() + 2 * hists[cpu][bm]["32.0"].GetStdDev()
        fits.append(TF1(bm, "gaus", low, high))
        fits[counter].SetLineColor(1)
        hists[cpu][bm]["32.0"].Fit(fits[counter], "R")

        counter = counter + 1

    counter = 0
    c2[cpu] = TCanvas("c2", "c2", 800, 1200)
    c2[cpu].Divide(2, 4)
    for bm in bms:
        c2[cpu].cd(counter + 1)
        
        # Strange magic
        if bm == "atlas_sim":
            hists_coarse[cpu][bm]["32.0"].GetXaxis().SetMaxDigits()

        hists_coarse[cpu][bm]["32.0"].GetXaxis().SetTitle(bmtitles[bm] + " Score (Events / s)")
        hists_coarse[cpu][bm]["32.0"].GetXaxis().SetLabelOffset(0.01)
        hists_coarse[cpu][bm]["32.0"].GetXaxis().SetTitleSize(0.05)
        hists_coarse[cpu][bm]["32.0"].GetYaxis().SetTitleSize(0.05)
        hists_coarse[cpu][bm]["32.0"].GetXaxis().SetLabelSize(0.05)
        hists_coarse[cpu][bm]["32.0"].GetYaxis().SetLabelSize(0.05)
        hists_coarse[cpu][bm]["32.0"].GetYaxis().SetTitle("Entries")
        #hists_coarse[cpu][bm]["32.0"].SetTitle(bmtitles[bm])
        hists_coarse[cpu][bm]["32.0"].Draw("E")

        fitname = bm + "_coarse"
        if bm == "atlas_gen":
            low = hists_coarse[cpu][bm]["32.0"].GetMean() - 1.5 * hists_coarse[cpu][bm]["32.0"].GetStdDev()
            high = hists_coarse[cpu][bm]["32.0"].GetMean() + 0.8 * hists_coarse[cpu][bm]["32.0"].GetStdDev()
        else:
            low = hists_coarse[cpu][bm]["32.0"].GetMean() - 2 * hists_coarse[cpu][bm]["32.0"].GetStdDev()
            high = hists_coarse[cpu][bm]["32.0"].GetMean() + 2 * hists_coarse[cpu][bm]["32.0"].GetStdDev()

        fits_coarse.append(TF1(fitname, "gaus", low, high))
        fits_coarse[counter].SetLineColor(4)
        fits_coarse[counter].SetNpx(500)
        fits_coarse[counter].SetParName(1, "\mu")
        fits_coarse[counter].SetParName(2, "\sigma")
        hists_coarse[cpu][bm]["32.0"].Fit(fits_coarse[counter], "R")

        fits_coarse_draw.append(TF1(fitname + "_draw", "gaus", limits[bm][0], limits[bm][1]))
        fits_coarse_draw[counter].SetLineColor(4)
        fits_coarse_draw[counter].SetNpx(500)
        fits_coarse_draw[counter].SetLineStyle(2)

        fits_coarse[counter].FixParameter(0, fits_coarse[counter].GetParameter(0))
        hists_coarse[cpu][bm]["32.0"].Fit(fits_coarse[counter], "R")
        fits_coarse_draw[counter].SetParameters(fits_coarse[counter].GetParameters())
        fits_coarse_draw[counter].Draw("same")

        counter = counter + 1


outfile = TFile("RefMachineHists.root", "RECREATE")
cpu = "Intel(R) Xeon(R) CPU E5-2630 v3 @ 2.40GHz"

for bm in bms:
    hists_coarse[cpu][bm]["32.0"].SetName(bm)
    hists_coarse[cpu][bm]["32.0"].Write()

outfile.Close()

               
gApplication.Run()
