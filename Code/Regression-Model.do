////////////////////////////////////////////////////////////////////////////////

// Will Carpenter 
// Stata, long time no see my good friend ... let's goooo

////////////////////////////////////////////////////////////////////////////////

// Import dataset 

// import delimited "`folder'/`file'", clear stringcols(_all) varnames(1)

// Run summaries, run tests on data validity 
// Run regressions, generate predictions 
// Save down predictions 

clear all
set more off 
cls	

import delimited "https://raw.githubusercontent.com/wrcarpenter/MMA-Handicapping-Model/main/Data/ufcBouts_model_v2.csv", varnames(1)

// clean up variables 
gen event_date_val = date(event_date, "YMD")
format event_date_val %td Mon-DD-YY

gen event_year = year(event_date_val)

gen win_bout = win

br event_date event_date_val

local regressors ///
/// add variables here 

logit win_bout age opp_age prev_num_fights roster_time event_year if upcoming == 0

predict pwin_bout if upcoming==1


