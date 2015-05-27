function [MM, PP] = truncation(M, P, E0, E, r, dr)
PTrunc = P;
xTrunc = M;
[D, E2, d1] = ConstraintDeriv(xTrunc, (r-dr*2)^2, E);
[D, E2, d2] = ConstraintDeriv(xTrunc, (r+dr*2)^2, E);
% only 1 constraint
[Utrunc, Wtrunc, Vtrunc] = svd(PTrunc);
Ttrunc = Utrunc;
TTT = Ttrunc * Ttrunc';
if (norm(eye(size(TTT)) - TTT) > 1e-8)
    disp('Error - Ttrunc is not orthogonal.');
    return;
end
if (norm(Utrunc*Wtrunc*Utrunc' - PTrunc) > 1e-8)
    disp('Error - SVD failed for trunction');
    return;
end
% Gram-Schmidt
Amgs = sqrt(Wtrunc) * Ttrunc' * D';
[Wmgs, S] = MGS(Amgs);
S = S * sqrt(D * PTrunc * D') / Wmgs;
cTrunc = (d1 - D * xTrunc) / sqrt(D * PTrunc * D');
dTrunc = (d2 - D * xTrunc) / sqrt(D * PTrunc * D');

% The next 3 lines are commented out because they apply only for inequality constraints
alpha = sqrt(2/pi) / (erf(dTrunc/sqrt(2)) - erf(cTrunc/sqrt(2)));
mu = alpha * (exp(-cTrunc^2/2) - exp(-dTrunc^2/2));
sigma2 = alpha * (exp(-cTrunc^2/2) * (cTrunc - 2 * mu) - exp(-dTrunc^2/2) * (dTrunc - 2 * mu)) + mu^2 + 1;

zTrunc = zeros(size(xTrunc));
zTrunc(1) = mu;
CovZ = eye(length(zTrunc));
CovZ(1,1) = sigma2;
MM = Ttrunc * sqrt(Wtrunc) * S' * zTrunc + xTrunc;
PP = Ttrunc * sqrt(Wtrunc) * S' * CovZ * S * sqrt(Wtrunc) * Ttrunc';

