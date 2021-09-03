#!/usr/bin/python2

# Make Figure 7
# Data comes from Riccardo Maganza as csv files
# This plot needs to be edited manually to add lines and text labels
# I used OpenOffice

from ROOT import TCanvas, TPad, TGraph, gApplication, TLegend, TF1, TH1F, gStyle

time = []
cpu_util = []
rss = []

graph_cpu = TGraph()
graph_rss = TGraph()

rssfile = open('./rss_plot.csv', 'r')
resultsstring = rssfile.read()
results_lines = resultsstring.split('\n')

for line in results_lines:
    if len(line.split(",")) > 1:
        time.append(float(line.split(",")[0]))
        rss.append(float(line.split(",")[1]))

cpufile = open('./cpu_util_plot.csv', 'r')
resultsstring = cpufile.read()
results_lines = resultsstring.split('\n')

for line in results_lines:
    if len(line.split(",")) > 1:
        cpu_util.append(float(line.split(",")[1]) * 100)

for i in range(0, len(cpu_util)):
    graph_cpu.SetPoint(i, time[i], cpu_util[i])
    graph_rss.SetPoint(i, time[i], rss[i])

c1 = TCanvas("c1", "c1", 1200, 800)
c1.Divide(1, 2)
c1.cd(1)
graph_cpu.GetXaxis().SetLimits(0, 18000)
graph_cpu.GetXaxis().SetTitleSize(0.05)
graph_cpu.GetYaxis().SetTitleSize(0.05)
graph_cpu.GetYaxis().SetTitleOffset(0.5)
graph_cpu.GetXaxis().SetTitle("Wall Time (s)")
graph_cpu.GetYaxis().SetTitle("CPU Utilization (%)")
graph_cpu.Draw("ALP")
c1.cd(2)
graph_rss.GetXaxis().SetLimits(0, 18000)
graph_rss.GetXaxis().SetTitleSize(0.05)
graph_rss.GetYaxis().SetTitleSize(0.05)
graph_rss.GetYaxis().SetTitleOffset(0.5)
graph_rss.GetXaxis().SetTitle("Wall Time (s)")
graph_rss.GetYaxis().SetTitle("Resident Set Size (GB)")
graph_rss.Draw("ALP")

gApplication.Run()
