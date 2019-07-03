clear all
set maxvar 32000
set matsize 10000
set more off, perm

cd D:\Users\Alex\Git_Repositories\Thesis

capture log close
log using Stata_log_files\management.log,replace 

*data directory (where posted datasets are stored)
global datafiles "D:\Users\Alex\Git_Repositories\Thesis"

use  "$datafiles\Stata_Regressions\US_Paid_leave_analysis_altered.dta", clear

global X "i.rhcalyr i.lBirth i.rhcalyr#i.state i.lBirth#i.state i.lBirth#i.rhcalyr _LlBiXpos_2_1 _LlBiXpos_8_1-_LlBiXpos_50_1"

/* run DD regressions for various occupational groups, save the estimates for later use */
/* verify xtset */
xtset

/* run fixed effects regressions, sippid is the cross-sectional unit */
foreach i in rm_lfp working looking  {
	foreach j in 11  {
		quietly xtreg `i' $X [pweight=end_weight] if industry_pre_birth=="`j'",fe vce(cluster sippid)
		estimates save Stata_ster/`i'_`j',replace 
	} 	
}

global m3_p3 "_LlBiXpos_22_1 _LlBiXpos_23_1 _LlBiXpos_24_1 _LlBiXpos_25_1 _LlBiXpos_26_1 _LlBiXpos_27_1 _LlBiXpos_28_1"
global m0_p6 "_LlBiXpos_25_1 _LlBiXpos_26_1 _LlBiXpos_27_1 _LlBiXpos_28_1 _LlBiXpos_29_1 _LlBiXpos_30_1 _LlBiXpos_31_1"


matrix b_all = J(49,1,.) 
foreach j in 11 {
	foreach i in rm_lfp working looking {
	    /* read in the estimates */
		estimates use Stata_ster/`i'_`j'
		/* store the coefficients in a column vector that you create and name b`i'_`j' */
		matrix b`i'_`j'=_b[_LlBiXpos_2_1] \ _b[_LlBiXpos_8_1] \ _b[_LlBiXpos_9_1]
		matrix list b`i'_`j'
		forvalues k=10(1)50 {
		/* collect all of the coefficients into the matrix b_all */
			matrix b`i'_`j' = b`i'_`j' \ _b[_LlBiXpos_`k'_1]
			*global rnames = "$rnames" + "m`k'"
		}
		*matrix b_all = b_all , b`i'_`j'
		foreach k in m3_p3 m0_p6 {
			test "$`k'" 
			display "F-test of window `k' for occupation `j' and dependent variable `i'"
			matrix F_`i'_`j'_`k'=r(F)
			matrix p_`i'_`j'_`k'=r(p)
		}
	}
}



    Rename rows and columns of matrix

        matname A namelist [, rows(range) columns(range) explicit]


log close

/*
testing the loop code 

foreach i in rm_lfp working looking {
	foreach j in 11 43 {
		summarize `i' if industry_pre_birth=="`j'"
		reg `i' if industry_pre_birth=="`j'"
		estimates save Stata_ster/`i'_`j',replace
	}
}


