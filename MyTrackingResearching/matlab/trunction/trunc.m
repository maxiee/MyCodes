f = @(x,param) [1 param(1) 0 0;0  1 0 0;0  0 1 param(1);0  0 0 1]*x;
h = @(x, params) [x(1,:);x(3,:)];
E = @(X) (X(1,:)).^2 + (X(3,:)).^2;
 
dt = 1;
radius = 100;
delta = 2*pi/360*5;
count = 70;
E0 = radius*radius;

txs = zeros(2, count); % target true
uxs = zeros(4, count); % UKF estimate
ttxs = zeros(4, count); % trunction estimation
cxs = zeros(4, count); % CKF estimate
tcxs = zeros(4, count); % TCKF


x0 = [radius 0 0 0]';
P0 = diag([100 10 100 10]);

M_ukf = x0;
P_ukf = P0;
M_ckf = x0;
P_ckf = P0;

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

    % UKF truncation
    [M_tukf, P_tukf] = truncation(M_ukf, P_ukf, E0, E);
    ttxs(:,i) = M_tukf;

    % CKF
    [M_ckf, P_ckf] = ckf_predict(M_ckf, P_ckf, f, Qv, dt);
    [M_ckf, P_ckf] = ckf_update(M_ckf, P_ckf, [zx; zy], h, Qw);
    cxs(:,i) = M_ckf;

    % TCKF
    [M_tckf, P_tckf] = truncation(M_ckf, P_ckf, E0, E);
    tcxs(:,i) = M_tckf;

end

plot(txs(1,:), txs(2,:),'-o', ...
    uxs(1,:), uxs(3,:),'-^', ...
    ttxs(1,:), ttxs(3,:),'-+', ...
    cxs(1,:), cxs(3,:), '-x', ...
    tcxs(1,:), tcxs(3,:),'-*');
legend('True','UKF','TUKF','CKF','TCKF');
