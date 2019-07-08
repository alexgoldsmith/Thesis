clear all
set maxvar 32000
set matsize 10000
set more off, perm

cd C:\Users\Alex\Git_Repositories\Thesis

* data directory
global datafiles "C:\Users\Alex\Git_Repositories\Thesis"

* Create an datafile to store weighted coefficients 
clear
save "$datafiles/Stata_Results/joint_tests_main_weighted.dta", replace emptyok

* Declare tests
global m3_p3 "_LlBiXpos_22_1 _LlBiXpos_23_1 _LlBiXpos_24_1 _LlBiXpos_25_1 _LlBiXpos_26_1 _LlBiXpos_27_1 _LlBiXpos_28_1"
global m0_p6 "_LlBiXpos_25_1 _LlBiXpos_26_1 _LlBiXpos_27_1 _LlBiXpos_28_1 _LlBiXpos_29_1 _LlBiXpos_30_1 _LlBiXpos_31_1"

* Use stored weighted results, create files for figures
foreach y in rm_lfp working looking  {
	foreach i of numlist 1 2 3 4 5 {
		use "$datafiles/Stata_Results/joint_tests_main_weighted.dta", clear
		estimates use Stata_ster/`y'_model_`i'_weighted
		gen p_`y'_`i'=.
		foreach j in m3_p3 m0_p6 {
			quietly test "$`j'"
			forvalues k = 1/`j' {    
				replace p_`y'_`i'= r(p)
			}
		}
		save "$datafiles/Stata_Results/joint_tests_main_weighted.dta", replace
	}  
}
