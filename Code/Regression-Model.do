////////////////////////////////////////////////////////////////////////////////

// Implementing Regressions for MMA Betting Model
// William Carpenter 

////////////////////////////////////////////////////////////////////////////////
// Import dataset 
// import delimited "`folder'/`file'", clear stringcols(_all) varnames(1)

// Run summaries, run tests on data validity 
// Run regressions, generate predictions 
// Save down predictions 

clear all
set more off 
cls	

import delimited "https://raw.githubusercontent.com/wrcarpenter/MMA-Handicapping-Model/main/Data/model_data.csv", varnames(1)

// clean up variables 
gen event_date_val = date(event_date, "MDY")
format event_date_val %td Mon-DD-YY

gen event_year = year(event_date_val)

gen win_bout = win

br event_date event_date_val

local regressors ///
/// add variables here

// Logistic model
logit win_bout age height_inches event_year prev_num_fights prev_fight_result opp_age opp_height if upcoming == 0

// Formulating predictions for upcoming matches
predict pwin_bout if upcoming==1 


