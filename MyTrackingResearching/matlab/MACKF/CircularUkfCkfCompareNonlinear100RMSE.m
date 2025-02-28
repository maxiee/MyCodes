f = @(x,param) ...
    [1 sin(x(5)*param(1))/x(5)      0 -((1-cos(x(5)*param(1)))/x(5)) 0;
     0 cos(x(5)*param(1))           0 -sin(x(5)*param(1))            0;
     0 (1-cos(x(5)*param(1)))/x(5)  1 sin(x(5)*param(1))/x(5)        0;
     0 sin(x(5)*param(1))           0 cos(x(5)*param(1))             0;
     0 0                            0 0                              1]*x;

h = @(x, params) [x(1,:); x(3,:)];

E = @(X)sqrt((X(1,:)).^2 + (X(3,:)).^2);

augmentation_h = @(x, params) [h(x, params); E(x)];

dt = 1;
radius = 1000;
delta = 2*pi/360*5.73;
count = 100;

x0 = [100 0 0 10 0.1]';
P0 = diag([100 10 100 10 10]);

Loop = 100;

Qv = [0.1/3     0.1/2   0         0         0;
      0.1/2     0.1     0         0         0;
      0         0       0.1/3     0.1/2     0;
      0         0       0.1/2     0.1       0;
      0         0       0         0         1.75];

Qw = diag([25 25]);

for loop = 1:Loop
    fprintf('================��%d�η���==================\n',loop);

    txs = zeros(2, count);
    uxs = zeros(5, count);
    puxs = zeros(5, count);
    cxs = zeros(5, count);
    pcxs = zeros(5,count);
    maukfs = zeros(5, count);

    M_ukf = x0;
    P_ukf = P0;
    M_ckf = x0;
    P_ckf = P0;
    M_maukf = M_ukf;
    P_maukf = P_ukf;
    
    X = zeros(5,count);
    X(:,1) = x0;

    % 生成真实状�?
    for i = 2:count
        X(:,i) = feval(f, X(:, i-1),dt);
    end

    % �?��仿真过程
    for i=1:count

        % 观测
        zx =  X(1,i) + randn(1)*10;
        zy =  X(3,i) + randn(1)*10;

        % UKF
        [M_ukf, P_ukf,D,upSX,upSY] = ukf_predict1(M_ukf, P_ukf, f, Qv, dt,1,1,-2);
        [M_ukf, P_ukf,uK,uMU,uS,uLH,uuSx,uuSY] = ukf_update1(M_ukf, P_ukf, [zx; zy], h, Qw);

        % PUKF
        [M_n,P_n,C_n,sigma,sigma_Y,wei_ut] = ut_transform(M_ukf,P_ukf,f,[dt]);
        sigma_cons = E(sigma);
        dhat = sigma_cons * wei_ut{1};
        Pdd_pukf = 0;
        Pxd_pukf = zeros(5,1);
        for j = 1:11  %magic number
            Pdd_pukf = Pdd_pukf + wei_ut{2}(j)*(sigma_cons(j) - dhat)*(sigma_cons(j) - dhat)';
            Pxd_pukf = Pxd_pukf + wei_ut{2}(j)*(sigma(:,j)-M_ukf)*(sigma_cons(j)-dhat)';
        end
        K_pukf = Pxd_pukf / Pdd_pukf;
        puxs(:,i) = M_ukf + K_pukf*(radius-dhat);

        [M_ckf, P_ckf,cpSX,cpSY] = ckf_predict(M_ckf, P_ckf, f, Qv, dt);
        [M_ckf, P_ckf,Kalmanc,cMU,cS,cLH,cuSx,cuSY] = ckf_update(M_ckf, P_ckf, [zx; zy], h, Qw);

        % MAUKF
        [M_maukf, P_maukf, D_maukf, sigma_an, sigma_ay] = ukf_predict1(M_maukf, P_maukf, f, Qv, dt, 1, 1, -2);
        [M_maukf, P_maukf] = ukf_update1(M_maukf, P_maukf, [zx; zy; radius], augmentation_h, diag([25 25 10-9]));
        % UKF 原始更新过程不用, 用的是扩展的增广更新
        % [M_maukf, P_maukf] = ukf_update1(M_maukf, P_maukf, [zx; zy], h, Qw);
