clear all
set maxvar 32000
set matsize 10000
set more off, perm

cd C:\Users\Alex\Git_Repositories\Thesis

* data directory 
global datafiles "C:\Users\Alex\Git_Repositories\Thesis"

use  "$datafiles\Stata_Regressions\US_Paid_leave_analysis_altered.dta", clear

global X "i.rhcalyr i.lBirth i.rhcalyr#i.state i.lBirth#i.state i.lBirth#i.rhcalyr _LlBiXpos_2_1 _LlBiXpos_8_1-_LlBiXpos_50_1"

/* run fixed effects regressions, sippid is the cross-sectional unit */
foreach i in rm_lfp working looking  {
	foreach j in 11 13 15 17 19 21 23 25 27 29 31 33 35 37 39 41 43 45 47 49 51 53  {
		quietly xtreg `i' $X [pweight=end_weight] if industry_pre_birth=="`j'",fe vce(cluster sippid)
		estimates save Stata_ster/`i'_`j',replace 
	} 	
}

/* run unweighted effects regressions, sippid is the cross-sectional unit */
foreach i in rm_lfp working looking {
	foreach j in 11 13 15 17 19 21 23 25 27 29 31 33 35 37 39 41 43 45 47 49 51 53  {
		quietly xtreg `i' $X if industry_pre_birth=="`j'",fe vce(cluster sippid)
		estimates save Stata_ster/`i'_`j'_unweighted, replace 
	} 	
}

* Create an datafile to store weighted coefficients
clear
set obs 49
gen time = _n -25
save "$datafiles/Stata_Results/results_occupations_weighted.dta", replace emptyok

* Use stored weighted results, create files for figures
foreach y in rm_lfp working looking  {
	foreach i in 11 13 15 17 19 21 23 25 27 29 31 33 35 37 39 41 43 45 47 49 51 53 {
		use "$datafiles/Stata_Results/results_occupations_weighted.dta", clear
		estimates use Stata_ster/`y'_`i'
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
		save "$datafiles/Stata_Results/results_occupations_weighted.dta", replace  
	}
}
