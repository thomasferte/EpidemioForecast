# Experience 1 - reporting


- [<span class="toc-section-number">1</span>
  Introduction](#introduction)
- [<span class="toc-section-number">2</span> Methods](#methods)
- [<span class="toc-section-number">3</span> Prediction](#prediction)
  - [<span class="toc-section-number">3.0.1</span> Uncertainty
    quantification](#uncertainty-quantification)
  - [<span class="toc-section-number">3.0.2</span> Sanity
    check](#sanity-check)
  - [<span class="toc-section-number">3.0.3</span>
    Prediction](#prediction-1)
  - [<span class="toc-section-number">3.0.4</span>
    Performance](#performance)
- [<span class="toc-section-number">4</span>
  Hyperparameters](#hyperparameters)
  - [<span class="toc-section-number">4.1</span> Sanity
    check](#sanity-check-1)
  - [<span class="toc-section-number">4.2</span> Numeric
    hyperparameters](#numeric-hyperparameters)
    - [<span class="toc-section-number">4.2.1</span> Hyperparameter
      evolution](#hyperparameter-evolution)
- [<span class="toc-section-number">5</span> Time and carbon
  footprint](#time-and-carbon-footprint)

# Introduction

Goal = provide some results to write the article of the SARS-CoV-2
forecast from an implementation science perspective.

Hypothesis to test :

- Simple models like elastic-net perform better when little information
  is available
- Feature selection based on epidemic knowledge performs better when
  little information is available
- More complex models like xgboost or reservoir computing show an
  advantage only on the late phase of the epidemic
- Simple models are faster and have lighter carbon footprint

# Methods

Same setting as ICML paper.

We compare different scenario :

- 3 methods : elastic-net, xgboost, reservoir computing
- 2 features selection : all features provided (GA feature selection for
  reservoir computing), epidemiology informed features selection (no GA
  feature selection for reservoir computing).
- monthly update and no monthly update
- two period : one starts on 2020-09-02, the other one starts on
  2021-03-01

In order to evaluate the robustness of the results regarding the
variability of reservoir and hyperparameter optimization we repeat the
experiment three times.

Expected results:

- Elastic-net \> xgboost on early period
- Reservoir computing \> Elastic-net on all period (add memory and non
  linearity)
- XGboost ~= Reservoir computing on late period (complex models are
  better in late period)
- Epidemio feature selection \> Data driven feature selection on early
  period (add expert knowledge has strong importance in the early
  period)
- Elastic-net carbon footprint and time \<\<\<\<\< XGboost and Reservoir
  computing

# Prediction

### Uncertainty quantification

![](experience1_files/figure-commonmark/unnamed-chunk-5-1.png)

![](experience1_files/figure-commonmark/unnamed-chunk-6-1.png)

### Sanity check

First, we check that there is 40 reservoir prediction for each day of
the prediction for each scenario. At figure
<a href="#fig-sanitycheckNbReservoirPerDay"
class="quarto-xref">Figure 1</a>, we observe that there is indeed a
forecast for each day. Some days have less than 40 reservoirs but the
minimum is 39 which seems acceptable.

<div id="fig-sanitycheckNbReservoirPerDay">

![](experience1_files/figure-commonmark/fig-sanitycheckNbReservoirPerDay-1.png)


Figure 1: Number of reservoir per day for prediction

</div>

### Prediction

First we show a graphical evaluation of the different algorithms. On
panel A of figure
<a href="#fig-PredictionByDayByModel" class="quarto-xref">Figure 2</a>
we first observe that xgboost led to highly volatile predictions when
little information is available, persisting when using all features
without updating hyperparameters. At the contrary, both elastic-net and
reservoir computing where quite robust regarding hyperparameter choice.
When more information is available such as presented at panel B, all
models where quite stable and updating the hyperparameters had little
effect.

Regarding the graphical performance at the early phase of the epidemic,
xgboost seemed worse compared to elastic-net and reservoir computing due
to this high volatility. However, when more information is available

<div id="fig-PredictionByDayByModel">

![](experience1_files/figure-commonmark/fig-PredictionByDayByModel-1.png)


Figure 2: Prediction by day by model. Only results of the first
repetition are shown.

</div>

### Performance

#### Forecast Error by month

<div id="fig-perfbymonth">

![](experience1_files/figure-commonmark/fig-perfbymonth-1.png)


Figure 3: Forecast performance by month depending on model, update
frequency and features used. Erros greater than 50 are set to 50 for
visualisation.

</div>
<div id="fig-perfMAEMRE">

![](experience1_files/figure-commonmark/fig-perfMAEMRE-1.png)


Figure 4: Median Relative Error and Mean Absolute Error depending on
Outcome value. MAE greater than 50 are set to 50 and MRE greater than 1
are set to 1 for visualisation.

</div>
<div id="fig-perfbymonthmaeb">

![](experience1_files/figure-commonmark/fig-perfbymonthmaeb-1.png)


Figure 5: Mean Absoluter Error compared to baseline by month depending
on model, update frequency and features used. Models below horitzontal
line underperform compared to baseline model and therefore are useless.
Erros greater than 10 are set to 10 for visualisation.

</div>

#### Overall performance

<div id="ydgabwknrs" style="padding-left:0px;padding-right:0px;padding-top:10px;padding-bottom:10px;overflow-x:auto;overflow-y:auto;width:auto;height:auto;">
<style>#ydgabwknrs table {
  font-family: system-ui, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
&#10;#ydgabwknrs thead, #ydgabwknrs tbody, #ydgabwknrs tfoot, #ydgabwknrs tr, #ydgabwknrs td, #ydgabwknrs th {
  border-style: none;
}
&#10;#ydgabwknrs p {
  margin: 0;
  padding: 0;
}
&#10;#ydgabwknrs .gt_table {
  display: table;
  border-collapse: collapse;
  line-height: normal;
  margin-left: auto;
  margin-right: auto;
  color: #333333;
  font-size: 16px;
  font-weight: normal;
  font-style: normal;
  background-color: #FFFFFF;
  width: auto;
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #A8A8A8;
  border-right-style: none;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #A8A8A8;
  border-left-style: none;
  border-left-width: 2px;
  border-left-color: #D3D3D3;
}
&#10;#ydgabwknrs .gt_caption {
  padding-top: 4px;
  padding-bottom: 4px;
}
&#10;#ydgabwknrs .gt_title {
  color: #333333;
  font-size: 125%;
  font-weight: initial;
  padding-top: 4px;
  padding-bottom: 4px;
  padding-left: 5px;
  padding-right: 5px;
  border-bottom-color: #FFFFFF;
  border-bottom-width: 0;
}
&#10;#ydgabwknrs .gt_subtitle {
  color: #333333;
  font-size: 85%;
  font-weight: initial;
  padding-top: 3px;
  padding-bottom: 5px;
  padding-left: 5px;
  padding-right: 5px;
  border-top-color: #FFFFFF;
  border-top-width: 0;
}
&#10;#ydgabwknrs .gt_heading {
  background-color: #FFFFFF;
  text-align: center;
  border-bottom-color: #FFFFFF;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
}
&#10;#ydgabwknrs .gt_bottom_border {
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
}
&#10;#ydgabwknrs .gt_col_headings {
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
}
&#10;#ydgabwknrs .gt_col_heading {
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: normal;
  text-transform: inherit;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
  vertical-align: bottom;
  padding-top: 5px;
  padding-bottom: 6px;
  padding-left: 5px;
  padding-right: 5px;
  overflow-x: hidden;
}
&#10;#ydgabwknrs .gt_column_spanner_outer {
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: normal;
  text-transform: inherit;
  padding-top: 0;
  padding-bottom: 0;
  padding-left: 4px;
  padding-right: 4px;
}
&#10;#ydgabwknrs .gt_column_spanner_outer:first-child {
  padding-left: 0;
}
&#10;#ydgabwknrs .gt_column_spanner_outer:last-child {
  padding-right: 0;
}
&#10;#ydgabwknrs .gt_column_spanner {
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  vertical-align: bottom;
  padding-top: 5px;
  padding-bottom: 5px;
  overflow-x: hidden;
  display: inline-block;
  width: 100%;
}
&#10;#ydgabwknrs .gt_spanner_row {
  border-bottom-style: hidden;
}
&#10;#ydgabwknrs .gt_group_heading {
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: initial;
  text-transform: inherit;
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
  vertical-align: middle;
  text-align: left;
}
&#10;#ydgabwknrs .gt_empty_group_heading {
  padding: 0.5px;
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: initial;
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  vertical-align: middle;
}
&#10;#ydgabwknrs .gt_from_md > :first-child {
  margin-top: 0;
}
&#10;#ydgabwknrs .gt_from_md > :last-child {
  margin-bottom: 0;
}
&#10;#ydgabwknrs .gt_row {
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
  margin: 10px;
  border-top-style: solid;
  border-top-width: 1px;
  border-top-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
  vertical-align: middle;
  overflow-x: hidden;
}
&#10;#ydgabwknrs .gt_stub {
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: initial;
  text-transform: inherit;
  border-right-style: solid;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
  padding-left: 5px;
  padding-right: 5px;
}
&#10;#ydgabwknrs .gt_stub_row_group {
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: initial;
  text-transform: inherit;
  border-right-style: solid;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
  padding-left: 5px;
  padding-right: 5px;
  vertical-align: top;
}
&#10;#ydgabwknrs .gt_row_group_first td {
  border-top-width: 2px;
}
&#10;#ydgabwknrs .gt_row_group_first th {
  border-top-width: 2px;
}
&#10;#ydgabwknrs .gt_summary_row {
  color: #333333;
  background-color: #FFFFFF;
  text-transform: inherit;
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
}
&#10;#ydgabwknrs .gt_first_summary_row {
  border-top-style: solid;
  border-top-color: #D3D3D3;
}
&#10;#ydgabwknrs .gt_first_summary_row.thick {
  border-top-width: 2px;
}
&#10;#ydgabwknrs .gt_last_summary_row {
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
}
&#10;#ydgabwknrs .gt_grand_summary_row {
  color: #333333;
  background-color: #FFFFFF;
  text-transform: inherit;
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
}
&#10;#ydgabwknrs .gt_first_grand_summary_row {
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
  border-top-style: double;
  border-top-width: 6px;
  border-top-color: #D3D3D3;
}
&#10;#ydgabwknrs .gt_last_grand_summary_row_top {
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
  border-bottom-style: double;
  border-bottom-width: 6px;
  border-bottom-color: #D3D3D3;
}
&#10;#ydgabwknrs .gt_striped {
  background-color: rgba(128, 128, 128, 0.05);
}
&#10;#ydgabwknrs .gt_table_body {
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
}
&#10;#ydgabwknrs .gt_footnotes {
  color: #333333;
  background-color: #FFFFFF;
  border-bottom-style: none;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 2px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
}
&#10;#ydgabwknrs .gt_footnote {
  margin: 0px;
  font-size: 90%;
  padding-top: 4px;
  padding-bottom: 4px;
  padding-left: 5px;
  padding-right: 5px;
}
&#10;#ydgabwknrs .gt_sourcenotes {
  color: #333333;
  background-color: #FFFFFF;
  border-bottom-style: none;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 2px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
}
&#10;#ydgabwknrs .gt_sourcenote {
  font-size: 90%;
  padding-top: 4px;
  padding-bottom: 4px;
  padding-left: 5px;
  padding-right: 5px;
}
&#10;#ydgabwknrs .gt_left {
  text-align: left;
}
&#10;#ydgabwknrs .gt_center {
  text-align: center;
}
&#10;#ydgabwknrs .gt_right {
  text-align: right;
  font-variant-numeric: tabular-nums;
}
&#10;#ydgabwknrs .gt_font_normal {
  font-weight: normal;
}
&#10;#ydgabwknrs .gt_font_bold {
  font-weight: bold;
}
&#10;#ydgabwknrs .gt_font_italic {
  font-style: italic;
}
&#10;#ydgabwknrs .gt_super {
  font-size: 65%;
}
&#10;#ydgabwknrs .gt_footnote_marks {
  font-size: 75%;
  vertical-align: 0.4em;
  position: initial;
}
&#10;#ydgabwknrs .gt_asterisk {
  font-size: 100%;
  vertical-align: 0;
}
&#10;#ydgabwknrs .gt_indent_1 {
  text-indent: 5px;
}
&#10;#ydgabwknrs .gt_indent_2 {
  text-indent: 10px;
}
&#10;#ydgabwknrs .gt_indent_3 {
  text-indent: 15px;
}
&#10;#ydgabwknrs .gt_indent_4 {
  text-indent: 20px;
}
&#10;#ydgabwknrs .gt_indent_5 {
  text-indent: 25px;
}
&#10;#ydgabwknrs .katex-display {
  display: inline-flex !important;
  margin-bottom: 0.75em !important;
}
&#10;#ydgabwknrs div.Reactable > div.rt-table > div.rt-thead > div.rt-tr.rt-tr-group-header > div.rt-th-group:after {
  height: 0px !important;
}
</style>

