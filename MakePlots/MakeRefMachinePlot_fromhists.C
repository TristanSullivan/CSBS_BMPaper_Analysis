// Code to make Figure 3
// I had to resort to hard-coding the formatting for each stat box

{
    gStyle->SetOptStat(0);
    gStyle->SetOptFit(101);
    gStyle->SetStatX(0.89);
    gStyle->SetStatY(0.89);
    gStyle->SetStatW(0.18);
    gStyle->SetStatH(0.25);
    gStyle->SetStatFont(43);
    gStyle->SetStatFontSize(12);
    gStyle->SetStatBorderSize(0);
    gStyle->SetFitFormat("5.2e");

    gStyle->SetPadBottomMargin(0.15);
    char histnames[7][50] = {"atlas_gen", "atlas_sim", "belle2_gen_sim_reco", "cms_gen_sim", "cms_digi", "cms_reco", "lhcb_gen_sim"};

    // Full fitting range
    char means[7][10];
    char sigmas[7][10];

    char fitname[10];
    char statname[10];
    TH1F *hists[7];
    TF1 *fits[7];

    TFile *histfile = new TFile("./RefMachineHists.root");

    TPaveStats *statboxes[7];

    for (int i = 0; i < 7; i++)
    {
        hists[i] = (TH1F*)histfile->Get(histnames[i]);
    }

    TCanvas *c1 = new TCanvas("c1", "c1", 1200, 800);
    c1->Divide(2, 4);

    for (int i = 0; i < 7; i++)
    {
        c1->cd(i + 1);
        sprintf(fitname, "fit%d", i);
        sprintf(statname, "stat%d", i);

        // Do it like this so initial conditions aren't automatically calculated each time
        fits[i] = new TF1(fitname, "[0] * exp(-1 * pow(x - [1], 2) / (2 * pow([2], 2)))", 0, 10);
        fits[i]->SetParName(0, "Amplitude");
        fits[i]->SetParName(1, "#mu");
        fits[i]->SetParName(2, "#sigma");

        fits[i]->SetParameter(0, hists[i]->GetBinContent(hists[i]->GetMaximumBin()));
        fits[i]->SetParameter(1, hists[i]->GetMean());
        fits[i]->SetParameter(2, hists[i]->GetStdDev());
        fits[i]->SetRange(hists[i]->GetXaxis()->GetXmin(), hists[i]->GetXaxis()->GetXmax());
        fits[i]->SetLineColor(kBlue);

        hists[i]->GetXaxis()->SetTitleOffset(1.1);
        hists[i]->GetYaxis()->SetTitleOffset(0.5);
        hists[i]->GetXaxis()->SetLabelOffset(0.02);
        hists[i]->GetXaxis()->SetTitleSize(0.07);
        hists[i]->GetYaxis()->SetTitleSize(0.07);
        hists[i]->GetXaxis()->SetLabelSize(0.06);
        hists[i]->GetYaxis()->SetLabelSize(0.06);
        hists[i]->Fit(fitname, "R");
        hists[i]->Draw("E");
        c1->Update();

        // Get the stat box
        statboxes[i] = (TPaveStats*)gPad->GetPrimitive("stats");
        statboxes[i]->SetName(statname);

        // Take out current contents
        TList *listOfLines = statboxes[i]->GetListOfLines();
        TText *Chisquaretext = statboxes[i]->GetLineWith("#chi");
        TText *Amptext = statboxes[i]->GetLineWith("Amplitude");
        TText *Meantext = statboxes[i]->GetLineWith("#mu");
        TText *Sigmatext = statboxes[i]->GetLineWith("#sigma");
        listOfLines->Remove(Chisquaretext);
        listOfLines->Remove(Amptext);
        listOfLines->Remove(Meantext);
        listOfLines->Remove(Sigmatext);

        char textstring[20];
        sprintf(textstring, "#chi^{2} / ndf = %.1f / %d", fits[i]->GetChisquare(), fits[i]->GetNDF());
        TLatex *chisquaretext = new TLatex(0,0, textstring);
        chisquaretext->SetTextFont(43);
        chisquaretext->SetTextSize(13);
        listOfLines->Add(chisquaretext);

        //sprintf(textstring, "#mu = %.3f", fits[i]->GetParameter(1));
        //TLatex *meantext = new TLatex(0,0, textstring);

        // Format means
        switch (i)
        {
            case 0:
                sprintf(textstring, "#mu = %.0f", fits[i]->GetParameter(1));
                break;
            case 1:
                sprintf(textstring, "#mu = %.1e", fits[i]->GetParameter(1));
                break;
            case 2:
                sprintf(textstring, "#mu = %.1f", fits[i]->GetParameter(1));
                break;
            case 3:
                sprintf(textstring, "#mu = %.2f", fits[i]->GetParameter(1));
                break;
            case 4:
                sprintf(textstring, "#mu = %.1f", fits[i]->GetParameter(1));
                break;
            case 5:
                sprintf(textstring, "#mu = %.1f", fits[i]->GetParameter(1));
                break;
            case 6:
                sprintf(textstring, "#mu = %.1f", fits[i]->GetParameter(1));
                break;
        }

        //sprintf(textstring, "#mu = %s", means[i]);
        TLatex *meantext = new TLatex(0,0, textstring);
        meantext->SetTextFont(43);
        meantext->SetTextSize(13);
        listOfLines->Add(meantext);

        //sprintf(textstring, "#sigma = %.2e", fits[i]->GetParameter(2));
        //TLatex *sigmatext = new TLatex(0,0, textstring);
        //sprintf(textstring, "#sigma = %s", sigmas[i]);

        // Format standard deviations
        switch (i)
        {
            case 0:
                sprintf(textstring, "#sigma = %.0f", fits[i]->GetParameter(2));
                break;
            case 1:
                sprintf(textstring, "#sigma = %.0e", fits[i]->GetParameter(2));
                break;
            case 2:
                sprintf(textstring, "#sigma = %.0e", fits[i]->GetParameter(2));
                break;
            case 3:
                sprintf(textstring, "#sigma = %.0e", fits[i]->GetParameter(2));
                break;
            case 4:
                sprintf(textstring, "#sigma = %.0e", fits[i]->GetParameter(2));
                break;
            case 5:
                sprintf(textstring, "#sigma = %.0e", fits[i]->GetParameter(2));
                break;
            case 6:
                sprintf(textstring, "#sigma = %.1f", fits[i]->GetParameter(2));
                break;
        }

        TLatex *sigmatext = new TLatex(0,0, textstring);
        sigmatext->SetTextFont(43);
        sigmatext->SetTextSize(13);
        listOfLines->Add(sigmatext);

        //statboxes[i]->SetTextFont(4);
        //statboxes[i]->SetTextSize(12);

        hists[i]->SetStats(0);

        gPad->Modified();
        gPad->Update();
    }
}
