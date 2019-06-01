** Create an datafile to store Event-Study DD coefficients (can be used to make figures)
clear
set obs 49
gen time = _n -25
save "$datafiles/ES_DD_estimates_altered.dta", replace emptyok

*data directory (where posted datasets are stored)
global datafiles "D:\Users\Alex\Git_Repositories\Thesis"

***************** Pattern of LFP around birth for mothers giving birth in CA and NJ before and after paid leave mandates  
foreach i of numlist 1 2 {
use  "$datafiles\US_Paid_leave_analysis_altered.dta", clear
local X1  "_IBirth_2-_IBirth_51  [fweight=end_weight] if  post_policy==1 & (state==6 | state==34) "
local X2  "_IBirth_2-_IBirth_51  [fweight=end_weight] if  post_policy==0 & (state==6 | state==34) "
qui reg rm_lfp `X`i'', vce(cluster sippid)

use "$datafiles/ES_DD_estimates_altered.dta", clear
quietly {
         gen b_X`i'=.
		 forval j=1/49{
		               if `j'==1{
					              replace b_X`i'=_b[_cons] in `j'
							      }
						else {
						      replace b_X`i'=_b[_IBirth_`j'] + _b[_cons] in `j'
							 }
					     }
          }
		save "$datafiles/ES_DD_estimates_altered.dta", replace  
      }   
	  
***************** Simple difference estimates (note that some combinations of years and relative-to-birth month do not exist (for example if a panel only included part of a year - these will be omitted)	  
use  "$datafiles\US_Paid_leave_analysis_altered.dta", clear
qui reg  rm_lfp i.lBirth  i.post_policy _LlBiXpos_2_1 _LlBiXpos_8_1-_LlBiXpos_50_1 [fweight=end_weight] if (state==6 | state==34),  vce(cluster sippid)

use "$datafiles/ES_DD_estimates_altered.dta", clear
qui {
         gen b_X3=.
		 		 forval j=1/49{       
							local var`j'=`j'+0
							if `j'>=1 & `j'<=7{
					              replace b_X3=0 in `j'
								  }
						else {
		                      replace b_X3=_b[_LlBiXpos_`var`j''_1]  in `j'
							 
			}
			}
          }
		save "$datafiles/ES_DD_estimates_altered.dta", replace  
 
***************** Event-Study DD estimates for full sample and by education	  
foreach i of numlist  4 5 6  {
use  "$datafiles\US_Paid_leave_analysis_altered.dta", clear
local X4  " i.rhcalyr i.lBirth i.rhcalyr#i.state i.lBirth#i.state i.lBirth#i.rhcalyr _LlBiXpos_2_1 _LlBiXpos_8_1-_LlBiXpos_50_1 [pweight=end_weight] "
local X5  " i.rhcalyr i.lBirth i.rhcalyr#i.state i.lBirth#i.state i.lBirth#i.rhcalyr _LlBiXpos_2_1 _LlBiXpos_8_1-_LlBiXpos_50_1 [pweight=end_weight] if  lt_college==0 "
local X6  " i.rhcalyr i.lBirth i.rhcalyr#i.state i.lBirth#i.state i.lBirth#i.rhcalyr _LlBiXpos_2_1 _LlBiXpos_8_1-_LlBiXpos_50_1 [pweight=end_weight] if  lt_college==1 "
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
		save "$datafiles/ES_DD_estimates_altered.dta", replace  
}
***************** Decomposing LFP DD estimates into component parts: "With a Job" and "Looking"  (note there are a few other small categories not included (see SIPP definitions and coding above)
foreach i of numlist  7 8 {
use  "$datafiles\US_Paid_leave_analysis_altered.dta", clear
local X7  " looking i.rhcalyr i.lBirth i.rhcalyr#i.state i.lBirth#i.state i.lBirth#i.rhcalyr _LlBiXpos_2_1 _LlBiXpos_8_1-_LlBiXpos_50_1 [pweight=end_weight] if  lt_college==1 "
local X8  " working i.rhcalyr i.lBirth i.rhcalyr#i.state i.lBirth#i.state i.lBirth#i.rhcalyr _LlBiXpos_2_1 _LlBiXpos_8_1-_LlBiXpos_50_1 [pweight=end_weight] if  lt_college==1 "
qui xtreg `X`i'', fe  vce(cluster sippid)
di "joint test for mth +6 to +12:"
qui test _LlBiXpos_31_1 _LlBiXpos_32_1 _LlBiXpos_33_1 _LlBiXpos_34_1 _LlBiXpos_35_1 _LlBiXpos_36_1 
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
		save "$datafiles/ES_DD_estimates_altered.dta", replace  
      }                    			        
	  
	  
	