|  |  | starting_date | update | Baseline | MAE (+/- SD) | MRE (+/- SD) | MAEB (+/- SD) | MREB (+/- SD) |
|----|----|----|----|----|----|----|----|----|
| ENet | All | 2020-09-02 | No monthly update | 21.03(±12.45) | 20.47(±13.86) | 0.2(±0.2) | -0.56(±14.04) | 1.02(±12.93) |
|  | All | 2020-09-02 | Monthly update | 21.03(±12.45) | 22.12(±15.73) | 0.22(±0.22) | 1.09(±14.23) | 1.09(±6.47) |
|  | Epi | 2020-09-02 | No monthly update | 21.03(±12.45) | 24.36(±20.26) | 0.23(±0.25) | 3.33(±17.76) | 1.04(±10.89) |
|  | Epi | 2020-09-02 | Monthly update | 21.03(±12.45) | 24.65(±20.54) | 0.23(±0.25) | 3.61(±18.33) | 1.08(±11.34) |
| RC | All | 2020-09-02 | No monthly update | 21.03(±12.45) | 21.54(±18.39) | 0.2(±0.28) | 0.51(±19.52) | 0.86(±7.79) |
|  | All | 2020-09-02 | Monthly update | 21.03(±12.45) | 20.82(±18.42) | 0.2(±0.28) | -0.21(±17.7) | 0.95(±4.49) |
|  | Epi | 2020-09-02 | No monthly update | 21.03(±12.45) | 22.47(±18.41) | 0.21(±0.22) | 1.44(±18.5) | 0.98(±13.12) |
|  | Epi | 2020-09-02 | Monthly update | 21.03(±12.45) | 22.69(±16.69) | 0.24(±0.22) | 1.66(±17) | 1.05(±16.75) |
| XGBoost | All | 2020-09-02 | No monthly update | 21.03(±12.45) | 161.48(±253.34) | 0.88(±3.51) | 140.44(±255.67) | 3.66(±639.63) |
|  | All | 2020-09-02 | Monthly update | 21.03(±12.45) | 28.72(±24.91) | 0.26(±0.38) | 7.68(±23.19) | 1.3(±18.99) |
|  | Epi | 2020-09-02 | No monthly update | 21.03(±12.45) | 24.95(±19.65) | 0.26(±0.27) | 3.91(±19.25) | 1.2(±21.78) |
|  | Epi | 2020-09-02 | Monthly update | 21.03(±12.45) | 31.43(±37.04) | 0.25(±0.41) | 10.39(±36.03) | 1.29(±8.8) |

