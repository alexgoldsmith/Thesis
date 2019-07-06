clear all
set maxvar 32000
set matsize 10000
set more off, perm

cd C:\Users\Alex\Git_Repositories\Thesis

capture log close
log using Stata_log_files\hypothesis_tests_and_plots_of_coefficients.log,replace 

/* run unweighted effects regressions, sippid is the cross-sectional unit */
foreach i in rm_lfp working looking {
	foreach j in 11 13 15 17 19 21 23 25 27 29 31 33 35 37 39 41 43 45 47 49 51 53  {
		estimates use Stata_ster/`i'_`j'_unweighted
		estimates store `i'_`j'_unweighted
		
		estimates use Stata_ster/`i'_`j'
		estimates store `i'_`j'_weighted
	} 	
}

global m3_p3 "_LlBiXpos_22_1 _LlBiXpos_23_1 _LlBiXpos_24_1 _LlBiXpos_25_1 _LlBiXpos_26_1 _LlBiXpos_27_1 _LlBiXpos_28_1"
global m0_p6 "_LlBiXpos_25_1 _LlBiXpos_26_1 _LlBiXpos_27_1 _LlBiXpos_28_1 _LlBiXpos_29_1 _LlBiXpos_30_1 _LlBiXpos_31_1"

matrix b_all = J(44,1,.) 
foreach j in 11 13 {
	foreach i in rm_lfp working looking {
	    /* read in the estimates */
		estimates restore `i'_`j'_weighted
		foreach k in m3_p3 m0_p6 {
			if "`k'"=="m3_p3" {
			   lincom _LlBiXpos_25_1 + _LlBiXpos_26_1 + _LlBiXpos_27_1 + _LlBiXpos_28_1 + _LlBiXpos_29_1 + _LlBiXpos_30_1 + _LlBiXpos_31_1
				}
			display "F-test of sums for window `k' in occupation `j' and activity `i'"
			matrix F_`i'_`j'_`k'=r(F)
			matrix p_`i'_`j'_`k'=r(p)
		}
	}
}

log close






