* Challenger O-ring data: 23 flights before STS-51-L (Dalal, Fowlkes & Hoadley 1989)
* temp = launch temperature (F); damage = 1 if any field-joint O-ring distress
clear
set obs 23
local t "66 70 69 68 67 72 73 70 57 63 70 78"
local t "`t' 67 53 67 75 70 81 76 79 75 76 58"
local d "0 1 0 0 0 0 0 0 1 1 1 0 0 1 0 0"
local d "`d' 0 0 0 0 1 0 1"
generate temp   = real(word("`t'", _n))
generate damage = real(word("`d'", _n))
tab damage

regress damage temp, robust
margins, at(temp=(31 53 70 81))
margins, dydx(temp)

logit damage temp
margins, at(temp=(31 53 70 81))
margins, dydx(temp)

probit damage temp
margins, at(temp=(31 53 70 81))
margins, dydx(temp)
