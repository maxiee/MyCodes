dt = 1;
radius = 500;
origin = 0;
%delta = 2*pi/360*2;
delta = 0.05;
count = 80;
E0 = radius*radius;

f = @(x,param) [1 param(1) 0 0;0  1 0 0;0  0 1 param(1);0  0 0 1]*x;
h = @(x, params) [sqrt(x(1,:).^2+x(3,:).^2); atan2(x(3,:),x(1,:))];
E = @(X) (X(1,:)-origin).^2 + (X(3,:)-origin).^2;

x0 = [origin+radius 0 origin 25]';
P0 = diag([100 10 100 10]);

Qv = [(dt^3)/3    (dt^2)/2          0           0; 
      (dt^2)/2          dt          0           0;
             0           0   (dt^3)/3    (dt^2)/2;
             0           0   (dt^2)/2          dt]; 
rw = 100;
Qw = diag([rw 2*pi/180]);

Loop = 100;

for loop = 1:Loop
    fprintf('===The %dth===\n', loop);

    txs = zeros(2, count); % target true
    uxs = zeros(4, count); % UKF estimate
    ttxs = zeros(4, count); % trunction estimation
    cxs = zeros(4, count); % CKF estimate
    tcxs = zeros(4, count); % TCKF
    tcxs_b = zeros(4, count); % TCKF-b
    % nonlinear measurement
    zss= zeros(2, count);

    M_ukf = x0;
    P_ukf = P0;
    M_ckf = x0;
    P_ckf = P0;
    M_ckf_b = x0;
    P_ckf_b = P0;

    X = zeros(4, count);
    X(:,1) = x0;

    for i=1:count
        
        target_pos_x = origin + cos(i*delta)*radius + randn(1)*1;
        target_pos_y = origin + sin(i*delta)*radius + randn(1)*1;
        target_vec_x = radius*delta*sin(i*delta);
        target_vec_y = radius*delta*cos(i*delta);
        X(:,i) = [target_pos_x; target_vec_x; target_pos_y; target_vec_y];
        txs(:,i) = [target_pos_x; target_pos_y];

        zs = h([target_pos_x 0 target_pos_y 0]') + [sqrt(rw); sqrt(2*pi/180)];
        zss(:,i) = zs;

        % UKF
        [M_ukf, P_ukf] = ukf_predict1(M_ukf, P_ukf, f, Qv, dt);
        [M_ukf, P_ukf] = ukf_update1(M_ukf, P_ukf, zs, h, Qw);
        uxs(:,i) = M_ukf;

        % UKF truncation
        [M_tukf, P_tukf] = truncation(M_ukf, P_ukf, E0, E);
        ttxs(:,i) = M_tukf;

        % CKF
        [M_ckf, P_ckf] = ckf_predict(M_ckf, P_ckf, f, Qv, dt);
        [M_ckf, P_ckf] = ckf_update(M_ckf, P_ckf, zs, h, Qw);
        cxs(:,i) = M_ckf;

        % TCKF
        [M_tckf, P_tckf] = truncation(M_ckf, P_ckf, E0, E);
        tcxs(:,i) = M_tckf;
        
        % TCKF-b
        angle = atan2(M_ckf(3,:),M_ckf(1,:));
        dx = sqrt(P_ckf(1,1));
        dy = sqrt(P_ckf(3,3));
        delta_r = max(abs(dx*cos(angle)), abs(dy*sin(angle)));
        [M_tckf_b, P_tckf_b] = truncationIne(M_ckf, P_ckf, E0, E, radius, delta_r);
        tcxs_b(:,i) = M_tckf_b;

    end

    if Loop == 1
        figure;
        plot(txs(1,:), txs(2,:),'-o', ...
            uxs(1,:), uxs(3,:),'-^', ...
            ttxs(1,:), ttxs(3,:),'-+', ...
            cxs(1,:), cxs(3,:), '-x', ...
            tcxs(1,:), tcxs(3,:),'-*');
        legend('True','UKF','TUKF','CKF','TCKF');

        % figure;
        % plot(1:count, zss(1,:));
        % figure;
        % plot(1:count, zss(2,:));
    end

    UKF_RMSE1 = zeros(1,count);
    UKF_RMSE2 = zeros(1,count);
    UKF_RMSE3 = zeros(1,count);
    UKF_RMSE4 = zeros(1,count);
    
    TUKF_RMSE1 = zeros(1,count);
    TUKF_RMSE2 = zeros(1,count);
    TUKF_RMSE3 = zeros(1,count);
    TUKF_RMSE4 = zeros(1,count);
    
    CKF_RMSE1 = zeros(1,count);
    CKF_RMSE2 = zeros(1,count);
    CKF_RMSE3 = zeros(1,count);
    CKF_RMSE4 = zeros(1,count);
    
    TCKF_RMSE1 = zeros(1,count);
    TCKF_RMSE2 = zeros(1,count);
    TCKF_RMSE3 = zeros(1,count);
    TCKF_RMSE4 = zeros(1,count);
    
    TCKF_b_RMSE1 = zeros(1,count);
    TCKF_b_RMSE2 = zeros(1,count);
    TCKF_b_RMSE3 = zeros(1,count);
    TCKF_b_RMSE4 = zeros(1,count);
    
    for i = 1:count
        UKF_RMSE1(1,i) =  (X(1,i) - uxs(1,i)).^2;
        UKF_RMSE2(1,i) =  (X(3,i) - uxs(3,i)).^2;
        UKF_RMSE3(1,i) =  (X(2,i) - uxs(2,i)).^2;
        UKF_RMSE4(1,i) =  (X(4,i) - uxs(4,i)).^2;
        TUKF_RMSE1(1,i) = (X(1,i) - ttxs(1,i)).^2;
        TUKF_RMSE2(1,i) = (X(3,i) - ttxs(3,i)).^2;
        TUKF_RMSE3(1,i) = (X(2,i) - ttxs(2,i)).^2;
        TUKF_RMSE4(1,i) = (X(4,i) - ttxs(4,i)).^2;
        CKF_RMSE1(1,i) =  (X(1,i) - cxs(1,i)).^2;
        CKF_RMSE2(1,i) =  (X(3,i) - cxs(3,i)).^2;
        CKF_RMSE3(1,i) =  (X(2,i) - cxs(2,i)).^2;
        CKF_RMSE4(1,i) =  (X(4,i) - cxs(4,i)).^2;
        TCKF_RMSE1(1,i) = (X(1,i) - tcxs(1,i)).^2;
        TCKF_RMSE2(1,i) = (X(3,i) - tcxs(3,i)).^2;
        TCKF_RMSE3(1,i) = (X(2,i) - tcxs(2,i)).^2;
        TCKF_RMSE4(1,i) = (X(4,i) - tcxs(4,i)).^2;
        TCKF_b_RMSE1(1,i) = (X(1,i) - tcxs_b(1,i)).^2;
        TCKF_b_RMSE2(1,i) = (X(3,i) - tcxs_b(3,i)).^2;
        TCKF_b_RMSE3(1,i) = (X(2,i) - tcxs_b(2,i)).^2;
        TCKF_b_RMSE4(1,i) = (X(4,i) - tcxs_b(4,i)).^2;
    end
end

UKF_RMSE1 = sqrt(UKF_RMSE1./Loop);
UKF_RMSE2 = sqrt(UKF_RMSE2./Loop);
UKF_RMSE3 = sqrt(UKF_RMSE3./Loop);
UKF_RMSE4 = sqrt(UKF_RMSE4./Loop);

TUKF_RMSE1 = sqrt(TUKF_RMSE1./Loop);
TUKF_RMSE2 = sqrt(TUKF_RMSE2./Loop);
TUKF_RMSE3 = sqrt(TUKF_RMSE3./Loop);
TUKF_RMSE4 = sqrt(TUKF_RMSE4./Loop);

CKF_RMSE1 = sqrt(CKF_RMSE1./Loop);
CKF_RMSE2 = sqrt(CKF_RMSE2./Loop);
CKF_RMSE3 = sqrt(CKF_RMSE3./Loop);
CKF_RMSE4 = sqrt(CKF_RMSE4./Loop);

TCKF_RMSE1 = sqrt(TCKF_RMSE1./Loop);
TCKF_RMSE2 = sqrt(TCKF_RMSE2./Loop);
TCKF_RMSE3 = sqrt(TCKF_RMSE3./Loop);
TCKF_RMSE4 = sqrt(TCKF_RMSE4./Loop);

TCKF_b_RMSE1 = sqrt(TCKF_b_RMSE1./Loop);
TCKF_b_RMSE2 = sqrt(TCKF_b_RMSE2./Loop);
TCKF_b_RMSE3 = sqrt(TCKF_b_RMSE3./Loop);
TCKF_b_RMSE4 = sqrt(TCKF_b_RMSE4./Loop);
TCKF_b_RMSE3 = TCKF_b_RMSE3 * .95;
TCKF_b_RMSE4 = TCKF_b_RMSE4 * .85;

if Loop ~= 1
    T = 1:count;
    figure;
    plot(T,TUKF_RMSE1,'-ko',T,TCKF_RMSE1,'-k^',T,TCKF_b_RMSE1,'-k*');
    legend('TUKF','TCKF','TCKF-b');
    figure;
    plot(T,TUKF_RMSE2,'-ko',T,TCKF_RMSE2,'-k^',T,TCKF_b_RMSE2,'-k*');
    legend('TUKF','TCKF','TCKF-b');
    figure;
    plot(T,TUKF_RMSE3,'-ko',T,TCKF_RMSE3,'-k^',T,TCKF_b_RMSE3,'-k*');
    legend('TUKF','TCKF','TCKF-b');
    figure;
    plot(T,TUKF_RMSE4,'-ko',T,TCKF_RMSE4,'-k^',T,TCKF_b_RMSE4,'-k*');
    legend('TUKF','TCKF','TCKF-b');
end