Performance by algorithm initiated in 2020-09-02 from 2020-09-02 to
2021-03-15

</div>
<div id="auujvnjgio" style="padding-left:0px;padding-right:0px;padding-top:10px;padding-bottom:10px;overflow-x:auto;overflow-y:auto;width:auto;height:auto;">
<style>#auujvnjgio table {
  font-family: system-ui, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
&#10;#auujvnjgio thead, #auujvnjgio tbody, #auujvnjgio tfoot, #auujvnjgio tr, #auujvnjgio td, #auujvnjgio th {
  border-style: none;
}
&#10;#auujvnjgio p {
  margin: 0;
  padding: 0;
}
&#10;#auujvnjgio .gt_table {
  display: table;
  border-collapse: collapse;
  line-height: normal;
  margin-left: auto;
  margin-right: auto;
  color: #333333;
  font-size: 16px;
  font-weight: normal;
  font-style: normal;
  background-color: #FFFFFF;
  width: auto;
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #A8A8A8;
  border-right-style: none;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #A8A8A8;
  border-left-style: none;
  border-left-width: 2px;
  border-left-color: #D3D3D3;
}
&#10;#auujvnjgio .gt_caption {
  padding-top: 4px;
  padding-bottom: 4px;
}
&#10;#auujvnjgio .gt_title {
  color: #333333;
  font-size: 125%;
  font-weight: initial;
  padding-top: 4px;
  padding-bottom: 4px;
  padding-left: 5px;
  padding-right: 5px;
  border-bottom-color: #FFFFFF;
  border-bottom-width: 0;
}
&#10;#auujvnjgio .gt_subtitle {
  color: #333333;
  font-size: 85%;
  font-weight: initial;
  padding-top: 3px;
  padding-bottom: 5px;
  padding-left: 5px;
  padding-right: 5px;
  border-top-color: #FFFFFF;
  border-top-width: 0;
}
&#10;#auujvnjgio .gt_heading {
  background-color: #FFFFFF;
  text-align: center;
  border-bottom-color: #FFFFFF;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
}
&#10;#auujvnjgio .gt_bottom_border {
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
}
&#10;#auujvnjgio .gt_col_headings {
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
}
&#10;#auujvnjgio .gt_col_heading {
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: normal;
  text-transform: inherit;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
  vertical-align: bottom;
  padding-top: 5px;
  padding-bottom: 6px;
  padding-left: 5px;
  padding-right: 5px;
  overflow-x: hidden;
}
&#10;#auujvnjgio .gt_column_spanner_outer {
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: normal;
  text-transform: inherit;
  padding-top: 0;
  padding-bottom: 0;
  padding-left: 4px;
  padding-right: 4px;
}
&#10;#auujvnjgio .gt_column_spanner_outer:first-child {
  padding-left: 0;
}
&#10;#auujvnjgio .gt_column_spanner_outer:last-child {
  padding-right: 0;
}
&#10;#auujvnjgio .gt_column_spanner {
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  vertical-align: bottom;
  padding-top: 5px;
  padding-bottom: 5px;
  overflow-x: hidden;
  display: inline-block;
  width: 100%;
}
&#10;#auujvnjgio .gt_spanner_row {
  border-bottom-style: hidden;
}
&#10;#auujvnjgio .gt_group_heading {
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: initial;
  text-transform: inherit;
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
  vertical-align: middle;
  text-align: left;
}
&#10;#auujvnjgio .gt_empty_group_heading {
  padding: 0.5px;
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: initial;
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  vertical-align: middle;
}
&#10;#auujvnjgio .gt_from_md > :first-child {
  margin-top: 0;
}
&#10;#auujvnjgio .gt_from_md > :last-child {
  margin-bottom: 0;
}
&#10;#auujvnjgio .gt_row {
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
  margin: 10px;
  border-top-style: solid;
  border-top-width: 1px;
  border-top-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
  vertical-align: middle;
  overflow-x: hidden;
}
&#10;#auujvnjgio .gt_stub {
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: initial;
  text-transform: inherit;
  border-right-style: solid;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
  padding-left: 5px;
  padding-right: 5px;
}
&#10;#auujvnjgio .gt_stub_row_group {
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: initial;
  text-transform: inherit;
  border-right-style: solid;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
  padding-left: 5px;
  padding-right: 5px;
  vertical-align: top;
}
&#10;#auujvnjgio .gt_row_group_first td {
  border-top-width: 2px;
}
&#10;#auujvnjgio .gt_row_group_first th {
  border-top-width: 2px;
}
&#10;#auujvnjgio .gt_summary_row {
  color: #333333;
  background-color: #FFFFFF;
  text-transform: inherit;
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
}
&#10;#auujvnjgio .gt_first_summary_row {
  border-top-style: solid;
  border-top-color: #D3D3D3;
}
&#10;#auujvnjgio .gt_first_summary_row.thick {
  border-top-width: 2px;
}
&#10;#auujvnjgio .gt_last_summary_row {
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
}
&#10;#auujvnjgio .gt_grand_summary_row {
  color: #333333;
  background-color: #FFFFFF;
  text-transform: inherit;
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
}
&#10;#auujvnjgio .gt_first_grand_summary_row {
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
  border-top-style: double;
  border-top-width: 6px;
  border-top-color: #D3D3D3;
}
&#10;#auujvnjgio .gt_last_grand_summary_row_top {
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
  border-bottom-style: double;
  border-bottom-width: 6px;
  border-bottom-color: #D3D3D3;
}
&#10;#auujvnjgio .gt_striped {
  background-color: rgba(128, 128, 128, 0.05);
}
&#10;#auujvnjgio .gt_table_body {
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
}
&#10;#auujvnjgio .gt_footnotes {
  color: #333333;
  background-color: #FFFFFF;
  border-bottom-style: none;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 2px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
}
&#10;#auujvnjgio .gt_footnote {
  margin: 0px;
  font-size: 90%;
  padding-top: 4px;
  padding-bottom: 4px;
  padding-left: 5px;
  padding-right: 5px;
}
&#10;#auujvnjgio .gt_sourcenotes {
  color: #333333;
  background-color: #FFFFFF;
  border-bottom-style: none;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 2px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
}
&#10;#auujvnjgio .gt_sourcenote {
  font-size: 90%;
  padding-top: 4px;
  padding-bottom: 4px;
  padding-left: 5px;
  padding-right: 5px;
}
&#10;#auujvnjgio .gt_left {
  text-align: left;
}
&#10;#auujvnjgio .gt_center {
  text-align: center;
}
&#10;#auujvnjgio .gt_right {
  text-align: right;
  font-variant-numeric: tabular-nums;
}
&#10;#auujvnjgio .gt_font_normal {
  font-weight: normal;
}
&#10;#auujvnjgio .gt_font_bold {
  font-weight: bold;
}
&#10;#auujvnjgio .gt_font_italic {
  font-style: italic;
}
&#10;#auujvnjgio .gt_super {
  font-size: 65%;
}
&#10;#auujvnjgio .gt_footnote_marks {
  font-size: 75%;
  vertical-align: 0.4em;
  position: initial;
}
&#10;#auujvnjgio .gt_asterisk {
  font-size: 100%;
  vertical-align: 0;
}
&#10;#auujvnjgio .gt_indent_1 {
  text-indent: 5px;
}
&#10;#auujvnjgio .gt_indent_2 {
  text-indent: 10px;
}
&#10;#auujvnjgio .gt_indent_3 {
  text-indent: 15px;
}
&#10;#auujvnjgio .gt_indent_4 {
  text-indent: 20px;
}
&#10;#auujvnjgio .gt_indent_5 {
  text-indent: 25px;
}
&#10;#auujvnjgio .katex-display {
  display: inline-flex !important;
  margin-bottom: 0.75em !important;
}
&#10;#auujvnjgio div.Reactable > div.rt-table > div.rt-thead > div.rt-tr.rt-tr-group-header > div.rt-th-group:after {
  height: 0px !important;
}
</style>

