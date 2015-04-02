f = @(x,param) [1 param(1) 0 0;0  1 0 0;0  0 1 param(1);0  0 0 1]*x;
h = @(x, params) [x(1,:);x(3,:)];
E = @(X)sqrt((X(1,:)).^2 + (X(3,:)).^2);

dt = 1;
radius = 100;
delta = 2*pi/360*5;
count = 70;

txs = zeros(2, count);
uxs = zeros(4, count);
puxs = zeros(4, count);
cxs = zeros(4, count);

x0 = [100 0 0 0]';
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

for i=1:70
    fprintf('==================第%d轮======================\n',i);
    
    target_pos_x = cos(i*delta)*radius + randn(1)*0.0001;
    target_pos_y = sin(i*delta)*radius + randn(1)*0.0001;
    txs(:,i) = [target_pos_x; target_pos_y];
    
    zx = target_pos_x + randn(1)*5;
    zy = target_pos_y + randn(1)*5;
    
    [M_ukf, P_ukf,D,upSX,upSY] = ukf_predict1(M_ukf, P_ukf, f, Qv, dt);
    [M_ukf, P_ukf,uK,uMU,uS,uLH,uuSx,uuSY] = ukf_update1(M_ukf, P_ukf, [zx; zy], h, Qw);
    
    % PUKF
    [M_n,P_n,C_n,sigma,sigma_Y,wei_ut] = ut_transform(M_ukf,P_ukf,f,[dt]);
    sigma_cons = E(sigma);
    dhat = sigma_cons * wei_ut{1};
    Pdd_pukf = 0;
    Pxd_pukf = zeros(4,1);
    for j = 1:9  %magic number
        Pdd_pukf = Pdd_pukf + wei_ut{2}(j)*(sigma_cons(j) - dhat)*(sigma_cons(j) - dhat)';
        Pxd_pukf = Pxd_pukf + wei_ut{2}(j)*(sigma(:,j)-M_ukf)*(sigma_cons(j)-dhat)';
    end
    K_pukf = Pxd_pukf / Pdd_pukf;
    puxs(:,i) = M_ukf + K_pukf*(radius-dhat);
    
    [M_ckf, P_ckf,cpSX,cpSY] = ckf_predict(M_ckf, P_ckf, f, Qv, dt);
    [M_ckf, P_ckf,cK,cMU,cS,cLH,cuSx,cuSY] = ckf_update(M_ckf, P_ckf, [zx; zy], h, Qw);
    
    fprintf('predict 变换前 Sigma/Cubature 点比较：\n');
    upSX
    uuSx
    fprintf('predict 变换后 Sigma/Cubature 点比较：\n');
    upSY
    cpSY
    fprintf('update 变换前 Sigma/Cubature 点比较：\n');
    uuSx
    cuSx
    fprintf('update 变换后 Sigma/Cubature 点比较：\n');
    uuSY
    cuSY
    
    fprintf('UKF CKF 结果输出：\n');
    M_ukf
    M_ckf
    
    uxs(:,i) = M_ukf;
    cxs(:,i) = M_ckf;
    fprintf('==============================================\n');
end

plot(txs(1,:), txs(2,:), uxs(1,:), uxs(3,:), cxs(1,:), cxs(3,:));
hold;
plot(puxs(1,:),puxs(3,:),'o');
legend('True','UKF','CKF','PUKF');
