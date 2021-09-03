// Code to make Figure 9 with nice stat boxes

{
    gStyle->SetOptStat(0);
    gStyle->SetOptFit(101);
    gStyle->SetStatX(0.89);
    gStyle->SetStatY(0.89);
    gStyle->SetStatW(0.15);
    gStyle->SetStatH(0.15);
    gStyle->SetStatFont(43);
    gStyle->SetStatFontSize(12);
    gStyle->SetStatBorderSize(0);
    gStyle->SetFitFormat("5.3f");

    gStyle->SetPadBottomMargin(0.18);

    TF1 *fit_hepscore = new TF1("fit_hepscore", "[0] * exp(-1 * pow(x - [1], 2) / (2 * pow([2], 2)))", 0, 10);
    TF1 *fit_hs06 = new TF1("fit_hs06", "[0] * exp(-1 * pow(x - [1], 2) / (2 * pow([2], 2)))", 0, 10);

    TH1F *HEPscore;
    TH1F *HS06;

    TFile *histfile = new TFile("./ProcurementHists.root");
    HEPscore = (TH1F*)histfile->Get("HEPscore");
    HS06 = (TH1F*)histfile->Get("HS06");

    fit_hepscore->SetParName(0, "Amplitude");
    fit_hepscore->SetParName(1, "#mu");
    fit_hepscore->SetParName(2, "#sigma");

    fit_hepscore->SetParameter(0, HEPscore->GetBinContent(HEPscore->GetMaximumBin()));
    fit_hepscore->SetParameter(1, HEPscore->GetMean());
    fit_hepscore->SetParameter(2, HEPscore->GetStdDev());

    fit_hepscore->SetParLimits(2, 0, 0.02);

    fit_hepscore->SetRange(HEPscore->GetXaxis()->GetXmin(), HEPscore->GetXaxis()->GetXmax());
    fit_hepscore->SetLineColor(kBlue);
    fit_hepscore->SetNpx(500);

    fit_hs06->SetParName(0, "Amplitude");
    fit_hs06->SetParName(1, "#mu");
    fit_hs06->SetParName(2, "#sigma");

    fit_hs06->SetParLimits(2, 0, 0.02);

    fit_hs06->SetParameter(0, HS06->GetBinContent(HS06->GetMaximumBin()));
    fit_hs06->SetParameter(1, HS06->GetMean());
    fit_hs06->SetParameter(2, HS06->GetStdDev());
    fit_hs06->SetRange(HS06->GetXaxis()->GetXmin(), HS06->GetXaxis()->GetXmax());
    fit_hs06->SetLineColor(kBlue);
    fit_hs06->SetNpx(500);

    TPaveStats *statbox_hs06;
    TPaveStats *statbox_hepscore;

    TCanvas *c1 = new TCanvas("c1", "c1", 800, 800);
    c1->Divide(1, 2);

    c1->cd(1);
    HS06->GetXaxis()->SetTitleOffset(1.1);
    HS06->GetYaxis()->SetTitleOffset(0.5);
    HS06->GetXaxis()->SetLabelOffset(0.02);
    HS06->GetXaxis()->SetTitleSize(0.06);
    HS06->GetYaxis()->SetTitleSize(0.06);
    HS06->GetXaxis()->SetLabelSize(0.05);
    HS06->GetYaxis()->SetLabelSize(0.05);
    HS06->Fit(fit_hs06, "R");
    HS06->Draw("E");
    c1->Update();

    // Get the stat box
    statboxes_hs06 = (TPaveStats*)gPad->GetPrimitive("stats");
    statboxes_hs06->SetName("statbox_hs06");

    // Take out current contents
    TList *listOfLines_hs06 = statboxes_hs06->GetListOfLines();
    TText *Chisquaretext_hs06 = statboxes_hs06->GetLineWith("#chi");
    TText *Amptext_hs06 = statboxes_hs06->GetLineWith("Amplitude");
    TText *Meantext_hs06 = statboxes_hs06->GetLineWith("#mu");
    TText *Sigmatext_hs06 = statboxes_hs06->GetLineWith("#sigma");
    listOfLines_hs06->Remove(Chisquaretext_hs06);
    listOfLines_hs06->Remove(Amptext_hs06);
    listOfLines_hs06->Remove(Meantext_hs06);
    listOfLines_hs06->Remove(Sigmatext_hs06);

    char textstring[50];
    sprintf(textstring, "#chi^{2} / ndf = %.1f / %d", fit_hs06->GetChisquare(), fit_hs06->GetNDF());
    TLatex *chisquaretext_hs06 = new TLatex(0,0, textstring);
    chisquaretext_hs06->SetTextFont(43);
    chisquaretext_hs06->SetTextSize(16);
    listOfLines_hs06->Add(chisquaretext_hs06);

    sprintf(textstring, "#mu = %.2f", fit_hs06->GetParameter(1));
    TLatex *meantext_hs06 = new TLatex(0,0, textstring);
    meantext_hs06->SetTextFont(43);
    meantext_hs06->SetTextSize(16);
    listOfLines_hs06->Add(meantext_hs06);

    sprintf(textstring, "#sigma = %.0e", fit_hs06->GetParameter(2));
    TLatex *sigmatext_hs06 = new TLatex(0,0, textstring);
    sigmatext_hs06->SetTextFont(43);
    sigmatext_hs06->SetTextSize(16);
    listOfLines_hs06->Add(sigmatext_hs06);

    //statboxes[i]->SetTextFont(4);
    //statboxes[i]->SetTextSize(12);

    HS06->SetStats(0);

    gPad->Modified();
    gPad->Update();

    c1->cd(2);
    HEPscore->GetXaxis()->SetTitleOffset(1.1);
    HEPscore->GetYaxis()->SetTitleOffset(0.5);
    HEPscore->GetXaxis()->SetLabelOffset(0.02);
    HEPscore->GetXaxis()->SetTitleSize(0.07);
    HEPscore->GetYaxis()->SetTitleSize(0.07);
    HEPscore->GetXaxis()->SetLabelSize(0.06);
    HEPscore->GetYaxis()->SetLabelSize(0.06);
    HEPscore->Fit(fit_hepscore, "R");
    HEPscore->Draw("E");
    c1->Update();

    // Get the stat box
    statboxes_hepscore = (TPaveStats*)gPad->GetPrimitive("stats");
    statboxes_hepscore->SetName("statbox_hepscore");

    TList *listOfLines_hepscore = statboxes_hepscore->GetListOfLines();
    TText *Chisquaretext_hepscore = statboxes_hepscore->GetLineWith("#chi");
    TText *Amptext_hepscore = statboxes_hepscore->GetLineWith("Amplitude");
    TText *Meantext_hepscore = statboxes_hepscore->GetLineWith("#mu");
    TText *Sigmatext_hepscore = statboxes_hepscore->GetLineWith("#sigma");
    listOfLines_hepscore->Remove(Chisquaretext_hepscore);
    listOfLines_hepscore->Remove(Amptext_hepscore);
    listOfLines_hepscore->Remove(Meantext_hepscore);
    listOfLines_hepscore->Remove(Sigmatext_hepscore);

    sprintf(textstring, "#chi^{2} / ndf = %.1f / %d", fit_hepscore->GetChisquare(), fit_hepscore->GetNDF());
    TLatex *chisquaretext_hepscore = new TLatex(0,0, textstring);
    chisquaretext_hepscore->SetTextFont(43);
    chisquaretext_hepscore->SetTextSize(16);
    listOfLines_hepscore->Add(chisquaretext_hepscore);

    sprintf(textstring, "#mu = %.2f", fit_hepscore->GetParameter(1));
    TLatex *meantext_hepscore = new TLatex(0,0, textstring);
    meantext_hepscore->SetTextFont(43);
    meantext_hepscore->SetTextSize(16);
    listOfLines_hepscore->Add(meantext_hepscore);

    sprintf(textstring, "#sigma = %.0e", fit_hepscore->GetParameter(2));
    TLatex *sigmatext_hepscore = new TLatex(0,0, textstring);
    sigmatext_hepscore->SetTextFont(43);
    sigmatext_hepscore->SetTextSize(16);
    listOfLines_hepscore->Add(sigmatext_hepscore);

    //statboxes[i]->SetTextFont(4);
    //statboxes[i]->SetTextSize(12);

    HEPscore->SetStats(0);

    gPad->Modified();
    gPad->Update();
}
