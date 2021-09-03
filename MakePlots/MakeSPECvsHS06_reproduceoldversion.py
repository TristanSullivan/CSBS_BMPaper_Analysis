#!/usr/bin/python2

# Code to make Figure 1. Data comes from GetSPECvsHS06data.py
# The plot needs to be edited manually (see bottom of file)

from ROOT import TCanvas, TPad, TGraph, gApplication, TLegend, TF1, TGraphErrors, TMultiGraph, gStyle

bmresults = {}
#bms = ["hepscore", "belle2_gen_sim_reco", "lhcb_gen_sim", "atlas_gen", "cms_gen_sim", "cms_digi", "cms_reco", "hs06", "DB12", "spec2017", "belle2_gen", "belle2_sim", "belle2_reco"]


# Data format:
# CPU
# Copies 
# HS06 32 bit mean
# HS06 32 bit std dev
# HS06 64 bit mean
# HS06 64 bit std dev
# Spec2017 mean
# Spec2017 std dev

schema = ["hs06_32", "hs06_32_error", "hs06_64", "hs06_64_error", "spec2017", "spec2017_error"]

bmresultsfile = open('./SPECvsHS06data_reproduceoldversion_sigma', 'r')
bmresultsstring = bmresultsfile.read()
bmresults_lines = bmresultsstring.split('\n')
counter = -2
currentcpu = "none"

# Read data file
for line in bmresults_lines:
    print(line)
    try: 
        if float(line) > 0:
            if currentcpu == "none" or counter < -1:
                print("This isn't supposed to happen!")

            elif counter > -1 and counter < 6:
                bmresults[currentcpu][currentcores][schema[counter]] = float(line)
                counter = counter + 1

            else:
                currentcores = int(line)
                bmresults[currentcpu][currentcores] = {}
                counter = 0
                
            
       
    except ValueError:
        currentcpu = line
        bmresults[currentcpu] = {}
        counter = -1


for key in bmresults:
    print(key)

    for key2 in bmresults[key]:
        print(key2)
            
        for key3 in bmresults[key][key2]:
            print(key3, bmresults[key][key2][key3])


graphs = {}
graphs["hs06_32"] = TGraphErrors()
graphs["hs06_64"] = TGraphErrors()

bmcount = 0

pointcounter = 0

# Put data into graphs
for key in bmresults:
    maxcores = 0

    for key2 in bmresults[key]:
        if key2 > maxcores:
            maxcores = key2
    
    for key2 in bmresults[key]:
        graphs["hs06_32"].SetPoint(pointcounter, bmresults[key][key2]["hs06_32"], bmresults[key][key2]["spec2017"])
        graphs["hs06_32"].SetPointError(pointcounter, bmresults[key][key2]["hs06_32_error"], bmresults[key][key2]["spec2017_error"])
        graphs["hs06_64"].SetPoint(pointcounter, bmresults[key][key2]["hs06_64"], bmresults[key][key2]["spec2017"])
        graphs["hs06_64"].SetPointError(pointcounter, bmresults[key][key2]["hs06_64_error"], bmresults[key][key2]["spec2017_error"])
        pointcounter = pointcounter + 1

graphs["hs06_64"].SetMarkerStyle(20)
graphs["hs06_64"].GetXaxis().SetTitle("HS06_{64bits} Score per Core")
graphs["hs06_64"].GetYaxis().SetTitle("SPEC CPU 2017 Score per Core")
graphs["hs06_64"].GetXaxis().SetLimits(8, 15.4)
#graphs["hs06_64"].GetYaxis().SetRangeUser(1, 1.8)

# Fix intercept to zero
fit = TF1("fit", "[0] * x", 8, 16)
fit.SetLineColor(1)
fit.SetLineStyle(2)
fit.SetParName(0, "Slope")

#gStyle.SetOptFit(0111)

c1 = TCanvas("c1", "c1", 1200, 800)
c1.Divide(1, 1)
c1.cd(1)
graphs["hs06_64"].Draw("AP")
graphs["hs06_64"].Fit("fit", "R")

# I added the correlation factor to the plot interactively with ROOT.
# View -> Toolbar, create a Pave Text
# Right click, InsertText "r = blah"
# View -> Editor, set font to 4 (Helvetica) and size to 32
# On the editor, set fill colour and line colour to white
# Right click on Pave Text, SetShadowColor 0
print(graphs["hs06_64"].GetCorrelationFactor())


gApplication.Run()
