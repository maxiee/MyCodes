f = @(x,param) [1 param(1) 0 0;0  1 0 0;0  0 1 param(1);0  0 0 1]*x;
h = @(x, params) [x(1,:);x(3,:)];
E = @(X) (X(1,:)).^2 + (X(3,:)).^2;
 
dt = 1;
radius = 100;
delta = 2*pi/360*5;
count = 70;
E0 = radius*radius;
global E0;

txs = zeros(2, count); % target true
uxs = zeros(4, count); % UKF estimate
ttxs = zeros(4, count); % trunction estimation


x0 = [radius 0 0 0]';
P0 = diag([100 10 100 10]);

M_ukf = x0;
P_ukf = P0;

Qv = [(dt^3)/3    (dt^2)/2          0           0; 
      (dt^2)/2          dt          0           0;
             0           0   (dt^3)/3    (dt^2)/2;
             0           0   (dt^2)/2          dt]; 
Qw = diag([25 25]);

for i=1:count
    fprintf('===The %dth===\n', i);

    target_pos_x = cos(i*delta)*radius + randn(1)*0.0001;
    target_pos_y = sin(i*delta)*radius + randn(1)*0.0001;
    txs(:,i) = [target_pos_x; target_pos_y];

    % measurement
    zx = target_pos_x + randn(1)*5;
    zy = target_pos_y + randn(1)*5;

    % UKF
    [M_ukf, P_ukf] = ukf_predict1(M_ukf, P_ukf, f, Qv, dt);
    [M_ukf, P_ukf] = ukf_update1(M_ukf, P_ukf, [zx; zy], h, Qw);
    uxs(:,i) = M_ukf;

    % Truncation
    PTrunc = P_ukf;
    xTrunc = M_ukf;
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
    xTrunc = Ttrunc * sqrt(Wtrunc) * S' * zTrunc + xTrunc;
    PTrunc = Ttrunc * sqrt(Wtrunc) * S' * CovZ * S * sqrt(Wtrunc) * Ttrunc';
    ttxs(:,i) = xTrunc;
end

plot(txs(1,:), txs(2,:),'-o', uxs(1,:), uxs(3,:),'-^', ttxs(1,:), ttxs(3,:));
legend('True','UKF','TUKF');
