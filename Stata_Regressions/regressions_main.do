clear all
set maxvar 32000
set matsize 10000
set more off, perm

cd C:\Users\Alex\Git_Repositories\Thesis

* data directory
global datafiles "C:\Users\Alex\Git_Repositories\Thesis"

* Run weighted regressions, store results
foreach y in rm_lfp working looking  {
	foreach i of numlist 1 2 3 4 5 {
		use  "$datafiles\Stata_Regressions\US_Paid_leave_analysis_altered.dta", clear
		local X1  " i.rhcalyr i.lBirth i.rhcalyr#i.state i.lBirth#i.state i.lBirth#i.rhcalyr _LlBiXpos_2_1 _LlBiXpos_8_1-_LlBiXpos_50_1 [pweight=end_weight] "
		local X2  " i.rhcalyr i.lBirth i.rhcalyr#i.state i.lBirth#i.state i.lBirth#i.rhcalyr _LlBiXpos_2_1 _LlBiXpos_8_1-_LlBiXpos_50_1 [pweight=end_weight] if  lt_college==0 "
		local X3  " i.rhcalyr i.lBirth i.rhcalyr#i.state i.lBirth#i.state i.lBirth#i.rhcalyr _LlBiXpos_2_1 _LlBiXpos_8_1-_LlBiXpos_50_1 [pweight=end_weight] if  lt_college==1 "
		local X4  " i.rhcalyr i.lBirth i.rhcalyr#i.state i.lBirth#i.state i.lBirth#i.rhcalyr _LlBiXpos_2_1 _LlBiXpos_8_1-_LlBiXpos_50_1 [pweight=end_weight] if  blue_collar==0 "
		local X5  " i.rhcalyr i.lBirth i.rhcalyr#i.state i.lBirth#i.state i.lBirth#i.rhcalyr _LlBiXpos_2_1 _LlBiXpos_8_1-_LlBiXpos_50_1 [pweight=end_weight] if  blue_collar==1 "
		qui xtreg `y' `X`i'', fe  vce(cluster sippid)
		estimates save Stata_ster/`y'_model_`i'_weighted, replace 
	}
}

* Create an datafile to store Event-Study DD coefficients (can be used to make figures)
clear
set obs 49
gen time = _n -25
save "$datafiles/Stata_Results/results_main.dta", replace emptyok

* Use stored results, create files for figures
foreach y in rm_lfp working looking  {
	foreach i of numlist 1 2 3 4 5 {
		use "$datafiles/Stata_Results/results_main.dta", clear
		estimates use Stata_ster/`y'_model_`i'_weighted
		qui {
			gen b_`y'_X`i'=.
		 	forval j=1/49{       
				local var`j'=`j'
				if `j'>=1 & `j'<=7 {
					replace b_`y'_X`i'= 0 in `j'
				} 
				else {
		            replace b_`y'_X`i'=_b[_LlBiXpos_`var`j''_1]  in `j'			 
				}	
			}
		}
		save "$datafiles/Stata_Results/results_main.dta", replace  
	}
}