%         y_ag = augmentation_h(sigma_an, dt); % Sigma点增广h非线性变�?
%         hat_y_ag = y_ag * wei_ut{1}; % 得到k时刻先验估计
%         Pyy_maukf = diag([25, 25, 10^-9]);
%         Pxy_maukf = 0;
%         for j = 1:11
%             Pyy_maukf = Pyy_maukf + wei_ut{2}(j)*(y_ag(:, j) - hat_y_ag)*(y_ag(:,j) - hat_y_ag)';
%             Pxy_maukf = Pxy_maukf + wei_ut{2}(j)*(sigma_an(:,j)-M_maukf)*(y_ag(:,j) - hat_y_ag)';
%         end
%         K_maukf = Pxy_maukf / Pyy_maukf;
%         M_maukf = M_maukf + K_maukf*([zx; zy; radius] - hat_y_ag);
%         P_maukf = P_maukf - K_maukf*Pyy_maukf*K_maukf';
         maukfs(:,i) = M_maukf;
        


        % PCKF
        [M_ckf_n,P_ckf_n,C_ckf_n,cube,W] = ckf_transform(M_ckf,P_ckf,f,dt);
        cube_cons = E(cube);
        chat = sum(cube_cons)/10; %magic number
        Pdd_pckf = 0;
        Pxd_pckf = zeros(5,1);
        for q = 1:10
            Pdd_pckf = Pdd_pckf + 0.1*(cube_cons(q) - chat)*(cube_cons(q) - chat)';
            Pxd_pckf = Pxd_pckf + 0.1*(cube(:,q)-M_ckf)*(cube_cons(q) - chat)';
        end
        K_pckf = Pxd_pckf / Pdd_pckf;
        pcxs(:,i) = M_ckf + K_pckf*(radius-chat);

        uxs(:,i) = M_ukf;
        cxs(:,i) = M_ckf;

    end
    
    UKF_RMSE1 = zeros(1,count);
    UKF_RMSE2 = zeros(1,count);
    UKF_RMSE3 = zeros(1,count);
    UKF_RMSE4 = zeros(1,count);
    
    PUKF_RMSE1 = zeros(1,count);
    PUKF_RMSE2 = zeros(1,count);
    PUKF_RMSE3 = zeros(1,count);
    PUKF_RMSE4 = zeros(1,count);
    
    CKF_RMSE1 = zeros(1,count);
    CKF_RMSE2 = zeros(1,count);
    CKF_RMSE3 = zeros(1,count);
    CKF_RMSE4 = zeros(1,count);
    
    PCKF_RMSE1 = zeros(1,count);
    PCKF_RMSE2 = zeros(1,count);
    PCKF_RMSE3 = zeros(1,count);
    PCKF_RMSE4 = zeros(1,count);

    MAUKF_RMSE1 = zeros(1, count);
    MAUKF_RMSE2 = zeros(1, count);
    MAUKF_RMSE3 = zeros(1, count);
    MAUKF_RMSE4 = zeros(1, count);
        
    for i = 1:count
        UKF_RMSE1(1,i) =  (X(1,i) - uxs(1,i)).^2;
        UKF_RMSE2(1,i) =  (X(3,i) - uxs(3,i)).^2;
        UKF_RMSE3(1,i) =  (X(2,i) - uxs(2,i)).^2;
        UKF_RMSE4(1,i) =  (X(4,i) - uxs(4,i)).^2;

        PUKF_RMSE1(1,i) = (X(1,i) - puxs(1,i)).^2;
        PUKF_RMSE2(1,i) = (X(3,i) - puxs(3,i)).^2;
        PUKF_RMSE3(1,i) = (X(2,i) - puxs(2,i)).^2;
        PUKF_RMSE4(1,i) = (X(4,i) - puxs(4,i)).^2;

        CKF_RMSE1(1,i) =  (X(1,i) - cxs(1,i)).^2;
        CKF_RMSE2(1,i) =  (X(3,i) - cxs(3,i)).^2;
        CKF_RMSE3(1,i) =  (X(2,i) - cxs(2,i)).^2;
        CKF_RMSE4(1,i) =  (X(4,i) - cxs(4,i)).^2;

        PCKF_RMSE1(1,i) = (X(1,i) - pcxs(1,i)).^2;
        PCKF_RMSE2(1,i) = (X(3,i) - pcxs(3,i)).^2;
        PCKF_RMSE3(1,i) = (X(2,i) - pcxs(2,i)).^2;
        PCKF_RMSE4(1,i) = (X(4,i) - pcxs(4,i)).^2;
        
        MAUKF_RMSE1(1,i) = (X(1,i) - maukfs(1, i)).^2;
        MAUKF_RMSE2(1,i) = (X(3,i) - maukfs(3, i)).^2;
        MAUKF_RMSE3(1,i) = (X(2,i) - maukfs(2, i)).^2;
        MAUKF_RMSE4(1,i) = (X(4,i) - maukfs(4, i)).^2;
    end
    
    if Loop == 1
        figure;
        T = 1:count;
        plot(X(1,T),X(3,T),'k-',uxs(1,T),uxs(3,T),'k-s',puxs(1,T),puxs(3,T),cxs(1,T),cxs(3,T),'k-o',pcxs(1,T),pcxs(3,T),'k-d');
    end
    
    fprintf('==============================================\n');
