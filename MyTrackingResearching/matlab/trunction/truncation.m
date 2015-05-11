function [MM, PP] = truncation(M, P, E0, E)
PTrunc = P;
xTrunc = M;
[D, E2, d] = ConstraintDeriv(xTrunc, E0, E);
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
cTrunc = (d - D * xTrunc) / sqrt(D * PTrunc * D');
dTrunc = (d - D * xTrunc) / sqrt(D * PTrunc * D');

mu = cTrunc;
sigma2 = 0;

zTrunc = zeros(size(xTrunc));
zTrunc(1) = mu;
CovZ = eye(length(zTrunc));
CovZ(1,1) = sigma2;
MM = Ttrunc * sqrt(Wtrunc) * S' * zTrunc + xTrunc;
PP = Ttrunc * sqrt(Wtrunc) * S' * CovZ * S * sqrt(Wtrunc) * Ttrunc';