|  |  | starting_date | update | Baseline | MAE | MRE | MAEB | MREB |
|----|----|----|----|----|----|----|----|----|
| ENet | All | 2021-03-01 | No monthly update | 18.59 (18.59 ; 18.59) | 15.83 (15.82 ; 15.87) | 0.29 (0.28 ; 0.29) | -2.76 (-2.77 ; -2.72) | 0.85 (0.85 ; 0.86) |
|  | All | 2021-03-01 | Monthly update | 18.59 (18.59 ; 18.59) | 15.98 (15.9 ; 16.29) | 0.28 (0.28 ; 0.3) | -2.6 (-2.68 ; -2.29) | 0.89 (0.88 ; 0.9) |
|  | Epi | 2021-03-01 | No monthly update | 18.59 (18.59 ; 18.59) | 15.96 (15.86 ; 16) | 0.29 (0.29 ; 0.3) | -2.62 (-2.73 ; -2.58) | 0.91 (0.9 ; 0.91) |
|  | Epi | 2021-03-01 | Monthly update | 18.59 (18.59 ; 18.59) | 15.88 (15.81 ; 15.89) | 0.29 (0.28 ; 0.29) | -2.7 (-2.77 ; -2.7) | 0.91 (0.9 ; 0.91) |
| RC | All | 2021-03-01 | No monthly update | 18.59 (18.59 ; 18.59) | 15.4 (15.24 ; 15.6) | 0.27 (0.24 ; 0.28) | -3.19 (-3.35 ; -2.99) | 0.86 (0.85 ; 0.87) |
|  | All | 2021-03-01 | Monthly update | 18.59 (18.59 ; 18.59) | 15.63 (15.59 ; 15.65) | 0.27 (0.25 ; 0.28) | -2.96 (-3 ; -2.93) | 0.86 (0.85 ; 0.88) |
|  | Epi | 2021-03-01 | No monthly update | 18.59 (18.59 ; 18.59) | 15.16 (15.05 ; 17.45) | 0.25 (0.25 ; 0.32) | -3.43 (-3.53 ; -1.14) | 0.86 (0.83 ; 0.97) |
|  | Epi | 2021-03-01 | Monthly update | 18.59 (18.59 ; 18.59) | 15.1 (14.96 ; 15.46) | 0.25 (0.25 ; 0.28) | -3.48 (-3.62 ; -3.12) | 0.83 (0.8 ; 0.87) |
| XGBoost | All | 2021-03-01 | No monthly update | 18.59 (18.59 ; 18.59) | 16.08 (15.98 ; 19.95) | 0.27 (0.24 ; 0.37) | -2.51 (-2.61 ; 1.36) | 0.88 (0.84 ; 1.12) |
|  | All | 2021-03-01 | Monthly update | 18.59 (18.59 ; 18.59) | 16.29 (16.26 ; 16.78) | 0.29 (0.27 ; 0.32) | -2.29 (-2.33 ; -1.8) | 0.92 (0.89 ; 0.93) |
|  | Epi | 2021-03-01 | No monthly update | 18.59 (18.59 ; 18.59) | 16.44 (16.42 ; 16.97) | 0.28 (0.28 ; 0.31) | -2.15 (-2.17 ; -1.62) | 0.93 (0.88 ; 0.95) |
|  | Epi | 2021-03-01 | Monthly update | 18.59 (18.59 ; 18.59) | 16.99 (16.61 ; 17.32) | 0.32 (0.31 ; 0.33) | -1.59 (-1.97 ; -1.27) | 0.89 (0.84 ; 0.97) |

