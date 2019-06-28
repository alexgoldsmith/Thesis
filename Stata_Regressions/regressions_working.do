***************** Event-Study DD estimates for occupation groups	  
foreach i of numlist 9 10  {
use  "$datafiles\US_Paid_leave_analysis_altered.dta", clear
local X5  " i.rhcalyr i.lBirth i.rhcalyr#i.state i.lBirth#i.state i.lBirth#i.rhcalyr _LlBiXpos_2_1 _LlBiXpos_8_1-_LlBiXpos_50_1 [pweight=end_weight] if  blue_collar==0 "
local X6  " i.rhcalyr i.lBirth i.rhcalyr#i.state i.lBirth#i.state i.lBirth#i.rhcalyr _LlBiXpos_2_1 _LlBiXpos_8_1-_LlBiXpos_50_1 [pweight=end_weight] if  blue_collar==1 "
qui xtreg rm_lfp `X`i'', fe  vce(cluster sippid)

di "joint test for mth -3 to +3:"
qui test _LlBiXpos_22_1 _LlBiXpos_23_1 _LlBiXpos_24_1 _LlBiXpos_25_1 _LlBiXpos_26_1 _LlBiXpos_27_1 _LlBiXpos_28_1
di r(p)

use "$datafiles/ES_DD_estimates_altered.dta", clear
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
}
