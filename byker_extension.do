clear
set obs 49
gen time = _n -25
save "$datafiles/my_estimates.dta", replace emptyok
***************** Pattern of LFP around birth for mothers giving birth in CA and NJ before and after paid leave mandates  
foreach i of numlist 1 2 {
use  "$datafiles\US_Paid_leave_analysis_altered.dta", clear
local X1  "_IBirth_2-_IBirth_51  [fweight=end_weight] if  post_policy==1 & (state==6 | state==34) & industry_mode == "13" "
local X2  "_IBirth_2-_IBirth_51  [fweight=end_weight] if  post_policy==0 & (state==6 | state==34) & industry_mode == "13" "
qui reg rm_lfp `X`i'', vce(cluster sippid)

use "$datafiles/my_estimates.dta", clear
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
		save "$datafiles/my_estimates.dta", replace  
      }   