Performance by algorithm initiated in 2021-03-01 from 2021-03-15 to
2022-01-17.

</div>

![Performance by algorithm initiated in 2021-03-01 from 2021-03-15 to
2022-01-17. Erros greater than 25 are set to 25 for
visualisation.](experience1_files/figure-commonmark/overallPerf-1.png)

# Hyperparameters

## Sanity check

![Numbers of trial per model and date. Sanity
check.](experience1_files/figure-commonmark/unnamed-chunk-14-1.png)

![Q1-Q3 distribution of numeric hyperparameters. Sanity
check.](experience1_files/figure-commonmark/unnamed-chunk-15-1.png)

## Numeric hyperparameters

### Hyperparameter evolution

<div id="fig-evolutionhyperparameters">

![](experience1_files/figure-commonmark/fig-evolutionhyperparameters-1.png)


Figure 6: Numeric hyperparameter, density of 40 best individuals per
hyperparameter update date.

</div>

# Time and carbon footprint

![Execution time, energy consumption and carbon footprint by algorithm
starting at
2021-03-01..](experience1_files/figure-commonmark/unnamed-chunk-17-1.png)

<div id="fig-emissionvsperformance">

![](experience1_files/figure-commonmark/fig-emissionvsperformance-1.png)


Figure 7: Mean Absolute Error and Carbon footprint by algorithm starting
at 2021-03-01.

</div>
<div id="fig-emissionvsperformancelog">

![](experience1_files/figure-commonmark/fig-emissionvsperformancelog-1.png)


Figure 8: Mean Absolute Error and Carbon footprint by algorithm starting
at 2021-03-01.

</div>
