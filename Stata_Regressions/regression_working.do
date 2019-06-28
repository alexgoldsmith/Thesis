clear all
set maxvar 32000
set matsize 10000
set more off, perm

*data directory (where posted datasets are stored)
global datafiles "D:\Users\Alex\Git_Repositories\Thesis"

** Create an datafile to store Event-Study DD coefficients (can be used to make figures)
clear
set obs 49
gen time = _n -25
save "$datafiles/Stata_Results/results_working.dta", replace emptyok
 
***************** Event-Study DD estimates for full sample and by education	  
foreach i of numlist 1 2 3 4 5 {
use  "$datafiles\Stata_Regressions\US_Paid_leave_analysis_altered.dta", clear
local X1  " i.rhcalyr i.lBirth i.rhcalyr#i.state i.lBirth#i.state i.lBirth#i.rhcalyr _LlBiXpos_2_1 _LlBiXpos_8_1-_LlBiXpos_50_1 [pweight=end_weight] "
local X2  " i.rhcalyr i.lBirth i.rhcalyr#i.state i.lBirth#i.state i.lBirth#i.rhcalyr _LlBiXpos_2_1 _LlBiXpos_8_1-_LlBiXpos_50_1 [pweight=end_weight] if  lt_college==0 "
local X3  " i.rhcalyr i.lBirth i.rhcalyr#i.state i.lBirth#i.state i.lBirth#i.rhcalyr _LlBiXpos_2_1 _LlBiXpos_8_1-_LlBiXpos_50_1 [pweight=end_weight] if  lt_college==1 "
local X4  " i.rhcalyr i.lBirth i.rhcalyr#i.state i.lBirth#i.state i.lBirth#i.rhcalyr _LlBiXpos_2_1 _LlBiXpos_8_1-_LlBiXpos_50_1 [pweight=end_weight] if  blue_collar==0 "
local X5  " i.rhcalyr i.lBirth i.rhcalyr#i.state i.lBirth#i.state i.lBirth#i.rhcalyr _LlBiXpos_2_1 _LlBiXpos_8_1-_LlBiXpos_50_1 [pweight=end_weight] if  blue_collar==1 "
qui xtreg working `X`i'', fe  vce(cluster sippid)

di "joint test for mth -3 to +3:"
qui test _LlBiXpos_22_1 _LlBiXpos_23_1 _LlBiXpos_24_1 _LlBiXpos_25_1 _LlBiXpos_26_1 _LlBiXpos_27_1 _LlBiXpos_28_1
di r(p)

use "$datafiles/Stata_Results/results_working.dta", clear
qui {
         gen b_X`i'=.
		 		 forval j=1/49{       
							local var`j'=`j'+0
							if `j'>=1 & `j'<=7{
					              replace b_X`i'=0 in `j'
								  }
						else {
		                      replace b_X`i'=_b[_LlBiXpos_`var`j''_1]  in `j'
							 
			}
			}
          }
		save "$datafiles/Stata_Results/results_working.dta", replace  
}