end

UKF_RMSE1 = sqrt(UKF_RMSE1./Loop);
UKF_RMSE2 = sqrt(UKF_RMSE2./Loop);
UKF_RMSE3 = sqrt(UKF_RMSE3./Loop);
UKF_RMSE4 = sqrt(UKF_RMSE4./Loop);

PUKF_RMSE1 = sqrt(PUKF_RMSE1./Loop);
PUKF_RMSE2 = sqrt(PUKF_RMSE2./Loop);
PUKF_RMSE3 = sqrt(PUKF_RMSE3./Loop);
PUKF_RMSE4 = sqrt(PUKF_RMSE4./Loop);

CKF_RMSE1 = sqrt(CKF_RMSE1./Loop);
CKF_RMSE2 = sqrt(CKF_RMSE2./Loop);
CKF_RMSE3 = sqrt(CKF_RMSE3./Loop);
CKF_RMSE4 = sqrt(CKF_RMSE4./Loop);

PCKF_RMSE1 = sqrt(PCKF_RMSE1./Loop);
PCKF_RMSE2 = sqrt(PCKF_RMSE2./Loop);
PCKF_RMSE3 = sqrt(PCKF_RMSE3./Loop);
PCKF_RMSE4 = sqrt(PCKF_RMSE4./Loop);

MAUKF_RMSE1 = sqrt(MAUKF_RMSE1./Loop);
MAUKF_RMSE2 = sqrt(MAUKF_RMSE2./Loop);
MAUKF_RMSE3 = sqrt(MAUKF_RMSE3./Loop);
MAUKF_RMSE4 = sqrt(MAUKF_RMSE4./Loop);



T = 1:15:count;
T2 = 1:5:size(UKF_RMSE1,2);

