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

global rnames "m2 m8 m9"
global cnames ""
matrix b_all = J(44,1,.) 
foreach j in 11 13 {
	foreach i in rm_lfp working looking {
	    /* read in the estimates */
		estimates restore `i'_`j'_weighted
		/* store the coefficients in a column vector that you create and name b`i'_`j' */
		matrix b`i'_`j'=_b[_LlBiXpos_2_1] \ _b[_LlBiXpos_8_1] \ _b[_LlBiXpos_9_1]
		matrix list b`i'_`j'
		forvalues k=10(1)50 {
		/* collect all of the coefficients into the matrix b_all */
			matrix b`i'_`j' = b`i'_`j' \ _b[_LlBiXpos_`k'_1]
			if "`i'"=="rm_lfp" & "`j'"=="11" {
				global rnames = "$rnames" + " m`k'"
			}
		}
		foreach k in m3_p3 m0_p6 {
			test "$`k'" 
			display "F-test of window `k' for occupation `j' and dependent variable `i'"
			matrix F_`i'_`j'_`k'=r(F)
			matrix p_`i'_`j'_`k'=r(p)
		}
	    matrix b_all = b_all , b`i'_`j'
		global cnames = "$cnames" + " m_`i'_`j'"
	}
}
matrix rownames b_all=$rnames
matrix c=b_all[1...,2...]
matrix colnames c=$cnames
svmat c,names(col)

gen period=_n
replace period=2 in 1
replace period=8 in 2 
replace period=9 in 3
replace period=period[_n-1]+1 if _n>3

save Stata_Results/estimated_coefficients_all_models,replace

log close






