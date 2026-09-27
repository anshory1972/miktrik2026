clear all
set more off
set linesize 78
set scheme s1color
sysuse auto, clear
tab foreign
* ---- 1. logit and odds ratios
logit foreign weight mpg
logistic foreign weight mpg
* ---- 2. predicted probabilities
predict phat
list make foreign weight mpg phat in 1/8, sep(0) noobs
quietly logit foreign weight mpg
quietly summarize mpg, meanonly
local mbar = r(mean)
twoway (scatter foreign weight, msymbol(circle_hollow) mcolor(gs9) msize(medium)) ///
       (scatter phat weight, msymbol(circle) mcolor(maroon%60) msize(small)) ///
       (function y = invlogit(_b[_cons] + _b[weight]*x + _b[mpg]*`mbar'), ///
            range(1700 4900) lwidth(thick) lcolor(navy)), ///
       ytitle("Pr(foreign)") xtitle("Weight (lbs.)") ylabel(0(.25)1, angle(0)) ///
       legend(order(1 "data (0/1)" 2 "fitted P, each car" 3 "logit curve at mean mpg") ///
              rows(1) size(small) position(6) region(lstyle(none)))
graph export "phat_weight.png", replace width(1800)
* ---- 3. margins
quietly logit foreign weight mpg
margins, dydx(*)
margins, dydx(*) atmeans
margins, at(weight=(2000(500)4500))
marginsplot, ytitle("Pr(foreign)") title("") xtitle("Weight (lbs.)")
graph export "marginsplot_weight.png", replace width(1800)
* ---- 4. goodness of fit
estat classification
estat classification, cutoff(0.3)
lroc, title("")
graph export "lroc.png", replace width(1800)
estat gof, group(10)
* ---- 5. probit and LPM for comparison
probit foreign weight mpg
margins, dydx(*)
regress foreign weight mpg, vce(robust)
* ---- 6. standard errors
logit foreign weight mpg, vce(robust)
logit foreign weight mpg, vce(cluster rep78)
* ---- 7. perfect prediction
capture noisily logit foreign i.rep78
* ---- 8. interaction
logit foreign c.weight##c.mpg
margins, dydx(weight) at(mpg=(15 20 25 30))