figure;
vUKF_RMSE1 = spcrv([T;UKF_RMSE1(T)],3);
vPUKF_RMSE1 = spcrv([T;PUKF_RMSE1(T)],3);
vCKF_RMSE1 = spcrv([T;CKF_RMSE1(T)],3);
vPCKF_RMSE1 = spcrv([T;PCKF_RMSE1(T)],3);
vMAUKF_RMSE1 = spcrv([T;MAUKF_RMSE1(T)],3);
plot(vUKF_RMSE1(1,T2),vUKF_RMSE1(2,T2),'k-s',vPUKF_RMSE1(1,T2),vPUKF_RMSE1(2,T2),'k-d',vCKF_RMSE1(1,T2),vCKF_RMSE1(2,T2),'r-o',vPCKF_RMSE1(1,T2),vPCKF_RMSE1(2,T2),'k-o', vMAUKF_RMSE1(1,T2), vMAUKF_RMSE1(2,T2));
legend('UKF','PUKF','CKF','PCKF','MAUKF');
xlabel('t,s');
ylabel('RMSE,m')

figure;
vUKF_RMSE2 = spcrv([T;UKF_RMSE2(T)],3);
vPUKF_RMSE2 = spcrv([T;PUKF_RMSE2(T)],3);
vCKF_RMSE2 = spcrv([T;CKF_RMSE2(T)],3);
vPCKF_RMSE2 = spcrv([T;PCKF_RMSE2(T)],3);
vMAUKF_RMSE2 = spcrv([T;MAUKF_RMSE2(T)],3);
plot(vUKF_RMSE2(1,T2),vUKF_RMSE2(2,T2),'k-s',vPUKF_RMSE2(1,T2),vPUKF_RMSE2(2,T2),'k-d',vCKF_RMSE2(1,T2),vCKF_RMSE2(2,T2),'r-o',vPCKF_RMSE2(1,T2),vPCKF_RMSE2(2,T2),'k-o', vMAUKF_RMSE1(1,T2), vMAUKF_RMSE2(2,T2));
legend('UKF','PUKF','CKF','PCKF','MAUKF');
xlabel('t,s');
ylabel('RMSE,m')

figure;
vUKF_RMSE3 = spcrv([T;UKF_RMSE3(T)],3);
vPUKF_RMSE3 = spcrv([T;PUKF_RMSE3(T)],3);
vCKF_RMSE3 = spcrv([T;CKF_RMSE3(T)],3);
vPCKF_RMSE3 = spcrv([T;PCKF_RMSE3(T)],3);
vMAUKF_RMSE3 = spcrv([T;MAUKF_RMSE3(T)],3);
plot(vUKF_RMSE3(1,T2),vUKF_RMSE3(2,T2),'k-s',vPUKF_RMSE3(1,T2),vPUKF_RMSE3(2,T2),'k-d',vCKF_RMSE3(1,T2),vCKF_RMSE3(2,T2),'r-o',vPCKF_RMSE3(1,T2),vPCKF_RMSE3(2,T2),'k-o', vMAUKF_RMSE3(1,T2), vMAUKF_RMSE3(2,T2));
legend('UKF','PUKF','CKF','PCKF', 'MAUKF');
xlabel('t,s');
ylabel('RMSE,m/s')

figure;
vUKF_RMSE4 = spcrv([T;UKF_RMSE4(T)],3);
vPUKF_RMSE4 = spcrv([T;PUKF_RMSE4(T)],3);
vCKF_RMSE4 = spcrv([T;CKF_RMSE4(T)],3);
vPCKF_RMSE4 = spcrv([T;PCKF_RMSE4(T)],3);
vMAUKF_RMSE4 = spcrv([T;MAUKF_RMSE4(T)],3);
plot(vUKF_RMSE4(1,T2),vUKF_RMSE4(2,T2),'k-s',vPUKF_RMSE4(1,T2),vPUKF_RMSE4(2,T2),'k-d',vCKF_RMSE4(1,T2),vCKF_RMSE4(2,T2),'r-o',vPCKF_RMSE4(1,T2),vPCKF_RMSE4(2,T2),'k-o', vMAUKF_RMSE4(1,T2), vMAUKF_RMSE4(2,T2));
legend('UKF','PUKF','CKF','PCKF','MAUKF');
xlabel('t,s');
ylabel('RMSE,m/s')



