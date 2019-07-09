clear all
set maxvar 32000
set matsize 10000
set more off, perm

cd C:\Users\Alex\Git_Repositories\Thesis

* data directory
global datafiles "C:\Users\Alex\Git_Repositories\Thesis"

* Create an datafile to store weighted coefficients 
clear
set obs 10
save "$datafiles/Stata_Results/joint_tests_main_weighted.dta", replace emptyok

* Declare tests
global m17_m12 "_LlBiXpos_8_1 _LlBiXpos_9_1 _LlBiXpos_10_1 _LlBiXpos_11_1 _LlBiXpos_12_1 _LlBiXpos_13_1 "
global m15_m9  "_LlBiXpos_10_1 _LlBiXpos_11_1 _LlBiXpos_12_1 _LlBiXpos_13_1 _LlBiXpos_14_1 _LlBiXpos_15_1 _LlBiXpos_16_1"
global m12_m6  "_LlBiXpos_13_1 _LlBiXpos_14_1 _LlBiXpos_15_1 _LlBiXpos_16_1 _LlBiXpos_17_1 _LlBiXpos_18_1 _LlBiXpos_19_1"
global m9_m3   "_LlBiXpos_16_1 _LlBiXpos_17_1 _LlBiXpos_18_1 _LlBiXpos_19_1 _LlBiXpos_20_1 _LlBiXpos_21_1 _LlBiXpos_22_1"
global m6_p0   "_LlBiXpos_19_1 _LlBiXpos_20_1 _LlBiXpos_21_1 _LlBiXpos_22_1 _LlBiXpos_23_1 _LlBiXpos_24_1 _LlBiXpos_28_1"
global m3_p3   "_LlBiXpos_22_1 _LlBiXpos_23_1 _LlBiXpos_24_1 _LlBiXpos_25_1 _LlBiXpos_26_1 _LlBiXpos_27_1 _LlBiXpos_28_1"
global m0_p6   "_LlBiXpos_25_1 _LlBiXpos_26_1 _LlBiXpos_27_1 _LlBiXpos_28_1 _LlBiXpos_29_1 _LlBiXpos_30_1 _LlBiXpos_31_1"
global p3_p9   "_LlBiXpos_28_1 _LlBiXpos_29_1 _LlBiXpos_30_1 _LlBiXpos_31_1 _LlBiXpos_32_1 _LlBiXpos_33_1 _LlBiXpos_34_1"
global p6_p12  "_LlBiXpos_31_1 _LlBiXpos_32_1 _LlBiXpos_33_1 _LlBiXpos_34_1 _LlBiXpos_35_1 _LlBiXpos_36_1 _LlBiXpos_37_1"
global p9_p15  "_LlBiXpos_34_1 _LlBiXpos_35_1 _LlBiXpos_36_1 _LlBiXpos_37_1 _LlBiXpos_38_1 _LlBiXpos_39_1 _LlBiXpos_40_1"



* Use stored weighted results, create files for figures
foreach y in rm_lfp working looking  {
	foreach i of numlist 1 2 3 4 5 {
		use "$datafiles/Stata_Results/joint_tests_main_weighted.dta", clear
		estimates use Stata_ster/`y'_model_`i'_weighted
		quietly gen p_`y'_`i'=.
		local k = 0
		foreach j in m17_m12 m15_m9 m12_m6 m9_m3 m6_p0 m3_p3 m0_p6 p3_p9 p6_p12 p9_p15 {
			*display "F-test of window `j' for model `i' and dependent variable `y'"
			quietly test "$`j'"
			local k = `k' + 1
			quietly replace p_`y'_`i' = r(p) in `k'
			}
		save "$datafiles/Stata_Results/joint_tests_main_weighted.dta", replace
	}  
}
